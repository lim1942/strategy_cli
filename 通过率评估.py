import pandas as pd
from gen_strategy.mx_verify_code_533 import VerifyTree as old_strategy
from gen_strategy.mx_verify_code_534 import VerifyTree as new_strategy

apply = pd.read_parquet("data/apply.pq")
apply['old_pass'] = apply.apply(lambda x: old_strategy().calculate(x)[0], axis=1)
apply['new_pass'] = apply.apply(lambda x: new_strategy().calculate(x)[0], axis=1)

old_pass_rate = (apply['old_pass'] == "PASS").sum() / apply.shape[0]
new_pass_rate = (apply['new_pass'] == "PASS").sum() / apply.shape[0]
print("通过率变化:", new_pass_rate - old_pass_rate)
