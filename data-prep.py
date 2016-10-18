# loading libs and configs....
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

# clean up body 
so_dat = pd.read_csv("SESE/sql-html-js-1.csv", nrows=10000)

so_dat_main = so_dat[['id', 'title', 'body', 'tags']]
so_dat_main['body'] = pd.Series([collapse_spaces(h.handle(x)) for x in so_dat_main['body'].tolist()])

# now try to train... lda for the body...

import gensim
from gensim.parsing import stem_text
from gensim.utils import smart_open, simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

def tokenize(text):
    return [stem_text(token) for token in simple_preprocess(text) if token not in STOPWORDS]

texts = [tokenize(x) for x in so_dat_main[['body']].tolist()]
dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 100 was used in the stackoverflow paper...
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, update_every=1, chunksize=10000, passes=1)

# lda.print_topics(5)
