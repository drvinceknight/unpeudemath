---
layout     : post
title      : "Scheduling class presentations using linear programming with Python"
categories : mathematics
tags       :
- python
- linear programming
comments   : true
---

My first year programming class culminates in a final week of group
presentations. This is always a highlight of the teaching period as I get to see
the awesome things my students have come up with. However, scheduling 30-40
group presentations every year could be a real nightmare. This is where
mathematics comes to the rescue. I'll describe in this post how I use linear
programming implemented in the Python library
[Pulp](https://github.com/coin-or/pulp) to get the schedule easily.

**TLDR** We built a python library for scheduling conferences, you can find the
source code
here:[github.com/PyconUK/ConferenceScheduler](https://github.com/PyconUK/ConferenceScheduler),
the documentation is here:
[conference-scheduler.readthedocs.io/en/latest/](http://conference-scheduler.readthedocs.io/en/latest/)
and you can `pip install conference_scheduler`.

I have previously done this using [Sagemath](http://www.sagemath.org/) but this
year I decided to use Pulp ("A python Linear Programming API"). This probably
follows from [@DRMacIver](https://twitter.com/DRMacIver)'s talk at PyCon UK
2016: ["Easy solutions to hard
problems"](https://www.youtube.com/watch?v=OkusHEBOhmQ) in which I saw Pulp for
the first time.

The first step to solving this problem is getting the availability of all the
student groups. I use [doodle](http://www.doodle.com/) for this just to get a
quick poll with dates and times. Doodle has the ability to export a poll to
excel so I open that up in spreadsheet and tidy things up a bit (deleting
irrelevant rows/columns).

Once I've done that I can read in the file which I do using
[Pandas](http://pandas.pydata.org/):

```python
>>> import pandas as pd
>>> df = pd.read_excel("availability.xls")
>>> df = df.replace("OK", 1)
>>> df = df.fillna(0)
>>> df.head()
                          Company          Time slot
0               Alternative Maths  Wed 13:30 – 14:00
1                          Europa  Thu 13:00 – 13:30
2                  L.A.S.T Resort  Mon 12:30 – 13:00
3            DividedByZeroStudios  Mon 17:30 – 18:00
4                   Effervescence  Fri 17:30 – 18:00

```

I then transform that in to a numeric array:

```python
>>> import numpy as np
>>> A = np.array(df)

```

**Now I start using Pulp**, first let's create a problem:

```python
>>> import pulp
>>> M, N = A.shape  # Dimensions
>>> prob = pulp.LpProblem("Scheduling")
>>> x = pulp.LpVariable.dicts("x", itertools.product(range(M), range(N)),
							  cat=pulp.LpBinary)  # Variables
```

Then we add constraints:

$$x_{ij} \leq A_{ij}$$

Ie \\(x\_{ij}\\) can be 1 iff team \\(i\\) is available in slot \\(j\\).

Here is how we __add__ the constraint to our pulp `prob`:


```python
>>> for index in x:
... 	try:
...         x[index].upBound = float(A[index])
...     except ValueError:  # Seemed to be an artifact in the matrix
...         x[index].upBound = 0

```

Next we need to make sure that any slot can only be used by one team at a time:

$$\sum_{i=1}^{M}x_{ij}\leq1$$

Ie slot \\(j\\) can only be used by one team.

```python
>>> for slot in range(N):
... 	prob += sum(x[(team, slot)] for team in range(M)) <= 1

```

I quite like this syntax: we're "literally" __adding__ the constraints to our
problem.

We now need to make sure that each team appears in exactly one slot:

$$\sum_{j=1}^{N}x_{ij}=1$$

```
>>> for team in range(M):
...     prob += sum(x[(team, slot)] for slot in range(N)) == 1

```

Once we have done this **we could** add an objective function. I could for
example write a mathematical function that chooses to minimise the number of
days used but in practice I don't need to do that so I'm just looking for a
feasible solution to the problem:

```
>>> prob.solve(pulp.GLPK())
1

```

The `1` is the status which confirms in this case that a solution has been found.

So let us take a look at the solution:


```python
>>> solution = []
>>> for company in range(M):
...     for slot in range(N):
...         if x[(company, slot)].value() == 1:
...         	solution.append([df.index[company], df.columns[slot]])
>>> df = pd.DataFrame(solution, columns=["Company", "Time slot"])
>>> df.sort_values(by="Company")
                           Company          Time slot
14                          Apollo  Tue 16:30 – 17:00
17                  Coding Cymraeg  Thu 13:30 – 14:00
23                       Complexus  Tue 10:00 – 10:30
3             DividedByZeroStudios  Mon 17:30 – 18:00
4                    Effervescence  Fri 17:30 – 18:00
1                           Europa  Thu 13:00 – 13:30
11                        F.E.J.L.  Tue 15:00 – 15:30
12                     Ferdie Amor  Wed 12:30 – 13:00
16                         Framtak  Tue 17:30 – 18:00
15                   FridgeVentory  Tue 17:00 – 17:30
30                   Generic Group  Tue 16:00 – 16:30
26                       GeoCampus  Tue 11:30 – 12:00
5       Green and Russian Standard  Fri 16:30 – 17:00
19                            JALE  Mon 16:00 – 16:30
27                           JEM'D  Fri 16:00 – 16:30
7                            J^2AG  Wed 16:30 – 17:00
2                   L.A.S.T Resort  Mon 12:30 – 13:00
29                MACT enterprises  Tue 12:30 – 13:00
10                            MBAS  Thu 17:30 – 18:00
21                            MRJL  Mon 15:30 – 16:00
8                            Merge  Wed 09:00 – 09:30
13                          MyTime  Tue 15:30 – 16:00
22                        Noteable  Mon 17:00 – 17:30
20                        Oakheart  Mon 15:00 – 15:30
24                         PoshFit  Tue 10:30 – 11:00
25                       ReCollect  Tue 11:00 – 11:30
0                Alternative Maths  Wed 13:30 – 14:00
6                           Room 1  Tue 14:00 – 14:30
9                     StockSensors  Fri 11:30 – 12:00
28                           Swigg  Tue 12:00 – 12:30
18                        The Cyps  Mon 16:30 – 17:00
31                    Ticket Tiger  Mon 13:00 – 13:30

```

This is a great example of using implemented applied mathematics to quickly
solve a real world problem. The other benefit is that when/if I need to do this
again in the feature I simply need to read in a different availability file.

[Here is a notebook version of all of the above]({{site.baseurl}}/assets/code/Scheduling final group presentations.ipynb).
