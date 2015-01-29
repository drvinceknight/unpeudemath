---
layout     : post
title      : "Recreating golden balls in class"
categories : pedagogy
tags       :
- gametheory
comments   : false
---

Here is a blog post that mirrors [this post](http://drvinceknight.blogspot.co.uk/2014/02/an-attempt-at-golden-balls-in-class.html) from last year.
I will describe the attempt at playing Golden Balls in class.

The purpose of this was to discuss the concept of Dominance.
If you are not familiar with Golden Balls take a look at this video:

<div class="video">
    <figure>
    <iframe width="420" height="315" src="https://www.youtube.com/embed/p3Uos2fzIJ0" frameborder="0" allowfullscreen></iframe>
    </figure>
</div>

This is what we did.

Firstly we played a series of four games where the score of the row player would correspond to a total of chocolates that both players would share at the end of the game (given that all the games are zero sum this is equivalent to the opposite of the score of the column player).

1. No strategy is dominated:

    $$
    \begin{pmatrix}
    (1,-1)&(-1,1)\\
    (-1,1)&(1,-1)\\
    \end{pmatrix}
    $$

    In this instance both players went for the column strategy.
    There is no real explanation for this: in essence they got lucky :)
    Thus at this stage we had 1 bar of chocolate.

2. The first row strategy is dominated:

    $$
    \begin{pmatrix}
    (1,-1)&(-1,1)\\
    (1,-1)&(1,-1)\\
    \end{pmatrix}
    $$

    From here it is obvious that the row player would go for their second strategy.
    This indeed happened and the column player went for their first strategy (which in fact makes no difference: the column strategy could have played either strategy).
    Thus at this stage we had 2 bars of chocolate.

3. No strategies are dominated:

    $$
    \begin{pmatrix}
    (2,-2)&(-1,1)\\
    (-1,1)&(2,-2)\\
    \end{pmatrix}
    $$

    This is very similar to the first game except I upped the number of chocolate bars available.
    Both players played their second strategy and thus we had a total of 4 bars of chocolate at this stage.

4. The first row strategy is dominated:

    $$
    \begin{pmatrix}
    (2,-2)&(1,-1)\\
    (-1,1)&(2,-2)\\
    \end{pmatrix}
    $$

    The row played went with their first strategy (as expected given the domination) however the column player went with their second strategy.
    This is possibly due to the slightly 'fake' setup of the game in terms of chocolates.
    Picking the second strategy ensured that they would not _lose_ chocolates.

At the end of this I added another chocolate bar to the stash so that we had a nice even number of 6.
At this point the players actually played a version of Golden Balls:

$$
\begin{pmatrix}
(1,1)&(0,1.5)\\
(1.5,0)&(2,2)\\
\end{pmatrix}
$$

The utility in that game corresponded to the share of the chocolates: so a score of 1 implies they would both get 6, a score of 1.5 would imply they both got 9.

Both player here managed to stay away from the Nash equilibrium (which is the pair of second strategies due to iterated elimination of dominated strategies) and ended up with 6 chocolates each.
Well done to G and K who were good sports and without whom we would not have been able to play the game.

This was in stark contrast with the cool result from [last year](http://drvinceknight.blogspot.co.uk/2014/02/an-attempt-at-golden-balls-in-class.html).

After this I proceeded to play a best out of three game of tic-tac-toe with J to get to the idea of a game like that being pre defined: no one should really ever win that unless someone makes a mistake (or indeed plays irrationally: on that note I owe J a chocolate bar).

Here is Randall Munroe's [solution of tic-tac toe](http://xkcd.com/832/).

This leads us to the idea of best responses which is the subject of another game we played in class and one for which I'm about to start reading in the data.
If you're inpatient take a look at the [corresponding post from last year](http://drvinceknight.blogspot.co.uk/2014/02/best-responses-to-mixed-strategies-in.html).
