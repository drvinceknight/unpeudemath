---
layout     : post
title      : "Discussing the game theory of walking/driving in class"
categories : gametheory
tags       :
- pedagogy
- sage
comments   : true
---

Last week, in game theory class we looked at pairwise contest games.
To introduce this we began by looking at the particular game that one could use to model the situation of two individuals walking or driving towards each other:

$$
\begin{pmatrix}
(1,1)&(-1,-1)\\
(-1,-1)&(1,1)\\
\end{pmatrix}
$$

The above models people walking/driving towards each other and choosing a side of the road.
If they choose the same side they will not walk/drive in to each other.

I got a coupe of volunteers to simulate this and 'walk' towards each other having picked a side.
We very quickly arrived at one of the stage Nash equilibria: both players choosing left and/or choosing right.

I wrote a blog post about this a while ago when the BBC wrote an article about social convention.
You can read that [here]({{site.baseurl}}/mathematics/2014/07/27/game-theory-and-pavement-etiquette/).

We went on to compute the evolutionary stability of 3 potential stable equilibria:

1. Everyone driving on the left;
2. Everyone driving on the right;
3. Everyone randomly picking a side each time.

Note that the above corresponds to the three Nash equilibria of the game itself.
You can see this using some Sage code immediately ([here is a video I just put together showing how one can use Sage to obtain Nash equilibria](https://www.youtube.com/watch?v=QjXAvRiU4Og)) - just click on 'Evaluate':

<div class="compute"><script type="text/x-sage">
A = matrix([[1,-1],[-1,1]])
g = NormalFormGame([A,A])
g.obtain_nash()
</script></div>

We did this calculations in two ways:

1. From first principles using the definitions of evolutionary stability (this took a while).
2 Using a clever theoretic result that in effect does the analysis for us once and for all.

Both gave us the same result: driving on a given side of the road is evolutionarily stable whereas everyone randomly picking a side is not (a nudge in any given direction would ensure people picked a side).

This kind of corresponds to the two (poorly drawn) pictures below:

![]({{site.baseurl}}/assets/images/stability.svg)

To further demonstrate the instability of the 'choose a random side' situation here is a plot of the actual evolutionary process ([here is a video that shows what is happening](https://www.youtube.com/watch?v=Tz-lZy0AKRI)):

![]({{site.baseurl}}/assets/images/evolution_from_random_walking.png)

We see that if we start by walking randomly the tiniest of mutation send everyone to picking a side.
