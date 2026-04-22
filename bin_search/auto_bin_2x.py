import pandas as pd
import itertools
from datetime import datetime
from sst.strategy2.risk import Risk
from bin_search.prepare import prepare
from sst.strategy2.logic.docs.excel_writer import ExcelDocWriter
from bin_search.auto_bin_1x import (
    _merge_bins,
    _bin_feature,
    _extract_categorical_cuts,
    _extract_cuts,
    get_bin_label,
)

class ExcelDocWriter2(ExcelDocWriter):
    SHEET_COLUMN_WIDTH = 6


def auto_bin_2x(
    df,
    risk_min=-0.1,
    risk_max=0.6,
    cate_cols=None,
    exclude_cols=None,
    filter_prefix=None,
    target="target",
    time_col="due_time_date",
    weight="trans_money",
    bins=10,
    samples_min=50,
    iv_min=0.001,
    csi_max=0.25,
    corr_max=0.96,
    risk_need_col=[
        "0+流入",
        "3+流入",
        "交易人数",
    ],
    filter_rank=None,
):
    """
    传入到期交易的数据，按照风险阈值搜索高风险和低风险的分箱
    :param df: 到期的交易样本
    :param risk_min: 最小风险阈值,低风险低于该值的变量会入选。默认0.1
    :param risk_max: 最大风险阈值,高风险高于该值的变量会入选。默认0.6
    :param cate_cols: 指定为类别变量的变量,默认不指定
    :param exclude_cols: 需要指定排查的变量,apply_time、随机数等已经排除
    :param filter_prefix: 需要筛选指定前缀开头的变量来搜索，默认不筛选
    :param target: 目标变量,默认target
    :param time_col: 时间列,默认due_time_date
    :param weight: 权重列,默认trans_money
    :param bins: 保留分箱数,默认10
    :param samples_min: 每个分箱的样本数最低值,默认50.
    :param iv_min: IV阈值,默认0.001
    :param csi_max: CSI阈值,默认0.25
    :param corr_max: 相关系数阈值,默认0.96
    :param risk_need_col: get_risk输出的列。[ "0+流入", "3+流入", "交易人数"]
    :param filter_rank: int
    :return: 分箱结果列表
    """
    # 数据预处理
    total, features, (left, right) = prepare(
        df,
        cate_cols=cate_cols,
        exclude_cols=exclude_cols,
        filter_prefix=filter_prefix,
        target=target,
        time_col=time_col,
        weight=weight,
        iv_min=iv_min,
        csi_max=csi_max,
        corr_max=corr_max,
    )

    # 初始excel
    excel_writer = ExcelDocWriter2(
        f"auto_bin_2x_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        default_sheet_name="近期数据",
        max_merge_cell_cnt=2,
    )
    excel_writer.add_sheet("后段数据")

    print("\n===============开始变量分箱搜索===============")
    results = []
    for seg_df, sheet_name in [(right, "近期数据"), (left, "后段数据")]:
        time_range = f"{seg_df[time_col].min().strftime('%Y-%m-%d')}~{seg_df[time_col].max().strftime('%Y-%m-%d')}"
        excel_writer.set_active_sheet(sheet_name)
        # 近期数据和后段数据 只使用近期的分箱结果
        if sheet_name == "近期数据":
            # 1.维分箱搜索
            print(f"1.开始{sheet_name}【{time_range}】时段1维分箱搜索")
            for feat in features:
                bin_df = _bin_feature(seg_df, feat, target, weight)
                if bin_df is None or len(bin_df) < 2:
                    continue
                rows = _merge_bins(bin_df.to_dict("records"), samples_min, max_bins=bins)
                if len(rows) < 2:
                    continue
                min_risk = min(r["risk"] for r in rows)
                max_risk = max(r["risk"] for r in rows)
                if min_risk < risk_min or max_risk > risk_max:
                    is_num = pd.api.types.is_numeric_dtype(seg_df[feat])
                    cuts = ( _extract_cuts(rows, seg_df[feat]) if is_num else _extract_categorical_cuts(rows) )
                    results.append(
                        {
                            "feature": feat,
                            "min_risk": round(min_risk, 4),
                            "max_risk": round(max_risk, 4),
                            "cuts": cuts,
                            "bins": pd.DataFrame(rows),
                            "sort_value": max_risk,
                        }
                    )
            print(f"满足条件的特征【{len(results)}】个\n")
        
        # 2.二维交叉
        print(f"2.开始{sheet_name}【{time_range}】时段2维变量交叉")
        var_pairs = list(itertools.combinations(results, 2))
        print(f"满足条件的变量交叉【{len(var_pairs)}】对\n")
        risk_dfs = []
        for idx, (p1, p2) in enumerate(var_pairs):
            print(f"\r第{idx + 1}对变量交叉", flush=True, end="")
            feat1, feat2 = p1["feature"], p2["feature"]
            cut1, cut2 = p1["cuts"], p2["cuts"]
            temp = seg_df[
                [
                    feat1,
                    feat2,
                    "target",
                    "due_time_date",
                    "trans_money",
                    "repay_time_date",
                    "repay_time",
                    "penalty_day",
                    "user_id",
                    "borrow_id",
                    "loan_time"
                ]
            ].copy()
            temp[feat1] = get_bin_label(temp, feat1, cut1)
            temp[feat2] = get_bin_label(temp, feat2, cut2)
            risk_df = Risk.get_risk(temp, [feat1, feat2], need_col=risk_need_col, to_pct=True)
            # 交换索引层级
            risk_df = risk_df.swaplevel(i=0, j=1, axis=1).sort_index(axis=1)
            first_row = risk_df["0+流入"].iloc[0].dropna().apply(lambda x: float(x.replace("%", ""))/100)
            first_col = risk_df.iloc[:-1, 0].dropna().apply(lambda x: float(x.replace("%", ""))/100 )
            first_row_is_rank = first_row.is_monotonic_increasing or first_row.is_monotonic_decreasing
            first_col_is_rank = first_col.is_monotonic_increasing or first_col.is_monotonic_decreasing
            if filter_rank:
                if not(first_row_is_rank or first_col_is_rank):
                    continue
            risk_dfs.append((f"{feat1} / {feat2}", "title2"))
            risk_dfs.append((risk_df,'df3'))
        
        # 3.写入excel
        sheet_title = f"\n【{time_range}】时段2维变量交叉:{len(risk_dfs)//2}对。"
        excel_writer.write_items([(sheet_title, "title1"), *risk_dfs])
        
    excel_writer.close()
    print("\n===============完成===============")
        
if __name__ == "__main__":
    df = pd.read_parquet("/home/lim/data/project/sst_model_tool/src/sst/strategy2/bin_search/data.pq")
    auto_bin_2x(df, filter_rank=True)
