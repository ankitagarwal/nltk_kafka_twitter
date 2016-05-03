import pickle
from kafka import KafkaConsumer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import time
from nltk.tokenize import TweetTokenizer
import json
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

# Create a consumer.
consumer = KafkaConsumer('spark_topic', bootstrap_servers='localhost:9092');

# Load our classifier
f = open('/mnt/hgfs/shared/final.pickle', 'rb')
classifier = pickle.load(f)
f.close()

# Stop words.
stop = stopwords.words('english')

# Remove stop words and convert to lower case.
def clean_msg(post):
    tknzr = TweetTokenizer()
    tokens = tknzr.tokenize(post["text"])
    return dict([(word.lower(), True) for word in tokens if word not in stop])

# ax = plt.axes(projection=ccrs.Robinson())
# ax.coastlines(resolution='110m')
# ax.gridlines()
# ax.stock_img()
# plt.title("Live Tweeter sentiment around the world")

# Loop until killed and classify each tweet
count = 0
for msg in consumer:
    msg = json.loads(msg.value)
    coordinates = msg["coordinates"]
    tweet = clean_msg(msg)
    label = classifier.classify(tweet)
    count += 1
    print ("time - " + str(time.strftime("%H:%M:%S")) + " " + "count - " + str(count))
    print("label : " + label)
    print("tweet : " + " " . join(tweet))
    # # Plot the point.
    # if (coordinates):
    #     lon = coordinates[0]
    #     lat = coordinates[1]
    #     x,y = map(lon, lat)
    #     msize = 2
    #     if (label == "pos"):
    #         col = "blue"
    #     else:
    #         col = "red"
    #     plt.plot([lon], [lat],
    #      color=col, linewidth=2, marker='o',
    #      transform=ccrs.Geodetic(),
    #      )
    #     plt.plot();
