---
layout        : post
title         : "A Sneak Preview of Game Theory in Sage (2/3): Matching Games"
categories    : code
tags          :
- code
- game theory
- sage
comments      : false
---

In my previous post [here](http://vincent-knight.com/unpeudemath/code/2014/08/01/a-sneak-preview-of-game-theory-in-sage-1-of-3/) I described some of the [Sage](http://sagemath.org/) development that [+James Campbell](https://plus.google.com/+JamesCampbell95/posts) and I spent a lot of time this Summer working on.
In that post I described some work that has subsequently been accepted and including in the latest release of Sage (here's the latest [changlog](http://www.sagemath.org/mirror/src/changelogs/sage-6.3.txt): code to calculate the Shapley value.

In this post I'll talk about the second of 3 tickets that James and I worked on: looking at Matching games.
**This has not actually been reviewed yet so please do help us get this code in to Sage by taking a look at the ticket: [16331](http://trac.sagemath.org/ticket/16331).**

**What is a matching game?**

One of the best explanations of a matching game (also called the stable marriage problem) can be found in [this video](https://www.youtube.com/watch?v=w1leqkpDaRw).
That video really is awesome but it might be a bit long (it's 25 minutes) so this very [short video](http://youtu.be/ZMK3qW4ZHqI) I threw together for a class I teach might be of interest (it is no where near as good as the previous one but it's 3 minutes long).

Basically a matching game attempts to create links between two groups of people (referred to as suitors and reviewers) in such a way as no one wants to break their link:

![]({{site.baseurl}}/assets/images/base_matching_game.png)

In the above picture we see the _preferences_ of the suitors and the reviewers.
So \\(a\\), prefers \\(B\\) to \\(A\\), and \\(A\\) to \\(C\\).

Here is the actual definition of a stable matching that I give my students:

A matching game of size \\(N\\) is defined by two disjoint sets \\(S\\) and \\(R\\) or suitors and reviewers of size \\(N\\).
Associated to each element of \\(S\\) and \\(R\\) is a preference list:

$$f:S\to R^N\text{ and }g:R\to S^N$$

A matching \\(M\\) is a any bijection between \\(S\\) and \\(R\\). If \\(s\in S\\) and \\(r\in R\\) are matched by \\(M\\) we denote:

$$M(s)=r$$

The above image defines a matching game, one possible matching could be given below:

![]({{site.baseurl}}/assets/images/unstable_matching.png)

**It's immediate to note however that \\(B\\) and \\(c\\) prefer each other to their current matching: so the above matching is unstable.**
In that example \\((B,c)\\) is called a 'blocking pair'.

Luckily Gale and Shapley obtained an algorithm that guarantees a stable matching and this is what James and I put together in to Sage.

First, let's define a matching game:

{% highlight python %}
sage: suitr_pref = {'a': ('B', 'A', 'C'),
....:               'b': ('B', 'C', 'A'),
....:               'c': ('A', 'B', 'C')}
sage: reviewr_pref = {'A': ('a', 'b', 'c'),
....:                 'B': ('a', 'c', 'b'),
....:                 'C': ('b', 'c', 'a'),
sage: m = MatchingGame([suitr_pref, reviewr_pref])
{% endhighlight %}

You can

We then create an instance of the `CooperativeGame` class (which is what James and I put together):

{% highlight python %}
sage: taxi_game = CooperativeGame(v)
{% endhighlight %}

If you tab complete after typing `taxi_game.` you can see some of the methods and attributes associated with the `CooperativeGame` class:

{% highlight python %}
sage: taxi_game.
taxi_game.category          taxi_game.dump              taxi_game.is_monotone       taxi_game.nullplayer        taxi_game.rename            taxi_game.shapley_value
taxi_game.ch_f              taxi_game.dumps             taxi_game.is_superadditive  taxi_game.number_players    taxi_game.reset_name        taxi_game.version
taxi_game.db                taxi_game.is_efficient      taxi_game.is_symmetric      taxi_game.player_list       taxi_game.save
{% endhighlight %}

I won't go in to much of the details of that year but you can get some help on anyone of those by typing `?` after one of them (below you can see some of the output):

{% highlight python %}
sage: taxi_game.is_symmetric?
Type:       instancemethod
String Form:<bound method CooperativeGame.is_symmetric of A 3 player co-operative game>
File:       /Users/vince/sage/local/lib/python2.7/site-packages/sage/game_theory/cooperative_game.py
Definition: taxi_game.is_symmetric(self, payoff_vector)
Docstring:
   Return "True" if "payoff_vector" possesses the symmetry property.

   A payoff vector possesses the symmetry property if v(C cup i) =
   v(C cup j) for all C in 2^{Omega} setminus {i,j}, then x_i =
   x_j.

   INPUT:

   * "payoff_vector" -- a dictionary where the key is the player and
     the value is their payoff
...
{% endhighlight %}


**But what we really want to know is how much should Alice, Bob and Celine pay the taxi?**

To calculate this we simply get Sage to tell us the Shapley value:

{% highlight python %}
sage: taxi_game.shapley_value()
{'A': 5/3, 'B': 55/6, 'C': 169/6}
{% endhighlight %}

This shows that in this particular case Alice should pay £1.67, Bob £9.17 and Celine £28.17 (rounding has obviously caused us to gain a penny along the way but you get the idea) :)

**This is the first in a series of 3 posts that I'll get around to writing, in the next one I'll cover ticket 16331 which takes care of matching games :)**

To go back to the process of contributing to an open source project, I really think this is something everyone with any interests in code should have a go at doing as it has a large number of benefits.
None more so than improving the standard of code that one writes.
When you're writing because you hope that someone will look at **and review** your code you make sure it's well written (or at least try to!).
