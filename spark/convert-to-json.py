import pandas as pd
import html2text

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True
h.ignore_tables = True

def collapse_spaces(x):
    import re 
    x = re.sub(r'\s+', ' ', x)
    return x.strip()

def split_tags(x):
    import re
    x = re.sub(r'[<>]+', ' ', x)
    return x.strip()


fname = "../SESE/sql-html-js-1"

input_file = open(fname+".json", 'a')

for i, so_dat in enumerate(pd.read_csv(fname+".csv", chunksize=9000)):
    print(i)
    so_dat_main = so_dat[['id', 'title', 'body', 'tags']]
    so_dat_main.loc[:,'body'] = pd.Series([collapse_spaces(h.handle(x)) for x in so_dat_main['body'].tolist()])
    so_dat_main.loc[:,'tags'] = pd.Series([collapse_spaces(split_tags(x)) for x in so_dat_main['tags'].tolist()])
    
    so_dat_main.to_json(input_file, orient='records', lines=True)

input_file.close()


for fname in [
"../SESE/sql-html-js-2",
"../SESE/sql-html-js-3",
"../SESE/sql-html-js-4",
"../SESE/sql-html-js-5"
]:
    input_file = open(fname+".json", 'a')

    for i, so_dat in enumerate(pd.read_csv(fname+".csv", chunksize=9000)):
        print(i)
        so_dat_main = so_dat[['id', 'title', 'body', 'tags']]
        so_dat_main.loc[:,'body'] = pd.Series([collapse_spaces(h.handle(x)) for x in so_dat_main['body'].tolist()])
        so_dat_main.loc[:,'tags'] = pd.Series([collapse_spaces(split_tags(x)) for x in so_dat_main['tags'].tolist()])
        
        so_dat_main.to_json(input_file, orient='records', lines=True)
    
    input_file.close()

