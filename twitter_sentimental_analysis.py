import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sengtimental analysis
    '''
    def __init__(self):
        '''
        Class constructor or initialization method
        '''
        #keys and tokens from the Twitter Dev Console
        consumer_key = 'lFpfWXoKTdvM3MrueamqfY1aL'
        consumer_secret='dXZ5n0grM8yub8HpG3jv0b0PVujzxaRjFe1SQ2yPmejeGAD5Tk'
        access_token='113358888-IqaVvXwr9fAIZrNBI02aGWR8J5psj27H1aLRcRGC'
        access_token_secret='5hRT3VKnfsArFk8zB0eCDBXFM0mv0B08QkVsMOobKZTeK'

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
        Utility function to classify sentiments of passed tweet
        using textblob's sentiment method
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        #create textblob object of passed tweet text
        analysis=TextBlob(self.clean_tweet(tweet))
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
    #calling function to get the tweets
    tweets = api.get_tweets(query='Donald Trump', count=200)

    #picking positive tweets from the tweets
    ptweets= [tweet for tweet in tweets if tweet['sentiment']=='positive']
    #percentage of positive tweets
    print ("positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    #picking negative tweets from the tweets
    ntweets= [tweet for tweet in tweets if tweet['sentiment']=='negative']
    #percentage of negative tweets
    print ("negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    #percentage of neutral tweets
    print ("neutral tweets percentage: {} %".format(100*(len(tweets)-len(ntweets)-len(ptweets))/len(tweets)))

    #print first 5 Positive tweets
    print("\n\n Positive tweets:")
    for tweets in ptweets[:10]:
        print(tweet['text'])

    #printing first 5 Negative tweets
    print("\n\n Negative Tweets:")
    for tweets in ntweets[:10]:
        print(tweet['text'])

if __name__=="__main__":
    #calling main function
    main()
