---
layout: post
title:  "The Mathematics of Pavement Etiquette"
categories: Mathematics
tags:
- Game Theory
- Walking
- Etiquette
comments: false
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
In game theory we call these strategies and write: \\(S=\{L,R\}\\) where \\(L\\) denotes walk on the left and \\(R\\) denotes walk on the right.

We imagine that Alexandre and Bernard were to close there eyes and simply walk towards each other making a choice from \\(S\\).
To analyse the outcome of these choices we'll attribute a value of \\(1\\) to someone who doesn't bump in to someone else and \\(-1\\) if they do bump in to the opposite person.

Thus we write:

\\[u\_{A}(L,L)=u\_{B}(R,R)=1\\]

and

\\[u\_{A}(L,R)=u\_{B}(L,R)=-1\\]

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

Of course though (as alluded to in the BBC article), some people might not always do the same thing.
Perhaps Bernard would randomly choose from \\(S\\).
In which case it makes sense to refer to what Bernard does by the __mixed strategy__ \\(\sigma\_{B}=(x,1-x)\\) for \\(0\leq x\leq 1\\).

- Plot utility
- Discuss Equilibria: A [Nash Equilibrium](http://en.wikipedia.org/wiki/Nash_equilibrium) is a pair of strategies
- Discuss worst case

Possible plot evolutionary game theoretic behaviour.

