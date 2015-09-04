---
layout     : post
title      : "Picking a good Vainglory jungler with game theory and sagemath"
categories : code
tags       :
- sage
- gametheory
- vainglory
comments   : false
---

I've recently been playing a really cool video game:
[vainglory](http://www.vainglorygame.com/). This is described as a MOBA which I
must admit I had never heard off until this year when my students mentioned it
to me, but basically it's an online multi player game in which players form two
teams of 6 heroes and fight each other. The choice of the heroes is very
important as the composition of a team can make or break a match. This seems to
have a bit of a cult following (so no doubt just like for my [post about clash
of
clans](http://drvinceknight.blogspot.fr/2014/05/wizards-giants-linear-programming-and.html)
I might annoy people again) and there is a [great
wiki](http://www.vaingloryfire.com/) that gives guides for the play of each
player. In this post I'll describe using Python to scrape that wiki to get data
that feeds in to a game theoretic model which I then analyse using
[Sagemath](http://www.sagemath.org/) to give some insight about the choice of
hero.

Here's the map where this all takes place:

![](http://22aeqb1ndrnn3j0r8k2b47j2.wpengine.netdna-cdn.com/wp-content/uploads/2014/11/Map.jpg)

So first of all, my understanding is that there are generally three types of
playing strategy in the game:

- Lane: a hero that occupies and tries to take over the main route between the
  two bases.
- Jungle: a hero that goes 'off road' and kills monsters, gets gold etc...
- Roam: a hero who roams in between the two and whose main job is to support the
  other two players.

My personal strategy is to pick a roamer/protector: Ardan (pic below),

![Ardan](http://www.gamezebo.com/wp-content/uploads/2015/02/ardan.jpg)

I generally help out the jungler in my team and try my best to not be a
liability by dying.

- Describe the wiki
- Show the scraping code and one of the payoff matrices for a single guide (not
  all guides have all players as threats)
- Show the best response graph for the all guides
- Describe NE: show some of the pure ones
- Show mean NE calculation and list players to play
- Show best response graph
- Highlight effect of choosing guides: number of equilibria, showing gifs

- Conclude: only looking at 16 by 16 game. Could be used to describe the best
  team and not the best 1 v 1. Axelrod.
