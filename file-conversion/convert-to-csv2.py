import csv
import html2text

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True
h.ignore_tables = True

def collapse_spaces(x1):
    import re 
    x = re.sub(r'[^\x00-\x7F]+','', x1)
    x = re.sub(r'\s+', ' ', x)
    return x.strip()

def split_tags(x):
    import re
    x = re.sub(r'[<>]+', ' ', x)
    return x.strip()

def convert_to_ascii(x):
    x1 = x.decode("utf-8")
    return str(x1.encode("ascii", "ignore"))

for fname in [
"../SESE/sql-html-js-2",
#"../SESE/sql-html-js-1",
#"../SESE/sql-html-js-3",
#"../SESE/sql-html-js-4",
#"../SESE/sql-html-js-5"
]:
    input_file = open(fname+"_fix.csv", 'a', encoding='utf-8')

    with open(fname+".csv") as f:
        creader = csv.reader(f)
        for row in creader:
            input_file
    for i, so_dat in enumerate(pd.read_csv(fname+".csv", chunksize=9000)):
        print(i)
        so_dat_main = so_dat[['id', 'title', 'body', 'tags']]
        so_dat_main['bodyString'] = [collapse_spaces(h.handle(x)) for x in so_dat_main['body'].tolist()]
        so_dat_main['tagsString'] = [collapse_spaces(split_tags(x)) for x in so_dat_main['tags'].tolist()]
        so_dat_main = so_dat_main[['id', 'title', 'bodyString', 'tagsString']]
        
        if i == 0:
            so_dat_main.to_csv(input_file, encoding='ascii', index=False)
        else:
            so_dat_main.to_csv(input_file, header=False, encoding='ascii', index=False)
    
    input_file.close()




