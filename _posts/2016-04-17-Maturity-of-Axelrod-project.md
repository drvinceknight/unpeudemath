---
layout     : post
title      : "The Axelrod project is over a year old"
categories : code
tags       :
- python
- gametheory
- axelrod
comments   : true
---

Over the past month or so, various cool things have happened with the Axelrod
project. As well as a variety of cool and clever internal improvements you can
now use it to run Probabilistic ending tournaments and also Moran Processes.
There is also [now a preprint on the arXiv](http://arxiv.org/abs/1604.00896)
presenting the library as a research tool. This felt like it all came together
as a bit of a milestone so I'm writing this blog post to briefly discuss those 3
things and also reflect on the development of library itself.

### Probabilistic Ending Tournaments

So first of all, it's now possible to create tournaments where each match
between players is not of a constant length but has a given probability of
ending after each repetition. You can read the [full documentation about
it](http://axelrod.readthedocs.org/en/latest/tutorials/further_topics/probabilistict_end_tournaments.html)
but here is a brief example of how to run this:

```python
>>> import axelrod as axl
>>> players = [axl.Cooperator(), axl.TitForTat(), axl.Grudger()]
>>> tournament = axl.ProbEndTournament(players, prob_end=0.5)
>>> results = tournament.play()
```

As well as getting the usual set of results it's possible to see a plot of the
lengths of each match:

```python
>>> plot = axl.Plot(results)
>>> p = plot.boxplot()
>>> p.show()
```

![]({{site.baseurl}}/assets/images/prob_end_lengthplot.svg)

This is an addition to the library that I'm particularly happy to see. [I run
probabilistic ending tournaments in class when looking at infinitely repeated
games](http://vknight.org/unpeudemath/pedagogy/2015/03/08/playing-an-infinitely-repeated-game-in-class.html). I'll probably use this as a demonstration tool in class.

For example, below is the results for the above, with a probability of the Match
ending being high: \\(p=.5\\).

![]({{site.baseurl}}/assets/images/prob_end_boxplot.svg)

We see that the `Defector` strategy does much better (far higher utility) than
the other strategies. Below are the results when \\(p=.001\\): the chance of
Match ending is very low, in other words the reputation of a player is of higher
importance.

![]({{site.baseurl}}/assets/images/prob_end_boxplot_low_prob_end.svg)

As reputation has a higher importance the `Defector` does no longer do as well
and cooperative strategies do better.

### Moran Processes

Another cool addition is something I don't actually know much about: [Moran
Processes](https://en.wikipedia.org/wiki/Moran_process). These mimic an
evolutionary process: following all players being matched up, and randomly
chosen (according to a distribution based on their performance) to
"reproduce"/"die". As for the probabilistic ending, [you can read the
documentation for
this](http://axelrod.readthedocs.org/en/latest/tutorials/getting_started/moran.html)
but here is a little demonstration (using the same strategies as above):

```python
>>> import random
>>> random.seed(1)  # This is a random process
>>> players = [axl.Cooperator(), axl.TitForTat(), axl.Grudger()]
>>> mp = axl.MoranProcess(players)
>>> populations = mp.play()
```

The `populations` variable contains lists of counters of the population. The
process ends when there is only a single strategy left in the population:

```python
>>> populations
[Counter({'Cooperator': 1, 'Grudger': 1, 'Tit For Tat': 1}),
 Counter({'Cooperator': 2, 'Tit For Tat': 1}),
 Counter({'Cooperator': 2, 'Tit For Tat': 1}),
 Counter({'Cooperator': 2, 'Tit For Tat': 1}),
 Counter({'Cooperator': 1, 'Tit For Tat': 2}),
 Counter({'Cooperator': 1, 'Tit For Tat': 2}),
 Counter({'Cooperator': 1, 'Tit For Tat': 2}),
 Counter({'Tit For Tat': 3})]
```

This process is studied extensively in the literature and will hopefully
further contribute to the use of the library as a research tool.

### An open reproducible framework for the study of the iterated prisoner's dilemma

That is the title of a paper that has been submitted to the [Jounral of Open
Research Software](http://openresearchsoftware.metajnl.com/). You can see a
preprint of it [on the arXiv](http://arxiv.org/abs/1604.00896). One of the
cool things for this paper is that we there is a long list of
authors: 20 people who contributed code are going to 'get credit': this was the
particular them of [Sustainable Software Institute collaborations
workshop](http://www.software.ac.uk/cw16) I attended last month.

### Reflecting on development/research done this way

The work the entire set of contributors (25 at the moment of writing) has done
is really awesome. A **completely personal highlight** has been working with
the 3 other core developers on this: [Owen
Campbell](https://github.com/meatballs), [Marc Harper](,
and://github.com/marcharper) and [Karol Langner](https://github.com/langner).

Karol was the one who suggested (a while back):

> "[...] if you are interested in giving the thing a life of its own, you should
consider creating a dedicated organization:"

This was frankly, the best decision as far as the project was concerned. It's
meant that the decision making was not purely my own and the project has indeed
'had a life of its own'. Open discussions with a sole goal of making the right
decision.

We often disagree. We often disagree in a completely open way: using the github
issues to keep track of the discussions. What's great about our disagreements
is: they are always polite and respectful, I'm now a
contributor to a couple of other open source projects, some of which I will
think twice about suggesting my students join in as they're simply not nice
environments.  What's great about our disagreements is that we each have
the same end goal, making the software as good as we can.

I certainly have been lucky to do research with the same attitude towards
disagreements but this does feel different for some reason... I'm not sure what.

Another great aspect about the Axelrod project is that it's been done
completely in the open. So the reach of the expertise is not just a single
person or perhaps two. A great example of this is the two current best
performing strategies which have been trained with a [genetic
algorithm](http://mojones.net/evolving-strategies-for-an-iterated-prisoners-dilemma-tournament.html)
and a [particle swam
algorithm](https://gist.github.com/GDKO/60c3d0fd423598f3c4e4). This is not a
thing that I would have gone towards for years, but being completely open has
meant that someone could come in and make progress. The work comes first.

Finally: github. Github, issues and the various integrations have been
fantastic for this. I expect this is nothing new to the software engineering
community but I now use this for all my work.
