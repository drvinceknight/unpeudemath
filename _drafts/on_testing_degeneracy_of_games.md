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

# What is a bi-matrix
A bi-matrix is a matrix of tuples corresponding to payoffs for a 2 player Normal Form Game.
Rows represent strategies for Player1 and columns represent strategies for player2.

$$
\begin{pmatrix}
(3,3)&(3,3)\\
(2,2)&(5,6)\\
(0,3)&(6,1)\\
\end{pmatrix}
$$

This could also be written as two seperate matrices. A matrix \\(A\\) for Player1 and \\(B\\) for Player2.

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

We could do this Normal Form game in sage using

{% highlight python %}
sage: A = matrix([[3,3],[2,5],[0,6]])
sage: B = matrix([[3,3],[2,6],[3,1]])
sage:g = NormalFormGame([A, B])
{% endhighlight %}

# What is a degenerate game
A bimatrix game is called nondegenerate if the number of pure best responses to a mixed strategy never exceeds the size of its support.
In a degenerate game, this definition is violated, for example if there is a pure strategy that has two pure best responses.

# What does the literature say about it
The following are equivalent:

- The game is nondegenerate according to Definition 2.6
- For any \\(x \in X\\) and \\(y \in Y\\), the rows of IMB for the labels of \\(x\\) are linearly independent, and the rows of AIN for the labels of \\(y\\) are linearly independent.
- For any \\(x \in X\\) with set of labels \\(K\\) and \\(y \in Y\\) with set of labels \\(L\\), the set has dimension \\(m − K\\), and the set has dimension \\(n − L\\).
- P1 andP2 in  (2.18)  are  simple  polytopes,  and  any  pure  strategy  of  a  player  thatis weakly dominated by or payoff equivalent to another mixed strategy is strictlydominated by some mixed strategy.
- In any basic feasible solution to (2.20), all basic variables have positive values.

2002 - Von Stengel - Computing equilibria for two-person games

# Our result
Let \\(X\\) be the set of all strategies for Player1.
Let \\(Y\\) be the set of all strategies for Player2.
For any \\(x \in X\\) let \\(S(x)\\) be the size of the support of \\(x\\).
(Similar for any \\(y \in Y\\)).

If the game is degenerate, then there exists \\(x_* \in X\\) such that \\(S(x_*) = K\\) and Player2 has pure best responses \\(y_1, y_2,...,y_N\\) with \\(N > K\\).
(By definition)

For all \\(y_1, y_2,...,y_N\\) to be best responses, \\(x_* \\) must make each of them have the same utility.
Then there must also exist \\(y_* \in Y\\) with the same utility where the support of \\(y_* \\) is the strategies \\(y_1, y_2,...,y_N\\).
For this to be possible, \\(x_* \\) must make Player2 indifferent.