import pandas as pd
import numpy as np
import glob
import pandas as pd
import os, sys

pwd_file = os.path.dirname(__file__)
data_dir = pwd_file + '/data/'
files = glob.glob(data_dir + 'best_*.xlsx') 

all_data = pd.DataFrame()
for f in files:
    df = pd.read_excel(f)
    all_data = all_data.append(df,ignore_index=True)

# --- combine all file to best_seller_book.xlsx
all_data.to_excel(pwd_file + '/' + "best_seller_book.xlsx")

