---
layout     : post
title      : "Profiling and reducing memory consumption in Python"
categories : python
tags       :
- python
comments   : true
---

I am one of the core developers of the
[Axelrod-Python](http://axelrod.readthedocs.io/en/latest/) project. This Python
library lets you carry out Iterated Prisoner's dilemma tournaments. One of the
great success of the library is the number of strategies it contains, at
present (thanks to many awesome contributions) it has 139 strategies (149 if
you count the cheaters). This is great but **also** created a bit of a
challenge. Running full tournaments became quite expensive computationally. This
is now fixed, thanks mainly to writing and reading to/from disk instead of
using memory. This post will describe some tools and techniques that can be
used to do this.

## Running example

As a running example we're going to consider calculating the average of a large
number of numbers.

```python
>>> N = 5
>>> nbrs = list(range(0, 10 ** N))
>>> total = sum(nbrs)
>>> mean = total / len(nbrs)
>>> mean
49999.5

```

## Profiling

First of all let us take a look at how much memory our code uses. There's a
great tool for this called
[`memory_profiler`](https://pypi.python.org/pypi/memory_profiler).

To use it, let's put the following in a script: `profile.py`:

```python
from memory_profiler import profile

precision = 10

fp = open('memory_profiler_basic_mean.log', 'w+')
@profile(precision=precision, stream=fp)
def basic_mean(N=5):
    nbrs = list(range(0, 10 ** N))
    total = sum(nbrs)
    mean = sum(nbrs) / len(nbrs)
    return mean

if __name__ == '__main__':
    basic_mean()

```

After running that file (`$python profile.py`), the
`memory_profiler_basic_mean.log` file now contains the following:

```
Filename: profile.py

Line #    Mem usage    Increment   Line Contents
================================================
     6  30.6015625000 MiB   0.0000000000 MiB   @profile(precision=precision, stream=fp)
     7                             def basic_mean(N=5):
     8  34.4492187500 MiB   3.8476562500 MiB       nbrs = list(range(0, 10 ** N))
     9  34.4492187500 MiB   0.0000000000 MiB       total = sum(nbrs)
    10  34.4492187500 MiB   0.0000000000 MiB       mean = total / len(nbrs)
    11  34.4492187500 MiB   0.0000000000 MiB       return mean
```

The `Increment` column shows the amount of memory each step takes. In this
particular case the largest culprit is getting the list of numbers.

## Generators

If you're using python 3, then `range` is a generator and not an actual list.
To get the list you need to convert it to one as I've done above.  One of the
first things we can do to reduce memory consumption is not convert that `nbrs`
in to a list but keep it as `range` which is amongst other things a
`generator`. [This blog post is a great explanation about
generators](https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/)
but the basic idea is that you can create a Python generator which will not
immediately create all elements you want. Instead it will keep track of them as
you go. In essence this is perfect for memory consumption: by keeping track of
where you are and what's next you don't have to keep everything in memory.

```
Filename: profile.py

Line #    Mem usage    Increment   Line Contents
================================================
    14  34.0820312500 MiB   0.0000000000 MiB   @profile(precision=precision, stream=fp)
    15                             def basic_mean_with_gen(N=5):
    16  34.0820312500 MiB   0.0000000000 MiB       nbrs = range(0, 10 ** N)
    17  34.0820312500 MiB   0.0000000000 MiB       total = sum(nbrs)
    18  34.0820312500 MiB   0.0000000000 MiB       mean = total / len(nbrs)
    19  34.0820312500 MiB   0.0000000000 MiB       return mean

```

## Stepping through generators

Now let us assume we didn't want to calculate the mean number of all the numbers
but just of the even ones:

```python
>>> N = 5
>>> nbrs = [n for n in range(0, 10 ** N) if n % 2 == 0]
>>> total = sum(nbrs)
>>> mean = sum(nbrs) / len(nbrs)
>>> mean  # (This is what we expect)
49999.0
```

If we profile this in a similar way we get an error when it comes to a generator:

```
Traceback (most recent call last):
...
TypeError: object of type 'generator' has no len()
```

Indeed, the whole point of a generator is that it cannot know how many things
are in it...

So let's modify the generator approach as follows:

```python
@profile(precision=precision, stream=fp)
def basic_mean_with_gen(N=5):
    nbrs = (n for n in range(0, 10 ** N) if n % 2 == 0)
    total = 0
    count = 0
    for n in nbrs:
        total += n
        count += 1
    mean = total / count
    return mean
```

The above makes use of the [generator
comprehension](http://stackoverflow.com/questions/364802/generator-comprehension)
syntax to build the generator.  Instead of calculating the sum all in one go we
just step through, this might take longer but it will not cost much at all in
terms of memory. The profile log now looks like below:

```
Filename: profile_even.py

Line #    Mem usage    Increment   Line Contents
================================================
     6  30.3281250000 MiB   0.0000000000 MiB   @profile(precision=precision, stream=fp)
     7                             def basic_mean(N=5):
     8  32.1289062500 MiB   1.8007812500 MiB       nbrs = [n for n in range(0, 10 ** N) if n % 2 == 0]
     9  32.3984375000 MiB   0.2695312500 MiB       total = sum(nbrs)
    10  32.3984375000 MiB   0.0000000000 MiB       mean = total / len(nbrs)
    11  32.3984375000 MiB   0.0000000000 MiB       return mean


Filename: profile_even.py

Line #    Mem usage    Increment   Line Contents
================================================
    13  32.0234375000 MiB   0.0000000000 MiB   @profile(precision=precision, stream=fp)
    14                             def basic_mean_with_gen(N=5):
    15  32.0234375000 MiB   0.0000000000 MiB       nbrs = (n for n in range(0, 10 ** N) if n % 2 == 0)
    16  32.0234375000 MiB   0.0000000000 MiB       total = 0
    17  32.0234375000 MiB   0.0000000000 MiB       count = 0
    18  32.0234375000 MiB   0.0000000000 MiB       for n in nbrs:
    19  32.0234375000 MiB   0.0000000000 MiB           total += n
    20  32.0234375000 MiB   0.0000000000 MiB           count += 1
    21  32.0234375000 MiB   0.0000000000 MiB       mean = total / count
    22  32.0234375000 MiB   0.0000000000 MiB       return mean
```

One other aspect that we could do but it's not going to show up substantially
with our little example here is to write the numbers to file and calculate the
means as they are read in. This is in fact how we fixed the high memory
consumption on the Axelrod project. If you're interested in seeing a **real**
example you can see the PR that fixed that here:
https://github.com/Axelrod-Python/Axelrod/pull/672. In essence we had to do
similar things like I did above, instead of calculating the mean in one go we
walk through the file and calculate all the various
[results](http://axelrod.readthedocs.io/en/latest/tutorials/getting_started/tournament_results.html)
as we go.

## TLDR

Stay out of memory: use generators (and/or use files).

Of course, it's important to not over optimise on just one dimension. If your
memory consumption is not an actual constraint then perhaps don't worry about it.
