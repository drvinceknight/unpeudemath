---
layout     : post
title      : "When hospitals interact and act rationally inefficiencies can occur"
categories : Mathematics
tags       :
- healthcare
- math
comments   : true
---

This is a blog post describing a paper [Izabela
Spernaes](https://twitter.com/IzabelaSpernaes), [Jeff
Griffiths](https://www.cardiff.ac.uk/people/view/98574-griffiths-jeff)
and I had published last year. I am going to start using this blog to [write
about
papers](https://medium.com/advice-and-help-in-authoring-a-phd-or-non-fiction/how-to-write-a-blogpost-from-your-journal-article-6511a3837caa)
I publish and I'm starting with a paper called
[Measuring the
price of anarchy in critical care unit interactions](https://link.springer.com/article/10.1057/s41274-016-0100-8). In this paper, we used
game theory and Markov models to model interactions between two critical care
units.

The underlying idea here is that when you have uncoordinated behaviour you get
inefficiency. A good example of this is the [Prisoner's
Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma). If two prisoner's
act in a coordinated way, where there was some form of central control that
wanted to reduce time in Prison: they would cooperate with each other and go to
prison for 2 years each. If however we remove that central control and let both
players do exactly what is rational for themselves they would go to prison for 4
years each.

This paper is not the first that's looked at inefficiencies in healthcare caused
by uncoordinated behaviour:

- In [Centralized
  vs. Decentralized Ambulance Diversion: A Network Perspective](http://pubsonline.informs.org/doi/abs/10.1287/mnsc.1110.1342) a game theoretic
  model is used to look at Ambulance diversion from one emergency room to
  another. The see what happens to Ambulances when hospitals don't coordinate
  behaviour. So one hospital might say they're too full to take an ambulance
  without coordinating this declaration with another ambulance.
- In [Selfish routing in Public servicesThe Price of Anarchy in Public
  services](http://www.sciencedirect.com/science/article/pii/S0377221713003019),
  [Paul Harper](https://twitter.com/profpaulharper) and I look at how
  uncoordinated patient behaviour can increase waiting times.

In the paper I'm discussing here we took a look at modelling interactions
between critical care units. We noticed in another piece of research: [a 2015
paper about combining two critical care
units](https://www.ncbi.nlm.nih.gov/pubmed/25267582), that behavioural models of
waiting lines seemed to model two critical care units better than standard
models. This gave us the idea to look at how two critical care units would
interact when one accepts slightly less patients (sending them to the other) if
its occupancy is passed a certain point.

The first thing we had to do was build a Markov chain model of the occupancy of
the hospital: we do this by considering the state of the system as a two
dimensional vector. For example: \\((2, 15)\\) would indicate that there were 2
people in the first unit and 15 in the second. We can then build up linear
relationships between any two states using the rate at which a patient arrives
and how long they stay in service. This does make an assumption about the fact
that the length of stay follows a so called [exponential
distribution](https://en.wikipedia.org/wiki/Exponential_distribution). An image
of the entire chain is shown here:

![](https://static-content.springer.com/image/art%3A10.1057%2Fs41274-016-0100-8/MediaObjects/41274_2016_100_Fig3_HTML.gif)

The red lines shows the "strategies" of both hospital: ie the point of occupancy
at which they take in less patients. We considered two possible scenarios:

1. If both hospitals are past that point (ie they both stop taking patients)
   then those patients are lost to the system;
2. If both hospitals are past that point then they do take the patients that
   were originally intended for them.

From the point of a central controller, we would hope to ensure that as many
patient as possible are seen. This does not necessarily imply that both
units should never send patients to the other. Indeed our Markov model will
capture the variability in the system and always working at full capacity will
imply that new patients often find the system full.

From the point of view of the individual unit they will try to be as efficient
as possible. Often, with a hope to align the social good with the goals of the
individual agents in a system, targets will be imposed. For example, perhaps
some guideline about the target occupancy rate of a unit

Once we have this we can build a normal form game representation, of the number
of total patients seen in total. So that would look like this:


$$
A =
\begin{pmatrix}
(U_{1}(1,1)-t)^2&\dots&(U_{1}(1,c_{2})-t)^2\\
(U_{1}(2,1)-t)^2&\dots&(U_{1}(2,c_{2})-t)^2\\
\vdots&\ddots&\vdots\\
(U_{1}(c_{1},1)-t)^2&\dots&(U_{1}(c_{1},c_{2})-t)^2\\
\end{pmatrix}
$$

$$
B =
\begin{pmatrix}
(U_{2}(1,1)-t)^2&\dots&(U_{2}(1,c_{2})-t)^2\\
(U_{2}(2,1)-t)^2&\dots&(U_{2}(2,c_{2})-t)^2\\
\vdots&\ddots&\vdots\\
(U_{2}(c_{2},1)-t)^2&\dots&(U_{2}(c_{2},c_{2})-t)^2\\
\end{pmatrix}
$$

Where \\(A_{ij}\\) is the "utility" to the first unit when the first unit's
threshold is at \\(i\\) patients and the second is at \\(j\\) patients.


Following this, in the paper we proved a theoretic result about the location of
the Nash equilibrium: the point at which both hospitals will end up when aiming
to get as close as possible to the target occupancy \\(t\\).

Then finally we carried out a number of numerical experiments. All using
[sagemath](http://sagemath.com/) which was my tool of choice at the time, if we
were to do this again we would probably use Python.

Some of the insight we gained from these numerical experiments:

- Inefficiency (ie lost patients) can be relatively high in some scenarios (10%
  loss of patients for example).
- It is possible to find a target that ensures that there is no inefficiency.

This was a paper I very much enjoyed working on as it was a direct application
of Game Theory and demonstrates the importance of understanding the effect of
behaviour on complex systems.



- The paper can be found here:
  [link.springer.com/article/10.1057/s41274-016-0100-8](https://link.springer.com/article/10.1057/s41274-016-0100-8)
- The code for this can be found here:
  [github.com/drvinceknight/Measuring_the_price_of_anarchy_in_ccu_interactions](https://github.com/drvinceknight/Measuring_the_price_of_anarchy_in_ccu_interactions)
- If you would like to listen to a 15 min screencast (from 2014) of a talk I gave
 on this you can see it here:

  <div class="video">
        <figure>
        <iframe width="560" height="315" src="https://www.youtube.com/embed/-u-62LxSYsA" frameborder="0" allowfullscreen></iframe>
        </figure>
  </div>
