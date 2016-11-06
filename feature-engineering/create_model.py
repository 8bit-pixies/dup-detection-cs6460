# create model for milestone 1 - based on some sample of SO data
import gensim
import pandas as pd
import numpy as np
import scipy

from create_dictionary import train_corpus, transform_doc2bow, tokenize
from sklearn.metrics.pairwise import cosine_similarity

from online_lsi_sim import sim_two_lsi, sim_all_lsi
from online_lda_sim import sim_two_lda, sim_all_lda
from word2vec_sim import sim_two_w2v, sim_all_w2v
from doc_sim import sim_two, sim_all

def sim_query(doc1, doc2, dictionary,
              lsi_mod, lda_mod, w2v_mod):
    """takes in two documents and computes similarity between
    both based on the models above, with all equal weights"""
    
    sim_vec = {'lsi': sim_two_lsi(doc1, doc2, lsi_mod, dictionary),
               'lda': sim_two_lda(doc1, doc2, lda_mod, dictionary), 
               'w2v': sim_two_w2v(doc1, doc2, w2v_mod), 
               'doc': sim_two(doc1, doc2, dictionary)}
    
    return sim_vec, np.mean(np.array([x[1] for x in sim_vec.items()]))
    
def sim_query_all(single, docs, dictionary,
              lsi_mod, lda_mod, w2v_mod):
    """takes in two documents and computes similarity between
    both based on the models above, with all equal weights"""
    
    #sim_all_lda(single, doc_test, lda_mod, dictionary)
    #sim_all_w2v(single, doc_test, w2v_mod)
    #sim_all_lsi(single, doc_test, lsi_mod, dictionary)
    #sim_all(single, doc_test, dictionary)
    
    sim_vec = {'lsi': sim_all_lsi(single, docs, lsi_mod, dictionary),
               'lda': sim_all_lda(single, docs, lda_mod, dictionary), 
               'w2v': sim_all_w2v(single, docs, w2v_mod), 
               'doc': sim_all(single, docs, dictionary)}
    
    return sim_vec

def sim_stackoverflow(single_dict, docs_df, columns, dictionary, 
                      lsi_mod, lda_mod, w2v_mod):
    """
    single_dict is a dictionary...
    
    docs_df is dataframe
    
    """
    if columns is None:
        columns = {'title': 'title', 
                   'body': 'bodyString', 
                   'tag': 'tagsString'}
    body_sim = sim_query_all(single_dict[columns['body']], docs_df[columns['body']].tolist(), 
                             dictionary, lsi_mod, lda_mod, w2v_mod)
    title_sim = sim_query_all(single_dict[columns['title']], docs_df[columns['title']].tolist(), 
                             dictionary, lsi_mod, lda_mod, w2v_mod)
    tag_sim = sim_query_all(single_dict[columns['tag']], docs_df[columns['tag']].tolist(), 
                             dictionary, lsi_mod, lda_mod, w2v_mod)
    
    # more efficient to exclude it in `sim_query_all`    
    title_sim.pop('lda', None)
    title_sim.pop('lsi', None)
    
    tag_sim.pop('lsi', None)
    tag_sim.pop('lda', None)
    tag_sim.pop('w2v', None)
    
    return {
            'body': body_sim, 
            'title': title_sim, 
            'tag' : tag_sim            
            }


dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
fname = "../SESE/cleaned/sql-html-sample.csv"

so_dat = pd.read_csv(fname)
so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

# build each feature, and model
corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)

# all these models have online learning support
print "training lda..."
lda_mod = gensim.models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10, minimum_probability=0.0)
print "training lsi..."
lsi_mod = gensim.models.lsimodel.LsiModel(corpus, id2word=dictionary, num_topics=100)
print "training word2vec..."
w2v_mod = gensim.models.Word2Vec(min_count=5, sg=5)
sentences = [tokenize(x) for x in so_dat_main['bodyString'].tolist()]
w2v_mod.build_vocab(sentences )
w2v_mod.train(sentences)

# `doc_mod` is not needed - determined upon run time
# `tag_mod` is not needed - determined upon run time
print sim_query("html angular", "html javascript", dictionary,
                 lsi_mod, lda_mod, w2v_mod)

# say we update with another sample of documents
print "preparing to update models..."
f_update = "../SESE/cleaned/sql-html-sample-update.csv"
so_dat = pd.read_csv(fname)
so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

print "updating lda"
corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)
lda_mod.update(corpus)
print "updating lsi"
lsi_mod.add_documents(corpus, chunksize=1000, decay=0.99999) # decay to weigh newer data higher

print "updating w2v"
sentences2 = [tokenize(x) for x in so_dat_main['bodyString'].tolist()]
w2v_mod.build_vocab(sentences2, update=True)
w2v_mod.train(sentences2)

print sim_query("html angular", "html javascript", dictionary,
                 lsi_mod, lda_mod, w2v_mod)

"""
#######################################################################

# try one which is marked as a dup...
# we can see that all metrics, but doc is actualyl quite high on similarity
# which is why raw doc sim is only for tags?
print sim_query("Angular2 exception: Can't bind to 'ngForIn' since it isn't a known native property", 
                "Angular 2 *ngFor syntax", dictionary,
                 lsi_mod, lda_mod, w2v_mod) # 0.726

from sample_docs import doc_text1 # this one shoudl be sim
from sample_docs import doc_text2 # this one shoudl not be sim

# it is clear that w2v sees that it is quite similar
print sim_query(doc_text1[0], doc_text1[1], dictionary,
                 lsi_mod, lda_mod, w2v_mod)
# {'w2v': 0.85930765, 'doc': 0.098250151, 'lda': 0.36619797317536301, 'lsi': 0.002013389}, 0.33144228990711677)

print sim_query(doc_text2[0], doc_text2[1], dictionary,
                 lsi_mod, lda_mod, w2v_mod)

"""

# step 2...figure out a way to do it for:
# title...tags...description
# and combine it for one big model and not pairwise either.


# compare index with first 10
doc_test = so_dat_main['bodyString'].tolist()[:10]
single = so_dat_main['bodyString'].tolist()[20]

#sim_all_lda(single, doc_test, lda_mod, dictionary)
#sim_all_w2v(single, doc_test, w2v_mod)
#sim_all_lsi(single, doc_test, lsi_mod, dictionary)
#sim_all(single, doc_test, dictionary)
print sim_query_all(single, doc_test, dictionary,
                 lsi_mod, lda_mod, w2v_mod)

test = sim_stackoverflow(so_dat_main.iloc[21].to_dict(), so_dat_main.iloc[:20], None, dictionary, 
                  lsi_mod, lda_mod, w2v_mod)

