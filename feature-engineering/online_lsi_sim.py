import gensim
import pandas as pd
import gc

from create_dictionary import train_corpus, transform_doc2bow

def sim_two_lsi(doc1, doc2, lsi, dictionary):
    corpus = train_corpus([doc1, doc2], dictionary)
    d2b1 = transform_doc2bow(doc1, dictionary)
    index = gensim.similarities.docsim.MatrixSimilarity(lsi[corpus])
    return index[lsi[d2b1]][1]

if __name__ == "__main__":
    
    dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
    
    fname = "../SESE/cleaned/sql-html-sample.csv"
    lsi = gensim.models.lsimodel.LsiModel(train_corpus(['html'], dictionary), id2word=dictionary, num_topics=100)
    
    so_dat = pd.read_csv(fname)
    so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]
    corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)
    lsi.add_documents(corpus, chunksize=1000, decay=0.99999)
    
    lsi.save("../data/lsi-sample.gz")
                            
    test = sim_two_lsi("html angular", "html javascript")