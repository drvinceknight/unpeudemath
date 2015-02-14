---
layout     : post
title      : "On the worst play in superbowl history"
categories : gametheory
tags       :
- sport
- superbowl
comments   : false
---

In my last game theory class I gave students the choice between starting to rigorously look at extensive form games or to look at the last play of this years superbowl.
No one objected to looking at the superbowl play (which has been called ['the worst play in superbowl history'](https://www.youtube.com/watch?v=CZSqjfYaX4M)) as an opportunity to go over all the normal form game theory we have seen so far.

First of all I had to give a brief overview of American football so I drew a couple of pictures on the board, here is more or less what I drew:

![]({{site.baseurl}}/assets/images/football_field.svg)

I highlighted that the offensive team (the blue guys in my picture) can basically at any point do one of two things:

- **Pass**: the quarter back throws the ball down field.
    This works better when there is more room down the field for guys to get open but in general is a high risk high reward player.
- **Run**: the quarter back hands the ball to the _running back_.
    This in general ensures a small gain of yards and is less risky (but has less reward).

The defence can (at a very simplistic level) set up in two ways:

- **Defend the pass**: they might drop some of guys (red circles) 'out of the box' in a way as to cover blue guys trying to get open.
- **Defend the run**: they might drop more guys (red crosses) 'in to the box', leaving less people to cover the pass but having more people ready to stop the running back from gaining yards.

This immediately lets us set up (in a simplistic way) every phase of play in American Football as a two player normal form game where the _Offense_ has strategy set: \\(S_O=\\{\text{P},\text{R}\\}\\) and the _Defense_ has strategy set: \\(S_D=\\{\text{DP},\text{DR}\\}\\).

Now, to return to what is being called 'the worst play in superbowl history':

<div class="video">
    <figure>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/CZSqjfYaX4M" frameborder="0" allowfullscreen></iframe>
    </figure>
</div>

- The Seahawks have one of the best running backs in the game (funny interview of his [here](https://www.youtube.com/watch?v=G1kvwXsZtU8));
- They had the ball very close to the score line with downs (attempts) to spare.

Everyone seems to be saying that 'not rushing' was an idiotic thing to do.
[This article by the Economist](http://www.economist.com/blogs/gametheory/2015/02/game-theory-american-football) explains things pretty well (including the back story), but in my class on Friday I thought I would go through the mathematics of it all.

First of all let us build some basic utilities (to be clear I am more or less pulling these out of a hat although I will carry out some monte carlo simulation at the end of this blog post).

- Let us assume (because Lynch is awesome) that on average running against a run defence would work 60% of the time;
- Running against a pass defence would work 98% of the time;
- Passing against a rush defence would work 90% of the time;
- Passing against a pass defence would work 50% of the time.

Our normal form game then looks like this (assuming that the game is zero sum):

\[
\begin{pmatrix}
(60,-60)&(98,-98)\\
(90,-90)&(50,-50)\\
\end{pmatrix}
\]

__If the Seahawks were 100% going to run the ball__, in such a way as that the defence were in no doubt then the obvious best response is to use a rush defence (in reality this is actually what happened and the defensive player that was fairly isolated just made an amazing play).
Then, the chance of the Seahawks scoring is 60%.

**What does game theory say should happen?**

First of all what should the offence do to ensure that the defense sometimes defends the pass?
The theory tells us that the offence should make the defense indifferent.
So let us assume that the offence runs \\(x\\) of the time so that the player is playing mixed strategy: \\(\sigma_{\text{O}}=(x,1-x)\\).
The Nash equilibrium strategy for the offence would then obey the following equation:

\[
u_{\text{D}}(\sigma_{\text{O}},\text{RD})=u_{\text{D}}(\sigma_{\text{O}},\text{PD}
\]
