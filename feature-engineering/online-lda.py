"""
import gensim

documents = ["Apple is releasing a new product",
             "Amazon sells many things",
             "Microsoft announces Nokia acquisition"]

stoplist = ['is', 'and']

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
dictionary = gensim.corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, update_every=1, chunksize=10000, passes=1)

lda.print_topics(5)
# update incoming files
# lda.update(new_corpus)


#print feature vector:
lda[corpus[0]]
"""

import gensim
import pandas as pd

from create_dictionary import train_corpus

# create dictionary, as gensim doesn't have an implementation for infinitely large
# dictionaries at this stage.
# this is a static dictionary - check "create_dictionary.py"
dictionary = gensim.corpora.Dictionary.load("../data/SESE.gz")
lda = gensim.models.ldamodel.LdaModel(id2word=dictionary, num_topics=10)

for fname in [
"../SESE/cleaned/sql-html-js-2",
"../SESE/cleaned/sql-html-js-1",
"../SESE/cleaned/sql-html-js-3",
"../SESE/cleaned/sql-html-js-4",
"../SESE/cleaned/sql-html-js-5"
]:

    for i, so_dat in enumerate(pd.read_csv(fname+"_fix.csv", chunksize=9000)):
        if i == 0:
            print(fname)
        print(i)
        so_dat_main = so_dat[['id', 'title', 'bodyString', 'tagsString']]

        corpus = train_corpus(so_dat_main['bodyString'].tolist(), dictionary)
        lda.update(corpus)

"""
>>> pprint.pprint(lda.print_topics(5))
[(1,
  '0.047*java + 0.005*viewer + 0.005*bla + 0.005*xscale + 0.004*javax + '
  '0.003*yscale + 0.003*lx + 0.003*printer + 0.003*extent + 0.002*nil'),
 (2,
  '0.067*var + 0.044*function + 0.024*document + 0.019*map + 0.014*data + '
  '0.014*new + 0.013*return + 0.012*getelementbyid + 0.012*attr + 0.010*event'),
 (4,
  '0.004*dropzonefil + 0.004*acc + 0.003*cbp + 0.003*popupwin + 0.003*xmh + '
  '0.003*ddata + 0.003*pizza + 0.002*styler + 0.002*guidanc + '
  '0.002*featuretyp'),
 (9,
  '0.008*song + 0.006*pellentesqu + 0.003*budgetpric + 0.003*mz + '
  '0.002*secondsect + 0.002*mej + 0.002*hendrerit + 0.002*casper + '
  '0.002*hp_unit_detail + 0.002*met'),
 (0,
  '0.044*px + 0.025*div + 0.021*width + 0.018*style + 0.017*imag + 0.016*text '
  '+ 0.016*color + 0.015*height + 0.013*background + 0.013*css')]
>>> pprint.pprint(lda.print_topics(2))
[(7,
  '0.025*function + 0.013*var + 0.011*file + 0.011*data + 0.010*return + '
  '0.009*log + 0.009*code + 0.009*js + 0.009*consol + 0.009*error'),
 (3,
  '0.035*td + 0.034*valu + 0.028*input + 0.028*id + 0.027*type + 0.023*form + '
  '0.022*option + 0.017*select + 0.016*php + 0.016*text')]
"""

lda.save("../data/lda.gz")
