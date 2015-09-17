---
layout     : post
title      : "A Summer of game theory software development"
categories : code
tags       :
- sage
- gametheory
comments   : true
---

This Summer has seen 3 undergraduates carry out 8 week placements with me
developing further game theoretic code in Sagemath:

Hannah Lorrimore (going in to her 2nd year) spent her placement working
very hard to implement classes for extensive form games. These are mainly
a graphical representation of games based on a tree like structure. Hannah
not only developed the appropriate data structures but also worked hard to
make sure the graphics looked good. You can see an example of the output
below:

![]({{site.baseurl}}/assets/images/tree.png)

James Campbell (going in to an industrial placement year) picked up where he
left off last Summer (James built the first parts of Game Theory code for
Sagemath) and developed a test for degeneracy of games. This involves building a
corresponding linear system for the game and testing a particular condition.
James and I wrote a blog post about some of the theory here:
[http://vknight.org/unpeudemath/code/2015/06/25/on_testing_degeneracy_of_games/](http://vknight.org/unpeudemath/code/2015/06/25/on_testing_degeneracy_of_games/).

Rhys Ward (going in to his first year) has been working at the interface
between extensive form games and normal form games. His main contribution
(Rhys is still working as of the writing of this) has been to build code
that converts an extensive form game to a normal form game. This requires
carefully traversing the underlying tree and keeping track of the strategy
space. Rhys has also built a catalog of normal form games and is now
starting to work on the capability to remove dominated strategies from a
normal form game.

Hannah, Rhys and James have also been working in conjunction with Tobenna
Peter Igwe who is a PhD student at the University of Liverpool. Tobenna has
been implementing a variety of game theoretic code as part of the Google
Summer of Code project with me as his mentor.

Hannah, James, Tobenna and I visited Oxford University to spend two days
working with Dr Dima Pasechnik and giving a talk. You can see a video of the
talk here: https://www.youtube.com/watch?v=v4kKYr5I2io

All of this code will now be reviewed by the Sagemath community and will
(just as James’s code last year) be eventually available to anyone who wants
to study game theory.

**Note: this blog post is based on a similar Cardiff University newsletter item.**
