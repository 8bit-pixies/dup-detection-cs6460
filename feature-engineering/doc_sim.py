# not learnt online - but that is okay
# as the whole corpus will only ever be two documents.


"""
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

docs = ["Julie loves me more than Linda loves me",
"Jane likes me more than Julie loves me"]

count_vec = CountVectorizer().fit(docs)
count_vec.transform(docs).todense()

cosine_similarity(count_vec.transform(docs)[0],
                  count_vec.transform(docs)[1])
"""

import gensim
from create_dictionary import train_corpus, transform_doc2bow
import pandas as pd

# or just do it on two things...
def sim_two(doc1, doc2):
    corpus = train_corpus([doc1, doc2], dictionary)
    index_sparse = gensim.similarities.docsim.SparseMatrixSimilarity(corpus, num_features=dictionary.num_docs)
    return index_sparse[transform_doc2bow(doc1, dictionary)][1]

                        
dictionary = gensim.corpora.Dictionary.load("../data/SESE_tags.gz")

if __name__ == "__main__":
    
    fname = "../SESE/cleaned/sql-html-sample.csv"
    
    so_dat = pd.read_csv(fname)
    so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]
    corpus = train_corpus(so_dat_main['tagsString'].tolist(), dictionary)
    
    index_sparse = gensim.similarities.docsim.SparseMatrixSimilarity(corpus, num_features=dictionary.num_docs)
    index_sparse.num_best = 3
    print(index_sparse[transform_doc2bow("html javascript angular", dictionary)])
                            
    sim_two("html angular", "html python")
    
    
