---
layout     : post
title      : "Verifying a neat identity: showing a connection between linear algebra and calculus"
categories : math
tags       :
- python
- math
comments   : true
---

My PhD student [Nikoleta](https://twitter.com/NikoletaGlyn) and I are doing some
work relating the Prisoner's Dilemma to quadratic forms (a linear algebraic
generalisation of quadratics) and it's led me to really come to appreciate a
specific identity regarding their derivatives. In this post I'll describe what
the identity is and what it means but also verify it using Python.

Let us assume we have 2 symbolic variables: \\(x, y\\) and we have a polynomial
expression in these two variables where the degree of each term is 2:

$$
P(x, y) = - x ^ 2 - 4 x y + y ^ 2 
$$

Here is a heatmap of it:

![]({{site.baseurl}}/assets/images/plot_of_quadratic_form.svg)


A [quadratic form](https://en.wikipedia.org/wiki/Quadratic_form) has the nice
property that it can be represented using a linear algebraic representation. If
we let:

$$
v = 
\begin{pmatrix}
x\\
y
\end{pmatrix}
$$

and

$$
A = \begin{pmatrix}
-1 & -2\\
-2 & 1
\end{pmatrix}
$$

then:

$$
P(x, y) = v ^ T A v
$$

(\\(v ^ T\\) denotes the transpose of \\(v\\) so it's a row vector.)

Let's start by verifying this using [Sympy](http://www.sympy.org/en/index.html)
(the Python library for symbolic mathematics):


```python
>>> import sympy as sym
>>> x, y = sym.symbols("x, y")
>>> quadratic_form =  - x ** 2 - 4 * x * y + y ** 2 
>>> quadratic_form
-x**2 - 4*x*y + y**2
>>> v = sym.Matrix([[x], [y]])
>>> A = sym.Matrix([[-sym.S(1), - sym.S(2)], [-sym.S(2), sym.S(1)]])
>>> ((v.transpose() * A * v)[0, 0]).expand() == quadratic_form
True

```

The identity that my student and I have been using is for the derivative
of a quadratic form:

$$
\frac{dv ^ T A v}{dv} = 2v^T(A + A^ T)
$$

and more specifically in the case where \\(A ^ T = A\\) (\\(A ^ T\\) is the
transpose of \\(A\\)):

$$
\frac{dv ^ T A v}{dv} = 2v^TA
$$

A good overview of the mathematical background behind this is given here:
[http://michael.orlitzky.com/articles/the_derivative_of_a_quadratic_form.xhtml](http://michael.orlitzky.com/articles/the_derivative_of_a_quadratic_form.xhtml).

One of the intuitive reasons why this is "nice" and/or "looks right" is that it
looks eerily familiar to \\(\frac{dx^2}{dx}=2x\\): the derivative of the most
basic quadratic.

The first thing to realise about \\(2v^TA\\) is that it is a row vector. Each
element of the vector corresponds to the partial derivate of the
quadratic form according to each variable.

In our case:

$$\frac{dP}{dx}=-2x-4y$$

$$\frac{dP}{dy}=-4x+2y$$

Here is how to do these derivatives using Sympy:

```python
>>> sym.diff(quadratic_form, x)
-2*x - 4*y
>>> sym.diff(quadratic_form, y)
-4*x + 2*y

```

The identify above shows that we do not need to do any differentiation
at all to obtain this: we can instead do a linear algebraic manipulation:

$$
2v^TA=2(x, y)
\begin{pmatrix}
-1 & -2\\
-2 & 1
\end{pmatrix}=
(-2x - 4y, -4x+2y)
$$

We see that the only stationary point is \\((x, y)=(0, 0)\\) (which we can
see in the picture above).

This can extend to larger quadratic forms: indeed this holds for any
quadratic form over any number of variables.
