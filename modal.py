import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
import random
import math
import pickle


# Transform into a binary encoded feature list.
def transform_feature(words):
    # Ignore stop words.
    return dict([(word.lower(), True) for word in words if word not in stop])

# Positive and negative words
negfileids =  movie_reviews.fileids('neg')
posfileids = movie_reviews.fileids('pos')

# Stop words.
stop = stopwords.words('english')

negfeatures = [(transform_feature(movie_reviews.words(fileids=[f])), 'neg') for f in negfileids]
posfeatures = [(transform_feature(movie_reviews.words(fileids=[f])), 'pos') for f in posfileids]

data = negfeatures + posfeatures
ratio = int(math.ceil(0.67 * len(data)))
# Split data after shuffle.
random.shuffle(data)
train = data[:ratio]
test = data[ratio:]

print 'Train dataset -  %d instances, test dataset - %d instances' % (len(train), len(test))

classifier = NaiveBayesClassifier.train(train)
print 'accuracy:', nltk.classify.util.accuracy(classifier, test)
classifier.show_most_informative_features()

# Save classifier.
f = open('/home/ankit/Desktop/vm_shared/final.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

