import pandas as pd

from bin_search.auto_bin_1x import auto_bin_1x
from bin_search.auto_bin_2x import auto_bin_2x


df = pd.read_parquet("./data/trans.pq")
auto_bin_1x(df, risk_max=0.6, samples_min=10)
