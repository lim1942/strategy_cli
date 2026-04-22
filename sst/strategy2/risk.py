
import numpy as np
import pandas as pd
from datetime import timedelta, datetime

def date_now_get():
    return datetime.now().date()


def target_get(perfdate, bad_days, good_days, due_time_date, repay_time_date):
    """0是坏，1是好"""
    if bad_days < good_days:
        return -9999979
    if pd.Timestamp(perfdate - timedelta(days=bad_days)) <= due_time_date:
        return -1
    elif (repay_time_date != repay_time_date) | (repay_time_date is None):
        return 0
    elif bad_days < (repay_time_date - due_time_date).days:
        return 0
    elif good_days < (repay_time_date - due_time_date).days:
        return -2
    else:
        return 1
    
def target_df(loan, bad_days, good_days, perfdate, target="target"):
    """
    :param loan: 需要打标的df
    :param bad_days: 坏的天数
    :param good_days: 好的天数
    :param perfdate: 决策时间
    :param target: target结果列，0是坏，1是好
    :return:df
    """
    loan[target] = loan.apply(
        lambda x: target_get(
            perfdate, bad_days, good_days, x["due_time_date"], x["repay_time_date"]
        ),
        axis=1,
    )


def float_2_pct(x):
    return f"{x:.2%}" if not pd.isna(x) else None


