import pandas as pd
import numpy as np
from datetime import timedelta


# 获取不进行预处理和分析的列
def get_exclude_cols(exclude_cols: list[str] | None = None) -> list[str]:
    _exclude_cols = ["id", "user_id", 'userId', "app_id", "loan_time", "loan_time_date", "apply_time", "apply_time_date",
             "due_time_date", "repay_time", "repay_time_date", "batch_id", "borrow_id", "product_name", "due_time",
             "real_money", "repay_money", "repay_status", "is_reloan", "ext_num", "product_is_reloan", 'target',
            "penalty_day", "phone", "amount", "get_amt_time", "increase_amount_type", "credit_id", "credit_time", "biz208RegistTime", "biz209RegistDate",
            "refuse_code", "verify_id", "biz501Random1", "biz502Random2", "biz503Random3", "biz504Random4",
            "all501Random1", "all502Random2", "all503Random3", "all504Random4", "base030appCode",
            "biz037AppId", "biz122FirstReloanTime", "biz140FirstReloanCreditTime", "businessId", "trans_money",
            "biz141AmountFlowCredit", "biz186FirstGetCreditTime", "biz044RiskFlow", "base040FbcValue",
            "base041FbpValue", "base042UserAgent", "adv016IDFraud"]
    _exclude_cols.extend(exclude_cols or [])
    return _exclude_cols
    
    
# 获取要分析的特征列
def get_features(
    df: pd.DataFrame,
    exclude_cols: list[str] | None = None,
    filter_prefix: list[str] | None = None,
) -> list[str]:
    features = []
    exclude_cols = get_exclude_cols(exclude_cols)
    for col in df.columns:
        if col not in exclude_cols:
            # 有前缀过滤，且列名以前缀开头，添加到特征列表
            if filter_prefix:
                if any(col.startswith(prefix) for prefix in filter_prefix):
                    features.append(col)
            # 没有前缀过滤，直接添加
            else:
                features.append(col)
    return features


# 特殊列剔除，异常数据剔除
def base_handle(df: pd.DataFrame, cate_cols: list[str] | None = None, exclude_cols: list[str] | None = None, filter_prefix: list[str] | None = None, target_col: str = 'target'):
    # 1.获取特征列
    features = get_features(df, exclude_cols, filter_prefix)
    # 2.删除未表现数据
    data_df = df[df[target_col].isin([0, 1])]
    # 3.填充缺失值 -9999979
    data_df[features] = data_df[features].fillna(-9999979)
    # 4.类型转换
    for col in features:
        # 指定为类别变量，转换为字符串类型
        if cate_cols and col in cate_cols:
            data_df[col] = data_df[col].astype(str)
        # 非数值型变量，且类别数大于20，尝试转换为数值型
        elif not pd.api.types.is_numeric_dtype(data_df[col]):
            try:
                data_df[col] = data_df[col].astype(float)
            except ValueError:
                pass
    return data_df, features

def calc_iv(
    df: pd.DataFrame,
    feature: str,
    target: str = 'target',
    bins: int = 10,
    weight: str | None = 'trans_money',
) -> float:
    """
    计算单个特征的 Information Value (IV)。

    对连续变量自动分箱，对类别变量按类别分组。
    若指定 weight，则用金额加权计算 event/non-event 分布；
    传入 weight=None 退回普通计数模式。

    IV 参考标准:
        < 0.02  : 无预测力
        0.02~0.1: 弱
        0.1~0.3 : 中
        0.3~0.5 : 强
        > 0.5   : 可疑（过拟合风险）
    """
    cols = [feature, target] + ([weight] if weight and weight in df.columns else [])
    tmp = df[cols].copy()
    tmp.rename(columns={feature: 'x', target: 'y'}, inplace=True)
    use_weight = weight and weight in df.columns
    if use_weight:
        tmp.rename(columns={weight: 'w'}, inplace=True)
        tmp['w'] = tmp['w'].fillna(0).clip(lower=0)
    else:
        tmp['w'] = 1.0

    # 连续变量分箱，类别变量直接用原值
    if pd.api.types.is_numeric_dtype(tmp['x']):
        tmp["bucket"] = pd.qcut(tmp["x"], q=bins, duplicates="drop")
        # 常数列（所有值相同）qcut 会产生全 NaN，无预测力直接返回 0
        if tmp["bucket"].isna().all():
            return 0.0
    else:
        tmp['bucket'] = tmp['x'].astype(str)

    total_event = tmp.loc[tmp['y'] == 1, 'w'].sum()
    total_non_event = tmp.loc[tmp['y'] == 0, 'w'].sum()

    grouped = tmp.groupby('bucket', observed=True).apply(
        lambda g: pd.Series({
            'event': g.loc[g['y'] == 1, 'w'].sum(),
            'non_event': g.loc[g['y'] == 0, 'w'].sum(),
        }), 
    ).reset_index()

    grouped['dist_event'] = (grouped['event'] / total_event).replace(0, 1e-6)
    grouped['dist_non_event'] = (grouped['non_event'] / total_non_event).replace(0, 1e-6)
    grouped['woe'] = np.log(grouped['dist_event'] / grouped['dist_non_event'])
    grouped['iv'] = (grouped['dist_event'] - grouped['dist_non_event']) * grouped['woe']
    return grouped['iv'].sum()


