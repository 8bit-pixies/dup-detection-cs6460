"""
Train and learn weights for duplicate questions

This will be based on the the paper - we would have to be come up with an 
online learning version?

Essentially the formulation goes something like this:


1.   

[d for d in DUP_QUESTIONS]
and all questions posted before d...compute all similarity scores!

2.  

Fit model with those parameters (by guessing or otherwise)

3. Go to one till you're happy

Metric to optimize...

    recall = number detected / number total

Don't care too much about being "over zealous"

--------


Negative sampling? - how we're training is one variant of negative sampling.

"""

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


dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
fname = "../SESE/cleaned/sql-html-sample.csv"

so_dat = pd.read_csv(fname)
so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

label_dat = pd.read_csv("../SESE/labels/sql-html-js-2_labels.csv")


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

# do left join with labels.....
dat_combine = pd.merge(so_dat_main, label_dat)

# basically perform negative sampling to find weights to optimize these two cases....


# do stuff and output training dataset....(figure out how...)
# will be adhoc for future...







