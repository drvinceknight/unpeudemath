---
layout     : post
title      : "On testing degeneracy of bi-matrix games"
categories : code
tags       :
- sage
- game theory
comments   : false
---

We (James Campbell and Vince Knight are writing this together) have been working
on implementing code in [Sage](http://www.sagemath.org/) to test if a game is
degenerate or not. In this post we'll prove a simple result that is used in the
algorithm that we are/have implemented.

## Bi-Matrix games

For a general overview of these sorts of things take a look at [this post from a
while ago on the subject of bi-matrix games in
Sage]({{site.baseurl}}/code/2014/12/10/sneak-preview-of-game-theory-in-sage-3-of-3/).
A bi-matrix is a matrix of tuples corresponding to payoffs for a 2 player Normal Form Game.
Rows represent strategies for the first player and columns represent strategies
for the second player, and each tuple of the bi-matrix corresponds to a tuple of
payoffs. Here is an example:

$$
\begin{pmatrix}
(3,3)&(3,3)\\
(2,2)&(5,6)\\
(0,3)&(6,1)\\
\end{pmatrix}
$$

We see that if the first player plays their first row strategy and the second
player their second column strategy then the first player gets a utility of 5
and the second player a utility of 6.

This can also be written as two separate matrices.
A matrix \\(A\\) for Player 1 and \\(B\\) for Player 2.

$$
A =
\begin{pmatrix}
3&3\\
2&5\\
0&6\\
\end{pmatrix}
\quad
B =
\begin{pmatrix}
3&2\\
2&6\\
3&1\\
\end{pmatrix}
$$

Here is how this can be constructed in Sage using the `NormalFormGame` class:

{% highlight python %}
sage: A = matrix([[3,3],[2,5],[0,6]])
sage: B = matrix([[3,2],[2,6],[3,1]])
sage: g = NormalFormGame([A, B])
sage: g
Normal Form Game with the following utilities: {(0, 1): [3, 2], (0, 0): [3, 3],
(2, 1): [6, 1], (2, 0): [0, 3], (1, 0): [2, 2], (1, 1): [5, 6]}
{% endhighlight %}

What is presently implemented in Sage is that we can obtain the Nash equilibria
of games:

{% highlight python %}
sage: g.obtain_nash()
[[(0, 1/3, 2/3), (1/3, 2/3)], [(4/5, 1/5, 0), (2/3, 1/3)], [(1, 0, 0), (1, 0)]]
{% endhighlight %}

We see that this game has 3 Nash equilibrium. For each of them we see that the
supports (number of non zero entries) of both players' strategies are/have? the
same size. This is in fact a theoretic certainty when games are **non
degenerate**.

If we modify the game slightly:

$$
A =
\begin{pmatrix}
3&3\\
2&5\\
0&6\\
\end{pmatrix}
\quad
B =
\begin{pmatrix}
3&3\\
2&6\\
3&1\\
\end{pmatrix}
$$

{% highlight python %}
sage: A = matrix([[3,3],[2,5],[0,6]])
sage: B = matrix([[3,3],[2,6],[3,1]])
sage: g = NormalFormGame([A, B])
sage: g.obtain_nash()
[[(0, 1/3, 2/3), (1/3, 2/3)], [(1, 0, 0), (2/3, 1/3)], [(1, 0, 0), (1, 0)]]
{% endhighlight %}

We see that the second equilibria there has supports of different sizes. In fact,
 if the first player did play \\((1,0,0)\\) (in other words just play the
first row) the second player could play **any mixture** of strategies as a best
response and not particularly \((2/3,1/3)\\). This is because the game in
consideration is now **degenerate**.

(Note that both of the games above are taken from [AGT]().)

## What is a degenerate game

A bimatrix game is called nondegenerate if the number of pure best responses to
a mixed strategy never exceeds the size of its support.
In a degenerate game, this definition is violated, for example if there is a
pure strategy that has two pure best responses (as in the example above), but
it is also possible to have a mixed strategy with support size \\(k\\) that
has \\(k+1\\) strategies that are a best response.

Here is an example of this:

$$
A =
\begin{pmatrix}
3&0\\
0&3\\
1.5&1.5\\
\end{pmatrix}
\quad
B =
\begin{pmatrix}
4&3\\
2&6\\
3&1\\
\end{pmatrix}
$$

If we consider the mixed strategy for player 2: \\(y=(1/2,1/2)\\), then the
utility to player 1 is given by:

$$
Ay=(3/2,3/2,3/2)
$$

We see that there are 3 best responses to \\(y\\) and as \\(y\\) has support
size 2 this implies that the game above is degenerate.

## What does the literature say about degenerate games

The original definition of degenerate games was given in [Lemke, Howson 19..]()
and their definition was dependent on the labeling polytope that they used for
their famous algorithm for the computation of equilibria (which is currently
being implemented in Sage!).
Further to this [Stengel 19...]() offers a nice overview of a variety of
equivalent definitions.

Sadly, all of these definitions require finding a particular mixed strategy
profile \\(x,y\\) for which a particular condition holds.
To be able to implement a test for degeneracy based on any of these definitions
would require a continuous search over possible mixed strategy pairs.

In the previous example (where we take \\(y=(1/2,1/2)\\) we could have
identified this \\(y\\) by looking at the utilities for each pure strategy for
player 1 against \\(y=(y_1, 1-y_1)\\):

$$
u_1(r_1, y_1) = 3y_1
$$

$$
u_1(r_2, y_1) = 3-3y_1
$$

$$
u_1(r_3, y_1) = 3/2
$$

(\\(r_i\\) denotes row strategy \\(i\\) for player 1.)
A plot of this is shown:

![]({{site.baseurl}}/assets/images/plot_for_degenerate_game_post.svg)

We can (in this instance) quickly search through values of \\(y_1\\) and
identify the point that has **the most** best responses which gives the best
chance of passing the degeneracy condition (\\(y_1=1/2\\)).
This is not really practical from a generic point of view which leads to
this blog post: we have identified what the particular \\(x, y\\) is that
is sufficient to test.

## A sufficient mixed strategy to test for degeneracy

**Def.** A Normal Form Game is degenerate if:

\\( \exists \enspace x \\) s.t. \\( \mid S(x) \mid < \mid \sigma_2\mid \\)
where \\( (xB)_j = \text{ Max}(xB) \\), \\( \forall j \\) in \\( \sigma_2 \\)

OR

\\( \exists \enspace y \\) s.t. \\( \mid S(y) \mid < \mid \sigma_1\mid \\)
where \\( (Ay)_i = \text{ Max}(Ay) \\), \\( \forall i \\) in \\( \sigma_1 \\)


**Theorem.** A Normal Form Game is degenerate if:

\\( \exists \enspace \sigma_1 \subseteq X \\) and \\( \sigma_2 \subseteq Y \\)
such that \\( \mid \sigma_1\mid < \mid \sigma_2\mid \\) and \\( S(x^\*) = \sigma_1 \\)
where \\( x^\* \\) is a solution of \\( (xB)_j = \text{ Max}(xB) \\), \\( \forall j \\) in \\( \sigma_2 \\)

OR

\\( \exists \enspace \sigma_2 \subseteq Y \\) and \\( \sigma_1 \subseteq X \\)
such that \\( \mid \sigma_2\mid < \mid \sigma_1\mid \\) and \\( S(y^\*) = \sigma_2 \\)
where \\( y^\* \\) is a solution of \\( (Ay)_i = \text{ Max}(Ay) \\), \\( \forall i \\) in \\( \sigma_1 \\)


## References

- [Lemkey Howson...]()
- [Stengel ...]()
- [AGT ...]()
