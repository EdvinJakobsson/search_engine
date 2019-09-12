import os
import json

corpus_dir = "json_data"
json_dir = os.path.join(corpus_dir, "ALL-CPI-DATA-PARSED-version0.4")

filepaths = [os.path.join(json_dir, i) for i in os.listdir(json_dir)]
for i, path in enumerate(filepaths):
    print()