import gensim
from gensim.parsing import stem_text
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import pandas as pd
import string

from create_dictionary import tokenize, transform_doc2bow
import itertools

#

if __name__ == "__main__":
    
    dictionary = gensim.corpora.Dictionary()
    print("tokenize tags")
    tags = []    
    
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
    
            texts = [tokenize(document) for document in so_dat_main['tagsString'].tolist()]
            texts = list(itertools.chain.from_iterable(texts))
            tags.extend(list(set(texts)))
            
            
            
    dictionary.add_documents([texts])
    dictionary.save("../data/SESE.gz")
    
    
