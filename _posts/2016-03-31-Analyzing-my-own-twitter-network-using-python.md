---
layout     : post
title      : "Page ranking my twitter network using Python"
categories : code
tags       :
- python
- twitter
comments   : true
---

I follow too many people on twitter. It makes my stream a bit of a mismatch of
things and I often end up missing tweets from accounts I'm really interested in.
I'm not too sure how to solve this problem but I **am sure** that it must start
with my understanding my network. In this post I'll show a simple python script
that grabs my twitter network (disclaimer it takes time) and then some simple
graph theoretic analysis of my network.

## Getting the network

To get my network I use [`tweepy`](http://tweepy.readthedocs.org/), a Python
library that taps in to twitter's API. There are two things to remember:

1. You need to get an app authentication ([this is very simple to
   do](https://dev.twitter.com/oauth/application-only)).
2. You need time. Twitter limits the amount of requests you can put to its API.
   Thankfully `tweepy` can automatically limit how often you ask a request so as
   long as you have a machine that can be left running this isn't
   unsurmountable.

Once you've done 1, I suggest putting the authentication details in a
`twittersecrets.py` file. Something like:

```python
consumer_key = "XXXX"
consumer_secret = "XXXX"
token = "XXXX"
token_secret = "XXXX"
```

**Don't share those.** If you use version control, make sure you don't commit
those files.

Once you've done that here is a script that will go through the people you
follow and will write to file (in case something crashes):

- The id number of the user;
- The date of their last tweet;
- The id number of the people they follow.

**Note that in my script I didn't grab the screen name to file, you should do that, I show you how later. It's 1 extra line, I don't know why I didn't do that.**

```python
import tweepy
import csv
from tqdm import tqdm  # An awesome progress bar
from twittersecrets import *  # This grabs the authentication secrets
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
        # This is just to get rid of the file so I didn't add users twice as I
        # was debugging all this.
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
```

That can take quite a while, it took just under twenty hours for me.

This creates quite a mess of a csv file but it's not unbearable to deal with
(there were perhaps other ways of doing this).

## Reading in the data

First all here are the libraries I used:

```python
import datetime  # Deal with dates
import networkx as nx  # Network
import matplotlib.pyplot as plt  # Graph stuff
import seaborn  # Graph stuff pretty

import tweepy # To analyse further
from twittersecrets import *  # For authenticating

%matplotlib inline  # I did this in a notebook so ths magic makes the graphs appear
```

Here's a class to hold the data:

```python
class Friend(object):
    def __init__(self, user_id, last_tweet_date, friend_ids):
        self.user_id = user_id
        try:
            self.last_tweet_date = datetime.datetime.strptime(last_tweet_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            self.last_tweet_date = False
        self.friend_ids = friend_ids

    def friend_ids_in_network(self, list_of_ids):
        return [n for n in self.friend_ids if n in list_of_ids]

    def __str__(self):
        return self.user_id

    def __repr__(self):
        return str(self)
```

and here is me reading in the data:

```python
import csv
with open("friends.csv", "r") as f:
    # Removing myself from the network
    network_nodes = [Friend(row[0], row[1], row[2:]) for row in csv.reader(f)][1:]
network_ids = [n.user_id for n in network_nodes]  # Ids for all the network
```

A quick look at the distribution of "friends" (this is what people you follow
are referred to as):

```python
plt.hist([len(f.friend_ids) for f in network_nodes], bins=40)
plt.title("Friend numbers of people I follow");
```

![]({{site.baseurl}}/assets/images/friend_numbers_of_my_friends.svg)

You can see the peak at 5000 (I think that's the upper limit of what twitter allows).

Some of those are outside of the network of people I follow, so let me "cut of
the outside" of my own network:

```python
for friend in network_nodes:
    friend.friend_ids_in_network = friend.friend_ids_in_network(network_ids)
plt.hist([len(f.friend_ids_in_network) for f in network_nodes], bins=40)
plt.title("Friend numbers of people I follow in network of people I follow");
```

![]({{site.baseurl}}/assets/images/friend_numbers_of_my_friends_in_network.svg)

I have probably followed people who don't really use twitter anymore. Let me
remove them from my network:

```python
>>> # Consider a 1 year limit
>>> limit = datetime.datetime.now() - datetime.timedelta(days=365)

>>> active_network_nodes = []
>>> for f in network_nodes:
...     if f.last_tweet_date and f.last_tweet_date >= limit:
...         active_network_nodes.append(f)
```

This is how many people haven't tweeted for a year (for me: 95).

```python
>>> inactive_users = [n for n in network_nodes if n not in active_network_nodes]
>>> len(inactive_users)
95
```

Once I've done that, I can go through and find out the user names of them (and
even use the api to unfollow them if I cared to):

```python
>>> auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
>>> auth.set_access_token(token, token_secret)

>>> api = tweepy.API(auth, wait_on_rate_limit=True,
...                  wait_on_rate_limit_notify=False)

>>> users = api.lookup_users(user_ids=inactive_users)
>>> for u in users:
...     print(u.screen_name)
```

**I probably should have collected the screen name in my data collection
script. Not sure why I didn't do that...**

Let me look at the active user friend numbers:

```python
>>> plt.hist([len(f.friend_ids_in_network) for f in active_network_nodes], bins=40)
>>> plt.title("Friend numbers of active people I follow in network of people I follow");
```

![]({{site.baseurl}}/assets/images/friend_numbers_of_my_active_friends_in_network.svg)

These two graphs look quite similar for me (I'm removing a very biased part of
my network).

## Let's build the network

To do this I'm going to use [`networkx`](https://networkx.github.io/), a great
library for manipulating and building networks in Python.

First let me build a dictionary mapping nodes to nodes:

```python
>>> network_map = {f.user_id:f.friend_ids_in_network for f in active_network_nodes}
```

Before I go any further, let me draw my network. I won't actually draw the whole network: it's big and messy but I'll draw a sample of it:

```python
>>> import random
>>> random.seed(0)  # So that this is reproducible
>>> number_of_nodes = 400
>>> sampled_nodes = random.sample(network_map.keys(), number_of_nodes)
>>> sampled_sub_network_map = {key: [node for node in network_map[key] if node in sampled_nodes]
...                        for key in sampled_nodes}
>>> G = nx.Graph(sampled_sub_network_map)
```

Writing the network to a dot file:

```python
>>> from networkx.drawing.nx_agraph import write_dot
>>> write_dot(G, 'net.dot')
```

Using graphviz and imagemagick to turn this in to a png:

```bash
neato -Tps -Goverlap=scale net.dot -o net.ps; convert net.ps net.png
```

This gives, it's a big file...: [net.png]({{site.baseurl}}/assets/images/net.png).

If you look closely at that image you'll see that it's not a completely
connected network, this extend to the entire graph:

```python
>>> G = nx.Graph(network_map)  # Graph for the whole network
>>> components = list(nx.connected_components(G))
>>> len(components)
8
```

I have 8 components in my graph.
Most of these have just 1 user in them:

```python
>>> [len(c) for c in components]
[1124, 1, 1, 1, 1, 1, 1, 1]
```

It's then easy enough to look at the components that have just 1 user and
decide what I want to do with them.

**Now for the interesting stuff: let me create a network from the active users
in the connected component:**

```python
>>> G = nx.Graph({key:value for key, value in network_map.items() if key in components[0]})
```

Now that I've done that I can start looking at all sorts of thing, including
the [center](https://en.wikipedia.org/wiki/Graph_center) of the network:

```python
>>> nx.center(G)
['11348282']
```

This center is apparently a single node, and represents the node that has
lowest greatest distance to all other nodes. We can use the twitter API to find
out who this account is:

```python
>>> api.lookup_users(center)[0].screen_name
'NASA'
```

Given my interests that's actually quite neat and not so unsuspected.
One in particular is apply a page rank calculation:

```python
>>> pr = nx.pagerank(G)
>>> sorted_nodes = sorted([(node, pagerank) for node, pagerank in pr.items()], key=lambda x:pr[x[0]])
```

This will then identify the 10 nodes with the highest page rank:

```python
>>> users = api.lookup_users(user_ids=[pair[0] for pair in sorted_nodes[:10]])
>>> for u in users:
...    print(u.screen_name)
```

I am not sure if a high page rank is actually a good or a bad thing when it
comes to my twitter network. I need to think about this a bit more, but one
thing that is easy to do is build what is called a [maximal independent
set](https://en.wikipedia.org/wiki/Independent_set_(graph_theory)).

```python
>>> mis = nx.maximal_independent_set(G)  # This is in fact an approximative algorithm
>>> len(mis)
300
```

So this seems to indicate that there is a set of just 300 accounts that would
perhaps be sufficient to follow. This would assume that tweets flow through the
network which is of course not quite true.

**I'm not going to rush to unfollow anyone but having this data and all the
networkx algorithms at my finger tips is awesome.**
