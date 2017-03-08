---
layout     : post
title      : "A simple evolutionary process in 40 lines of Python"
categories : mathematics
tags       :
- python
- game theory
comments   : true
---

At [PyCon Namibia](https://na.pycon.org/en/) I gave a talk entitled **Rock,
Paper, Scissors, Lizard, Spock with Python**. I spoke about how it's easy to
compute equilibria of 2 player games with
[Nashpy](https://github.com/drvinceknight/Nashpy) but also spoke a bit about
evolutionary stability. In this blog post I'll go over how you can model a
simple evolutionary process using about 40 lines of Python + Numpy.

The first game I talked about was the [Travellers
Dilemma](https://en.wikipedia.org/wiki/Traveler's_dilemma). Here is a reduced
version of it:

$$
\begin{pmatrix}
2,2&4,0&4,0\\
0,4&3,3&5,1\\
0,4&1,5&4,4
\end{pmatrix}
$$

I won't go in to too much detail about what that game is modelling for now but
the "important" thing to understand at this stage is that we have two players:

1. The row player: chooses which row we are in;
2. The column player: chooses which column we are in.

So if the row player chooses the second row and the column player chooses the
3rd column the scores would be: \\(5, 1\\). The row player getting 5 and the
column player getting 1. It would be in the column players interest to change
the column to the first column (the scores would then be \\(0, 4\\).

We can use Nashpy to compute the equilibria of this game:

```python
>>> td = (np.array([[2, 4, 4],
...                [0, 3, 5],
...                [0, 1, 4]]),
...      np.array([[2, 0, 0],
...                [4, 3, 1],
...                [4, 5, 4]]))
>>> game = nash.Game(*td)
>>> list(game.equilibria())
[(array([ 1.,  0.,  0.]), array([ 1.,  0.,  0.]))]

```

We see that the Nash equilibria is a single collection of two vectors saying
how both players should play:

1. The row player should play `[1, 0, 0]`
2. The column player should (also) play `[1, 0, 0]`

Here `[1, 0, 0]` denotes a probability vector saying the probability with which
a player should play a given strategy. So in this case both players should pick
their first option which gives us a score of \\(2, 2\\). This is called a Nash
equilibrium because at this position neither player has a reason to deviate (if
they did their scores would go down).

We can also model [Rock, Paper,  Scissors, Lizard,
Spock](http://bigbangtheory.wikia.com/wiki/Rock_Paper_Scissors_Lizard_Spock)
this way. Here is the game in mathematical form:

$$
\begin{pmatrix}
0,0 & -1,1 & 1,-1 & 1,-1 & -1,1\\
1,-1 & 0,0 & -1,1 & -1,1 & 1,-1\\
-1,1 & 1,-1 & 0,0 & 1,-1 & -1,1\\
-1,1 & 1,-1 & -1,1 & 0,0 & 1,-1\\
1,-1 & -1,1 & 1,-1 & -1,1 & 0,0
\end{pmatrix}
$$

Let's see what the Nash equilibria are:

```python
>>> rpsls = np.array([[0, -1, 1, 1, -1],
...                   [1, 0, -1, -1, 1],
...                   [-1, 1, 0, 1, -1],
...                   [-1, 1, -1, 0, 1],
...                   [1, -1, 1, -1, 0]])
>>> rpsls = (rpsls, -rpsls)
>>> game = nash.Game(*rpsls)
>>> list(game.equilibria())
[(array([ 0.2,  0.2,  0.2,  0.2,  0.2]),
  array([ 0.2,  0.2,  0.2,  0.2,  0.2]))]

```

We here see that both players should play perfectly randomly: playing each
option with exactly 1/5 probability. This makes intuitive sense because when
both players do this they are in effect unpredictable.

That's all fair and good and Nash equilibria is a very powerful and important
solution concept in Game Theory but what would happen if we used these games as
a basis for evolution?

What if we had a large population with individuals that always choose the same
of the many options available to them. They each played against a member of
another large population and if they don't get a worse score than their
opponent they carry on. If they **do get a lower score** than their opponent
they they start doing what their opponent was doing.

Here is how that can be done with Python and Numpy.

First: get a random population:

```python
>>> def get_population(number_of_strategies, size=50):
...     """
...     Obtain a random population of strategies for a game.
...     """
...     population = np.random.randint(0, number_of_strategies, size)
...     return population
>>> np.random.seed(0)
>>> population = get_population(3, 10)
>>> population
array([0, 1, 0, 1, 1, 2, 0, 2, 0, 0])

```

Now let's play a given game:

```python
>>> def get_scores(population, opponents, game):
...     """
...     Score all the strategies
...     """
...     return [(game[0][i, j], game[1][i, j])
...             for i, j in zip(population, opponents)]
>>> opponents =  get_population(3, 10)
>>> scores = get_scores(population, opponents, td)
>>> scores
[(2, 2),
 (5, 1),
 (4, 0),
 (5, 1),
 (5, 1),
 (0, 4),
 (4, 0),
 (1, 5),
 (4, 0),
 (4, 0)]

```

Now for the mutation (where we simply swap what a given individual does if they were beaten):

```python
>>> def mutate(scores, population, opponents):
...     """
...     Mutate the strategies, this is a naive approach:
...     if a strategy was beaten it mutates to its opponent.
...     """
...     mutated_population = []
...
...     for score, strategy_pair in zip(scores, zip(population, opponents)):
...
...         if score[1] >= score[0]:
...             mutated_population.append(strategy_pair[1])
...         else:
...             mutated_population.append(strategy_pair[0])
...
...     return np.array(mutated_population)
>>> mutate(scores, population, opponents)
array([2, 0, 2, 1, 0, 0, 0, 1, 1, 0])

```

Finally let's put all this together, we play for a given number of generations
and repeat the mutation process:

```python
>>> def evolve(game, size, generations):
...     """
...     Evolve a population of strategies.
...     """
...     population = get_population(len(game[0]), size)
...     opponents = get_population(len(game[0]), size)
...
...     history = [population]
...
...     for _ in range(generations):
...         scores = get_scores(population, opponents, game)
...         population = mutate(scores, population, opponents)
...         opponents = get_population(len(game[0]), size)
...         history.append(population)
...
...     return history

```

Now let's see what plots of these look like ([here is a Jupyter notebook with
all of
this](http://vknight.org/Talks/2017-02-23-Rock-Paper-Scissors-Lizard-Spock-With-Python/demo.ipynb):

First let's take a look at what happens when we play the Travellers Dilemma
(recall the Nash equilibria is to all play the first strategy):

![Plot of evolutionary process for travellers dilemma]({{site.baseurl}}/assets/images/travellers_dilemma_evo.svg).

We see that the very soon the population is entirely full of players playing
the first strategy. This could of course be an artefact of the particular
random seed we're using. Here is a collection of the same graph for different
starting seeds:

![Multiple seeds for travellers dilemma](http://vknight.org/Talks/2017-02-23-Rock-Paper-Scissors-Lizard-Spock-With-Python/static/td_16.svg)

They're all different but we see the same conclusion: the population is overrun
with individuals playing the Nash equilibrium strategy.

**But here's the cool part**, let's see what things look like when we plot the
generations for Rock Paper Scissors Lizard Spock:

![Plot of evolutionary process for rpsls]({{site.baseurl}}/assets/images/rpsls_evo.svg).

We see that this seems to be much more unstable! Here's the plot showing that
it's not dependant on the seed:

![Multiple seeds for rpsls](http://vknight.org/Talks/2017-02-23-Rock-Paper-Scissors-Lizard-Spock-With-Python/static/rpsls_16.svg)

This difference in stability has an intuitive explanation: the Nash equilibrium
strategy in the Prisoner's dilemma is very strong: if everyone is doing that
then we do not have a reason to change and we will only ever meet people doing
that. For Rock, Paper, Scissors, Lizard, Spock if everyone is playing randomly,
or if the population is made up of a random combination of people player either
strategy then you risk to bump in to someone you will lose against.

There are two conclusions to take from this:

1. This is straightforward to do using Python :)
2. Population dynamics add a fascinating dimension to game theory. The
   evolutionary process I'm using here is **very** naive, in general these
   things are studied using [Moran
   Processes](https://en.wikipedia.org/wiki/Moran_process). You can actually use
   a Python library to study these in the context of the Prisoner's dilemma:
   [axelrod.readthedocs.io/en/latest/tutorials/getting_started/moran.html](http://axelrod.readthedocs.io/en/latest/tutorials/getting_started/moran.html)

Here are the resources from my talk at [PyCon
Namibia](https://na.pycon.org/en/):

- [Jupyter notebook](http://vknight.org/Talks/2017-02-23-Rock-Paper-Scissors-Lizard-Spock-With-Python/demo.ipynb)
- [Conda environment
  file](http://vknight.org/Talks/2017-02-23-Rock-Paper-Scissors-Lizard-Spock-With-Python/environment.yml)
- [Slides](http://vknight.org/Talks/2017-02-23-Rock-Paper-Scissors-Lizard-Spock-With-Python/index.html)

Finally, if you'd like to see some great photos from the conference you can see
them here:
[www.flickr.com/photos/phoenix-project/sets/72157680441007095/with/32934148716/](https://www.flickr.com/photos/phoenix-project/sets/72157680441007095/with/32934148716/)
