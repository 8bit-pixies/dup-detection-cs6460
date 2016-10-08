# create a feature vector using gensim
#from gensim.models import Word2Vec, Doc2Vec
import sys
sys.path.append("../utils")

from onlinew2v import Word2Vec as w2v # http://rutumulkar.com/blog/2015/word2vec
# can update
import numpy as np

sentences = [[u'with', u'all', u'this', u'stuff', u'going', u'down', u'at', u'the', u'moment', u'with', u'mj', u'i', u've', u'started', u'listening', u'to', u'his', u'music', u'watching', u'the', u'odd', u'documentary', u'here', u'and', u'there', u'watched', u'the', u'wiz', u'and', u'watched', u'moonwalker', u'again'],
             [u'maybe', u'i', u'just', u'want', u'to', u'get', u'a', u'certain', u'insight', u'into', u'this', u'guy', u'who', u'i', u'thought', u'was', u'really', u'cool', u'in', u'the', u'eighties', u'just', u'to', u'maybe', u'make', u'up', u'my', u'mind', u'whether', u'he', u'is', u'guilty', u'or', u'innocent']]
sentences2 = [['first', 'sentence'], ['second', 'sentence']]
model = w2v(min_count=1)
model.build_vocab(sentences)
model.train(sentences)

model.build_vocab(sentences2, update=True)
model.train(sentences2)

# build feature vector...
# based on code here: https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-3-more-fun-with-word-vectors
def makeFeatureVec(words, model):
    # Function to average all of the word vectors in a given
    # paragraph
    #
    # Pre-initialize an empty numpy array (for speed)
    
    #featureVec = np.zeros((num_features,),dtype="float32")
    # guess size of feature vec...    
    featureVec = np.zeros(model[model.index2word[0]].shape, dtype="float32")
    
    #
    nwords = 0.
    # 
    # Index2word is a list that contains the names of the words in 
    # the model's vocabulary. Convert it to a set, for speed 
    index2word_set = set(model.index2word)
    #
    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set and not np.any(np.isnan(model[word])): 
            nwords = nwords + 1.
            featureVec = np.add(featureVec, model[word])
    # 
    # Divide the result by the number of words to get the average
    if nwords != 0:
        print(featureVec)
        featureVec = np.divide(featureVec,nwords)
    return featureVec
    
def getAvgFeatureVecs(reviews, model):
    # Given a set of reviews (each one a list of words), calculate 
    # the average feature vector for each one and return a 2D numpy array 
    # 
    # Initialize a counter
    counter = 0.
    num_features = model[model.index2word[0]].shape[0]
    # 
    # Preallocate a 2D numpy array, for speed
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    # 
    # Loop through the reviews
    for review in reviews:
       #
       # Print a status message every 1000th review
       if counter%1000. == 0.:
           print("Review %d of %d" % (counter, len(reviews)))
       # 
       # Call the function (defined above) that makes average feature vectors
       reviewFeatureVecs[counter] = makeFeatureVec(review, model)
       #
       # Increment the counter
       counter = counter + 1.
    return reviewFeatureVecs

makeFeatureVec(["with", "all"], model)
makeFeatureVec(['second', 'sentence'], model)

getAvgFeatureVecs(sentences2, model)

