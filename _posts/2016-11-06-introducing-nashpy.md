---
layout     : post
title      : "A linear algebraic implementation of support enumeration for the computation of equilibria using numpy"
categories : mathematics
tags       :
- python
- gametheory
comments   : true
---

[Gambit](https://github.com/gambitproject/gambit) is the leading piece of
software for computing Nash equilibria of strategic games. A numpy of algorithms
are implemented that take advantage of the higher dimensional geometry relating
to the theory of games. In this post I will describe an approach for finding
Nash equilibria (of 2 player games) that reduces to solving two simple Matrix
equations. This can be implemented in Python using just numpy, I will also
introduce (briefly) a library that does just that.

Consider a 2 player game with row player having \\(m\\) strategies and column
player \\(n\\) strategies. This can be represented by two matrices \\(A,
B\in\mathbb{R}^{m\times n}\\) where \\(A_{ij}\\) is the utility of the row
player when row \\(i\\) is played against column \\(j\\) and \\(B_{ij}\\) is the
corresponding column player utility.

When consider the general case of mixed strategies: a row/column strategy
\\(u\\)/\\(v\\) is an element of \\(\mathbb{R}^{m}\\)/\\(\mathbb{R}^{n}\\) such
that \\(\sum u = \sum v = 1\\).

An example of this is:

$$
A = \begin{pmatrix}
	160 & 205 & 44\\
    175 & 180 & 45\\
    201 & 204 & 50\\
    120 & 207 & 49
	\end{pmatrix}
B = \begin{pmatrix}
	2 & 2 & 2\\
	1 & 0 & 0\\
	3 & 4 & 1\\
	4 & 1 & 2
	\end{pmatrix}
$$

If the column player is playing \\(v\\) (a mixed strategy) then the utilities
available to the row player are given by: \\(Av\\). For example, if the column
player is playing \\(v=(0.2, 0, 0.8)\\) then the utilities of the row player
reduce to:

$$
Av=(67.2,, 71., 80.2, 63.2)
$$

From that utility vector we see that the row player should play the third row
(it has the largest utility: 80.2). This is intuitive: the column player is
picking a strategy that spends 80% of the time in the final column, the third
row of \\(A\\) is the row with the highest value in that column.

**It can be shown** (I won't go in to the details of this here) that at Nash
equilibria, the strategies \\(u, v\\) are such that for the supports of \\(u,
v\\) (the strategies that are played with non zero probability), that the
available utilities to the opposite player (inside that support) must all be
equal.

For example, if we consider \\(v=(1/28, 27/28, 0)\\), we have:

$$
Av\approx(203.39285714,  179.82142857,  203.89285714,  203.89285714)
$$

As long as the row player plays a strategy that only picks the 1st, 3rd or 4th
row: then the column player has made them indifferent amongst their strategies.

**It can also be shown** that for what is called [non degenerate
games](http://vknight.org/unpeudemath/code/2015/06/25/on_testing_degeneracy_of_games.html),
an equilibria will always occur at points for which the support have equal
size.

So this allows us to identify potential (mixed) strategies that could be Nash
equilibria. To prove that they are Nash equilibria we just need to check that
no player has an incentive to deviate outside of the support.

For a given strategy pair \\(u, v\\), with supports \\(S(u), S(v)\\) (supports
are sets of indices), the indifference condition can be written in matrix
form as:

$$
M_{\text{row}}v=b_{\text{row}}
$$

$$
M_{\text{col}}u=b_{\text{col}}
$$

Where \\(M_{\text{row}}\\) is a function of \\(A, S(u)\\) and \\(S(v\)\\) and
\\(M_{\text{col}}\\) is a function of \\(B, S(u)\\) and \\(S(v\)\\) and has
dimension: \\((|S(u)| + n - |S(v)|)  \times n\\). Here is the form of
\\(M_{\text{row}})\\):

$$
(M_{\text{row}})_{ij} =
\begin{cases}
B_{S(u)_i,j} - B_{S(u)_{i +1}, j},&\text{ if }i \leq |S(u)| - 1\\
1,& \text{ if }|S(m)| + n - |S(v)|>i>|S(u)| - 1 = i - j \text{ and }j\notin S(u)\\
1,& \text{ if }i=|S(m)| + n - |S(v)|\\
0,&\text{ otherwise}
\end{cases}
$$

and:

$$
(b_{\text{row}})_{j} = \begin{cases}
1,&\text{ if }j = S(u) + n - |S(v)|\\
0,&\text{ otherwise}
\end{cases}
$$

\\(b\\) is just a vector of 0s followed by a 1.

- The first condition ensures we have indifference between all utilities;
- The second condition ensures we have the correct support (places a single one
  in the position corresponding to each strategy that must be played with
  probability 0);
- The final condition ensures we have a probability vector (a row of 1s)

To obtain expressions for \\(M_{\text{col}}\\) and \\(b_{\text{row}}\\) simply
consider \\(B^{T}\\) to be a row matrix of the corresponding game.

So for example, using the matrix \\(B\\) from before and assuming
\\(S(u)=\\{3,4\\}\\) and \\(S(v)=\\{1, 2\\}\\). We have \\(M_{\text{row}}\\) given
by:

$$
M_{\text{row}} =
\begin{pmatrix}
  81.&  -3.&   1.\\
   0.&   0.&   1.\\
   1.&   1.&   1.
\end{pmatrix}
$$

Similarly:

$$
M_{\text{col}} =
\begin{pmatrix}
  0.&  1.& -1.&  3.\\
  1.&  0.&  0.&  0.\\
  0.&  1.&  0.&  0.\\
  1.&  1.&  1.&  1.
\end{pmatrix}
$$

Solving:

$$M_{\text{row}}v=\begin{pmatrix}
0\\0\\1
\end{pmatrix}$$

gives: \\(v=(0.03571429,  0.96428571,  0)\\)

and solving:

$$M_{\text{col}}u=\begin{pmatrix}
0\\0\\0\\1
\end{pmatrix}$$

gives: \\(v=(0.  ,  0.  ,  0.75,  0.25)\\)

This gives a simple enough approach to calculating Nash equilibria:

1. Go through all potential supports (this corresponds to the powerset of the
   strategy sets);
2. Find potential indifference strategies (as above);
3. Check if they are Nash equilibrium (by seeing if there is any pure strategy
   that gives a better utility to either player. (I'm skipping this step in our
   running example).

Because we have been able to reduce this to a solving a simple linear equation,
we can use numpy to do the hard work for us.

## TLDR: Announcing Nashpy a library for the computation of equilibria in 2 player games

As I mentioned above: if you want to do serious Game Theoretic work, you should
use [Gambit](https://github.com/gambitproject/gambit) **but** if you want a
light weight python library that is pip installable and has just got numpy as a
dependency then `Nashpy` could do the trick.

Install it directly from `pypi` with `pip install nashpy`.
Here is how to solve the game we've been experimenting with:

```
>>> import nash
>>> A = [[160, 205, 44],
...      [175, 180, 45],
...      [201, 204, 50],
...      [120, 207, 49]]
>>> B = [[2, 2, 2],
...      [1, 0, 0],
...      [3, 4, 1],
...      [4, 1, 2]]
>>> g = nash.Game(A, B)
>>> equilibria = list(g.equilibria())
>>> equilibria
[(array([ 0.  ,  0.  ,  0.75,  0.25]), array([ 0.03571429,  0.96428571,  0.        ]))]

```

The library makes use of generators wherever possible and almost everything is
done in numpy to try and be as efficient as possible.

That is pretty much all this library does but if you want more information take
a look at the repository on github:
[github.com/drvinceknight/Nashpy](https://github.com/drvinceknight/Nashpy).