def calc_psi(
    df: pd.DataFrame,
    feature: str,
    time_col: str = 'due_time',
    bins: int = 10,
    threshold: float = 0.25,
    cutoff = None,
) -> float:
    """
    计算单个特征的 PSI。

    以时间列中位数为切分点，前半段为基准，后半段为对比。

    PSI 参考标准:
        < 0.1  : 稳定
        0.1~0.25: 轻微漂移，需关注
        > 0.25 : 不稳定，建议剔除
    """
    tmp = df[[feature, time_col]].copy()
    mask = pd.to_datetime(tmp[time_col]) <= cutoff
    base = tmp.loc[mask, feature]
    comp = tmp.loc[~mask, feature]
    if len(base) == 0 or len(comp) == 0:
        return np.nan

    is_numeric = pd.api.types.is_numeric_dtype(tmp[feature])
    if is_numeric:
        _, bin_edges = pd.qcut(base.dropna(), q=bins, retbins=True, duplicates='drop')
        bin_edges[0] = -np.inf
        bin_edges[-1] = np.inf
        base_dist = pd.cut(base, bins=bin_edges).value_counts(normalize=True).sort_index()
        comp_dist = pd.cut(comp, bins=bin_edges).value_counts(normalize=True).sort_index()
    else:
        all_cats = tmp[feature].astype(str).unique()
        base_dist = base.astype(str).value_counts(normalize=True).reindex(all_cats, fill_value=1e-6)
        comp_dist = comp.astype(str).value_counts(normalize=True).reindex(all_cats, fill_value=1e-6)
    base_a = base_dist.reindex(comp_dist.index, fill_value=1e-6).clip(lower=1e-6)
    comp_a = comp_dist.clip(lower=1e-6)
    return float(((comp_a - base_a) * np.log(comp_a / base_a)).sum())


def remove_collinear_features(
    df: pd.DataFrame,
    features: list[str],
    target: str = 'target',
    corr_max: float = 0.9,
    iv_dict: dict[str, float] | None = None,
    weight: str | None = 'trans_money',
    bins: int = 10,
) -> tuple[list[str], list[str]]:
    """
    基于相关性剔除共线特征，保留 IV 更高的一方。

    对每一对相关系数绝对值超过 corr_max 的特征，按相关系数从高到低贪心处理：
    保留 IV 较大的特征，剔除 IV 较小的特征。非数值型特征不参与相关性计算，直接保留。

    Parameters
    ----------
    df       : 数据集（需已完成缺失值填充）
    features : 候选特征列表
    target   : 标签列名
    corr_max : 相关系数阈值，|corr| 超过则视为共线（默认 0.9）
    iv_dict  : 预先计算好的 {feature: IV} 字典，传入可跳过重算
    weight   : IV 计算时的金额加权列名，None 则退回等权计数
    bins     : IV 连续变量分箱数

    Returns
    -------
    kept_features    : 保留的特征列表（顺序与入参一致）
    removed_features : 被剔除的特征列表
    """
    # 1. 计算 IV（如果未传入）
    if iv_dict is None:
        iv_dict = {
            feat: calc_iv(df, feat, target, bins=bins, weight=weight)
            for feat in features
        }

    # 2. 只对数值型特征做相关性分析，非数值直接保留
    numeric_feats = [f for f in features if pd.api.types.is_numeric_dtype(df[f])]

    corr_matrix = df[numeric_feats].corr().abs()
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    # 3. 找出所有高相关对，按相关系数降序处理（优先处理最强共线的一对）
    high_corr_pairs = (
        upper.stack()
        .reset_index()
        .rename(columns={'level_0': 'feat_a', 'level_1': 'feat_b', 0: 'corr'})
        .query('corr > @corr_max')
        .sort_values('corr', ascending=False)
    )

    # 4. 贪心剔除：已被标记移除的特征跳过，每次保留 IV 较高的一方
    remove_set: set[str] = set()
    for _, row in high_corr_pairs.iterrows():
        a, b = row['feat_a'], row['feat_b']
        if a in remove_set or b in remove_set:
            continue
        if iv_dict.get(a, 0) >= iv_dict.get(b, 0):
            remove_set.add(b)
        else:
            remove_set.add(a)

    kept = [f for f in features if f not in remove_set]
    removed = list(remove_set)
    return kept, removed


