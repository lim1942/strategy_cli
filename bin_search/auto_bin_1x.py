import numpy as np
import pandas as pd
from datetime import datetime
from bin_search.prepare import prepare
from sst.strategy2.risk import Risk
from sst.strategy2.logic.docs.excel_writer import ExcelDocWriter


def _bin_feature(df, feature, target, weight, init_bins=2000):
    tmp = df[[feature, target, weight]].copy()
    tmp.columns = ['x', 'y', 'w']
    tmp['w'] = tmp['w'].fillna(0).clip(lower=0)
    tmp['bw'] = tmp['w'] * (tmp['y'] == 0).astype(float)

    is_num = pd.api.types.is_numeric_dtype(tmp['x'])

    def _agg(t):
        return (t.groupby('g', observed=True)
                 .agg(count=('w', 'count'), weight_sum=('w', 'sum'), bad_weight=('bw', 'sum'))
                 .reset_index())

    if is_num:
        try:
            tmp['g'], edges = pd.qcut(tmp['x'], q=init_bins, duplicates='drop', retbins=True, labels=False)
        except Exception:
            return None
        if tmp['g'].isna().all():
            return None
        edges[[0, -1]] = [-np.inf, np.inf]
        g = _agg(tmp).sort_values('g')
        g[['left', 'right']] = [[edges[int(i)], edges[int(i)+1]] for i in g['g']]
        g['label'] = [f"({l}, {r}]" for l, r in zip(g['left'], g['right'])]
    else:
        tmp['g'] = tmp['x'].astype(str)
        g = _agg(tmp)
        g['label'] = g['g']

    g['risk'] = g['bad_weight'] / g['weight_sum'].clip(lower=1e-9)
    if not is_num:
        g = g.sort_values('risk')
    cols = (['left', 'right'] if is_num else []) + ['label', 'count', 'weight_sum', 'bad_weight', 'risk']
    return g[cols].reset_index(drop=True)


def _merge_two(a, b):
    ws = a['weight_sum'] + b['weight_sum']
    bw = a['bad_weight'] + b['bad_weight']
    base = {'count': a['count'] + b['count'], 'weight_sum': ws, 'bad_weight': bw, 'risk': bw / max(ws, 1e-9)}
    if 'left' in a:
        return {**base, 'left': a['left'], 'right': b['right'], 'label': f"({a['left']}, {b['right']}]"}
    return {**base, 'label': f"{a['label']} | {b['label']}"}


def _merge_bins(rows, min_samples, max_bins=None):
    # 阶段1：小样本合并
    changed = True
    while changed:
        changed = False
        for i, r in enumerate(rows):
            if r['count'] >= min_samples or len(rows) <= 1:
                continue
            if i == 0:
                j = 1
            elif i == len(rows) - 1:
                j = len(rows) - 2
            else:
                j = i - 1 if abs(r['risk'] - rows[i-1]['risk']) <= abs(r['risk'] - rows[i+1]['risk']) else i + 1
            lo, hi = min(i, j), max(i, j)
            rows = rows[:lo] + [_merge_two(rows[lo], rows[hi])] + rows[hi+1:]
            changed = True
            break

    # 阶段2：PAVA 单调合并，取保留箱数更多的方向
    def _pava(rows, asc):
        stack = []
        for r in rows:
            stack.append(r.copy())
            while len(stack) >= 2:
                a, b = stack[-2], stack[-1]
                violates = (a['risk'] > b['risk']) if asc else (a['risk'] < b['risk'])
                if violates:
                    stack.pop()
                    stack.pop()
                    stack.append(_merge_two(a, b))
                else:
                    break
        return stack

    asc = _pava(list(rows), True)
    desc = _pava(list(rows), False)
    result = asc if len(asc) >= len(desc) else desc

    # 阶段3：限制最大分箱数，合并相邻风险差最小的两箱
    if max_bins is not None:
        while len(result) > max_bins:
            min_idx = min(range(len(result) - 1), key=lambda i: abs(result[i]['risk'] - result[i+1]['risk']))
            result = result[:min_idx] + [_merge_two(result[min_idx], result[min_idx + 1])] + result[min_idx + 2:]

    return result


def _extract_cuts(rows, s):
    """从分箱结果中提取可直接用于 pd.cut 的有限端点列表（含 ±inf）。"""
    cuts =  [r['right'] for r in rows[:-1] if np.isfinite(r['right'])]
    # 若有缺失值，在左端点前加上缺失值
    has_missing = (s == -9999979).any()
    if has_missing:
        if ((s > -9999979) & (s < cuts[0])).any():
            cuts.insert(0, -9999979)
        # 缺失值和左端点之间无数据，用缺失值代替左端点
        else:
            cuts[0] = -9999979
    bins_list = [-np.inf] + cuts + [np.inf]
    return bins_list


def _extract_categorical_cuts(rows):
    """从分箱结果中提取离散型分箱的分组，每组为一个元组。"""
    return [tuple(v.strip() for v in r['label'].split(' | ')) for r in rows]


