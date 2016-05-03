from kafka import KafkaProducer
import twitter
import requests
import requests_oauthlib
import json
import time
import sys

if len(sys.argv) != 2:
    print("Error, please specify movie name or tag")
    exit()

#  Movie hash tag.
hash = sys.argv[1]

# Create a producer
producer = KafkaProducer(bootstrap_servers='localhost:9092');

# Send msgs until the client is killed.
while(True):
    auth = requests_oauthlib.OAuth1(twitter.CONSUMER_KEY, twitter.CONSUMER_SECRET
                                    ,twitter.ACCESS_TOKEN, twitter.ACCESS_TOKEN_SECRET)
    data = [('language', 'en'), ['track', hash]]
    query_url = twitter.URL + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in data])
    response = requests.get(query_url, auth = auth, stream = True)
    print(query_url, response)
    count = 0
    # Iterate over results.
    for line in response.iter_lines():
        try:
            post= json.loads(line.decode('utf-8'))
            producer.send('spark_topic', str(line));
            count += 1
            print ("time - " + str(time.strftime("%H:%M:%S")) + " " + "count -" + str(count))
        except:
            e = sys.exc_info()[0]
            print( "Error: %s" % e )

    time.sleep(2)


