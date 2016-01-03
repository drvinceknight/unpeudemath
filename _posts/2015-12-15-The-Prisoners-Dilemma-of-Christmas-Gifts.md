---
layout     : post
title      : "The Dilemma of giving Christmas Gifts"
categories : code
tags       :
- python
- axelrod
- christmas
comments   : true
---

This post gives a game theoretic explanation as to why we exchange gifts. On
twitter [@alexip](https://twitter.com/alexip) tweeted ["'Let's agree not to give
each other presents for Christmas' is just another case of the prisoner's
dilemma #gametheory"](https://twitter.com/alexip/status/673573450036981762).
This post builds on that and investigates the premise fully in an evolutionary
context investigating different values of how good it feels to give and receive
a gift :)

[![Photo of alex's
tweet]({{site.baseurl}}/assets/images/tweet_about_xmas.png)](https://twitter.com/alexip/status/673573450036981762)

To illustrate this consider the situation where Alex and Camille are approaching
Christmas:

> Alex: How about we don't buy Christmas present for each other this year?

> Camille: Sounds great.

**Let us describe how this situation corresponds to a prisoner's dilemma.**

- If Alex and Camille **cooperate** and indeed keep their promise of not getting
  gifts than let us assume they both get a utility of \\(R\\) (_reward_).
- If Alex cooperates but Camille decides to **defect** and nonetheless give a
  gift then Alex will feel a bit bad and Camille will feel good, so Alex gets a
  utility of \\(S\\) (_sucker_) and Camille a utility of \\(T\\) (_temptation_).
- Vice versa if Camille cooperates but Alex decides to give a gift.
- If **both** Alex and Camille go against their promise then they both get a
  utility of \\(P\\) (_punishment_).

This looks something like:

![PD]({{site.baseurl}}/assets/images/prisonersdilemma.svg)

If we assume that we feel better when we give gifts and will be keen to 'cheat'
a promise of not giving then that corresponds to the following inequality of
utilities:

$$T > R > P > S$$

In this case we see that if Camille chooses to cooperate then Alex's __best
response__ is to play defect (as \\(T>R\\)):

> If Camille is indeed going to not give a gift, then Alex should give a gift.

**Also** if Camille chooses to defect then Alex's __best response__ is to defect
once again (as \\(P>S\\)):

> If Camille is going to 'break the promise' then Alex should give a gift.

**So no matter what happens: Alex should defect.**

In game theory this is what is called a dominating strategy, and indeed this
situation is referred to as a [Prisoner's
Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) and is what Alex
was referring to in his original tweet.

## How does reputation effect gift giving?

**So far all we are really modelling is a SINGLE exchange of gifts.**
If we were to exchange gifts every year we would perhaps learn to trust each
other, so that when Camille says they are not going to give a gift Alex has
reason to believe that they will indeed not do so.

This is called an **iterated Prisoner's dilemma** and has been the subject of a
great amount of academic work.

Let us consider two types of behaviour that Camille and Alex could choose to
exhibit, they could be:

- Alternator: give gifts one year and not give gifts the next.
- TitForTat: do whatever the other does the previous year.

Let us assume that Alex and Camille will be faced with this situation for 10
years. I'm going to use the Python [Axelrod
library](http://axelrod.readthedocs.org/en/latest/) to illustrate things:

{% highlight python %}
>>> import axelrod as axl
>>> alex, camille = axl.Alternator(), axl.TitForTat()
>>> match = axl.Match([alex, camille], 10)
>>> _ = match.play()
>>> print(match.sparklines(c_symbol='😀', d_symbol='🎁'))
😀🎁😀🎁😀🎁😀🎁😀🎁
😀😀🎁😀🎁😀🎁😀🎁😀
{% endhighlight %}

We see that Alex and Camille never actually exchange gifts the same year (the 😀
means that the particular player cooperates, the 🎁 that they don't and give a
gift).

Most of the ongoing Iterated Prisoner's Dilemma research is directly due to a
computer tournament run by [Robert Axelrod](http://www-personal.umich.edu/~axe/)
in the 1980s. In that work Axelrod invited a variety of computer strategies to
be submitted and they then played against each other. You can read more about
that here:
[axelrod.readthedocs.org/en/latest/reference/description.html](http://axelrod.readthedocs.org/en/latest/reference/description.html)
but the important thing is that there are a bunch of 'behaviours' that have been
well studied and that we will look at here:

1. Cooperator: never give gifts
2. Defector: always give gifts
3. Alternator: give gifts one year and not give gifts the next.
4. TitForTat: do whatever the other does the previous year.
5. TwoTitForTat: will start by not giving a gift but if the other player gives a
  gift will give a gift the next two years.
6. Grudger: start by not giving gifts but if at any time someone else goes
  against the promise: give a gift no matter what.

What we will now do is see how much utility (how people feel about their gift
giving behaviour) if we have a situation where 6 people exchange gifts for 50
years and each person acts according to one of the above behaviours.

For our utility we will use the following values of \\(R, P, S, T\\):

$$
R=3, P=1, S=0, T=5
$$

Here is how we can do this in python:

{% highlight python %}
>>> family = [axl.Cooperator(),
...           axl.Defector(),
...           axl.Alternator(),
...           axl.TitForTat(),
...           axl.TwoTitsForTat(),
...           axl.Grudger()]
>>> christmas = axl.Tournament(family, turns=50, repetitions=1)
>>> results = christmas.play()
>>> results.scores
[[525], [562], [417], [622], [646], [646]]
{% endhighlight %}

We see that the people that do the best are the last two: TwoTitForTat and
Grudger. These are people who are quick enough to react to people who won't
keep their promise but that do give hope to people who will!

## At a population level: evolution of gift giving

We can consider this in an evolutionary context where we see how the behaviour
is allowed to evolve amongst a whole population of people. This particular type
of game theoretic analysis is concerned not in micro interactions but long term
macro stability of the system.

Here is how we can see this using Python:

{% highlight python %}
>>> evo = axl.Ecosystem(results)
>>> evo.reproduce(100)
>>> plot = axl.Plot(results)
>>> plot.stackplot(evo)
{% endhighlight %}

![Basic Christmas
Evolution]({{site.baseurl}}/assets/images/basic_christmas_evo.svg)

What we see is that over time, the population evolves to only Cooperator,
TitForTat, Grudger and TwoTitsForTat, **but** of course in a population with
only those strategies everyone is keeping their promise, cooperating and __not
giving gifts__.

Let us see how this changes for different values of \\(R, P, S, T\\).

To check if not giving presents is evolutionary stable we just need to see what
the last population numbers are for the Alternator and Defector. Here is a Python function to do this:

{% highlight python %}
>>> def check_if_end_pop_cooperates(r=3, p=1, s=0, t=5,
...                                 digits=5, family=family, turns=10000):
...    """Returns a boolean and the last population vector"""
...    game = axl.Game(r=r, p=p, s=s, t=t)
...    christmas = axl.Tournament(family, turns=50, repetitions=1, game=game)
...    results = christmas.play()
...    evo = axl.Ecosystem(results)
...    evo.reproduce(turns)
...    last_pop = [round(pop, digits) for pop in evo.population_sizes[-1]]
...    return last_pop[1] == last_pop[2] == 0, last_pop
{% endhighlight %}

We see that for the default values of \\(R, P, S, T\\) we have:

{% highlight python %}
>>> check_if_end_pop_cooperates(r=3, p=1, s=0, t=5)
(True, [0.16576, 0.0, 0.0, 0.26105, 0.28659, 0.28659])
{% endhighlight %}

As already seen we have that for these values we end up with everyone keeping to the promise.
Let us increase the value of \\(T\\) by a factor of 100:

{% highlight python %}
>>> check_if_end_pop_cooperates(r=3, p=1, s=0, t=500)
(False, [0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
{% endhighlight %}

We here see, that if the utility of giving a gift when the receiver is not giving
one in return is very large, the overall population will always give a gift:

![Increasing t by factor of 100]({{site.baseurl}}/assets/images/t_factor_of_100_christmas_evo.svg)

## Seeing the effect of how good giving gifts makes us feel

The final piece of analysis I will carry out is a parameter sweep of the above:

- \\(5\leq T \leq 100\\)
- \\(3\leq R < T\\)
- \\(1\leq P < R\\)
- \\(0\leq S < P\\)

All of this data sweep is in [this csv
file]({{site.baseurl}}/assets/code/christmas.csv). Here is the distribution of
parameters for which everyone gives a gift (reneging on the promise):

![Parameters for kept
promise]({{site.baseurl}}/assets/images/parameters_for_which_gifts_are_not_given.svg)

Here is the distribution of parameters for which everyone keeps their promise
and does not give gifts:

![Parameters for kept
promise]({{site.baseurl}}/assets/images/parameters_for_which_gifts_are_given.svg)

We see that people keep their promise if the \\(T\\) utility (the utility of
being tempted to break the promise) is very high compared to all other
utilities.

Carrying out a simple logistic regression we see the coefficients of each of the variables as follows:

- \\(P\\): 3.121547
- \\(R\\): -2.942909
- \\(S\\): 0.007738
- \\(T\\): -0.107386

The parameters that have a positive effect on keeping the promise is \\(R\\) and
\\(S\\) which is the reward for the promise being kept and for not giving a gift
but receiving one.

## TLDR

Agreeing to not give gifts at Christmas can be an evolutionary stable strategy,
but this is only in the specific case where the utility of 'giving' is less than
the utility of 'not giving'. **Given that in practice this promise is almost always broken
(that's my personal experience anyway) this would suggest that people enjoy
giving gifts a lot more than receiving them.**

**Merry christmas 🎄🎁⛄️.**

---

- [Jupyter notebook to produce graphics for
  this](https://github.com/drvinceknight/unpeudemath/tree/gh-pages/assets/code/prisoners_dilemma_of_giving_gifts.ipynb)
- [Python script to carry out parameter
  sweep]({{site.baseurl}}/assets/code/generate_christmas_data.py)
- [The Axelrod library](http://axelrod.readthedocs.org/en/latest/)