def get_bin_label(df, feature, cuts):
    """根据分箱结果，将特征值映射为对应的分组名称。"""
    def get_cat_name(x, cuts):
        """根据离散型分箱的分组，将值映射为对应的分组名称。"""
        for cut in cuts:
            if x in cut:
                return cut
        return "Other"
    if isinstance(cuts[0], tuple):
        return df[feature].apply(lambda x: get_cat_name(x, cuts))
    else:
        return pd.cut(df[feature], bins=cuts, right=True)


def save_excel(excel_writer, df, results, sheet_name, sheet_title, need_col=None, risk_dim2=False):
    # 切换到指定sheet
    excel_writer.set_active_sheet(sheet_name)
    risk_dfs = []
    for item in results:
        feature = item['feature']
        cuts = item['cuts']
        temp = df[
            [
                feature,
                "target",
                "due_time_date",
                "due_time_date_cut",
                "trans_money",
                "repay_time_date",
                "repay_time",
                "penalty_day",
                "user_id",
                "borrow_id",
                "loan_time"
            ]
        ].copy()
        temp[feature] = get_bin_label(temp, feature, cuts)
        risk_df = Risk.get_risk(
            temp,
            [feature] if not risk_dim2 else [ "due_time_date_cut", feature],
            need_col=need_col or ["交易单数", "交易人数", "交易金额", "金额占比", "0+流入", "3+流入"], 
            to_pct=True
        )
        item["bins"] = risk_df
        risk_dfs.append(risk_df)
    excel_writer.write_items([(sheet_title, "title1"), *risk_dfs])


def auto_bin_1x(
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
    risk_need_col=[ "交易单数", "交易人数", "交易金额", "金额占比", "0+流入", "3+流入", ],
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
    :param risk_need_col: get_risk输出的列。[ "交易单数", "交易人数", "交易金额", "金额占比", "0+流入", "3+流入"]
    """
    # 数据预处理
    total, features, (left, right) = prepare(df, cate_cols=cate_cols, exclude_cols=exclude_cols, filter_prefix=filter_prefix, target=target, 
                                             time_col=time_col, weight=weight, iv_min=iv_min, csi_max=csi_max, corr_max=corr_max)
    # 初始excel
    excel_writer = ExcelDocWriter(f"auto_bin_1x_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", default_sheet_name="近期数据")
    excel_writer.add_sheet("后段数据")
    excel_writer.add_sheet("整体数据")

    print("\n===============开始变量分箱搜索===============")
    all_results = {}
    for seg_df, sheet_name in [(right, "近期数据"), (left, "后段数据")]:
        time_range = f"{seg_df[time_col].min().strftime('%Y-%m-%d')}~{seg_df[time_col].max().strftime('%Y-%m-%d')}"
        print(f"开始{sheet_name}【{time_range}】时段变量分箱搜索")
        results = []
        for feat in features:
            bin_df = _bin_feature(seg_df, feat, target, weight)
            if bin_df is None or len(bin_df) < 2:
                continue
            rows = _merge_bins(bin_df.to_dict('records'), samples_min, max_bins=bins)
            if len(rows) < 2:
                continue
            min_risk = min(r['risk'] for r in rows)
            max_risk = max(r['risk'] for r in rows)
            if min_risk < risk_min or max_risk > risk_max:
                is_num = pd.api.types.is_numeric_dtype(seg_df[feat])
                cuts = _extract_cuts(rows, seg_df[feat]) if is_num else _extract_categorical_cuts(rows)
                results.append({'feature': feat, 'min_risk': round(min_risk, 4), 'max_risk': round(max_risk, 4),
                                'cuts': cuts, 'bins': pd.DataFrame(rows), 'sort_value': max_risk})
        print(f"满足条件的特征【{len(results)}】个, 开始保存excel")
        results = sorted(results, key=lambda x: x["sort_value"], reverse=True)
        sheet_title = f"【{time_range}】时段搜索结果:{len(results)}个变量。risk_min:【{risk_min}】,risk_max:【{risk_max}】,samples_min:【{samples_min}】"
        save_excel(excel_writer, seg_df, results, sheet_name, sheet_title, need_col=risk_need_col)
        all_results[sheet_name] = results
    # 整体数据
    print("整体数据")
    results = all_results["近期数据"].copy()
    sheet_title = f"整体数据使用近期数据的分箱。risk_min:【{risk_min}】,risk_max:【{risk_max}】,samples_min:【{samples_min}】"
    save_excel(excel_writer, total, results, "整体数据", sheet_title, need_col=risk_need_col, risk_dim2=True)
    excel_writer.close()
    print("\n===============完成===============")
    return all_results

if __name__ == "__main__":
    df = pd.read_parquet("/home/lim/data/project/sst_model_tool/src/sst/strategy2/bin_search/data.pq")
    auto_bin_1x(df, risk_max=0.7, samples_min=10)
