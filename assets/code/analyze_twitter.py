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
    try:
        friends = api.friends_ids(user_id=user_id)
        try:
            last_tweet = api.user_timeline(user_id=user_id, count=1)[0]
            return friends, last_tweet.created_at
        except IndexError:  # No tweets
            return friends, False
    except tweepy.error.TweepError:  # No access to user
        return [], False


class Friend(object):
    """Holds data"""
    def __init__(self, user_id, friends, last_tweet_date):
        self.user_id = user_id
        self.friends = friends
        self.last_tweet_date = last_tweet_date

    def write_to_csv(self, file="friends.csv"):
        with open('friends.csv', 'a') as f:
            writer = csv.writer(f)
            row = [self.user_id, self.last_tweet_date,
                   len(self.friends)] + self.friends
            writer.writerow(row)

if __name__ == "__main__":
    try:
        os.remove("friends.csv")
    except FileNotFoundError:
        pass

    # Analyse myself:

    me = Friend(0, *analyse_user())
    me.write_to_csv()

    # Go through all my friends and write their information to file.
    for user_id in tqdm(me.friends):
        f = Friend(user_id, *analyse_user(user_id))
        f.write_to_csv()
