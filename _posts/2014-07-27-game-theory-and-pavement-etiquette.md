---
layout: post
title:  "Game Theory and Pavement Etiquette"
categories: Mathematics
tags:
- Game Theory
- Walking
- Etiquette
comments: true
---

Last week the BBC published an article entitled: ['Advice for foreigners on how Britons walk'](http://www.bbc.co.uk/news/magazine-28352045).
The piece basically discusses the fact that in Britain there doesn't seem to be any etiquette over which side of the pavement one walks on:

> The British have little sense of pavement etiquette, preferring a slalom approach to pedestrian progress. When two strangers approach each other, it often results in the performance of a little gavotte as they double-guess in which direction the other will turn.

> Telling people how to walk is simply not British.

> But on the street? No, we don't walk on the left or the right. We are British and wander where we will.

I thought this was a really nice piece and more importantly it is very closely linked to an exercise in game theoretical modelling I've used in class.

Let's consider two people walking along a street.
We'll call one of them Alexandre and the other one Bernard.

Alexandre and Bernard have two options available to them.
In game theory we call these strategies and write: \\(S=\\{L,R\\}\\) where \\(L\\) denotes walk on the left and \\(R\\) denotes walk on the right.

We imagine that Alexandre and Bernard close there eyes and simply walk towards each other making a choice from \\(S\\).
To analyse the outcome of these choices we'll attribute a value of \\(1\\) to someone who doesn't bump in to someone else and \\(-1\\) if they do bump in to the opposite person.

Thus we write:

\\[u\_{A}(L,L)=u\_{B}(L,L)=u\_{A}(R,R)=u\_{B}(R,R)=1\\]

and

\\[u\_{A}(L,R)=u\_{B}(L,R)=u\_{A}(R,L)=u\_{B}(R,L)=-1\\]

We usually represent this situation using two matrices, one showing the utility of each player:

\\[
A = \begin{pmatrix}
1&-1\\\ \\
-1&1
\end{pmatrix}
\\]
\\[
B = \begin{pmatrix}
1&-1\\\ \\
-1&1
\end{pmatrix}
\\]

From these matrices it is easy to read the outcomes of any strategy pairs.
If Alexandre plays \\(L\\) and Bernard plays \\(R\\) then they both get a utility of \\(1\\).
If both are at that strategy pair then neither has a reason to 'deviate' their strategy: this is called a [Nash Equilibrium](http://en.wikipedia.org/wiki/Nash_equilibrium).

Of course though (as alluded to in the BBC article), some people might not always do the same thing.
Perhaps Bernard would randomly choose from \\(S\\).
In which case it makes sense to refer to what Bernard does by the __mixed strategy__ \\(\sigma\_{B}=(x,1-x)\\) for \\(0\leq x\leq 1\\).

If we know that Alexandre is playing \\(L\\) then Bernard's utility becomes:

\\[u\_{B}(L,\sigma)=x-(1-x)=2x-1\\]

Similarly:

\\[u\_{B}(R,\sigma)=-x+(1-x)=1-2x\\]

Here is a plot of both these utilities:

![]({{site.baseurl}}/assets/images/pavement_etiquette_1.svg)

With a little bit of work that I'll omit from this post we can show that there exists another **Nash equilibrium** which is when both Alexandre and Bernard play \\(\sigma=(1/2,1/2)\\).
At this equilibrium the utility to both players is in fact \\(u\_{A}(\sigma,\sigma)=u\_{B}(\sigma,\sigma)=0\\).

This Nash equilibrium is in fact much **worse** than the other Nash equilibria.
In a situation with central control (which if you recall the BBC article is not something that happens on British pavements) then we would be operating with either everyone walking on the left or everyone walking on the right so that the utility would be 1.
As this is also a Nash Equilibrium then there would be no reason for anyone to change.
Sadly it is possible that we get _stuck_ at the other Nash equilibrium where everyone randomly walks on the right or the left (again: at this point no one has an incentive to move).
This idea of comparing **worst case Nash Equilibrium** to the best possible outcome is referred to as the Price of Anarchy and has a lot to do with my personal research.
If it is of interest [here is a short video on the subject](https://www.youtube.com/watch?v=DWiAAWZfooE) and here's a publication that looked at the [effect of selfish behaviour in public service systems](http://www.sciencedirect.com/science/article/pii/S0377221713003019) (sadly that is behind a paywall but if anyone would like to read it please do get in touch).

There are some major assumptions being made in all of the above.
In particular two people walking with their eyes closed towards each other is probably not the best way to think of this.
In fact as all the people on the pavements of Britain constantly walk around you'd expect them to perhaps learn and **evolve** how they decide to walk.

This in fact fits in to a fascinating area of game theory called evolutionary game theory.
The main idea is to consider multiple agents randomly 'bumping in to each other' and playing the game above.

Below are two plots showing a simulation of this (using Python code I describe in [this video](https://www.youtube.com/watch?v=Tz-lZy0AKRI)).
Here is the script that makes use of this small [agent based simulation script](https://github.com/drvinceknight/Gamepy/blob/master/Abm/Abm.py):

{% highlight python %}
import Abm
number_of_agents = 1000  # Size of the population
generations = 100  # Number of generations of players
rounds_per_generation = 5  # How many time everyone from a given generation will `play`
death_rate = .1  # How many weak players we get rid of
mutation_rate = .2  # The chance of a player doing something new
row_matrix = [[1, -1], [-1, 1]]  # The utilities
col_matrix = row_matrix
initial_distribution = [{0: 100, 1: 0}, {0:100, 1:0}]  # The initial distribution which in this case has everyone walking on the left

g = Abm.ABM(number_of_agents, generations, rounds_per_generation, death_rate, mutation_rate, row_matrix, col_matrix, initial_distribution)
g.simulate(plot=True)
{% endhighlight %}


We see that if we start with everyone walking on one side of the left side of the pavement then things are pretty stable (using a little bit of algebra this can be shown to be a so called 'evolutionary stable strategy'):

![]({{site.baseurl}}/assets/images/pavement_etiquette_2.svg)

However, if we start with everyone playing the **worst possible Nash Equilibrium** (randomly choosing a side of the pavement) then we see that this is not stable and in fact we slowly converge towards the population picking a side of the pavement (this is what is called a **non** evolutionary stable strategy):

![]({{site.baseurl}}/assets/images/pavement_etiquette_3.svg)

So perhaps there is a chance yet for the British to automagically choose a side of the pavement...
