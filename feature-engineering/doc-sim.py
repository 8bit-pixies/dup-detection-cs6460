# not learnt online - but that is okay
# as the whole corpus will only ever be two documents.

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

docs = ["Julie loves me more than Linda loves me",
"Jane likes me more than Julie loves me"]

count_vec = CountVectorizer().fit(docs)
count_vec.transform(docs).todense()

cosine_similarity(count_vec.transform(docs)[0],
                  count_vec.transform(docs)[1])
