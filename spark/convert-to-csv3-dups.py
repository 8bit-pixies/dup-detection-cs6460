import csv
import html2text
import pandas as pd

h = html2text.HTML2Text()
h.ignore_links = True
h.ignore_images = True
h.ignore_emphasis = True
h.ignore_tables = True

def force_to_unicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else str(text).decode('utf8')

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

def try_convert(x):
    x = force_to_unicode(x)
    return collapse_spaces(h.handle(x.encode('ascii', 'ignore')))
    
    
for fname in [
"../SESE/2016_dups_only",
"../SESE/2016_link_dups",
"../SESE/2016_link_dups_time"
]:
    so_dat_main = pd.read_csv(fname+".csv")
    so_dat_main['bodyString'] = [try_convert(x) for x in so_dat_main['body'].tolist()]
    so_dat_main['tagsString'] = [try_convert(x) for x in so_dat_main['tags'].tolist()]
    so_dat_main['dbodyString'] = [try_convert(x) for x in so_dat_main['dbody'].tolist()]
    so_dat_main['dtagsString'] = [try_convert(x) for x in so_dat_main['dtags'].tolist()]

    so_dat_main = so_dat_main[['id', 'title', 'bodyString', 'tagsString', 'dbodyString', 'dtagsString', 'dtitle', 'did']]
    so_dat_main.to_csv(fname+"_fix.csv", index=False)




