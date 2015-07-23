---
layout     : post
title      : "Using the two thirds of the average game in class"
categories : pedagogy
tags       :
- sage
- game theory
- python
- publication
comments   : false
---

This past week I have been delighted to have a short pedagogic paper accepted
for publication in [MSOR
Connections](https://journals.gre.ac.uk/index.php/msor). The paper is entitled:
"Playing Games: A Case Study in Active Learning Applied to Game Theory". The
journal is open access and you can see a [pre print
here](https://github.com/drvinceknight/Playing-games-a-case-study-in-active-learning/blob/master/paper/paper.pdf).
As well as describing some literature on active learning I also present some
data I've been collecting (with the help of others) as to how people play two
subsequent plays of the [two thirds of the average
game](https://en.wikipedia.org/wiki/Guess_2/3_of_the_average).

In this post I'll briefly put up the results here as well as mention a
Python library I'm working on.

If you're not familiar with it, the two thirds of the average game asks players
to guess a number between 0 and 100. The closest number to 2/3rds of the average
number guessed is declared the winner.

I use this all the time in class and during outreach events. I start by asking
participants to play without more explanation than the basic rules of the game.
Following this, as a group we go over some simple best response dynamics that
indicate that the equilibrium play for the game is for everyone to guess 0.
**After this explanation, everyone plas again.**

Below you can see how this game has gone as a collection of all the data I've
put together:

![]({{site.baseurl}}/assets/images/histogram_of_guesses.png)

You will note that some participants actually increase their second guess but in
general we see a possible indication (based on two data points, so obviously
this is not meant to be a conclusive statement) of convergence towards the
theoretic equilibria.

Here is a plot showing the relationship between the first and second guess (when
removing the guesses that increase, although as you can see in the paper this
does not make much difference):

![]({{site.baseurl}}/assets/images/jointplot_of_guesses_removing_increasing_guesses.png)

The significant linear relationship between the guesses is given by:

$$
(\text{Second guess}) = .33(\text{First guess}) + .20
$$

So a good indication of what someone will guess in the second round is that it
would be a third of their first round guess.

Here is some Sage code that produces the cobweb diagram assuming the following
sequence represents each guess (using [code by Marshall
Hampton](http://wiki.sagemath.org/interact/dynsys)):

$$
X\_n = X_{n-1}/3 \quad X\_0 = 66
$$

<div class="compute"><script type="text/x-sage">
def cobweb(a_function, start, mask = 0, iterations = 20, xmin = 0, xmax = 1):
    '''
    Returns a graphics object of a plot of the function and a cobweb trajectory starting from the value start.

    INPUT:
        a_function: a function of one variable
        start: the starting value of the iteration
        mask: (optional) the number of initial iterates to ignore
        iterations: (optional) the number of iterations to draw, following the masked iterations
        xmin: (optional) the lower end of the plotted interval
        xmax: (optional) the upper end of the plotted interval

    EXAMPLES:
        sage: f = lambda x: 3.9*x*(1-x)
        sage: show(cobweb(f,.01,iterations=200), xmin = 0, xmax = 1, ymin=0)

    '''
    basic_plot = plot(a_function, xmin = xmin, xmax = xmax, color='green', legend_label='$y=f(X_{n-1})$')
    id_plot = plot(lambda x: x, xmin = xmin, xmax = xmax, legend_label='y=x')
    iter_list = []
    current = start
    for i in range(mask):
        current = a_function(current)
    for i in range(iterations):
        iter_list.append([current,a_function(current)])
        current = a_function(current)
        iter_list.append([current,current])
    cobweb = line(iter_list, rgbcolor = (1,0,0))
    return basic_plot + id_plot + cobweb

cobweb(lambda x:x/3, 66, xmax=100)
</script></div>

that plot shows the iterations of the hypothetical guesses if we were to play more rounds :)

**The other thing** I wanted to point at in this blog post is this
[twothirds](https://github.com/drvinceknight/TwoThirds) library which will
potentially allow anyone to analyse these games quickly. I'm still working on
it but if it's of interest please do jump in :) I have put up a [Jupyter
notebook demoing what it can do so far (which is almost everything but with
some rough
edges)](https://github.com/drvinceknight/TwoThirds/blob/master/demo.ipynb). If
you want to try it out, download that notebook and run:

{% highlight bash %}
$ pip install twothirds
{% endhighlight %}

I hope that once the library is set up anyone who uses it could simply send
over data of game plays via PR which would help update the above plots and
conclusions :)
