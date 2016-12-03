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
from sklearn.metrics import recall_score, make_scorer, confusion_matrix, precision_score
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt

from create_dictionary import train_corpus, transform_doc2bow, tokenize
from sklearn.metrics.pairwise import cosine_similarity

from online_lsi_sim import sim_two_lsi, sim_all_lsi
from online_lda_sim import sim_two_lda, sim_all_lda
from word2vec_sim import sim_two_w2v, sim_all_w2v
from doc_sim import sim_two, sim_all

from create_model import *


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

# train for recall..

# get the dups...
train = pd.read_csv("../SESE/cleaned/2016_link_dups_time_fix.csv")

"""
test = sim_stackoverflow(so_dat_main.iloc[21].to_dict(), so_dat_main.iloc[:20], None, dictionary, 
                      lsi_mod, lda_mod, w2v_mod)

## looking only at the dups/link data...

# maybe just take the first 17 rows, because this will create a dataset with 10% dup labels, and 90% nondups


pd.DataFrame(test['doc'], )

#pd.DataFrame(test['body'], columns=
"""
"""
a =  train.iloc[21].to_dict()['bodyString']
a1 = train.iloc[22].to_dict()['bodyString']
b = train.iloc[:20]['bodyString'].tolist()

b1 = sim_two_w2v(a, a1, w2v_mod)
"""

"""
bb1 = sim_all_lsi(a, b, lsi_mod, dictionary).flatten().tolist()
bb2 = sim_all_lda(a, b, lda_mod, dictionary).flatten().tolist()
bb3 = sim_all_w2v(a, b, w2v_mod).flatten().tolist()
bb4 = sim_all(a, b, dictionary).flatten().tolist()
"""
def sim_query_all(single, docs, dictionary,
              lsi_mod, lda_mod, w2v_mod, prefix=""):
    """takes in two documents and computes similarity between
    both based on the models above, with all equal weights"""
    
    sim_vec = {'lsi': sim_all_lsi(single, docs, lsi_mod, dictionary).flatten().tolist(),
               'lda': sim_all_lda(single, docs, lda_mod, dictionary).flatten().tolist(), 
               'w2v': sim_all_w2v(single, docs, w2v_mod).flatten().tolist(), 
               'doc': sim_all(single, docs, dictionary).flatten().tolist()}
    df = pd.DataFrame(sim_vec)
    df.columns = [x+prefix for x in df.columns]
    return df

def sim_stackoverflow(single_dict, docs_df, columns, dictionary, 
                      lsi_mod, lda_mod, w2v_mod):
    """
    single_dict is a dictionary...
    
    docs_df is dataframe
    
    """
    
    #pd.concat([df1, df4], axis=1)
    if columns is None:
        columns = {'title': 'title', 
                   'body': 'bodyString', 
                   'tag': 'tagsString'}
    #print columns
    body_sim = sim_query_all(single_dict[columns['body']], docs_df[columns['body']].tolist(), 
                             dictionary, lsi_mod, lda_mod, w2v_mod, "_body")
    title_sim = sim_query_all(single_dict[columns['title']], docs_df[columns['title']].tolist(), 
                             dictionary, lsi_mod, lda_mod, w2v_mod, "_title")
    tag_sim = sim_query_all(single_dict[columns['tag']], docs_df[columns['tag']].tolist(), 
                             dictionary, lsi_mod, lda_mod, w2v_mod, "_tag")
    
    full_df = pd.concat([body_sim, title_sim, tag_sim], axis=1)
    return full_df
    
"""
test = sim_query_all(a, b, dictionary,
              lsi_mod, lda_mod, w2v_mod, "_body")

a =  train.iloc[21].to_dict()['bodyString']
a1 = train.iloc[22].to_dict()['bodyString']
b = train.iloc[:20]['bodyString'].tolist()
"""
test = sim_stackoverflow(train.iloc[21].to_dict(), train.iloc[:20], None, dictionary, 
                         lsi_mod, lda_mod, w2v_mod)

# build train set...
train_subset = train.iloc[:17]
train_labels = train_subset[['id', 'did']]
train_labels.loc[:, 'label'] = 1

m_ids = sorted(train_subset['id'].tolist(), key=lambda x: int(x))
d_ids = sorted(train_subset['did'].tolist(), key=lambda x: int(x))

ddict = {'title': 'dtitle', 
        'body': 'dbodyString', 
        'tag': 'dtagsString'}
    
train_feats = []

for m_id in m_ids:
    train_temp = train_subset[train_subset['id'].astype(int) <= int(m_id)]
    # restack dataframe...
    dtrain_temp = train_temp[['dbodyString', 'dtagsString', 'dtitle', 'did']]
    dtrain_temp.columns = [x[1:] for x in dtrain_temp.columns]
    train_temp = train_temp[['id', 'title', 'bodyString', 'tagsString']]
    train_temp = pd.concat([train_temp, dtrain_temp])
    train_temp = train_temp[train_temp['id'] != m_id]
    single_doc = train_subset[train_subset['id'] == m_ids[0]].to_dict(orient="records")[0]
    temp_feats = sim_stackoverflow(single_doc, train_temp, None, dictionary,
              lsi_mod, lda_mod, w2v_mod)
    # input column and dup col - to infer id. 
    temp_feats.loc[:, 'id'] = m_id
    temp_feats.loc[:, 'did'] = train_temp['id'].tolist() 
    train_feats.append(temp_feats)
    
