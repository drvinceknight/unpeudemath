import tweepy
import csv
from tqdm import tqdm
from twittersecrets import *
import os
# Authenticating
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token, token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=False)


def analyse_user(user_id=None):
    """Return the list of followers and last tweet date and text"""
    followers = api.followers_ids(user_id=user_id)
    try:
        last_tweet = api.user_timeline(user_id=user_id, count=1)[0]
    except IndexError:
        last_tweet.text = False
        last_tweet.created_at = False
    return followers, last_tweet.text, last_tweet.created_at

class Follower(object):
    """Holds data"""
    def __init__(self, user_id, followers, last_tweet_text, last_tweet_date):
        self.user_id = user_id
        self.followers = followers
        self.last_tweet_text = last_tweet_text
        self.last_tweet_date = last_tweet_date

    def write_to_csv(self, file="followers.csv"):
        with open('followers.csv', 'a') as f:
            writer = csv.writer(f)
            row = [self.user_id, self.last_tweet_date, self.last_tweet_text,
                   len(self.followers), *self.followers]
            writer.writerow(row)

if __name__ == "__main__":
    try:
        os.remove("followers.csv")
    except FileNotFoundError:
        pass

    # Analyse myself:

    me = Follower(0, *analyse_user())
    me.write_to_csv()

    # Go through all my followers and write their information to file.
    for user_id in tqdm(me.followers):
        f = Follower(user_id, *analyse_user(user_id))
        f.write_to_csv()
