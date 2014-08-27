---
layout        : post
title         : "A Sneak Preview of Game Theory in Sage (2/3): Matching Games"
categories    : code
tags          :
- code
- game theory
- sage
comments      : true
---

In my previous post [here](http://vincent-knight.com/unpeudemath/code/2014/08/01/a-sneak-preview-of-game-theory-in-sage-1-of-3/) I described some of the [Sage](http://sagemath.org/) development that [+James Campbell](https://plus.google.com/+JamesCampbell95/posts) and I spent a lot of time this Summer working on.
In that post I described some work that has subsequently been accepted and included in the latest release of Sage (here's the latest [changlog](http://www.sagemath.org/mirror/src/changelogs/sage-6.3.txt)): code to calculate the Shapley value.

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
....:                 'C': ('b', 'c', 'a')}
sage: m = MatchingGame([suitr_pref, reviewr_pref])
{% endhighlight %}

You can see that python dictionaries are used for the functions \\(f\\) and \\(g\\) described above (the suitor preferences).

If you tab complete after typing `m.` you can see some of the methods and attributes associated with the `MatchingGame` class:

{% highlight python %}
sage: m.
m.add_reviewer  m.bi_partite    m.db            m.dumps         m.rename        m.reviewers     m.solve         m.version
m.add_suitor    m.category      m.dump          m.plot          m.reset_name    m.save          m.suitors
{% endhighlight %}

I won't go in to much of the details of that year but you can get some help on anyone of those by typing `?` after one of them (below you can see some of the output):

{% highlight python %}
sage: m.solve?

Type:            instancemethod
File:            /Users/vince/sage/local/lib/python2.7/site-packages/sage/game_theory/matching_game.py
Definition:      m.solve(self, invert=False)
Docstring:
   Computes a stable matching for the game using the Gale-Shapley
   algorithm.

...
{% endhighlight %}

Let's give that method a spin (as you can see it'll use the Gale-Shapley algorithm).

{% highlight python %}
sage: m.solve()
{'C': ['b'], 'a': ['B'], 'b': ['C'], 'A': ['c'], 'c': ['A'], 'B': ['a']}
{% endhighlight %}

We see that a matching has been obtained.
You can see the corresponding matching here:

![]({{site.baseurl}}/assets/images/stable_matching.png)

Another nice method that we implemented is to use the awesome graph theory stuff that's in Sage so you can obtain the corresponding bi-partite graph:

{% highlight python %}
sage: p = m.bi_partite()
Bipartite graph on 6 vertices
sage: p.show()
{% endhighlight %}

You can see the corresponding plot here:

![]({{site.baseurl}}/assets/images/graph_stable_matching.png)

All of the above has not been reviewed yet so if you do have any comments they'd be very gratefully received.
If you actually went over to [trac](http://trac.sagemath.org/ticket/16331) and took a look at it there that would be great but otherwise just commenting here would be awesome.

**This is the second in a series of 3 posts that I'll get around to writing, in the next one I'll cover ticket 16333: Normal Form Game. This is the biggest contribution by James as it involved interfacing with two other packages and also coding up a bespoke support enumeration algorithm.**
