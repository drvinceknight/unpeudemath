---
layout     : post
title      : "Using Python in R to study Game Theory"
categories : python
tags       :
- axelrod
- math
- game-theory
comments   : true
---

I just got back from a great camping holiday and as usual have started my return
by working through email. One particular email has asked if it was possible to
use the [Axelrod](http://axelrod.readthedocs.io) library through the statistical
programming language: R. I have here and there heard of a variety of libraries
that let you call R from Python and vice versa so I thought it was worth
experimenting and seeing exactly how to do this. This blog post will be a very
brief demo of using the R package: `reticulate` to interface to the Python
library for studying the Iterated Prisoners Dilemma.

## Installing R as an anaconda user

My main language of choice is Python. I use the Anaconda distribution which can
also be used to install R. Here are the commands I ran to get R on my machine:

```bash
$ conda install r-essentials
```

That brings down R without about 80 packages but does not include `reticulate`
so I install that also:

```bash
$ conda install -c mro r-reticulate
```

**I expect that if you are an R user your main question would be how to install
Python.** I am not entirely sure how the `reticulate` package interfaces to
Python but I would recommend installing Python via the
[anaconda](https://www.anaconda.com/) distribution and then installing the
Axelrod library using: `pip install axelrod` (or even `conda install axelrod`).

## Calling the Axelrod library in R

```R
> library(reticulate)  # Loading the `reticulate` library
> axl <- import("axelrod")  # Importing axelrod as axl
```

Now we can use this `axl` object. First let us create a match between two
players:

```R
> tft <- axl$TitForTat()
> alt <- axl$Alternator()
> match <- axl$Match(c(tft, alt))
```

Playing this match outputs all the interactions:

```
> interactions <- match$play()
```

Once played the `match` has attributes that contain things like the final score
per turn:

```R
> match$final_score_per_turn()
1. 2.49
2. 2.515
```

We see that in this case `Alternator` gets a better score than `Tit For Tat`.
It is also possible to create tournaments with the Axelrod library:

```R
> players <- c(axl$Cooperator(), axl$Defector(), axl$TitForTat(), axl$Grudger())
> tournament <- axl$Tournament(players)
> results <- tournament$play()
> results$ranked_names
'Defector' 'Tit For Tat' 'Grudger' 'Cooperator'
```

As detailed in the [documentation for creating a basic
tournament](http://axelrod.readthedocs.io/en/stable/tutorials/getting_started/tournament.html)
we see that Defector wins.

The Axelrod library has a large number of
capabilities (including population dynamics) but one of the main treasures it
contains is the number of documented and tested strategies that are available.
In version `3.5.0`:

```R
> length(axl$strategies)
202
```

If you'd like to read more about the Axelrod library take a look at the
documentation [axelrod.readthedocs.io](http://axelrod.readthedocs.io).

## Nash equilibria in R

Another game theoretic library is called [Nashpy](http://nashpy.readthedocs.io)
and it is used to find Nash equilibria of 2 player games. As it requires using
multi dimensional arrays as input (the payoff matrices) I though it might be
helpful to include a quick example.

Here's the Nash equilibria of Rock Paper Scissors:

```R
> nash <- import("nash")
> A = matrix(c(0, -1, 1, 1, 0, -1, -1, 1, 0), nrow=3, ncol=3)
> rps <- nash$Game(A)
> eq <- rps$vertex_enumeration()
```

The `vertex_enumeration` method return a Python iterator object that can then be
iterated through in a step wise manner to search the equilibria (generators are
a fantastic part of the Python library with huge implication on memory
footprints).

Thankfully the `reticulate` library has an `iter_next` function that speaks to
these generators:

```R
> iter_next(eq)
1. 0.333333333333333 0.333333333333333 0.333333333333333
2. 0.333333333333333 0.333333333333333 0.333333333333333
```

We see that the equilibria for Rock Paper Scissors is for both players to
uniformly randomly pick from Rock, Paper or Scissors.

Note that if we call `iter_next` again we retrieve nothing (the generator has
gone through all possible vertex pairs):

```R
> iter_next(eq)
NULL
```

If you'd like to read more about the Nashpy library take a look at the
documentation (which includes mathematical background to the implemented
algorithms): [nashpy.readthedocs.io](http://nashpy.readthedocs.io).

---

I'm really impressed with `reticulate` as an interface to Python from R. The
README seems to have sufficient information to get started:
[github.com/rstudio/reticulate#overview](https://github.com/rstudio/reticulate#overview)

EDIT: [Here is a Jupyter notebook with all the above
code](https://github.com/drvinceknight/unpeudemath/blob/gh-pages/assets/code/Using%20Python%20in%20R%20with%20reticulate.ipynb).
