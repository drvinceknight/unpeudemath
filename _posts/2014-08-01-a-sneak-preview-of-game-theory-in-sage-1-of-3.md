---
layout: post
title:  "A Sneak Preview of Game Theory in Sage (1/3): Cooperative Game Theory"
categories: code
tags:
- code
- game theory
- sage
comments : true
---

[+James Campbell](https://plus.google.com/+JamesCampbell95/posts) and I spent a lot of time this Summer working on implementing some Game Theory in to [Sage](http://sagemath.org/).

In this post I'll (very briefly) describe some of the process involved in contributing to Sage and give a sneak peek at some of the Game Theory code that will (hopefully) be in [Sage](http://sagemath.org/) soon.

This has been a really great experience as it was my first time **really** contributing to an open source project.

It involved a lot of coding, documentation writing and also being very thankful for all the help we got from the Sage community (a **huge** thanks to [Karl](http://www.math-cs.gordon.edu/~kcrisman/)).

It all starts with opening 'tickets' on the [trac server](http://trac.sagemath.org/).
We opened 3 tickets:

- [16331](http://trac.sagemath.org/ticket/16331): *Build capacity to solve matching games in to Sage.*
- [16332](http://trac.sagemath.org/ticket/16332): *Build capacity to calculate Shapley value of cooperative games.*
- [16333](http://trac.sagemath.org/ticket/16333): *Build class for normal form games as well as ability to obtain Nash equilibria*

After doing that James and I quickly realised that we needed to have our own common repository for Game Theory development so that's up on github [here](https://github.com/theref/sage-game-theory).

**In this post I'll talk briefly about some of the stuff that you will be able to do thanks to ticket 16332.**
This particular ticket has in fact been reviewed and given the all clear so should hopefully make its way in to a future release of Sage! (Which is very exciting indeed!).

If you would like to follow along with some of the stuff written here you'll need to grab the 16332 branch from the github repository: [https://github.com/theref/sage-game-theory/tree/16332](https://github.com/theref/sage-game-theory/tree/16332) or go directly to the trac server and grab the 16332 ticket.

**What is a cooperative game?**

Here is the definition that I give my students:

A characteristic function game G is given by a pair \\(N,v\\) where \\(N\\) is the number of players and \\(v:2[N]\to\mathbb{R}\\) is a characteristic function which maps every coalition of players to a payoff.

Here is something else that I describe to my students:

> Let's assume that Alice, Bob and Celine all share a taxi. They all live in a straight line (with regards to the trajectory of the taxi) and the costs associated with their trip is Alice: £5, Bob: £20, Celine: £39.

> What is the fairest way of sharing out the total taxi fair (which would be £39)?

From Alice's point of view she needs to pay less than £5 (or their would be no point in her sharing the taxi).
Similarly for Bob and Celine, however we also want the amount paid by Alice **and** Bob to be less than if **they** had shared a taxi etc...

To solve our problem we can use cooperative game theory and in particular use a characteristic function game:

\\[
v(c) = \begin{cases}
0 &\text{if } c = \emptyset, \\\
5 &\text{if } c = \\{A\\}, \\\
29 &\text{if } c = \\{B\\}, \\\
39 &\text{if } c = \\{C\\}, \\\
20 &\text{if } c = \\{A,B\\}, \\\
39 &\text{if } c = \\{A,C\\}, \\\
39 &\text{if } c = \\{B,C\\}, \\\
39 &\text{if } c = \\{A,B,C\\}. \\\
\end{cases}
\\]

This function maps each coalition of players to a value (in particular to their taxi fair).
So we see that if Alice and Bob shared a taxi without Celine then their taxi fair would be £20.

It can be shown (I won't cover that here as I want to get to the Sage code) that the 'fair' way of sharing the cost of the taxi is called the **Shapley value** \\(\phi\\) which is a vector given by:

\\[
\phi\_i(G) = \frac{1}{N!} \sum\_{\pi\in\Pi\_n} \Delta\_{\pi}^G(i)
\\]


where:

\\[ \Delta\_{\pi}^G(i) = v\bigl( S\_{\pi}(i) \cup \{i\} \bigr) - v\bigl( S\_{\pi}(i) \bigr) \\]

where \\(S\_{\pi}(i)\\) is the set of predecessors of \\(i\\) in some permutation of the players \\(\pi\\), i.e.  \\(S\_{\pi}(i) = \\{ j \mid \pi(i) > \\pi(j) \\}\\).

**I've got a video that describes all this if it's helpful: [https://www.youtube.com/watch?v=aThG4YAFErw](https://www.youtube.com/watch?v=aThG4YAFErw).**
Here however I want to give a sneak preview of how to figure out what Alice, Bob and Celine should pay using a future release of Sage:

First of all we need to define the characteristic function:


{% highlight python %}
sage: v = {(): 0,
....:      ('A'): 5,
....:      ('B'): 29,
....:      ('C'): 39,
....:      ('A', 'B'): 20,
....:      ('A', 'C'): 39,
....:      ('B', 'C'): 39,
....:      ('A', 'B', 'C'): 39}
{% endhighlight %}

As you can see we do this using a Python dictionary which allows us to map tuples (or indeed coalitions) to values (which is exactly what a characteristic function is).

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
{'A': 1/6, 'B': 73/6, 'C': 80/3}
{% endhighlight %}

This shows that in this particular case Alice should pay £0.17, Bob £12.17 and Celine £26.67 (rounding has obviously caused us to gain a penny along the way but you get the idea) :)

**This is the first in a series of 3 posts that I'll get around to writing, in the next one I'll cover ticket 16331 which takes care of matching games :)**

To go back to the process of contributing to an open source project, I really think this is something everyone with any interests in code should have a go at doing as it has a large number of benefits.
None more so than improving the standard of code that one writes.
When you're writing because you hope that someone will look at **and review** your code you make sure it's well written (or at least try to!).
