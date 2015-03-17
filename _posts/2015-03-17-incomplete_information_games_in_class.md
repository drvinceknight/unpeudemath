---
layout     : post
title      : "Incomplete information games in class"
categories : gametheory
tags       :
- pedagogy
- sage
comments   : true
---

Last week my class and I looked at the basics of games with incomplete information.
The main idea is that players do not necessarily know where there are in an extensive form game.
We repeated a game I played last year that you can read about [here](http://drvinceknight.blogspot.co.uk/2014/03/playing-game-with-incomplete.html).

Here is a picture of the game we played (for details take a look at the post from last year):

![]({{site.baseurl}}/assets/images/matchingpenniesunderuncertainty.png)

We played a round robing where everyone played against everyone else and you can see the results in these two notebook pages that Jason kept track off:

![]({{site.baseurl}}/assets/images/2015-incomplete-info-game-1.jpg)
![]({{site.baseurl}}/assets/images/2015-incomplete-info-game-2.jpg)

We see that the winner was Reg, who on both occasions of being the second player: went with the coin.

To find the Nash equilibria for this game we can translate it in to normal form game by doing the following two things:

1. Identify the strategy sets for the players
2. Averaging of the outcome probabilities

This gives the following strategies:

$$
S_1 = \{H, T\}
$$

and

$$
S_2 = \{HH, HT, TH, TT\}
$$

The strategies for the second player correspond to a 2-vector indexed by the information sets of the second player.
In other words the first letter says what to do if the coin comes up as heads and the second letter says what to do if the coin comes up as tails:

1. \\(HH\\): No matter what: play heads;
2. \\(HT\\): If the coin comes up as heads: play heads. If the coin comes up as tails: play tails.
3. \\(TH\\): If the coin comes up as heads: play tails. If the coin comes up as tails: play heads.
4. \\(TT\\): No matter what: play tails;

Once we have done that and using the above ordering we can obtain the normal form game representation:

$$
\begin{pmatrix}
(1/2,-1/2)&(-1/2,1/2)&(0,0)&(-1,1)\\
(-1,1)&(-1/2,1/2)&(0,0)&(1/2,-1/2)\\
\end{pmatrix}
$$

In class we obtained the Nash equilibria for this game by realising that the third column strategy (\\(TH\\): always disagree with the coin) was dominated and then carrying out some indifference analysis.

Here let us just throw it at Sage ([here is a video showing and explaining some of the code](https://www.youtube.com/watch?v=QjXAvRiU4Og)):

<div class="compute"><script type="text/x-sage">
A = matrix([[1/2, -1/2, 0, -1],
            [-1, -1/2, 0, 1/2]])
B = matrix([[-1/2, 1/2, 0, 1],
            [1, 1/2, 0, -1/2]])
g = NormalFormGame([A,B])
g.obtain_nash()
</script></div>

The equilibria returned confirms what we did in class: the first player can more or less randomly (with bounds on the distribution) pick heads or tails but the second player should always agree with the coin.
