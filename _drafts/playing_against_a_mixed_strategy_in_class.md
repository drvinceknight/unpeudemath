---
layout     : post
title      : "Playing against a mixed strategy in class"
categories : pedagogy
tags       :
- pedagogy
comments   : false
---

This post if very late but I have been very busy with some really exciting things.
I will describe some of the data gathered in class when we played against a random strategy played by a computer.
I have recently helped organise a conference in [Namibia](www.python-namibia.org) teaching Python.
It was a tremendous experience and I will write a post about that soon.

We played against a modified version of matching pennies which we have used quite a few times:

$$
\begin{pmatrix}
(2,-2) & (-2,2)\\
(-1,1) & (1,-1)
\end{pmatrix}
$$

I wrote a sage interact that allows for a quick visualisation of a random sample from a mixed strategy.
You can find the code for that [at the blog post I wrote last year](http://drvinceknight.blogspot.co.uk/2014/02/best-responses-to-mixed-strategies-in.html).
You can also find a python script with all the data [here](https://gist.github.com/d9af5f1bc6b24b9033d2).

I handed out sheets of papers on which students would input their preferred strategies ('H' or 'T') whilst I sampled randomly from 3 different mixed strategies:

1. \\(\sigma_1 = (.2, .8)\\)
2. \\(\sigma_1 = (.9, .1)\\)
3. \\(\sigma_1 = (1/3, 2/3\\)

Based on the class notation that implies that the computer was the row player and the students the column player.
The sampled strategies were:

1. TTTTTH
2. HHHHHH
3. HTTTHH

### Round 1

This mixed strategy (recall \\(\sigma_1=(.2,.8)\\)) implies that the computer will be mainly playing T (the second strategy equivalent to the second row), and so based on the bi-matrix it is in the students interest to play H.
Here is a plot of the mixed strategy played by all the students:

![]({{site.baseurl}}/assets/images/0strategiesvbestresponse.png)

The mixed strategy played was \\(\sigma_2=(.71,.29)\\).
Note that in fact in this particular instance that actual best response is to play \\(\sigma_2=(1,0)\\).
This will indeed maximise the expected value of:

$$
u_2(\sigma_1, (x, 1-x)) = -2 \times .2 \times x + .8 \times x + 2 \times .2 \times (1-x) - .8 \times (1-x)
$$

Indeed: the above is an increasing linear function in \\(x\\) so the highest value is obtained when \\(x=1\\).

The mean score for this round by everyone was: 2.09.
The theoretical mean score (when playing the best response is): \\(.8\times 2-.2=1.4\\), so students manager to actually do better than the expected mean.

Here is a distribution of the scores:

![]({{site.baseurl}}/assets/images/0score_histogram.png)
