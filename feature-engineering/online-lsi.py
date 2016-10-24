"""
import gensim

documents = ["Apple is releasing a new product",
             "Amazon sells many things",
             "Microsoft announces Nokia acquisition"]

stoplist = ['is', 'and']

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]


lsi = gensim.models.lsimodel.LsiModel(corpus=corpus, id2word=dictionary, num_topics=400)

documents2 = ["Google creates hardware division",
             "Yahoo is nowhere to be seen"]

texts2 = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
corpus2 = [dictionary.doc2bow(text) for text in texts2]

lsi.add_documents(corpus2)

lsi.print_topics(10)

# print stuff...

lsi[[(0, 1), (1, 1)]]

lsi[corpus2[1]]
# lsi adjusts weights but doesn't change in size! might not be suitable for our project


# https://github.com/RaRe-Technologies/gensim/issues/74
# https://groups.google.com/forum/#!topic/gensim/HvkeM2wAgMY
"""

import gensim
import pandas as pd
import gc

from create_dictionary import train_corpus, transform_doc2bow

dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
lsi = gensim.models.lsimodel.LsiModel(id2word=dictionary, num_topics=200)


for fname in [
"../SESE/cleaned/sql-html-js-2",
#"../SESE/cleaned/sql-html-js-1",
#"../SESE/cleaned/sql-html-js-3",
#"../SESE/cleaned/sql-html-js-4",
#"../SESE/cleaned/sql-html-js-5"
]:

    for i, so_dat in enumerate(pd.read_csv(fname+"_fix.csv", chunksize=5000)):
        if i == 0:
            print(fname)
        print(i)
        so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

        corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)
        lsi.add_documents(corpus, chunksize=1000, decay=0.99999)
        del so_dat_main
        del corpus
        gc.collect()

lsi.save("../data/lsi.gz")
# to get output...
"""
sample_doc = so_dat_main['bodyString'].tolist()[0]
lsi[transform_doc2bow(sample_doc, dictionary)]

# to check similarity
index = similarities.MatrixSimilarity(lda[corpus])
sims = index[lda[vec_bow]] # where vec_bow is created from saved dictionary model...`vec_bow = dictionary.doc2bow(...)`

# http://radimrehurek.com/topic_modeling_tutorial/3%20-%20Indexing%20and%20Retrieval.html
"""






