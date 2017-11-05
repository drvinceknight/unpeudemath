---
layout     : post
title      : "The effect of goats (on the Monty hall problem)"
categories : math
tags       :
- python
- math
- education
comments   : true
---

I've just written a 3 page example coursework submission as a demo for my first
year students. This is for a course called "Computer for Mathematics" which aims
to introduce mathematics students to programming techniques useful to
mathematicians (in Python). The particular example I chose to write about is one 
(of many
possibly) generalisation of the [Monty Hall
problem](https://en.wikipedia.org/wiki/Monty_Hall_problem). I'm rewriting what I
did here in case it's of interest to anyone.

The Monty hall problem is a lovely probabilistic problem which kept/keeps many people
puzzled. I still remember running up the stairs to speak to my first year
probability lecturer who assured me that there wasn't a mistake. The idea is the
following:

1. There are 3 doors: behind one of the doors is a car, behind the others:
   goats.
2. A game show contestant chooses a door.
3. The host then opens one of the two remaining doors to show where one of the
   goats is. Depending on the original chose of the contestant this could be the
   only remaining goat (if their choice is a goat) or one of the two remaining 
   goats (if their choice is a car).
4. The contestant is then asked if they want to swap their choice to the one
   remaining door or stick.

The reason this is puzzling is because at first it seems that there should not
be an affect of switching: the probability of winning should be the same. Right?

Wrong :)

In fact: the contestant's chance of winning is doubled if they switch.

In this blog post I'll explore what happens when we have more than just 2 goats,
with everything else staying as is (the host open just one of the remaining
doors).

## Simulating both strategies with Python

First of all here is a simple stochastic simulation to compute the
probabilities:

```python
>>> import random

>>> def stick(number_goats=2):
...     """A function to simulate a play of the game when we stick"""
...     doors = ['Car'] + number_goats * ['Goat']
...         
...     initial_choice = random.choice(doors)  # make a choice
...     return initial_choice == 'Car'

>>> def switch(number_goats=2):
...     """A function to simulate a play of the game when we swap"""
...     doors = ['Car'] + number_goats * ['Goat']  
...     
...     initial_choice = random.choice(doors)  # make a choice
...     
...     doors.remove(initial_choice)  # Switching: remove initial choice
...     doors.remove('Goat')  # The game show host shows us a goat
...     
...     new_choice = random.choice(doors)   # We choose our one remaining option
...             
...     return new_choice == 'Car'

```

We can then use the above to simulate the probabilities when using 2 goats (like
in the original game):

```python
>>> repetitions = 10000
>>> random.seed(0)
>>> prob_win_stick = sum([stick() for rep in range(repetitions)]) / repetitions
>>> prob_win_switch = sum([switch() for rep in range(repetitions)]) / repetitions
>>> prob_win_stick, prob_win_switch
(0.3346, 0.6636)

```

We can compute a probability of winning when switch in the case of \\(n\\) goats
(so \\(n + 1\\) total doors). In order to win when switching, two things need to
happen:

1. The original choice of the contestant must **not** contain the car (as they
   are going to switch). The probability of picking the car originally is given
   by \\(\frac{1}{n + 1}\\) thus not choosing the car has probability \\(1 -
   \frac{1}{n + 1}\\).
2. The swap to one of the random remaining doors must choose the car. After the
   host has shown one of the goats there are \\(n - 1\\) doors from which to
   choose, thus a switch will choose the car with probability 
   \\(\frac{1}{n - 1}\\). Note that in the case of \\(n = 2\\) 
   (the original game show) this probability is 1 which I suggest is why this is
   puzzling.

So the probability of winning when switching is given by:

$$
p_n = \left(1 - \frac{1}{n + 1}\right)\left(\frac{1}{n - 1}\right)
$$

Let us use Python's symbolic mathematics package to clear this up:

```python
>>> import sympy as sym
>>> n = sym.symbols('n')
>>> p_n = (1 - 1 / (n + 1)) * (1 / (n - 1))
>>> p_n.simplify()
n/(n**2 - 1)

```

This probability in itself is not what we're interested in here, lets see how
much better switching is compared to sticking. We know that the probability of
winning when we stick is given by \\(\frac{1}{n + 1}\\) thus the ratio is:

$$
\alpha_n = \frac{\frac{n}{n ^2 - 1}}{\frac{1}{n + 1}} = \frac{n}{n - 1}
$$

Again verifiable using Sympy:


```python
>>> (p_n / (1 / (n + 1))).simplify()
n/(n - 1)
```

Let us simulate this:

```python
>>> def ratio(repetitions=50000, number_goats=2):
...     """Obtain the ratio of win probabilities"""
...     prob_win_stick = sum([stick(number_goats=number_goats) 
...                           for rep in range(repetitions)]) / repetitions
...     prob_win_switch = sum([switch(number_goats=number_goats) 
...                            for rep in range(repetitions)]) / repetitions
...     return prob_win_switch / prob_win_stick 

```

And draw a plot:

```python
>>> import matplotlib.pyplot as plt
>>> random.seed(0)
>>> goats = range(2, 25 + 1)
>>> ratios = [ratio(number_goats=n) for n in goats]
>>> theoretic_ratio = [(n / (n - 1)) for n in goats]
>>> plt.figure()
>>> plt.scatter(goats, ratios, label="simulated")
>>> plt.plot(goats, theoretic_ratio, color="C1", label="theoretic")
>>> plt.xlabel("Number of goats")
>>> plt.ylabel("Ratio")
>>> plt.legend()
>>> plt.savefig("monty_hall_effect_of_goats.svg");

```

![]({{site.baseurl}}/assets/images/monty_hall_effect_of_goats.svg)

The plot clearly shows that as the number of goats goes up, switching has less 
and less of an advantage:

- The effect of revealing a goat becomes insignificant as the number of goats
  grows;
- The version with 2 goats is the one where the advantage of switching is at
  it's highest. This is due to the fact that upon switching (in a conditional
  probabilistic sense) there is just one door to choose from which will either
  have a goat or the car.

In the coursework example I've written for my students I complement this with a
limit calculation of the ratio (as \\(n\to\infty\\)) which can be verified using
Sympy:

```python
>>> sym.limit((p_n / (1 / (n + 1))), n, sym.oo)
1

```
