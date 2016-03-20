"""
Need to use https://pypi.python.org/pypi/ratelim/0.1.5
"""
import tweepy
from tqdm import tqdm

from twittersecrets import *

# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token, token_secret)
api = tweepy.API(auth)

# Get all my followers
followers = api.followers_ids()

with open('followers.csv', 'w') as f:
    for follower in followers:
        f.write(str(follower))
        f.write("\n")
