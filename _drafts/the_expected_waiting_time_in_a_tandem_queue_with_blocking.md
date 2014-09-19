---
layout     : post
title      : "Calculating the expected wait in a tandem queue with blocking"
categories : code
tags       :
- mathematics
- queueing theory
- sage
comments   : false
---

In this post I'll describe a particular mathematical model that I've been working on for the purpose of a research paper.
This is actually part of some work that I've done with [+James Campbell](https://plus.google.com/+JamesCampbell95/posts) an undergraduate who worked with me over the Summer.

Consider the system shown in the picture below:

![]({{site.baseurl}}/assets/images/tandem_queue.png)

This is a system composed of 'two queues in tandem' each with a number of servers \\(c\\) and a service rate \\(\mu\\).
It is assumed here (as is very familiar in queueing theory) that the service rate is exponentially distributed (in effect that the service time is random with mean \\(\mu\\)).

Individuals arrive at the queue with mean inter arrival time \\(\Lambda\\) (once again exponentially distributed).

There is room for up to \\(N\\) individuals to wait for a free server at the first station.
After their service at the first station is complete, individuals leave the system with probability \\(p\\), but if they don't and there is no free place in the next station (ie there are not less than \\(c_2\\) individuals in the second service center) then they become blocked.

There are a vast array of applications of queueing systems like the above (in particular in the paper we're working on we're using it to model a healthcare system).

**In this post I'll describe how to use Markov chains to be able to describe the system and in particular how to get the expected wait for an arrival at the queue.**

I have discussed Markov chains before (mainly posts on my old blog) and so I won't go in to too much detail about the underlying theory (I think this is perhaps a slightly technical post so is mainly aimed at people familiar with queueing theory but by all means ask in the comments if I can clarify anything).

**The state space**

One has to think about this carefully as it's important to keep track not only of where individuals are but whether or not they are blocked.
Based on that one might think of using a 3 dimensional state space: \\((i,j,k)\\) where \\(i\\) would denote the number of people at the first station, \\(j\\) the number at the second and \\(k\\) the number at the first who are blocked.
This wouldn't be a terrible idea but we can actually do things in a slightly neater and more compact way:

$$
S = \left\{(i,j)\in\mathbb{Z}^{2}_{\geq 0}\;|\;0\leq j \leq c_1+c_2,\; 0\leq i\leq c_1+N-\max(j-c_2,0)\right\}
$$

In the above \\(i\\) denotes the number of individuals in service or waiting for service at the first station and \\(j\\) denotes the number of individuals in service at the second station **or** blocked at the second station.

The continuous time transition rates between two states \\((i_1,j_1)\\) and \\((i_2, j_2)\\) are given by:

$$
q_{(i_1,j_1), (i_2,j_2)}=
    \begin{cases}
    \Lambda, & \text{ if } \delta = (1,0)\\
    \min(c_1-\max(j_1-c_2,0),i_1)(1-p)\mu_1, & \text{ if } \delta = (-1,1)\\
    \min(c_1-\max(j_1-c_2,0),i_1)p\mu_1, & \text{ if } \delta = (-1,0)\\
    \min(c_2, j_1)\mu_2, & \text{ if } \delta = (0,-1)
    \end{cases}
$$

where \\(\delta=(i_2,j_2)-(i_1,j_1)\\).

Here's a picture of the Markov Chain for \\(N=c_1=c_2=2\\):

![]({{site.baseurl}}/assets/images/small_chain.png)

Using the above we can index our states and keep all the information in a matrix \\(Q\\), to obtain the steady state distributions of the chain (the probabilities of finding the queue in a given state) we then simply solve the following equation:

$$
\pi Q = 0
$$

subject to \\(\sum \pi = 1\\).

Here's how we can do this using [Sage](http://sagemath.org/):