feature_df = pd.merge(pd.concat(train_feats), train_labels, on=['id', 'did'], how='left').drop_duplicates()
feature_df['label'] = feature_df['label'].fillna(0)
feature_df.describe()

# now create a linear model which optimizes recall. 

clf = RandomForestClassifier(n_estimators=20)

recall_scorer = make_scorer(recall_score)
# use a full grid over all parameters
param_grid = {
    'n_estimators': [200, 700],
    'max_features': ['auto', 'sqrt', 'log2']
}

# run grid search
grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, scoring=recall_scorer)

X = feature_df[[u'doc_body', u'lda_body', u'lsi_body', u'w2v_body', u'doc_title',
       u'lda_title', u'lsi_title', u'w2v_title', u'doc_tag', u'lda_tag',
       u'lsi_tag', u'w2v_tag']].as_matrix()
       
Y = feature_df[['label']].as_matrix().flatten()

grid_search.fit(X, Y)
grid_search.predict(X)

confusion_matrix(Y, grid_search.predict(X))

# build tree to see important feats?
feat_importance = grid_search.estimator.fit(X,Y).feature_importances_

feat_df = pd.DataFrame({
    'importances': feat_importance,
    'names': [u'doc_body', u'lda_body', u'lsi_body', u'w2v_body', u'doc_title',
       u'lda_title', u'lsi_title', u'w2v_title', u'doc_tag', u'lda_tag',
       u'lsi_tag', u'w2v_tag']
                        })
feat_df = feat_df.sort(['importances'], ascending=False)
feat_df.plot.bar(x="names", y="importances")




#### increase to say 250

# build train set...
train_subset = train.iloc[:250]
train_labels = train_subset[['id', 'did']]
train_labels.loc[:, 'label'] = 1

m_ids = sorted(train_subset['id'].tolist(), key=lambda x: int(x))
d_ids = sorted(train_subset['did'].tolist(), key=lambda x: int(x))

ddict = {'title': 'dtitle', 
        'body': 'dbodyString', 
        'tag': 'dtagsString'}
    
train_feats = []

for m_id in m_ids:
    train_temp = train_subset[train_subset['id'].astype(int) <= int(m_id)]
    # restack dataframe...
    dtrain_temp = train_temp[['dbodyString', 'dtagsString', 'dtitle', 'did']]
    dtrain_temp.columns = [x[1:] for x in dtrain_temp.columns]
    train_temp = train_temp[['id', 'title', 'bodyString', 'tagsString']]
    train_temp = pd.concat([train_temp, dtrain_temp])
    train_temp = train_temp[train_temp['id'] != m_id]
    single_doc = train_subset[train_subset['id'] == m_ids[0]].to_dict(orient="records")[0]
    temp_feats = sim_stackoverflow(single_doc, train_temp, None, dictionary,
              lsi_mod, lda_mod, w2v_mod)
    # input column and dup col - to infer id. 
    temp_feats.loc[:, 'id'] = m_id
    temp_feats.loc[:, 'did'] = train_temp['id'].tolist() 
    train_feats.append(temp_feats)
    
feature_df = pd.merge(pd.concat(train_feats), train_labels, on=['id', 'did'], how='left').drop_duplicates()
feature_df['label'] = feature_df['label'].fillna(0)
feature_df.describe()

clf = RandomForestClassifier(n_estimators=20)

recall_scorer = make_scorer(recall_score)
# use a full grid over all parameters
param_grid = {
    'n_estimators': [200, 700],
    'max_features': ['auto', 'sqrt', 'log2']
}

# run grid search
grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, scoring=recall_scorer)

X = feature_df[[u'doc_body', u'lda_body', u'lsi_body', u'w2v_body', u'doc_title',
       u'lda_title', u'lsi_title', u'w2v_title', u'doc_tag', u'lda_tag',
       u'lsi_tag', u'w2v_tag']].as_matrix()
       
Y = feature_df[['label']].as_matrix().flatten()

grid_search.fit(X, Y)
#grid_search.predict(X)

print(confusion_matrix(Y, grid_search.predict(X)))
print(recall_score(Y, grid_search.predict(X)))

"""
array([[61229,     0],
       [    7,  1263]])
"""

# build tree to see important feats?
feat_importance = grid_search.estimator.fit(X,Y).feature_importances_

feat_df = pd.DataFrame({
    'importances': feat_importance,
    'names': [u'doc_body', u'lda_body', u'lsi_body', u'w2v_body', u'doc_title',
       u'lda_title', u'lsi_title', u'w2v_title', u'doc_tag', u'lda_tag',
       u'lsi_tag', u'w2v_tag']
                        })
feat_df = feat_df.sort(['importances'], ascending=False)
feat_df.plot.bar(x="names", y="importances")


