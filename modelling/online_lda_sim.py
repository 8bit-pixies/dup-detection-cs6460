import gensim
import pandas as pd
import numpy as np
import scipy

from create_dictionary import train_corpus, transform_doc2bow
from sklearn.metrics.pairwise import cosine_similarity

# https://radimrehurek.com/gensim/tut3.html

# create dictionary, as gensim doesn't have an implementation for infinitely large
# dictionaries at this stage.
# this is a static dictionary - check "create_dictionary.py"

def sim_two_lda(doc1, doc2, lda, dictionary):
    def extract_prob(ls):
        return np.array([x[1] for x in ls]).reshape(1,-1)
    return cosine_similarity(extract_prob(lda[transform_doc2bow(doc1, dictionary)]), 
                             extract_prob(lda[transform_doc2bow(doc2, dictionary)]))[0][0]

def sim_all_lda(single, docs, lda, dictionary):
    def extract_prob_single(ls, num_topics):
        V = np.array([x[1] for x in ls])
        J = np.array([x[0] for x in ls])
        I = (V * 0) 
        output = np.array(scipy.sparse.coo_matrix((V, (I, J)), shape=(1, num_topics)).todense()).flatten()
        return output
    get_docs = np.vstack([extract_prob_single(lda[transform_doc2bow(doc, dictionary)], lda.num_topics) 
                 for doc in docs])
    get_single = extract_prob_single(lda[transform_doc2bow(single, dictionary)], lda.num_topics)
    soln = cosine_similarity(np.atleast_2d(get_single), get_docs)
    return soln
        
        
if __name__ == "__main__":
    
    dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
    
    fname = "../SESE/cleaned/sql-html-sample.csv"
    
    so_dat = pd.read_csv(fname)
    so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]
    
    corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)
    lda = gensim.models.ldamodel.LdaModel(train_corpus(['html'], dictionary), id2word=dictionary, num_topics=10, 
                                          minimum_probability=0.0)
    lda.update(corpus)
    lda.save("../data/lda-sample.gz")
    lda = gensim.models.LdaModel.load('../data/lda-sample.gz')
    
    
    print(sim_two_lda("html angular", "html python"))
    
    
