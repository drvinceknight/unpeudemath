---
layout     : post
title      : "The fallacy of a meritocracy (using game theory)"
categories : math
tags       :
- python
- math
comments   : true
---

Today we hosted [Dame Professor Celia
Hoyles](http://www.ucl.ac.uk/ioe/about/ioe-life/academics/celia-hoyles) who gave
a talk at the launch event of Cardiff's new Mathematics Education Research Group
(MERG). Amongst many interesting things the topic of the gender imbalance in
Mathematics came up. In this post I'll use a game theoretic model of evolution
to describe one aspect of lack of diversity: the fallacy that is a meritocracy.

One definition of a meritocracy is: "a society governed by people selected
according to merit". In other words, the idea is that people should be selected
based on their ability and their ability alone. For example, a paper should
be published in a mathematics journal based purely on the content of the paper
and not the gender of the authors.

Often, mathematicians are keen to say that mathematics is a meritocracy: the
"purity" of the subject being clear and the only thing that matters.

One anecdotal piece of evidence showing that this isn't the case is the fact
that the late [Maryam
Mirzakhani](https://en.wikipedia.org/wiki/Maryam_Mirzakhani) was the first women
to win a Fields Medal (out of 56!). It would be difficult to defend that this
represents a meritocracy, unless you believed that women were naturally less
able to do Mathematics than men (in which case please stop reading and go
elsewhere).

So despite our best intentions why does the idea of a meritocracy not really
work? (Although it is of course a lovely idea!)

I am not an expert in these things but I believe there are at least two reasons.
First of all: privilege, simply by being a white male I've started life with a
bit of a head start. Here's a nice video about privilege:

<div class="video">
    <figure>
<iframe width="560" height="315" src="https://www.youtube.com/embed/EIJqtWUiUCs"
frameborder="0" gesture="media" allowfullscreen></iframe>
    </figure>
</div>

Another reason is the well researched phenomena that with all things being equal
we are more likely to be receptive/enthusiastic/positive with/to things/people
who are like us. Here is an interesting piece about this:
https://sites.psu.edu/aspsy/2015/04/17/similar-to-me-effect-in-the-workplace/. 

I
know I'm guilty of this myself, for example when reading some of my research
students work my initial reaction is that something they've written **is not
good**. However, upon reflecting a bit more and distancing myself from my own
bias I usually realise that **it's not written how I would have written it**.
This particular bias is one type of what is often referred to as **unconscious
bias**. Here is a nice video by the Royal Society about this:

<div class="video">
    <figure>
<iframe width="560" height="315" src="https://www.youtube.com/embed/dVp9Z5k0dEE"
frameborder="0" gesture="media" allowfullscreen></iframe>
    </figure>
</div>

I'm now going to represent these ideas in a well studied mathematical model of
population dynamics. (Disclaimer: In the interest of keeping this post short I
won't go in to the background of the model more than I need to.)

Let us consider a normalised population of individuals of men and woman
represented by a vector \\x=(x_1, x_2\\) where \\(x_1 + x_2 = 1\\) so that
\\(x_1\\) represents the proportion of men and \\(x_2\\) the proportion of
women.

Let us assume that at any moment in time the rate of increase of a particular
type (gender) can be represented by the following matrix:

$$
A = \begin{pmatrix}
r & 1\\
1 & r
\end{pmatrix}
$$

With \\(r > 1\\): this is essential to our assumption regarding the "similar
to me effect".

The "fitness" (related to the idea of "merit") of both types is then given by:

- For men: \\(f_1 = rx_1 + x_2\\)
- For women: \\(f_2 = x_1 + rx_2\\)

So:

$$
f=(f_1, f_2) = Ax
$$

To ensure that \\(x_1 + x_2 = 1\\) we need to adjust the total increase rate by
taking away the average fitness of our individuals (I'm skipping some details
here but this is a standard model of evolutionary game theory).

$$
\phi = fx
$$

Using this we have the differential equation in matrix form:

$$
\frac{dx}{dt} = x(f- \phi)
$$

We can solve this differential equation numerically to get an idea of what is
happening. I'll use Python to do this.

First some functions to set
up creating the matrix \\(A\\) and defining the differential equation:

```python
>>> import numpy as np
>>> import matplotlib.pyplot as plt

>>> from scipy.integrate import odeint

>>> t = np.linspace(0, 200, 200)  # Obtain 200 time points

>>> def create_A(r=1.05):
...     A = np.array([[r, 1], [1, r]])
...     return A

>>> def dx(x, t, A):
...     """
...     Define the derivate of x.
...     """
...     f = np.dot(A, x)
...     phi = np.dot(f, x)
...     return x * (f - phi)

```

Let us assume \\(r = 1.05\\) (very close to a
meritocracy) and let us also assume that we start with (only) slightly more men
than women: \\(x = (.55, .45)\\).

```python
>>> xs = odeint(func=dx, y0=[.55, .45], t=t, args=(create_A(),))
>>> plt.plot(xs)
```

![]({{site.baseurl}}/assets/images/meritocracy_evolution.svg)

We see that very quickly the proportion of women in our population decreases.
This is simply due to the evolutionary fact that one of the types of individual
(the men) is creating an environment which is more accommodating to that type of
individual (men).

Note that if we run this with a perfect initial population then we get:

```python
>>> xs = odeint(func=dx, y0=[.5, .5], t=t, args=(create_A(),))
>>> plt.plot(xs)
```

![]({{site.baseurl}}/assets/images/meritocracy_evolution_perfect.svg)

So indeed, even with a slight bias (\\(r=1.05\\) when there is a perfect initial
situation then the gender balance remains. I won't go in to it here but this
would fail to be evolutionarily stable (ie it would not be stable given a small
random mutation).

Of course, this is a relatively simple model and there are far more dynamics
to consider but I'm hoping to have demonstrated one of the problems with a
meritocracy which is it makes sense in an ideal world. Sadly, we all have too
many unconscious biases for this to hold.

That doesn't mean all is lost. Just as is described in that Royal Society
video on unconscious bias, it's important to be aware of our biases and attempt
to keep them in mind.

For example, when I read my research students' work, if my initial reaction is
that it's "not good" but that that's because it's actually "different to how I
would have done it". This doesn't make me a terrible person, it's a normal
unconscious bias and because I *try* to be aware of them I correct myself and
realise that in fact the diversity offered by the writing of my students is not
only good but far better than what I would have written myself.

There are (at least) two reasons to actively strive for diversity:

- It's the right thing to do;
- It actually ensures things are better for everyone.

Whilst we are (very) far from where we need to be in Mathematics (and a number
of other subjects of course) it is something that many are trying to improve.
Recognising our biases is an important requirement and this includes
acknowledging the fallacy of a meritocracy.
