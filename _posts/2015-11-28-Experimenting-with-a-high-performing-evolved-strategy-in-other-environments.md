---
layout     : post
title      : "Survival of the fittest: Experimenting with a high performing strategy in other environments"
categories : gametheory
tags       :
- axelrod
- python
- evolution
comments   : true
---

[A common misconception about evolution is that "The fittest organisms in a
population are those that are strongest, healthiest, fastest, and/or
largest."](http://evolution.berkeley.edu/evolibrary/misconceptions_faq.php#b5)
However, as that link indicates, survival of the fittest is implied at the
genetic level: and implies that evolution favours genes that are most able to
continue in the next generation for a given environment. In this post, I'm going
to take a look at a high performing strategy from the Iterated Prisoner's
dilemma that was obtained through an evolutionary algorithm. I want to see how
well it does in other environments.

## Background

This is all based on the [Python Axelrod
package](http://axelrod.readthedocs.org/en/latest/) which makes iterated
prisoner dilemma research straightforward and **really** is just taking a look
at [Martin Jones's blog
post](http://mojones.net/evolving-strategies-for-an-iterated-prisoners-dilemma-tournament.html)
which described the evolutionary analysis performed to get a strategy (`EvolvedLookerUp`) that is
currently winning the overall tournament for the Axelrod library (with 108
strategies):

![Results from overall
tournament](https://camo.githubusercontent.com/04c9d74a5878e24e8da3c985ea393b5ee7439b3b/687474703a2f2f6178656c726f642d707974686f6e2e6769746875622e696f2f746f75726e616d656e742f6173736574732f737472617465676965735f626f78706c6f742e737667)

The strategy in question is designed to do exactly that and as you can see does
it really well (with a substantial gap between it's median score and the runner
up: `DoubleCrosser`).

There are some things lacking in the analysis I'm going to present (which
strategies I'm looking at, number of tournaments etc...) but hopefully the
numerical analysis is still interesting. In essence I'm taking a look at the
following question:

> If a strategy is good in a big environment, how good is it in any given
> environment?

From an evolutionary point of view this is kind of akin to seeing how good a
predator a shark would be in any random (potentially land based) environment...

## Generating the data

Thanks to the Axelrod, library it's pretty straightforward to quickly experiment
with a strategy (or group of strategies) in a random tournament:

{% highlight python %}
import axelrod as axl  # Import the axelrod library

def rank(strategies, test_strategies, repetitions=10, processes=None):
    """Return the rank of the test_strategy in a tournament with given
    strategiess"""
    for s in test_strategies:
        strategies.append(s())
    nbr = len(test_strategies)
    tournament = axl.Tournament(strategies,
                                repetitions=repetitions,
                                processes=processes)
    results = tournament.play()
    return results.ranking[-nbr:], results.wins[-nbr:]
{% endhighlight %}

This runs a tournament and returns the rankings and wins for the input
strategies. For example, let's see how `Cooperator` and `Defector` do in a
random tournament with 2 other strategies:

{% highlight python %}
>>> import axelrod as axl
>>> import random
>>> random.seed(1)  # A random seed
>>> strategies = random.sample([s() for s in axl.strategies], 2)
>>> strategies  # Our 2 random strategies
[Tricky Defector, Prober 3]
{% endhighlight %}

We can then use the above function to see how `Cooperator` and `Defector` do:

{% highlight python %}
>>> rank(strategies, [axl.Cooperator(), axl.Defector()])
([3, 2], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
{% endhighlight python %}

We see that cooperator ranks last (getting no wins), and defector just before last (getting 2 wins). This is confirmed by the actual tournament results:

![]({{site.baseurl}}/assets/images/small_tournament_boxplot.svg)
![]({{site.baseurl}}/assets/images/small_tournament_winplot.svg)

The idea is to reproduce the above for a variety of tournament sizes, repeating
random samples for each size and looking at the wins and ranks for the
strategies we're interested in.

This script generates our data:

{% highlight python %}
import axelrod as axl
import csv
import random
import copy

max_size = 25  # Max size of tournaments considered (maximum size of the sample)
tournaments = 20  # Number of tournaments of each size to run (number of samples)
repetitions = 10  # Number of repetitions of each tournament (for a given sample)

test_strategies = [axl.EvolvedLookerUp, axl.TitForTat, axl.Cooperator, axl.Defector, axl.DoubleCrosser]
strategies = [s() for s in axl.strategies if axl.obey_axelrod(s) and s not in test_strategies]

def rank(strategies, test_strategies=test_strategies, repetitions=10, processes=None):
    """Return the rank of the test_strategy in a tournament with given
    strategiess"""
    for s in test_strategies:
        strategies.append(s())
    nbr = len(test_strategies)
    tournament = axl.Tournament(strategies, repetitions=repetitions, processes=processes)
    results = tournament.play()
    return results.ranking[-nbr:], results.wins[-nbr:]

f = open('combined-data', 'w')
csvwrtr = csv.writer(f)
f_lookerup = open('data-lookerup.csv', 'w')
csvwrtr_lookerup = csv.writer(f_lookerup)
f_titfortat = open('data-titfortat.csv', 'w')
csvwrtr_titfortat = csv.writer(f_titfortat)
f_cooperator = open('data-cooperator.csv', 'w')
csvwrtr_cooperator = csv.writer(f_cooperator)
f_defector = open('data-defector.csv', 'w')
csvwrtr_defector = csv.writer(f_defector)
f_doublcrosser = open('data-doublecrosser.csv', 'w')
csvwrtr_doublcrosser = csv.writer(f_doublcrosser)

data = []
ind_data = [[], [], [], [], []]


for size in range(1, max_size + 1):

    row = [size]
    ind_row = [copy.copy(row) for _ in range(5)]

    for k in range(tournaments):

        s = random.sample(strategies, size)
        strategy_labels = ";".join([str(st) for st in s])

        trnmt_s = copy.copy(s)
        results = rank(copy.copy(s), test_strategies=test_strategies, repetitions=repetitions)
        row.append([strategy_labels, results[0]] + results[1])
        for i, ts in enumerate(test_strategies):
            trnmt_s = copy.copy(s)
            results = rank(copy.copy(s), test_strategies=[ts], repetitions=repetitions)
            ind_row[i].append([strategy_labels, results[0]] + results[1])



    data.append(row)
    csvwrtr.writerow(row)

    csvwrtr_lookerup.writerow(ind_row[0])

    csvwrtr_titfortat.writerow(ind_row[1])

    csvwrtr_cooperator.writerow(ind_row[2])

    csvwrtr_defector.writerow(ind_row[3])

    csvwrtr_doublcrosser.writerow(ind_row[4])

f.close()
f_lookerup.close()
f_titfortat.close()
f_cooperator.close()
f_defector.close()
f_doublcrosser.close()
{% endhighlight %}

The above creates tournaments up to a size of 25 other strategies, with 20 random tournaments for each size, creating six data files:

- [Data for tournaments with a random strategy sample and `EvolvedLookerUp`]({{site.baseurl}}/assets/code/data-lookerup.csv)
- [Data for tournaments with the random strategy sample and `TitForTat`]({{site.baseurl}}/assets/code/data-titfortat.csv)
- [Data for tournaments with the random strategy sample and `Cooperator`]({{site.baseurl}}/assets/code/data-cooperator.csv)
- [Data for tournaments with the random strategy sample and `Defector`]({{site.baseurl}}/assets/code/data-defector.csv)
- [Data for tournaments with the random strategy sample and `DoubleCrosser`]({{site.baseurl}}/assets/code/data-doublecrosser.csv)
- [Data for tournaments with the random strategy sample as well as the above strategies]({{site.baseurl}}/assets/code/combined-data)

## Analysing the data

I then used [this JuPyTer notebook](https://github.com/drvinceknight/unpeudemath/blob/gh-pages/assets/code/Experimenting_with_the_evolved_lookerup.ipynb) to analyse the data.

Here is what we see for the `EvolvedTitForTat` strategy:

![]({{site.baseurl}}/assets/images/rank-lookerup.svg)
![]({{site.baseurl}}/assets/images/wins-lookerup.svg)

The line is fitted to the median rank and number of wins (recall for each
number of strategies, 20 different sampled tournaments are considered) We see
that (as expected) as the number of strategies increases both the median rank
and wins increases, **but what is of interest** is the rate at which that increase happens.

Below is the fitted lines for all the considered strategies:

![]({{site.baseurl}}/assets/images/rank-regression.svg)
![]({{site.baseurl}}/assets/images/wins-regression.svg)

Here are the fits (and corresponding plots)  for the ranks:

- `EvolvedLookerUp`: \\(y=0.49x-0.10\\) [plot]({{site.baseurl}}/assets/images/rank-lookerup.svg)
- `TitForTat`: \\(y=0.53-0.45\\) [plot]({{site.baseurl}}/assets/images/rank-titfortat.svg)
- `Cooperator`: \\(y=0.42x+1.40\\) [plot]({{site.baseurl}}/assets/images/rank-cooperator.svg)
- `Defector`: \\(y=0.75x-0.33\\) [plot]({{site.baseurl}}/assets/images/rank-defector.svg)
- `DoubleCrosser`: \\(y=0.51x-0.47\\) [plot]({{site.baseurl}}/assets/images/rank-doublecrosser.svg)

Here are the fits (and corresponding plots) for the wins:

- `EvolvedLookerUp`: \\(y=0.28x+0.06\\) [plot]({{site.baseurl}}/assets/images/wins-lookerup.svg)
- `TitForTat`: \\(y=0.00x+0.00\\) [plot]({{site.baseurl}}/assets/images/wins-titfortat.svg)
- `Cooperator`: \\(y=0.00x+0.00\\) [plot]({{site.baseurl}}/assets/images/wins-cooperator.svg)
- `Defector`: \\(y=0.89x+0.14\\) [plot]({{site.baseurl}}/assets/images/wins-defector.svg)
- `DoubleCrosser`: \\(y=0.85-0.10\\) [plot]({{site.baseurl}}/assets/images/wins-doublecrosser.svg)

**It seems that the `EvolvedLookerUp` strategy does continue to do well (with a
low coefficient of 0.49) in these random environments**. However what's
interesting is that the simple `Cooperator` strategy also seems to do well
(this might indicate that the random samples are creating 'overly nice'
conditions).

**All of the above keeps the 5 strategies considered separated from each, here
is the analysis repeated when combining the strategies with the random
sample:**

![]({{site.baseurl}}/assets/images/rank-combined-lookerup.svg)
![]({{site.baseurl}}/assets/images/wins-combined-lookerup.svg)

Below is the fitted lines for all the considered strategies:

![]({{site.baseurl}}/assets/images/combined-rank-regression.svg)
![]({{site.baseurl}}/assets/images/combined-win-regression.svg)

Here are the fits (and corresponding plots)  for the ranks:

- `EvolvedLookerUp`: \\(y=0.42x+2.05\\) [plot]({{site.baseurl}}/assets/images/rank-combined-lookerup.svg)
- `TitForTat`: \\(y=0.44+1.95\\) [plot]({{site.baseurl}}/assets/images/rank-combined-titfortat.svg)
- `Cooperator`: \\(y=0.64+0.00\\) [plot]({{site.baseurl}}/assets/images/rank-combined-cooperator.svg)
- `Defector`: \\(y=0.47x+1.87\\) [plot]({{site.baseurl}}/assets/images/rank-combined-defector.svg)
- `DoubleCrosser`: \\(y=0.63x+1.88\\) [plot]({{site.baseurl}}/assets/images/rank-combined-doublecrosser.svg)

Here are the fits (and corresponding plots) for the wins:

- `EvolvedLookerUp`: \\(y=0.28x+0.05\\) [plot]({{site.baseurl}}/assets/images/wins-combined-lookerup.svg)
- `TitForTat`: \\(y=0.00x+0.00\\) [plot]({{site.baseurl}}/assets/images/wins-combined-titfortat.svg)
- `Cooperator`: \\(y=0.00x+0.00\\) [plot]({{site.baseurl}}/assets/images/wins-combined-cooperator.svg)
- `Defector`: \\(y=0.89x+4.14\\) [plot]({{site.baseurl}}/assets/images/wins-combined-defector.svg)
- `DoubleCrosser`: \\(y=0.85+2.87\\) [plot]({{site.baseurl}}/assets/images/wins-combined-doublecrosser.svg)

## Conclusion

**It looks like the `EvolvedLookerUp` strategy continues to perform well in
environments that are not the ones it evolved in.**

The Axelrod library makes this analysis possible as you can quickly create
tournaments from a wide library of strategies. You could also specify the
analysis further by considering strategies of a particular type. For example
you could sample only from strategies that act deterministically (no random
behaviour):

{% highlight python %}
>>> strategies = [s() for s in axl.strategies if not s().classifier['stochastic']]
{% endhighlight %}

It would probably be worth gathering even more data to be able to make
substantial claims about the performances as well as
considering other test strategies but ultimately this gives some insight in to
the performances of the strategies in other environments.

## For fun

The latest release of the library
([v0.0.21](https://pypi.python.org/pypi/Axelrod)) includes the ability to [draw
sparklines](http://axelrod.readthedocs.org/en/latest/tutorials/further_topics/creating_matches.html)
that give a visual representation of the interactions between pairs of
strategies. If you're running python 3 you can include emoji so here goes the
sparklines for the test strategies considered:

{% highlight python %}
>>> from itertools import combinations

>>> test_strategies = [axl.EvolvedLookerUp, axl.TitForTat, axl.Cooperator, axl.Defector, axl.DoubleCrosser]
>>> matchups = [(match[0](), match[1]()) for match in combinations(test_strategies, 2)]

>>> for matchup in matchups:
....    match = axl.Match(matchup, 10)
....    _ = match.play()
....    print(matchup)
....    print(match.sparklines(c_symbol=' 😀 ', d_symbol=' 😡 '))
...
(EvolvedLookerUp, Tit For Tat)
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
(EvolvedLookerUp, Cooperator)
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
(EvolvedLookerUp, Defector)
 😀  😀  😡  😡  😡  😡  😡  😡  😡  😡
 😡  😡  😡  😡  😡  😡  😡  😡  😡  😡
(EvolvedLookerUp, DoubleCrosser)
 😀  😀  😡  😡  😀  😀  😀  😀  😀  😀
 😀  😡  😡  😡  😡  😡  😡  😡  😡  😡
(Tit For Tat, Cooperator)
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
(Tit For Tat, Defector)
 😀  😡  😡  😡  😡  😡  😡  😡  😡  😡
 😡  😡  😡  😡  😡  😡  😡  😡  😡  😡
(Tit For Tat, DoubleCrosser)
 😀  😀  😡  😡  😡  😡  😡  😡  😡  😡
 😀  😡  😡  😡  😡  😡  😡  😡  😡  😡
(Cooperator, Defector)
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
 😡  😡  😡  😡  😡  😡  😡  😡  😡  😡
(Cooperator, DoubleCrosser)
 😀  😀  😀  😀  😀  😀  😀  😀  😀  😀
 😀  😡  😡  😡  😡  😡  😡  😡  😡  😡
(Defector, DoubleCrosser)
 😡  😡  😡  😡  😡  😡  😡  😡  😡  😡
 😀  😡  😡  😡  😡  😡  😡  😡  😡  😡
{% endhighlight %}

