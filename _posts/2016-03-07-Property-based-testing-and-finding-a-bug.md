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
single example,, test a whole range of parameters.

Here's a simple example, let's consider the following function:

```python
def count_steps(a, b, step_size):
    """A simple function to count 1 dimensional steps from a to b"""
    steps = 0
    position = a
    while position < b:
       position += step_size
       steps += 1
    return steps
```

The very simplest way to write a unit test for the above function is to write
the following in a simple script and call it `steps.py` (note that this is not
TDD, I've written the function first here):

```python
import unittest

def count_steps(a, b, step_size):
    """A simple function to count 1 dimensional steps from a to b"""
    steps = 0
    position = a
    while position < b:
       position += step_size
       steps += 1
    return steps

class testCountSteps(unittest.testcase):
    def test_count_steps(self):
        a = 5
        b = 10
        step_size = 2.5
        expected_count = 2
        self.assertEqual(count_steps(a, b, step_size), expected_count)
```

We can then run this by using the following:

```bash
$ python -m unittest steps
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Before feeling happy about a test we really should check that it fails properly
(otherwise it's perhaps not running correctly. So changing `b=10` to `b=25` in
the `test_count_steps` and rerunning gives:

```bash
$ python -m unittest steps
F
======================================================================
FAIL: test_count_steps (steps.testCountSteps)
A simple function to count 1 dimensional steps from a to b
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/vince/tmp/steps.py", line 19, in test_count_steps
    self.assertEqual(count_steps(a, b, step_size), expected_count)
AssertionError: 8 != 2

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

So things, are looking good! I could try to write a few more **examples** in to
the tests and that's a good first step towards getting confidence in my results.

**But that's just it, those are just examples.**

This is where property based testing and hypothesis comes in.  I can use
hypothesis to parametrize that test and check the 'properties' of the output
for a range of sampled parameters.

Here is how this is done:

```python
import unittest

from hypothesis import given
from hypothesis.strategies import integers, floats

def count_steps(a, b, step_size):
    """A simple function to count 1 dimensional steps from a to b"""
    steps = 0
    position = a
    while position < b:
       position += step_size
       steps += 1
    return steps

class testCountSteps(unittest.testcase):
    @given(a=integers(), b=integers(), step_size=floats())
    def test_count_steps(self, a, b, step_size):
        self.assertLessEqual(count_steps(a, b, step_size), b / step_size)
        self.assertGreaterEqual(count_steps(a, b, step_size), 1)
```

Running the above gives:

```bash
$ python -m unittest steps
Falsifying example: test_count_steps(self=<steps.testCountSteps testMethod=test_count_steps>, a=0, b=0, step_size=0.0)
E
======================================================================
ERROR: test_count_steps (steps.testCountSteps)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/vince/tmp/steps.py", line 17, in test_count_steps
    def test_count_steps(self, a, b, step_size):
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/hypothesis/core.py", line 502, in wrapped_test
    print_example=True, is_final=True
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/hypothesis/executors.py", line 57, in default_new_style_executor
    return function(data)
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/hypothesis/core.py", line 103, in run
    return test(*args, **kwargs)
  File "/Users/vince/tmp/steps.py", line 18, in test_count_steps
    self.assertLessEqual(count_steps(a, b, step_size), b / step_size)
ZeroDivisionError: float division by zero
```

The top there tells me that a test has failed for the case of `step_size=0.0`,
from that point it's quick to notice that the code is also only suited for
cases where `a>b` so let's modify the test and function:

```python
import unittest

from hypothesis import given
from hypothesis.strategies import integers, floats

def count_steps(a, b, step_size):
    """A simple function to count 1 dimensional steps from a to b"""
    if step_size == 0:
        raise ZeroDivisionError()
    steps = 0
    position = a
    while position < b:
       position += step_size
       steps += 1
    return steps

class testCountSteps(unittest.testcase):
    @given(a=integers(), b=integers(), step_size=floats())
    def test_count_steps(self, a, b, step_size):
        assume(step_size != 0)
        self.assertLessEqual(count_steps(a, b, step_size), b / step_size)
        self.assertGreaterEqual(count_steps(a, b, step_size), 1)

    @given(a=integers(), b=integers()))
    def test_zero_step_size(self, a, b):
        step_size = 0
        self.assertRaiseError(count_steps(a, b, step_size), ZeroDivisionError)
```

Running the above now gives:


```bash
$ python -m unittest steps
Falsifying example: test_count_steps(self=<steps.testCountSteps testMethod=test_count_steps>, a=0, b=0, step_size=5e-324)
F.
======================================================================
FAIL: test_count_steps (steps.testCountSteps)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/vince/tmp/steps.py", line 19, in test_count_steps
    def test_count_steps(self, a, b, step_size):
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/hypothesis/core.py", line 502, in wrapped_test
    print_example=True, is_final=True
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/hypothesis/executors.py", line 57, in default_new_style_executor
    return function(data)
  File "/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/hypothesis/core.py", line 103, in run
    return test(*args, **kwargs)
  File "/Users/vince/tmp/steps.py", line 22, in test_count_steps
    self.assertGreaterEqual(count_steps(a, b, step_size), 1)
AssertionError: 0 not greater than or equal to 1

----------------------------------------------------------------------
Ran 2 tests in 0.104s

FAILED (failures=1)
```

You see now that hypothesis found a another problem and this has nothing to do
with th step_size, indeed if `a=b` then my original assumption in writing the
test is now falsified. In this instance I'll go ahead and change my test as I'm
actually happy to take 0 steps.

Of course we've lost the original test that checked the actual value, I could
compliment the test I have with some example tests (always a good idea) but I
can also just throw in a quick manual calculation of what the number of steps
should be.

```python
import unittest

from hypothesis import given, assume
from hypothesis.strategies import integers, floats

def count_steps(a, b, step_size):
    """A simple function to count 1 dimensional steps from a to b"""
    if step_size == 0.0:
        raise ZeroDivisionError()
    steps = 0
    position = a
    while position < b:
       position += step_size
       steps += 1
    return steps

class testCountSteps(unittest.TestCase):
    @given(a=integers(min_value=0, max_value=10),
           b=integers(min_value=1, max_value=20),
           step_size=floats(min_value=.5,
                            allow_infinity=False,
                            allow_nan=False))
    def test_count_steps(self, a, b, step_size):
        counted_steps = count_steps(a, a + b, step_size)
        self.assertLessEqual(counted_steps, (a + b) / step_size + 1)
        self.assertGreaterEqual(counted_steps, 0)

    @given(a=integers(), b=integers())
    def test_zero_step_size(self, a, b):
        step_size = 0
        self.assertRaises(ZeroDivisionError, count_steps, a, b, step_size)
```

