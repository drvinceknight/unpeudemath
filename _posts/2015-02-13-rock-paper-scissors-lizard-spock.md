---
layout     : post
title      : "Rock paper scissors lizard spock tournement"
categories : pedagogy
tags       :
- gametheory
comments   : true
---

At the beginning of the week we played had one of my favourite class activity for my game theory class: the rock paper scissors lizard tournament :)
In this post I will briefly go over some of the results.

If you are not familiar with [Rock Paper Scissors Lizard Spock](http://bigbangtheory.wikia.com/wiki/Rock_Paper_Scissors_Lizard_Spock) this is a good video that explains it:

<div class="video">
    <figure>
        <iframe width="420" height="315" src="https://www.youtube.com/embed/Kov2G0GouBw" frameborder="0" allowfullscreen></iframe>
    </figure>
</div>

This is the second time I play this in class and you can read about the first time [on my old blog](http://drvinceknight.blogspot.co.uk/2014/02/a-rock-paper-scissors-lizard-spock.html).

Here is how the game went (thanks to Geraint for noting everything down and Saniya for grabbing the pictures!):

![]({{site.baseurl}}/assets/images/plot_rpsls.png)

(You can find the tikz code to draw that [here](https://gist.github.com/drvinceknight/5260648fcab53f66ff30).)

Here is a plot of the strategies played during the 1st, 2nd and 3rd rounds:

![]({{site.baseurl}}/assets/images/round1.png)
![]({{site.baseurl}}/assets/images/round2.png)
![]({{site.baseurl}}/assets/images/round3.png)

The overall strategy profile played is here:

![]({{site.baseurl}}/assets/images/allstrategies.png)

Just like last year we are not exactly at Nash equilibria.
In fact it seems that Scissors and Rock are being played a bit more often, so someone entering in to this game should respond by playing Spock (he vaporises Rock and smashes Scissors).

Here are the strategies that at some point won a duel:

![]({{site.baseurl}}/assets/images/winningstrategies.png)

and here are the losing strategies:

![]({{site.baseurl}}/assets/images/losingstrategies.png)

(All the code used to draw and analyse those plots is [here](https://gist.github.com/drvinceknight/17b2798f08a08989d474).)

Hopefully my class found this interesting and fun.
