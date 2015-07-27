---
layout     : post
title      : "A talk on computational game theory in Sagemath"
categories : code
tags       :
- sage
- game theory
- python
comments   : true
---

Today, Cardiff University, School of Mathematics students: James Campbell, Hannah
Lorrimore as well as Google Summer of Code student Tobenna P. Igwe (PhD student
at the University of Liverpool) as well as I presented the current game
theoretic capabilities of [Sagemath](http://www.sagemath.org/).

This talk happened as part of a two day visit to see [Dima
Pasechnik](http://www.cs.ox.ac.uk/people/dmitrii.pasechnik/) to work on the
stuff we've been doing and the visit was kindly supported by
[CoDiMa](http://www.codima.ac.uk/) (an
EPSRC funded project to support the development of GAP and Sagemath)

**Here is the video of the talk:**

<div class="video">
    <figure>
        <iframe width="640" height="360" src="https://www.youtube.com/embed/v4kKYr5I2io?rel=0" frameborder="0" allowfullscreen></iframe>
    </figure>
</div>

[Here is a link to the sage worksheet we used for the talk.](https://cloud.sagemath.com/projects/2a31f88b-4244-4bd1-8e3a-3169ff24daac/files/Talk-2015-07-27/talk.sagews)

Here are some photos I took during the talk:

![](https://lh3.googleusercontent.com/-0apjrcG0qEw/VbZsAWAPXtI/AAAAAAABlSo/ZYWuBQSwnL8/w747-h560-no/IMG_20150727_151428.jpg)
![](https://lh6.googleusercontent.com/Mdhv4ZH7H6Yww9H8P6hTJ5C8PTuTI55ysCjQUe-PTZ0=w747-h560-no)
![](https://lh3.googleusercontent.com/-p6qHJDfk-xc/VbZsAab_4yI/AAAAAAABlSo/aj65EG02mvo/w747-h560-no/IMG_20150727_152941.jpg)

and here are some I took of us working on code afterwards:

![](https://lh5.googleusercontent.com/-qBweJME_HBg/VbZsARW7D_I/AAAAAAABlTI/8GHa-SPNSxg/w747-h560-no/IMG_20150727_155756.jpg)
![](https://lh5.googleusercontent.com/-kZLhblBepTE/VbZsAYQk_CI/AAAAAAABlTA/2USGMza-jj8/w747-h560-no/IMG_20150727_175244.jpg)

**Here is the abstract of the talk:**

Game Theory is the study of rational interaction and is getting increasingly important in CS. Ability to quickly compute a solution concept for a nontrivial (non-)cooperative game helps a lot in practical and theoretic work, as well as in teaching.
This talk will describe
and demonstrate the game theoretic capabilities of Sagemath
(http://www.sagemath.org/), a Python library, described as having the following mission:
'Creating a viable free opensource alternative to Magma, Maple, Mathematica and
Matlab'.

The talk will describe algorithms and classes that are implemented for the
computation of Nash equilibria in bimatrix games. These include:

- A support enumeration algorithm;
- A reverse search algorithm through the lrs library;
- The Lemke-Howson algorithm using the Gambit library (https://github.com/gambitproject/gambit).

In addition to this, demonstrations of further capabilities that are actively being
developed will also be given:

- Tests for degeneracy in games;
- A class for extensive form games which include the use of the graph
  theoretic capabilities of Sage.

The following two developments which are being carried out as part of a
Google Summer of Code project will also be demonstrated:

- An implementation of the Lemke-Howson algorithm;
- Extensions to N player games;

Demonstrations will use the (free) online tool cloud.sagemath which allows anyone with
connectivity to use Sage (and solve game theoretic problems!). Cloud.sagemath
also serves as a great teaching and research tool with access to not only Sage but Jupyter
(Ipython) notebooks, R, LaTeX and a variety of other software tools.

The talk will concentrate on strategic non-cooperative games but matching games
and characteristic function games will also be briefly discussed.
