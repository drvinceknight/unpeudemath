---
layout     : post
title      : "Finding a Big Bang (Number) Theory wedding date"
categories : math
tags       :
- python
- numbertheory
comments   : true
---

In episode 17 of season 11 of the Big Bang Theory: ["The Athenaeum
Allocation"](http://bigbangtheory.wikia.com/wiki/The_Athenaeum_Allocation)
Sheldon (a character in the show) describes a wedding date (the 12th of May) as
romantic because it has a specific property. In this post I'll see what other
dates in a given year have the same property. This will use the python library
[SymPy](http://www.sympy.org/en/index.html) which is a great computer algebra
system.

Sheldon describes the date enthusiastically by saying:

> "The month squared equals the square of the sum of the members of the set of
> prime factors of the day"

If a given date has day \\(D\\) and month \\(M\\) this mathematically implies:

$$
M ^ 2 = \left(\sum_{d\in\mathbb{P}\text{ and } d| D}d\right)^2
$$

So for example for the 12th of May, we have \\(M=5\\) (May is the 5th month) and
\\(D=12\\):

$$
M ^ 2 = 25
$$

and

$$
\left(\sum_{d\in\mathbb{P}\text{ and } d| D}d\right)^2 = (2 + 3) ^ 2 = 25
$$

We see that actually the "squared" part of the condition is redundant. This is
because if:

$$x^2 = y ^2$$

then 

$$x = \pm y$$

but as everything here is positive integers we can just omit this all together.
So Sheldon should have said:

> "The month equals the sum of the members of the set of
> prime factors of the day"

(I'll give the show that this is perhaps less artistically impressive)

**So what other days could this marriage date land on?**

I'm going to investigate this using Python and it's fantastic
[SymPy](http://www.sympy.org/en/index.html) library which will quickly get us the
prime factors of a number.

```python
>>> import sympy as sym
>>> sym.primefactors(12)
[2, 3]
```

We're using Python which is a language not just used in science so has many
useful tools so first of all let's write a
[generator](https://wiki.python.org/moin/Generators) that gets all dates in a
year:

```python
import datetime as dt
def dates_in_year(year):
    """
    Generator that yields all dates in a given year
    """
    date = dt.date(year, 1, 1)
    while date.year == year:
        yield date
        date += dt.timedelta(1)

```

We can then combine this with the number theoretic abilities of SymPy to get all
dates that follow the condition:

```python
def find_dates(year):
    """
    Generator that yields dates in a given year for which the sum of the
    prime factors of the date is equal to the month.
    """
    for date in dates_in_year(year):
        day, month = date.day, date.month
        if sum(sym.primefactors(day)) == month:
            yield date

```

Now we can print out all these dates:

```python
>>> count = 0
>>> for date in find_dates(year=2017):
...     print(date)
...     count += 1
2017-02-02
2017-02-04
2017-02-08
2017-02-16
2017-03-03
2017-03-09
2017-03-27
2017-05-05
2017-05-06
2017-05-12
2017-05-18
2017-05-24
2017-05-25
2017-07-07
2017-07-10
2017-07-20
2017-08-15
2017-09-14
2017-09-28
2017-10-21
2017-10-30
2017-11-11
>>> print("Count:", count)
Count: 22
```

We see that there are 22 dates (including the 12th of May) that follow the
condition in 2017.

**Usually,** weddings are on weekends so which of those dates happens to fall on
a weekend?

```python
def find_weekend_dates(year):
    """
    Generator that yields weekend dates in a given year for which the sum of
    the prime factors of a date is equal to the month.
    """
    for date in find_dates(year):
        if date.weekday() >= 5:
            yield date
```

```python
>>> for date in find_weekend_dates(year=2017):
...     print(date)
2017-02-04
2017-05-06
2017-10-21
2017-11-11

```

So we see that actually the 12th of May is not an "OK" date in 2017.

Indeed, it looks like it's a Friday in 2017:

```python
>>> dt.date(2017, 5, 12).weekday()
4

```

Let us check 2018:

```python
>>> for date in find_weekend_dates(year=2018):
...     print(date)
2018-02-04
2018-03-03
2018-05-05
2018-05-06
2018-05-12
2018-07-07
2018-10-21
2018-11-11

```

Note that apart from the 12th of May and the 21st of October, these are
"trivial", they are dates where the \\(M\\)th day of month \\(M\\) is on a
weekend and is also prime.

If this wedding was to take place in 2018 (North hemisphere) Summertime it
looks like the 7th of July is the date.
