import pandas as pd
from sst.strategy2.risk import Risk

def get_pb(row):
    if row.model211MxAcardV127Cat <= 504:
        return "00"
    elif row.model203MxAcardV119Stack <= 500:
        return "01"
    elif row.model203MxAcardV119 <= 486:
        return "02"
    else:
        return "PASS"

trans = pd.read_parquet("data/trans.pq")
trans["get_pb"] = trans.apply(lambda x: get_pb(x), axis=1)
# 为每个用户计算了一个 get_pb 值，代表该用户在瀑布式拒贷流程中 被哪个变量命中
risk_df = Risk.get_risk( trans, [ "get_pb"], ["交易单数", "交易人数", "人数占比", "0+流入", "3+流入"])
print("风险变化:", risk_df.loc['PASS','0+流入']- risk_df.loc['合计','0+流入'])
