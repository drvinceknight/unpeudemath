---
layout     : post
title         : "A Sneak Preview of Game Theory in Sage (3/3): Normal Form Games"
categories : code
tags       :
- python
- mathematics
comments   : true
---

In two previous posts I have discussed two game theoretical concepts that are in/on their way in to [Sage](http://sagemath.org/):

- [Cooperative Games/Shapley value](http://vincent-knight.com/unpeudemath/code/2014/08/01/a-sneak-preview-of-game-theory-in-sage-1-of-3/): this is already in Sage.
- [Matching Games](http://vincent-knight.com/unpeudemath/code/2014/08/27/sneak-preview-of-game-theory-in-sage-2-of-3/): this has been merged in to the develop branch of Sage (so you can already play with it if you wanted to) so will be in the next release.

Since writing those and alluding to more development that myself and an undergraduate here at Cardiff are working on, I've had a fair few people asking about when Normal Form Games will be included...

**The purpose of this post is to say: extremely soon!** A `NormalFormGame` class has now also been merged in to the develop branch of Sage (so it will be in the next release).

# What is a normal form game

These are sometimes referred to as bi-matrix games or strategic form games.
I wrote a blog post about these in reference to choosing a side of the pavement to walk on: [here]({{site.baseurl}}/mathematics/2014/07/27/game-theory-and-pavement-etiquette/).

**In this post I'll take a look at what the new Sage class allows you to do.**

Consider the game I used to model two individuals walking on either the left or the right of the pavement:

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

Matrix \\(A\\) gives the utility to the first person (assuming they control the rows) and the matrix \\(B\\) gives the utility to the second person (assuming they control the columns).

## Defining a game

We can define these two matrices in Sage and will be able to define a `NormalFormGame` as follows:

{% highlight python %}
sage: A = matrix([[1, -1],[-1, 1]])
sage: B = matrix([[1, -1],[-1, 1]])
sage: g = NormalFormGame([A, B])
{% endhighlight %}

As you can see the `NormalFormGame` class uses a list of two matrices to construct a game.
If you look at the documentation you'll see that there are other ways to construct games.
To see that this has indeed worked we can just see the output of the game:

{% highlight python %}
sage: g
Normal Form Game with the following utilities: {(0, 1): [-1, -1], (1, 0): [-1, -1], (0, 0): [1, 1], (1, 1): [1, 1]}
{% endhighlight python %}

This returns a dicionary of the strategy:utility pairs.
The form of the output is actually based on [gambit](http://www.gambit-project.org/) syntax.

We can use this class to very easily obtain equilibria of games:

## Finding Nash equilibria

{% highlight python %}
sage: g.obtain_nash()
[[(0, 1), (0, 1)], [(1/2, 1/2), (1/2, 1/2)], [(1, 0), (1, 0)]]
{% endhighlight %}

The output shows that there are three Nash equilibria for this game:

- Both players walking on their right;
- Both players walking on their left;
- Both players alternating from left to right with 50% probability.

There are currently 2 algorithms implemented in Sage to calculate equilibria:

1. A support enumeration algorithm (this is not terribly efficient but is written in pure Sage so will work even if optional packages are not installed and for typical game sizes will work just fine).
2. A reverse search algorthim which calls the optional 'lrs' library.

My student and I are currently actively developing further integration with gambit which will allow for a linear complementarity algorithm and also solution algorithms for games with more than 2 players.

## Here is one other example:

{% highlight python %}
sage: A = matrix([[0, -1, 1, 1, -1],
....:             [1, 0, -1, -1, 1],
....:             [-1, 1, 0, 1 , -1],
....:             [-1, 1, -1, 0, 1],
....:             [1, -1, 1, -1, 0]])
sage: g = NormalFormGame([A])
sage: g.obtain_nash(algorithm='lrs')
[[(1/5, 1/5, 1/5, 1/5, 1/5), (1/5, 1/5, 1/5, 1/5, 1/5)]]
{% endhighlight %}

As you can see above, I've created a game by just passing a single matrix: this automatically creates a zero sum game.
I've also told Sage to make sure it uses the `'lrs'` algorithm (although `'enumeration'` would handle this 5 by 5 game just fine).

Finally if you're not actually sure what that game is take a look at this little video:

<div class="video">
    <figure>
    <iframe width="420" height="315" align='middle' src="//www.youtube.com/embed/iapcKVn7DdY" frameborder="0" allowfullscreen></iframe>
    </figure>
</div>


I'm very excited to see this in Sage (soon!) and am actively working on various other things that I know at least I will find useful in my research and teaching but hopefully others will also.