def prepare(
    df,
    cate_cols=None,
    exclude_cols=None,
    filter_prefix=None,
    target="target",
    time_col="due_time_date",
    weight="trans_money",
    iv_min=0.001,
    csi_max=0.25,
    corr_max=0.96,
):
    # 1.预处理数据
    print(f"一.数据预处理，尺寸【{df.shape}】")
    df, features = base_handle(df, cate_cols, exclude_cols, filter_prefix, target)
    print(f"\t剔除未表现数据,过滤特征。尺寸【{df.shape}】，特征数【{len(features)}】\n")
    
    # 2.跑iv
    print(f"二.iv筛选,iv_min={iv_min}")
    remove_features = []
    iv_dict = dict()
    for feat in features:
        iv = calc_iv(df, feat, target, bins=10, weight=weight)
        iv_dict[feat] = iv
        if iv < iv_min:
            remove_features.append(feat)
    features = [f for f in features if f not in remove_features]
    print(
        f"\t完成iv筛选,剔除iv小于{iv_min}的特征{len(remove_features)}个，特征数【{len(features)}】\n"
    )
    
    # 3.跑psi
    print(f"三.psi筛选,threshold={csi_max}")
    time_min, time_max = df[time_col].dt.date.min(), df[time_col].dt.date.max()
    time_cutoff_point = time_min + timedelta(days=(time_max - time_min).days // 2)
    time_cutoff_point = pd.to_datetime(time_cutoff_point)
    remove_features = []
    for feat in features:
        psi = calc_psi(df, feat, time_col, bins=10, threshold=csi_max, cutoff=time_cutoff_point)
        if psi > csi_max:
            remove_features.append(feat)
    features = [f for f in features if f not in remove_features]
    print(
        f"\t完成psi筛选,剔除psi大于{csi_max}的特征{len(remove_features)}个，特征数【{len(features)}】\n"
    )

    # 4.共线剔除
    print(f"四.共线剔除,corr_max={corr_max}")
    features, removed = remove_collinear_features(
        df, features, target=target, corr_max=corr_max, iv_dict=iv_dict, weight='trans_money'
    )
    print(
        f"\t完成共线剔除,剔除特征{len(removed)}个，特征数【{len(features)}】\n"
    )
    
    # 5.按时间切分为两段数据
    print(f"五.按时间切分为两段数据，时间点【{time_cutoff_point}】")
    df[f"{time_col}_cut"] = df[time_col].apply(lambda x: f"{time_min}_{time_cutoff_point.strftime('%Y-%m-%d')}" if x <= time_cutoff_point else f"{time_cutoff_point.strftime('%Y-%m-%d')}_{time_max}")
    left_df, right_df = df[df[time_col] <= time_cutoff_point], df[df[time_col] > time_cutoff_point]
    print(f"\t左数据集尺寸【{left_df.shape}】，右数据集尺寸【{right_df.shape}】")
    return df, features, (left_df, right_df)

if __name__ == '__main__':
    _df = pd.read_parquet("data.pq")
    prepare(_df)