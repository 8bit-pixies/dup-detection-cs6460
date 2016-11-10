import pandas as pd
import numpy as np

for fname in [
    "../SESE/sql-html-js-2",
    "../SESE/sql-html-js-1",
    "../SESE/sql-html-js-3",
    "../SESE/sql-html-js-4",
    "../SESE/sql-html-js-5"
    ]:
    so_dat = pd.read_csv(fname+".csv")
    so_dat_main = so_dat[['id', 'did', 'dtitle', 'dbody', 'dcreationdate']]
    so_dat_main = so_dat_main.assign(label = np.where(np.isnan(so_dat_main['did']), 0, 1))
    so_dat_main[['id', 'label', 'dtitle', 'dbody', 'dcreationdate']].to_csv(fname+"_labels.csv", index=False)


    
    
