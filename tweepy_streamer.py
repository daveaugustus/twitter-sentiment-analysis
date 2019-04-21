import os
import sys
import yaml
import numpy as np
import pandas as pd
from tweepy import API
from tweepy import Cursor
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

with open('/home/dave/route.yaml', 'r') as route_file:
    route = yaml.load(route_file, Loader=yaml.FullLoader)

with open(route['route_twitter'], 'r') as yaml_file:
    file = yaml.load(yaml_file, Loader=yaml.FullLoader)



consumer_key = file['consumer_key']
consumer_secret = file['consumer_secret']
access_token_key = file['access_token']
access_secret_key = file['access_secret']


# Twitter client class
class TwitterClient():

    def __init__(self, twitter_user = None):
        self.auth = TwitterAuthenticor().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# Twitter Authenticater
class TwitterAuthenticor():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_secret_key)
        return auth


# Twitter Streamer
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticor()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# Twitter stream listner
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occours
            return False
            print(status)


class TweetAnalyzer():
    """ Functionality for analyzing and categorizing content from tweets"""
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data = [tweet.text for tweet in tweets], columns = ['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['Length'] = np.array([len(tweet.text) for tweet in tweets])
        df['Date'] = np.array([tweet.created_at for tweet in tweets])
        df['Source'] = np.array([tweet.source for tweet in tweets])
        df['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['Retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name = 'davetweetlive', count=20)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df)
    # print(tweets[1].text, tweets[1].retweet_count)
