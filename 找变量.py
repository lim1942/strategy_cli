import pandas as pd
from bin_search.auto_bin_1x import auto_bin_1x
from bin_search.auto_bin_2x import auto_bin_2x



def get_bins():
    df = pd.read_parquet("./data/trans.pq")
    ret = auto_bin_1x(df, risk_max=0.55, samples_min=100)
    
