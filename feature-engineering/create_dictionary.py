import gensim
from gensim.parsing import stem_text
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import pandas as pd
import string

def tokenize(text):
    return [stem_text(token) for token in simple_preprocess(text) if token not in STOPWORDS and not bad_word(token)]

def bad_word(text):
    """returns true if it isn't a word, else returns false"""
    if not text[0] in list(string.ascii_letters):
        return True
    if len(text) > 30:
        return True
    return False

def train_corpus(text, dictionary):
    """text is list of sentences/body of question"""
    texts = [tokenize(x) for x in text]
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus
    
def transform_doc2bow(text, dictionary):
    return dictionary.doc2bow(tokenize(text))

dictionary = gensim.corpora.Dictionary()

for fname in [
"../SESE/cleaned/sql-html-js-2",
"../SESE/cleaned/sql-html-js-1",
"../SESE/cleaned/sql-html-js-3",
"../SESE/cleaned/sql-html-js-4",
"../SESE/cleaned/sql-html-js-5"
]:

    for i, so_dat in enumerate(pd.read_csv(fname+"_fix.csv", chunksize=9000)):
        print(i)
        so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

        texts = [tokenize(document) for document in so_dat_main['bodyString'].tolist()]
        dictionary.add_documents(texts)


dictionary.save("../data/SESE.gz")
