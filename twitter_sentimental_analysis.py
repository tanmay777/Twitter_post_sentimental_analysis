import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method
        '''
        #keys and tokens from the Twitter Dev Console
        consumer_key = 'XXXXXXXXXXXXXXXXXXX'
        consumer_secret='XXXXXXXXXXXXXXXXXXX'
        access_token='XXXXXXXXXXXXXXXXXXX'
        access_token_secret='XXXXXXXXXXXXXXXXXXX'

        #attempt authentication
        try:
            #create OAuthHandler object
            self.auth = OAuthHandler(consumer_key,consumer_secret)
            #set access token and secret
            self.auth.set_access_token(access_token,access_token_secret)
            #create tweepy API object to fetch tweets
            self.api= tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self,tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        #create TextBlob object of passed tweet text
        analysis=TextBlob(self.clean_tweet(tweet))
        analysis=analysis.correct()
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self,query, count =10):
        '''
        Main function to fetch tweets and parse them.
        '''
        #empty list to store parsed tweets
        tweets=[]

        try:
            #call twitter api to fetch tweets
            fetched_tweets=self.api.search(q=query,count=count)
            #parsing the tweets one by one
            for tweet in fetched_tweets:
                #empty dictionary to store required params of a tweet
                parsed_tweet={}

                #saving text of tweet
                parsed_tweet['text']=tweet.text
                #saving sentiment of tweet
                parsed_tweet['sentiment']=self.get_tweet_sentiment(tweet.text)

                #appending parsed tweet to the tweets list
                if tweet.retweet_count>0:
                    #if tweet has retweets, ensure that it is only appended once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            #return parsed tweets
            return tweets
        except tweepy.TweepError as e:
            # print error if any
            print("Error :"+str(e))

def main():
    #creating object of TwitterClient class
    api=TwitterClient()
    query=raw_input("Enter the query: ");
    #calling function to get the tweets
    tweets = api.get_tweets(query=query, count=200)

    #picking positive tweets from the tweets
    ptweets= [tweet for tweet in tweets if tweet['sentiment']=='positive']
    #percentage of positive tweets
    print ("positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    #picking negative tweets from the tweets
    ntweets= [tweet for tweet in tweets if tweet['sentiment']=='negative']
    #picking neutral tweets from the tweets
    neutral_tweets= [tweet for tweet in tweets if tweet['sentiment']=='neutral']
    #percentage of negative tweets
    print ("negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    #percentage of neutral tweets
    print ("neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    #print first 10 Positive tweets
    print("\n\n Positive tweets:")
    for tweet in ptweets[:10]:
        print("->"+tweet['text'])

    # printing first 10 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print("->"+tweet['text'])

    print("\n\nNeutral tweets:")
    for tweet in neutral_tweets[:10]:
        print("->"+tweet['text'])
if __name__=="__main__":
    #calling main function
    main()

'''
TextBlob is actually a high level library built over top of NLTK library. First we call clean_tweet method to remove links, special characters, etc. from the tweet using some simple regex.
Then, as we pass tweet to create a TextBlob object, following processing is done over text by textblob library:

Tokenize the tweet ,i.e split words from body of text.
Remove stopwords from the tokens.(stopwords are the commonly used words which are irrelevant in text analysis like I, am, you, are, etc.)
Do POS( part of speech) tagging of the tokens and select only significant features/tokens like adjectives, adverbs, etc.
Pass the tokens to a sentiment classifier which classifies the tweet sentiment as positive, negative or neutral by assigning it a polarity between -1.0 to 1.0 .
Here is how sentiment classifier is created:

TextBlob uses a Movies Reviews dataset in which reviews have already been labelled as positive or negative.
Positive and negative features are extracted from each positive and negative review respectively.
Training data now consists of labelled positive and negative features. This data is trained on a Naive Bayes Classifier.
Then, we use sentiment.polarity method of TextBlob class to get the polarity of tweet between -1 to 1
'''
