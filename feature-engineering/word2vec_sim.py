# create a feature vector using gensim
from gensim.models import Word2Vec, Doc2Vec # requires bleedy edge gensim
import sys
from create_dictionary import tokenize
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
sys.path.append("../utils")

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
        #print(featureVec)
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
    
def sim_two_w2v(doc1, doc2, model):
    return cosine_similarity(makeFeatureVec(tokenize(doc1), model).reshape(1, -1), 
                  makeFeatureVec(tokenize(doc2), model).reshape(1, -1))[0][0]
    
def sim_all_w2v(single, docs, model):
    """
    cosine_similarity(np.array(dataSetI).reshape(1,-1), allSet)
    
    there should be a way to "save" or hash the vectors...
    """
    return cosine_similarity(makeFeatureVec(tokenize(single), model).reshape(1, -1), 
                  [makeFeatureVec(tokenize(doc), model) for doc in docs])
    
    
    
# can update
if __name__ == "__main__":
    
    sentences = [tokenize("It is not known exactly when the text obtained its current standard form"),
                 tokenize("it may have been as late as the 1960s. Dr. Richard McClintock, a Latin scholar who was the publications director at Sydney College in Virginia"),
                 tokenize("discovered the source of the passage sometime before 1982 while searching for instances of the Latin word")] 
    sentences2 = [tokenize("The physical source of the Lorem Ipsum text may be the 1914"), 
                  tokenize("ut I must explain to you how all this mistaken idea of denouncing of a pleasure and praising pain was born and I will give you a complete account of the system")]
    model = Word2Vec(min_count=1, sg=1)
    model.build_vocab(sentences)
    model.train(sentences)
    
    model.build_vocab(sentences2, update=True)
    model.train(sentences2)
    
    print sim_two_w2v("It is not known exactly when the text obtained its current standard form",
                      "it may have been as late as the 1960s. Dr. Richard McClintock, a Latin scholar who was the publications director at Sydney College in Virginia")
    
    makeFeatureVec(sentences[0], model)
    makeFeatureVec(sentences[1], model)
    