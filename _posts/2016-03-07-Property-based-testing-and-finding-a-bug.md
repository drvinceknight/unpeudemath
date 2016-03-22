---
layout     : post
title      : "Property based testing, hypothesis and finding a bug"
categories : code
tags       :
- python
- axelrod
- hypothesis
comments   : false
---

I really have fallen in love with [test driven
development](https://en.wikipedia.org/wiki/Test-driven_development) and as much
as is reasonable stick to it. This mainly revolves around writing Python unit
tests, which makes programming a lot easier (for me). In Namibia I was lucky
enough to meet and chat with [David MacRiver](http://www.drmaciver.com/), the
main developer of the
[hypothesis](https://hypothesis.readthedocs.org/en/latest/) package. Before
that the [The Axelrod project](http://axelrod.readthedocs.org/en/latest/) had
already incorporated some of what hypothesis is for: property based testing.
This blog post will briefly describe what that is, how it took some hours of
sleep away from me (in a good way) and why it's particularly great for research
software.

## Property based testing

I'm slowly slowly learning that hypothesis is ridiculously clever but at a very
basic level what it allows you to do is take 1 test and instead of testing a
single example, test a whole range of parameters.

Here's a simple example, based on a short demo I gave at
[the collaborations workshop 2016 in Edinburgh](http://www.software.ac.uk/cw16).
You can find the slides I gave for that at this link:
[vknight.org/Talks/2016-03-22-Division-by-11-and-property-based-testing-with-hypothesis/index.html#/](http://vknight.org/Talks/2016-03-22-Division-by-11-and-property-based-testing-with-hypothesis/index.html#/).

Let us write a function that tests divisibility by 11 (assuming that we don't
know about `% 11`. To do this we'll use the following property:

> A number is divisible by 11 if and only if the alternating (in sign) sum of
> the number’s digits is 0.

For example: 121 is divisible by 11 because \(1-2+1=0\) (side note: if you're
about to yell at me in the comments please read the rest of this post).

Let's save below in a file called `main.py`:

```python
def divisible_by_11(number):
    """Uses above criterion to check if number is divisible by 11"""
    string_number = str(number)
    alternating_sum = sum([(-1) ** i * int(d) for i, d
                           in enumerate(string_number)])
    return alternating_sum == 0
```

Now if we write out some examples we get expected behaviour:

```python
>>> import main
>>> for k in range(10):
...     print(main.divisible_by_11(11 * k))
True
True
True
True
True
True
True
True
True
True
```

**But** let's write an actual test suite. Here's a very basic unittest that
we'll save in `test_main.py`:

```python
import unittest
import main

class TestDivisible(unittest.TestCase):
    def test_divisible_by_11(self):

        for k in range(10):
            self.assertTrue(main.divisible_by_11(11 * k))
            self.assertFalse(main.divisible_by_11(11 * k + 1))

        # Some more examples
        self.assertTrue(main.divisible_by_11(121))
        self.assertTrue(main.divisible_by_11(12122))

        self.assertFalse(main.divisible_by_11(123))
        self.assertFalse(main.divisible_by_11(12123))
```

The above tests the first 10 numbers divisible by 11 (and that that number + 1
is not) and also some specific tests (121 and 12123).

We then run this by using the following:

```bash
$ python -m unittest test_main
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

At this point we could be very happy and proud of ourselves: we have tested well written software that can be shipped and used by researchers world wide to test the divisibility of a number by 11!!!

**This is how mathematics breaks.**

![Everything is wrong.](http://vknight.org/Talks/2016-03-22-Division-by-11-and-property-based-testing-with-hypothesis/img/disaster.gif)

Let's write a [hypothesis](https://hypothesis.readthedocs.org/en/latest/) test.
We'll write the following in `test_property_main.py`:

```python
import unittest
import main

from hypothesis import given  # This is how we will define inputs
from hypothesis.strategies import integers  # This is the type of input we will use

class TestDivisible(unittest.TestCase):

    @given(k=integers(min_value=1))  # This is the main decorator
    def test_divisible_by_11(self, k):
        self.assertTrue(main.divisible_by_11(11 * k))
```

The above is actually a simpler test than before: we're only testing that a
number that we **know** is divisible by 11 is in fact getting the expected
output from our function.

Let's run it:

```bash
$ python -m unittest test_propert_main
Falsifying example: test_divisible_by_11(self=<test_property_main.TestDivisible testMethod=test_divisible_by_11>, k=19)
F
======================================================================
FAIL: test_divisible_by_11 (test_property_main.TestDivisible)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_property_main.py", line 10, in test_divisible_by_11
    def test_divisible_by_11(self, k):
  File "/usr/local/lib/python2.7/site-packages/hypothesis/core.py", line 502, in wrapped_test
    print_example=True, is_final=True
  File "/usr/local/lib/python2.7/site-packages/hypothesis/executors.py", line 57, in default_new_style_executor
    return function(data)
  File "/usr/local/lib/python2.7/site-packages/hypothesis/core.py", line 103, in run
    return test(*args, **kwargs)
  File "test_property_main.py", line 11, in test_divisible_by_11
    self.assertTrue(main.divisible_by_11(11 * k))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 1 test in 0.058s

FAILED (failures=1)
```

We get an error! An right at the top we get the `Falsifying example` so we see
that our function fails for `k=19`. For, `k=19` the number being tested is
\\(19\times 11=209\\). That number is obviously divisible by 11 (by
construction) but it's alternating sum is in fact 11 **which is not 0**.

At this point, as [described in this previous blog post about divisibility by
11](http://vknight.org/unpeudemath/code/2014/11/22/on-divisibility-by-11/) I
can let slip the **correct** property for divisibility by 11:

> A number is divisible by 11 if and only if the alternating (in sign) sum of
> the number’s digits is divisible by 11.

(There's a simple algebraic proof of that at [the older blog
post](http://vknight.org/unpeudemath/code/2014/11/22/on-divisibility-by-11/).)

Now let's modify our `main.py` (note that I'm using a slightly better
modification than the lazy one I gave in the demo at the collaboration
workshop):

```python
def divisible_by_11(number):
    """Uses above criterion to check if number is divisible by 11"""
    string_number = str(number)
    # Using abs as the order of the alternating sum doesn't matter.
    alternating_sum = abs(sum([(-1) ** i * int(d) for i, d
                               in enumerate(string_number)]))
    # Recursively calling the function
    return (alternating_sum in [0, 11]) or divisible_by_11(alternating_sum)
```

Running the tests:

```bash
$ python -m unittest test_propert_main
.
----------------------------------------------------------------------
Ran 1 test in 0.043s

OK
```

As we hoped!

**I think the above is a good example of why property based testing and tools
like hypothesis are useful for research software.**

It helped identify an error in my mathematical thought process, an error that I
in fact thought I had tested properly (using the `test_main.py` tests). If it
wasn't for hypothesis I would have shipped code that redefined what it meant to
be divisible by 11.

**If you only came here to get a basic working example of hypothesis you can stop now :)**

Obviously the above is a simple example but **hypothesis** recently found a bug
in [Axelrod](http://axelrod.readthedocs.org/en/latest/) (the python package for
reproducing Iterated Prisoner's Dilemma tournaments).

Axelrod creates tournaments of players picked from one of the (at time of
writing) 123 strategies. Here is one of the tests that randomly selects
strategies to create tournaments and check that they run:

```python
    @given(s=lists(sampled_from(axelrod.strategies),
                   min_size=2,  # Errors are returned if less than 2 strategies
                   max_size=5, unique=True),
           turns=integers(min_value=2, max_value=50),
           repetitions=integers(min_value=2, max_value=4),
           rm=random_module())
    @settings(max_examples=50, timeout=0)
    @example(s=test_strategies, turns=test_turns, repetitions=test_repetitions,
             rm=random.seed(0))
    def test_property_serial_play(self, s, turns, repetitions, rm):
        """Test serial play using hypothesis"""
        # Test that we get an instance of ResultSet

        players = [strat() for strat in s]

        tournament = axelrod.Tournament(
            name=self.test_name,
            players=players,
            game=self.game,
            turns=turns,
            repetitions=repetitions)
        results = tournament.play()
        self.assertIsInstance(results, axelrod.ResultSet)
        self.assertEqual(len(results.cooperation), len(players))
        self.assertEqual(results.nplayers, len(players))
        self.assertEqual(results.players, players)
```

Without going in to precise details, at one point hypothesis found that two
particular strategies could not play together. [Here is the github issue that
documented this](https://github.com/Axelrod-Python/Axelrod/issues/465). These
were:

- `Backstabber`
- `MindReader`

These two strategies **did in fact** already play in a tournament together. The
main tournament that includes all cheating strategies, but the side effect of
that is that another cheating strategy played `BackStabber` first and overwrite
it's strategy (meaning it could then play nice with `MindReader`). **Hypothesis
however created a tournament were they were directly opposed and then our bug
occured.**

Anyway, it's now fixed and the test includes a `@example` statement to ensure
that the specific bug is in fact fixed: [you can see this in the source
code](https://github.com/Axelrod-Python/Axelrod/blob/master/axelrod/tests/unit/test_tournament.py#L120).

In practice, the recommendation is to use a combination of property based tests
and traditional example based tests (as there are some specific things that
need to be checked) **but I think all test suites can be improved by using
tools like hypothesis, in particular research software**.

Helpful links:

- [@DRMacIver](https://twitter.com/DRMacIver): David is the writer of Hypothesis.
- [Github repo](https://github.com/DRMacIver/hypothesis).
- [Documentation](https://hypothesis.readthedocs.org/en/latest/).

Finally, if you're of the irc persuasion, I really recommend dropping in at
`#hypothesis` on freenode. Here's a direct link to the channel on irccloud:
[www.irccloud.com/invite?channel=%23hypothesis&hostname=irc.freenode.net&port=6697&ssl=1](https://www.irccloud.com/invite?channel=%23hypothesis&hostname=irc.freenode.net&port=6697&ssl=1).
Everyone there has always been very helpful.
