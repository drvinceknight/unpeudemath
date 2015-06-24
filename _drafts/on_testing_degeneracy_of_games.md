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
A degenerate game is one that has an infinite number of Nash Equilibria.

# What does the literature say about it
(Reference the papers)

# Our result
Let \\(X\\) be the set of all strategies for Player1.
Let \\(Y\\) be the set of all strategies for Player2.
For any \\(x \in X\\) let \\(S(x)\\) be the size of the support of \\(x\\).
(Similar for any \\(y \in Y\\)).

If the game is degenerate, then there exists \\(x_* \in X\\) such that \\(S(x_*) = K\\) and Player2 has \\(N\\) best responses with \\(N > K\\).