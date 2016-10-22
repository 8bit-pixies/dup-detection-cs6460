# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 21:27:49 2016

@author: chapm
"""

import codecs
import pandas as pd
input_codec = 'UTF-16'
output_codec = 'ASCII'

for fname in [
"../SESE/cleaned/sql-html-js-1_fix",
"../SESE/cleaned/sql-html-js-2_fix",
"../SESE/cleaned/sql-html-js-3_fix",
"../SESE/cleaned/sql-html-js-4_fix",
"../SESE/cleaned/sql-html-js-5_fix"]:
    unicode_file = open(fname + ".csv", encoding="ascii", errors="ignore")
    unicode_data = unicode_file.read()
    ascii_file = open(fname + "1.csv", 'w')
    ascii_file.write(unicode_data)
    ascii_file.close()




# read all csv in....
names = pd.DataFrame()
for fname in [
"../SESE/cleaned/sql-html-js-1_fix",
"../SESE/cleaned/sql-html-js-2_fix",
"../SESE/cleaned/sql-html-js-3_fix",
"../SESE/cleaned/sql-html-js-4_fix",
"../SESE/cleaned/sql-html-js-5_fix"
]:
    frame = pd.read_csv(fname + ".csv", names=['id', 'title', 'body', 'tags'],
                        low_memory=False)
    names = names.append(frame, ignore_index=True)

