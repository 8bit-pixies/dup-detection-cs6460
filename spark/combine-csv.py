# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 21:27:49 2016

@author: chapm
"""

import pandas as pd

# read all csv in....
names = pd.DataFrame()
for fname in [
"../SESE/cleaned/sql-html-js-1_fix",
"../SESE/cleaned/sql-html-js-2_fix",
"../SESE/cleaned/sql-html-js-3_fix",
"../SESE/cleaned/sql-html-js-4_fix",
"../SESE/cleaned/sql-html-js-5_fix"
]:
    frame = pd.read_csv(fname + ".csv", names=['id', 'title', 'bodyString', 'tagsString'],
                        low_memory=False)
    names = names.append(frame, ignore_index=True)