class Risk:

    @classmethod
    def target_df(cls, source_df, bad_days, good_days, perfdate, target='target'):
        """
        :param source_df: 需要打标的df
        :param bad_days: 坏的天数
        :param good_days: 好的天数
        :param perfdate: 决策时间
        :param target: target结果列，0是坏，1是好
        :return:原source_df, 新增target列
        """
        return target_df(source_df, bad_days, good_days, perfdate, target)

    @classmethod
    def get_risk(cls, source_df=None, group_list=None, need_col=None, sort_cols=None, ascending=False, to_pct=False, **kwargs):
        """
        :param source_df: 待分析的数据
        :param group_list: 交叉分析的变量列表
        :param need_col: 保留展示的列名列表
        :param sort_cols: 需要排序的列, 比如['交易金额', '金额占比']
        :param ascending: True正向排序，默认是False倒序
        :param to_pct: float转行百分比
        :return: 新的DataFrame
        """
        df_01 = source_df.copy()
        group_list = group_list or ['is_reloan']

        need_col = need_col or ['交易单数', '单数占比', '交易金额', '金额占比', '交易人数', '人数占比', 'T-2流入', 'T-1流入',
                                '0+流入', '3+流入', '7+流入', '当前流入', 'lift', '户均额度', '户均笔数', '笔均金额']

        target_df(df_01, -1, -1, date_now_get(), target='t_1_repay_target')
        target_df(df_01, -2, -2, date_now_get(), target='t_2_repay_target')
        target_df(df_01, 0, 0, date_now_get(), target='t0_repay_target')
        target_df(df_01, 1, 1, date_now_get(), target='t1_repay_target')
        target_df(df_01, 3, 3, date_now_get(), target='t3_repay_target')
        target_df(df_01, 7, 7, date_now_get(), target='t7_repay_target')

        df_01['t0_repay_target'] = np.where((df_01.penalty_day == 0) & (df_01.t0_repay_target == 0), 1,
                                            df_01['t0_repay_target'])
        df_01['t1_repay_target'] = np.where((df_01.penalty_day == 0) & (df_01.t0_repay_target == 0), 1,
                                            df_01['t1_repay_target'])
        df_01['t3_repay_target'] = np.where((df_01.penalty_day == 0) & (df_01.t0_repay_target == 0), 1,
                                            df_01['t3_repay_target'])
        df_01['t7_repay_target'] = np.where((df_01.penalty_day == 0) & (df_01.t0_repay_target == 0), 1,
                                            df_01['t7_repay_target'])

        df_01['t_1_repay_money'] = np.where(df_01.t_1_repay_target.isin([0, 1]), df_01.t_1_repay_target * df_01.trans_money, np.nan)
        df_01['t_2_repay_money'] = np.where(df_01.t_2_repay_target.isin([0, 1]), df_01.t_2_repay_target * df_01.trans_money, np.nan)
        df_01['t0_repay_money'] = np.where(df_01.t0_repay_target.isin([0, 1]), df_01.t0_repay_target * df_01.trans_money, np.nan)
        df_01['t1_repay_money'] = np.where(df_01.t1_repay_target.isin([0, 1]), df_01.t1_repay_target * df_01.trans_money, np.nan)
        df_01['t3_repay_money'] = np.where(df_01.t3_repay_target.isin([0, 1]), df_01.t3_repay_target * df_01.trans_money, np.nan)
        df_01['t7_repay_money'] = np.where(df_01.t7_repay_target.isin([0, 1]), df_01.t7_repay_target * df_01.trans_money, np.nan)

        df_01['t_1_trans_money'] = np.where(df_01.t_1_repay_target.isin([0, 1]), df_01.trans_money, np.nan)
        df_01['t_2_trans_money'] = np.where(df_01.t_2_repay_target.isin([0, 1]), df_01.trans_money, np.nan)
        df_01['t0_trans_money'] = np.where(df_01.t0_repay_target.isin([0, 1]), df_01.trans_money, np.nan)
        df_01['t1_trans_money'] = np.where(df_01.t1_repay_target.isin([0, 1]), df_01.trans_money, np.nan)
        df_01['t3_trans_money'] = np.where(df_01.t3_repay_target.isin([0, 1]), df_01.trans_money, np.nan)
        df_01['t7_trans_money'] = np.where(df_01.t7_repay_target.isin([0, 1]), df_01.trans_money, np.nan)

        df_01['repay_money'] = np.where(df_01.repay_time.isnull(), 0, df_01.trans_money)
        df_01['user_id_dt'] = df_01.apply(lambda x: f"{x['user_id']}_{x['loan_time'].strftime('%Y_%m_%d')}", axis=1)
        col = ['borrow_id', 'user_id', 'user_id_dt', 'repay_money', 't_2_repay_money', 't_1_repay_money', 't0_repay_money',
               't1_repay_money', 't3_repay_money', 't7_repay_money', 'trans_money', 't_2_trans_money', 't_1_trans_money',
               't0_trans_money', 't1_trans_money', 't3_trans_money', 't7_trans_money']
        col = col + group_list
        df_new_02 = df_01[col].copy()
        # 使用用户id_日期来做人维度的统计
        df_new_02 = df_new_02.rename(columns={'user_id': 'user_id_old'})
        df_new_02 = df_new_02.rename(columns={'user_id_dt': 'user_id'})
        df_new_02 = df_new_02.groupby(group_list).agg({"borrow_id": "count", 'user_id': "nunique",
                                                       "repay_money": "sum", 't_2_repay_money': "sum",
                                                       't_1_repay_money': "sum", "t0_repay_money": "sum",
                                                       "t1_repay_money": "sum", "t3_repay_money": "sum",
                                                       "t7_repay_money": "sum", "trans_money": "sum",
                                                       "t_2_trans_money": "sum", "t_1_trans_money": "sum",
                                                       "t0_trans_money": "sum", "t3_trans_money": "sum",
                                                       "t1_trans_money": "sum", "t7_trans_money": "sum"})
        if len(group_list) == 2:
            df_sum = df_new_02.groupby(group_list[0]).sum()
            df_sum[group_list[1]] = '合计'
            df_sum['user_id'] = df_01.groupby(group_list[0]).apply(lambda g: g['user_id_dt'].nunique())
            df_sum.reset_index(inplace=True)
            df_new_02.reset_index(inplace=True)
            df_new_02 = pd.concat([df_new_02, df_sum], sort=True)
        elif len(group_list) == 1:
            if isinstance(df_new_02.index, pd.CategoricalDtype):
                df_new_02.index = df_new_02.index.add_categories(['合计'])
            df_new_02.loc['合计'] = df_new_02.sum()
            df_new_02.loc['合计', 'user_id'] = df_01['user_id_dt'].nunique()

        df_new_02['T_1_rate'] = df_new_02.apply(lambda x:round((x['t_1_trans_money']-x['t_1_repay_money'])/x['t_1_trans_money'],4) if x['t_1_trans_money'] >0 else np.nan,axis=1)
        df_new_02['T_2_rate'] = df_new_02.apply(lambda x:round((x['t_2_trans_money']-x['t_2_repay_money'])/x['t_2_trans_money'],4) if x['t_2_trans_money'] >0 else np.nan,axis=1)
        df_new_02['T0_rate'] = df_new_02.apply(lambda x:round((x['t0_trans_money']-x['t0_repay_money'])/x['t0_trans_money'],4) if x['t0_trans_money'] >0 else np.nan,axis=1)
        df_new_02['T1_rate'] = df_new_02.apply(lambda x:round((x['t1_trans_money']-x['t1_repay_money'])/x['t1_trans_money'],4) if x['t1_trans_money'] >0 else np.nan,axis=1)
        df_new_02['T3_rate'] = df_new_02.apply(lambda x:round((x['t3_trans_money']-x['t3_repay_money'])/x['t3_trans_money'],4) if x['t3_trans_money'] >0 else np.nan,axis=1)
        df_new_02['T7_rate'] = df_new_02.apply(lambda x:round((x['t7_trans_money']-x['t7_repay_money'])/x['t7_trans_money'],4) if x['t7_trans_money'] >0 else np.nan,axis=1)
        df_new_02['now_rate'] = df_new_02.apply(lambda x:round((x['trans_money']-x['repay_money'])/x['trans_money'],4) if x['trans_money'] >0 else np.nan,axis=1)
        df_new_02['principal_amt'] = df_new_02['trans_money']
        df_new_02['户均额度'] = df_new_02['trans_money'] / df_new_02['user_id']
        df_new_02['户均笔数'] = df_new_02['borrow_id'] / df_new_02['user_id']
        df_new_02['笔均金额'] = df_new_02['trans_money'] / df_new_02['borrow_id']
        if len(group_list) == 2:
            df_new_02 = df_new_02.merge(df_sum[[group_list[0], 'trans_money','user_id','borrow_id','t0_repay_money','t0_trans_money']], on=group_list[0])
            df_new_02['金额占比'] = df_new_02['principal_amt'] / (df_new_02['trans_money_y'])
            df_new_02['人数占比'] = df_new_02['user_id_x'] / (df_new_02['user_id_y'])
            df_new_02['单数占比'] = df_new_02['borrow_id_x'] / (df_new_02['borrow_id_y'])
            df_new_02['lift'] = df_new_02['T0_rate'] / ((df_new_02['t0_trans_money_y'] - df_new_02['t0_repay_money_y']) / df_new_02['t0_trans_money_y'])
            df_new_02['lift'] = df_new_02['lift'].apply(lambda x: round(x, 2))
            col = ['borrow_id_x', '单数占比', 'principal_amt', '金额占比', 'user_id_x', '人数占比', 'T_2_rate', 'T_1_rate',
                   'T0_rate', 'T3_rate', 'T7_rate', 'now_rate', 'lift', '户均额度', '户均笔数', '笔均金额']
            col = group_list + col
            df_002 = df_new_02[col].copy()
            col_rename = {'borrow_id_x': '交易单数', 'principal_amt': '交易金额', 'user_id_x': '交易人数', 'T_2_rate': 'T-2流入',
                          'T_1_rate': 'T-1流入', 'T0_rate': '0+流入', 'T1_rate': '1+流入', 'T7_rate': '7+流入',
                          'T3_rate': '3+流入', 'now_rate': '当前流入'}
            df_002.rename(columns=col_rename, inplace=True)
            df_002[['交易单数', '交易金额', '交易人数']] = df_002[['交易单数', '交易金额', '交易人数']].astype(int)
            if to_pct:
                df_002[['单数占比', '金额占比', '人数占比', 'T-2流入', 'T-1流入', '0+流入', '3+流入', '7+流入', '当前流入']] =\
                    df_002[['单数占比', '金额占比', '人数占比', 'T-2流入', 'T-1流入', '0+流入', '3+流入', '7+流入', '当前流入']].applymap(float_2_pct)
            if sort_cols:
                df_002 = df_002.sort_values(sort_cols, ascending=ascending)
            df_002 = df_002[group_list + need_col]
            # 旋转坐标轴
            df_002 = df_002.pivot(index=group_list[1], columns=group_list[0])
            df_002 = df_002.swaplevel(0, 1, axis=1)
            df_002 = df_002.sort_index(axis=1, level=0, sort_remaining=False)
        elif len(group_list) == 1:
            df_new_02['金额占比'] = df_new_02['principal_amt'] / df_new_02.loc['合计', 'principal_amt']
            df_new_02['人数占比'] = df_new_02['user_id'] / df_new_02.loc['合计', 'user_id']
            df_new_02['单数占比'] = df_new_02['borrow_id'] / (df_new_02.loc['合计', 'borrow_id'])
            df_new_02['lift'] = df_new_02['T0_rate'] / df_new_02.loc['合计', 'T0_rate']
            df_new_02['lift'] = df_new_02['lift'].apply(lambda x: round(x, 2))
            col = ['borrow_id', 'user_id', '单数占比', 'principal_amt', '金额占比', '人数占比', 'T_2_rate', 'T_1_rate',
                   'T0_rate', 'T3_rate', 'T7_rate', 'now_rate', 'lift', '户均额度', '户均笔数', '笔均金额']
            df_002 = df_new_02[col].copy()
            col_rename = {'borrow_id': '交易单数', 'principal_amt': '交易金额', 'user_id': '交易人数', 'T_2_rate': 'T-2流入',
                          'T_1_rate': 'T-1流入', 'T0_rate': '0+流入', 'T1_rate': '1+流入', 'T7_rate': '7+流入',
                          'T3_rate': '3+流入', 'now_rate': '当前流入'}
            df_002.rename(columns=col_rename, inplace=True)
            df_002[['交易单数', '交易金额', '交易人数']] = df_002[['交易单数', '交易金额', '交易人数']].astype(int)
            if to_pct:
                df_002[['单数占比', '金额占比', '人数占比', 'T-2流入', 'T-1流入', '0+流入', '3+流入', '7+流入', '当前流入']] =\
                    df_002[['单数占比', '金额占比', '人数占比', 'T-2流入', 'T-1流入', '0+流入', '3+流入', '7+流入', '当前流入']].applymap(float_2_pct)
            if sort_cols:
                df_002 = df_002.sort_values(sort_cols, ascending=ascending)
            df_002 = df_002[need_col]
        else:
            raise Exception("最多两个维度")
        result_df = pd.concat([df_002.drop('合计'), df_002.loc[['合计']]])

        if '交易人数' in need_col:
            if len(group_list) == 2:
                # 修改交易人数的总计值
                for first_level_col in result_df.columns.get_level_values(0).unique():
                    sum_user_id = result_df[(first_level_col, '交易人数')].iloc[:-1].sum()
                    result_df.loc['合计', (first_level_col, '交易人数')] = sum_user_id

            elif len(group_list) == 1:
                # 修改交易人数的总计值
                sum_user_id = result_df['交易人数'].iloc[:-1].sum()
                result_df.loc['合计', '交易人数'] = sum_user_id

        return result_df

   