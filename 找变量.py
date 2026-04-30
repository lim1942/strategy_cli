import pandas as pd
from bin_search.auto_bin_1x import auto_bin_1x
from bin_search.auto_bin_2x import auto_bin_2x


df = pd.read_parquet("./data/trans.pq")
ret = auto_bin_1x(df, risk_max=0.55, samples_min=100)
past_features = [_["feature"] for _ in ret["后段数据"]]
lastest = [item for item in ret["近期数据"] if item["feature"] in past_features]

