---
layout     : post
title      : "Fitting ranks to a distribution"
categories : math
tags       :
- python
- math
comments   : true
---

This is a brief blog post to describe how to scale a set of ranks to some
distribution using a percentage point function. This is in the category of blog
posts of me writing myself a note so that I remember how to do this when I need
to.

A probabilistic distribution is a mathematical object that relates a given
variable to the probability that that variable occurs.

Distributions can be empirical: simply a collection of the data and a
calculation of the corresponding probabilities. For example, in a collection of
200 people, there heights could be measured and a probability distribution
calculated.

There are also a number of theoretic distributions that are not only well
understood and very useful but are seen in nature. For example, times between
arrivals at queueing systems often follow an exponential distribution, also
similarly heights often follow a normal distribution (a nice blog post about
exactly why this is the case is here:
[www.johndcook.com/blog/2008/07/20/why-heights-are-normally-distributed/](https://www.johndcook.com/blog/2008/07/20/why-heights-are-normally-distributed/)).

One we have a theoretic distribution we can further study the phenomenon in
question. For example a technique called [Inverse Random
Sampling](https://en.wikipedia.org/wiki/Inverse_transform_sampling) allows us to
use the [Cumulative Distribution Function
(CDF)](https://en.wikipedia.org/wiki/Cumulative_distribution_function) to
randomly sample from any theoretic distribution.

This is not the point of this blog post. Here I want to consider something else,
let us assume I have a group of 200 people, I don't know their heights but I
know their rank according to height (from shortest to tallest person): can I
take a guess as to their height? One approach to this is to scale their ranks to
a distribution (and as we know that height is normally distributed: a normal
distribution makes sense).

The tool we will use is the *percentage point function* which is the inverse of
the CDF (essentially the same tool used in inverse random
sampling). From the ranks we can obtain the percentiles that each individual
corresponds to and from there we can invert the CDF and find their height.

Let us illustrate this with Python and the `scipy` library (which has a number
of distributions available):
First the ranks:

```python
>>> number_of_people = 200
>>> ranks = range(number_of_people)
>>> len(ranks), min(ranks), max(ranks)
(200, 0, 199)

```

Now, let us put together some code that uses a truncated normal distribution
(because I know the extreme heights in my group say).

```python
>>> import scipy.stats
>>> import numpy as np
>>> def make_distribution(lower_bound=140,
...                       upper_bound=200,
...                       mean=175,
...                       std=10):
...     """Create a truncated normal distribution."""
...     a, b = (lower_bound - mean) / std, (upper_bound - mean) / std
...     return scipy.stats.truncnorm(a=a, b=b, loc=mean, scale=std)
>>> def obtain_values(number=200,
...                   lower_bound=140,
...                   upper_bound=200,
...                   mean=58,
...                   std=10):
...     """Obtain values according to the required distribution."""
...     dist = make_distribution(lower_bound=lower_bound,
...                              upper_bound=upper_bound,
...                              mean=mean,
...                              std=std)
...     percentiles = np.arange(1, number + 1) / number
...     values = dist.ppf(percentiles)
...     assert len(values) == number
...     return values

```

Using this we can obtain the expected heights for a group of 200 individuals:

```python
>>> heights = obtain_values()

```

We can now reverse the process and plot the expected pdf (checking that we've
mapped our ranks to a height from the distribution):

```python
>>> x = np.linspace(140, 200, 100)
>>> dist = make_distribution()
>>> plt.plot(x, dist.pdf(x), label="Theoretic truncated normal pdf")
>>> plt.hist(heights, bins=20, normed=True,
>>> label="Mean={:.02f}".format(np.mean(heights)))
>>> plt.legend();

```

![]({{site.baseurl}}/assets/images/heights_fitted_to_pdf.svg)
