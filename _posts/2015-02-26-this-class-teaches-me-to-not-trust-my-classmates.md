---
layout     : post
title      : "This class teaches me to not trust my classmates: An iterated prisoners dilemma in class"
categories : pedagogy
tags       :
- gametheory
comments   : true
---

On Monday, in class we played an iterated prisoner's dilemma tournament.
I have done this many times (both in outreach events with [Paul Harper](http://www.profpaulharper.com/) and in this class).
This is always a lot of fun but none more so than last year when Paul's son Thomas joined us.
You can read about that one [here](http://drvinceknight.blogspot.co.uk/2014/02/iterated-prisoners-dilemma-tournament.html).

The format of the game is as close to that of Axelrod's original tournament as I think it can be.
I split the class in to 4 teams and we create a round robin where each team plays every other team at 8 consecutive rounds of the prisoner's dilemma:

$$
\begin{pmatrix}
(2,2) & (5,0)\\
(0,5) & (4,4)\\
\end{pmatrix}
$$

The utilities represent 'years in prison' and over the 3 matches that each team will play (against every other team) the goal is to reduce the total amount of time spent in prison.

Here are some photos from the game:

![]({{site.baseurl}}/assets/images/pd_2015_01.jpg)

![]({{site.baseurl}}/assets/images/pd_2015_02.jpg)

![]({{site.baseurl}}/assets/images/pd_2015_03.jpg)

Here are the scores:

![]({{site.baseurl}}/assets/images/pd_2015_results.jpg)

We see that 'We will take the gun' acquired the least total score and so they won the collection of cookies etc...

![]({{site.baseurl}}/assets/images/pd_2015_cookies.jpg)

(The names followed a promise from me to let the team with the coolest name have a nerf gun... Can't say this had the wanted effect...)

At one point during the tournament, one team actually almost declared a strategy which was cool:

> We will cooperate until you defect at which point we will reevaluate

This was pretty cool as I hadn't discussed at all what a strategy means in a repeated game (ie I had not discussed the fact that a strategy in a repeated game takes count of both play histories).

Here are all the actual duels:

![]({{site.baseurl}}/assets/images/pd_2015_duels.jpg)

You'll also notice at the end that a coalition formed and one team agreed to defect so that they could share the prize.
This happens about 50% of the time when we play this game but I never cease to be amused by it.
Hopefully everyone found this fun and perhaps some even already agree with a bit of feedback I received on this course last year:

> 'This class teaches me to not trust my classmates'

One of the other really cool things that happened after this class was H asking for a hand to submit a strategy to my Axelrod repository.
She built a strategy called 'Once Bitten' that performs pretty well!
You can see it [here](https://github.com/drvinceknight/Axelrod/blob/master/axelrod/strategies/oncebitten.py) (click on 'Blame' and you can see the code that she wrote).

(Big thanks to Jason for keeping track of the scores and to Geraint for helping and grabbing some nice pictures)
