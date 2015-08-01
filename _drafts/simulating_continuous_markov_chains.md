---
layout     : post
title      : "Simulating continuous Markov chains"
categories : code
tags       :
- jekyll
- sage
- python
comments   : false
---

In a blog post I wrote in 2013, [I showed how to simulate a discrete Markov
chain](http://drvinceknight.blogspot.co.uk/2013/10/pigeon-holes-markov-chains-and-sagemath.html).
In this post I'll show how to do the same with a continuous chain which can be
used to speedily obtain steady state distributions for models of queueing
processes for example.

A continuous Markov chain is defined by a transition **rate** matrix which shows
the rates at which transitions from 1 state to an other occur. Here is an
example of a continuous Markov chain:

![]({{site.baseurl}}/assets/images/continuous_markov_chain_example)

This has transition rate matrix \\(Q\\) given by:

$$
Q = \begin{pmatrix}
-6&5&1\\
1&-2&1\\
1&8&-9\\
\end{pmatrix}
$$

The diagonals have negative entries, which can be interpreted as a rate of _no
change_. To obtain the steady state probabilities \\(\pi\\) for this chain we
can solve the following matrix equation:

$$
\pi Q = 0
$$

if we include the fact that the sum of \\(\pi\\) must be 1 (so that it is indeed
a probability vector) we can obtain the probabilities in
[Sagemath](http://www.sagemath.org/) using the following:

You can run this here (just click on 'Evaluate'):

{% highlight python %}
Q = matrix(QQ, [[-3, 2, 1], [1, -5, 4], [1, 8, -9]])
(transpose(Q).stack(vector([1,1,1])).solve_right(vector([0,0,0,1])))
{% endhighlight %}

<div class="compute"><script type="text/x-sage">
Q = matrix(QQ, [[-3, 2, 1], [1, -5, 4], [1, 8, -9]])
(transpose(Q).stack(vector([1,1,1])).solve_right(vector([0,0,0,1])))
</script></div>

This returns:

{% highlight python %}
(1/4, 1/2, 1/4)
{% endhighlight %}

Thus, if we were to randomly observe this chain:

- 25% of the time it would be in state 1;
- 50% of the time it would be in state 2;
- 25% of the time it would be in state 3.

Now, the markov chain in question means that if we're in the first state the
rate at which a change happens to go to the second state is 2 and the rate at
which a change happens that goes to the third state is 3.

Given that this is all Markovian we can sample two random numbers from the
exponential distribution and find out which of those 'changes' would happen
first so and move to that state:

{% highlight python %}
import random
[random.expovariate(2), random.expovariate(1)]
{% endhighlight %}

The above returned (for this particular instance):

{% highlight python %}
[0.5003491524841699, 0.6107995795458322]
{% endhighlight %}

So here it's going to take .5 time units to go to the second state whereas it
would take .61 time units to go to the third. Thus, the chain would transition
to the second state.

We can use this to write a function that will take a transition rate matrix,
simulate the transitions and keep track of the time spent in each state:

{% highlight python %}
def simulate_cmc(Q, time, warm_up):
    import random
    Q = list(Q)  # In case a matrix is input
    state_space = range(len(Q))  # Index the state space
    time_spent = {s:0 for s in state_space}  # Set up a dictionary to keep track of time
    clock = 0  # Keep track of the clock
    current_state = 0  # First state
    while clock < time:
        # Sample the transitions
        sojourn_times = [random.expovariate(rate) for rate in Q[current_state][:current_state]]
        sojourn_times += [oo]  # An infinite sojourn to the same state
        sojourn_times += [random.expovariate(rate) for rate in Q[current_state][current_state + 1:]]

        # Identify the next state
        next_state = min(state_space, key=lambda x: sojourn_times[x])
        sojourn = sojourn_times[next_state]
        clock += sojourn
        if clock > warm_up:  # Keep track if past warm up time
            time_spent[current_state] += sojourn
        current_state = next_state  # Transition

    pi = [time_spent[state] / sum(time_spent.values()) for state in state_space]  # Calculate probabilities
    return pi
{% endhighlight %}

Here are the probabilities from the same Markov chain as above:

<div class="compute"><script type="text/x-sage">
def simulate_cmc(Q, time, warm_up):
    import random
    Q = list(Q)  # In case a matrix is input
    state_space = range(len(Q))  # Index the state space
    time_spent = {s:0 for s in state_space}  # Set up a dictionary to keep track of time
    clock = 0  # Keep track of the clock
    current_state = 0  # First state
    while clock < time:
        # Sample the transitions
        sojourn_times = [random.expovariate(rate) for rate in Q[current_state][:current_state]]
        sojourn_times += [oo]  # An infinite sojourn to the same state
        sojourn_times += [random.expovariate(rate) for rate in Q[current_state][current_state + 1:]]

        # Identify the next state
        next_state = min(state_space, key=lambda x: sojourn_times[x])
        sojourn = sojourn_times[next_state]
        clock += sojourn
        if clock > warm_up:  # Keep track if past warm up time
            time_spent[current_state] += sojourn
        current_state = next_state  # Transition

    pi = [time_spent[state] / sum(time_spent.values()) for state in state_space]  # Calculate probabilities
    return pi

Q = matrix(QQ, [[-3, 2, 1], [1, -5, 4], [1, 8, -9]])
simulate_cmc(Q, 3000, 500)
</script></div>

