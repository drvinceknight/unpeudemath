---
layout     : post
title      : "Analysis of variance with different sized samples in Python"
categories : python
tags       :
- statistics
- python
comments   : true
---

Working with [Nikoleta](https://twitter.com/nikoletaglyn) we recently needed to
carry out an [Analysis of
Variance](https://en.wikipedia.org/wiki/Analysis_of_variance) (ANOVA) on a data
set where the sample size of each category is not constant. This blog post shows
very briefly how to carry this out in Python (when using Pandas).

We are going to be using
[SciPy](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html)'s
`stats.f_oneway` function which can handle different sized samples out of the
box. Here's a quick example:

```python
>>> import random
>>> random.seed(0)
>>> data = [[random.randint(1, 20) for _ in range(size)] for size in range(1, 5)]
>>> for sample in data:
...     print(sample)
[13]
[14, 2]
[9, 17, 16]
[13, 10, 16, 12]

```

We see that we have 4 samples of different size. Here let's carry out the
ANOVA:

```python
>>> from scipy import stats
>>> f_val, p_val = stats.f_oneway(*data)
>>> p_val
0.57172146848075944

```

We see that our \\(p\\) value is approximately \\(0.57\\).

**Where you need to be careful is when the data you have is in a pandas data
frame.** This was the particular case we were dealing with.

For the purposes of our experiment let us build up the dataframe in question.
First let us transform our samples in to their own dataframe. **This is an
artificial exercise to get data of the form required** as I'm just going to
show how to use `dropna` to get back to the situation above.

```python
>>> import pandas as pd
>>> dfs = [pd.DataFrame({k: sample}) for k, sample in enumerate(data)]
>>> df = pd.concat(dfs,  ignore_index=True, axis=1)
>>> df
      0     1     2   3
0  13.0  14.0   9.0  13
1   NaN   2.0  17.0  10
2   NaN   NaN  16.0  16
3   NaN   NaN   NaN  12

```

If we were to carry out the anova as before (pulling out the columns) we would
get an error:

```python
>>> data = [df[col] for col in df]
>>> f_val, p_val = stats.f_oneway(*[df[col] for col in df])
>>> p_val
nan

```

The missing step is to ignore the missing numbers in the pandas dataframe:

```python
>>> data = [df[col].dropna() for col in df]
>>> f_val, p_val = stats.f_oneway(*data)
>>> p_val
0.57172146848075944

```

We can finish things of by drawing a nice violin plot with a regression line
fitted to the median of the data.

```python
import numpy as np  # For the median
import matplotlib.pyplot as plt  # For the plot

# Fit line to median of distributions
x = range(1, len(data) + 1)
y = [np.median(sample) for sample in data]
slope, intercept, r_val, p_val, slope_std_error = stats.linregress(x, y)

def line(x):
    """The regression line"""
    return slope * x + intercept

plt.figure()
plt.violinplot(data);
x1, x2 = plt.xlim()
plt.plot((x1, x2), (line(x1), line(x2)), '--',
         label="$y = {0:.2f}x + {0:.2f}$ ($p={0:.2f}$)".format(slope,
                                                               intercept,
                                                               p_val),
         ),
plt.legend(loc=4);
```

which gives:

![]({{site.baseurl}}/assets/images/regression_anova.svg)
