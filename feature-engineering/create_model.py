# create model for milestone 1 - based on some sample of SO data

import gensim
import pandas as pd
import numpy as np

from create_dictionary import train_corpus, transform_doc2bow, tokenize
from sklearn.metrics.pairwise import cosine_similarity

from online_lsi_sim import sim_two_lsi
from online_lda_sim import sim_two_lda
from word2vec_sim import sim_two_w2v
from doc_sim import sim_two

dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
fname = "../SESE/cleaned/sql-html-sample.csv"

so_dat = pd.read_csv(fname)
so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

# build each feature, and model
corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)

# all these models have online learning support
lda_mod = gensim.models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10)

lsi_mod = gensim.models.lsimodel.LsiModel(corpus, id2word=dictionary, num_topics=100)

w2v_mod = gensim.models.Word2Vec(min_count=1, sg=1)
sentences = [tokenize(x) for x in so_dat_main['bodyString'].tolist()]
w2v_mod.build_vocab(sentences )
w2v_mod.train(sentences)

# `doc_mod` is not needed - determined upon run time
# `tag_mod` is not needed - determined upon run time

# test query
# assuming all models above...
def sim_query(doc1="html angular", doc2="html javascript"):
    """takes in two documents and computes similarity between
    both based on the models above, with all equal weights"""
    
    sim_vec = {'lsi': sim_two_lsi(doc1, doc2, lsi_mod, dictionary),
               'lda': sim_two_lda(doc1, doc2, lda_mod, dictionary), 
               'w2v': sim_two_w2v(doc1, doc2, w2v_mod), 
               'doc': sim_two(doc1, doc2)}
    
    return sim_vec, np.mean(np.array([x[1] for x in sim_vec.items()]))
    
print sim_query()




