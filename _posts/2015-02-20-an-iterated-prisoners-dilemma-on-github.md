---
layout     : post
title      : "An iterated prisoner's dilemma on github"
categories : code
tags       :
- gametheory
- axelrod
comments   : true
---

In the 1980s Axelrod ran a computer tournament inviting people to contribute code that specified strategies in an iterated prisoner's dilemma tournament.
I have just finished putting the final pieces on a Python repository on github ([github.com/drvinceknight/Axelrod](https://github.com/drvinceknight/Axelrod)) to carry out the same tournament and would be delighted for people to contribute strategies via pull request (or indeed via any way possible: just get in touch).
In this post I'll describe the process of adding a strategy to the repository (the first 3 minutes of a video at the end of this post show you exactly what you are required to do).

For a good overview of the iterated prisoner's dilemma take a look at this page about [Axelrod's tournament](http://cs.stanford.edu/people/eroberts/courses/soco/projects/1998-99/game-theory/axelrod.html) but in a nutshell the idea is that two players (prisoners) repeatedly play the following game:

$$
\begin{pmatrix}
(2,2)& (5,0)\\
(0,5)& (4,4)
\end{pmatrix}
$$

If in a particular round they both cooperate (first row/column) they both accrue 2 years in prison.
If one defects (second row/column) and the other cooperates: the defector gets 0 extra years in prison and the cooperator 5.
If they both defect they each accrue 4 years in prison.

Axelrod's tournament invited contribution of strategies that took account of the history of both players over several rounds.
Thus a strategy that punished defectors would perhaps wait until a defection to do that (cooperating until then).
The tournament was a round robin with the lowest total/mean years in prison being deemed the winner.

This tournament has often been used to describe how cooperation can emerge in a population: the tit for tat strategy (which starts by cooperating and then simply repeats the previous action) won! (In fact it won both times as the tournament was repeated.)

**I have put together a github repository that allows anyone to contribute a strategy using Python to this tournament.**
You can find it here: [https://github.com/drvinceknight/Axelrod](https://github.com/drvinceknight/Axelrod).

At present I have only implemented 6 strategies and you can see the result here:

![]({{site.baseurl}}/assets/images/axelrod_results.png)

To contribute you really only need to write very simple python code.
Here is the code for the tit for tat strategy:

{% highlight python %}
from axelrod import Player

class TitForTat(Player):
    """
    A player starts by cooperating and then mimics previous move by opponent.
    """
    def strategy(self, opponent):
        """
        Begins by playing 'C':
        This is affected by the history of the opponent: the strategy simply repeats the last action of the opponent
        """
        try:
            return opponent.history[-1]
        except IndexError:
            return 'C'

    def __repr__(self):
        """
        The string method for the strategy.
        """
        return 'Tit For Tat'
{% endhighlight %}

That is more or less just 3 lines of code.
I'll now briefly describe adding another strategy to [this repository](https://github.com/drvinceknight/Axelrod) (and I will do it entirely using the github web interface).

I am going to add a strategy called: 'alternator' which simply alternates strategies.

First I navigate to this url: [https://github.com/drvinceknight/Axelrod/tree/master/axelrod/strategies](https://github.com/drvinceknight/Axelrod/tree/master/axelrod/strategies):

![]({{site.baseurl}}/assets/images/strategies_on_github.png)

Here I can just click on the `+` at the top of the page (after: `Axelrod/axelrod/strategies/+`).
As this is my own github repository I can just immediately start creating a file, anyone else would be taken the github process of forking the repository:

![]({{site.baseurl}}/assets/images/creating_alternator.png)

After writing the code I simply scroll down to the bottom where I am able to commit the change but others would be able to submit a pull request:

![]({{site.baseurl}}/assets/images/committing_alternator.png)

Let us take a look at the actual code I wrote for the alternator class:

{% highlight python %}
from axelrod import Player

class Alternator(Player):
    """
    A player who alternates between cooperating and defecting
    """
    def strategy(self, opponent):
        """
        Alternate 'C' and 'D'
        """
        if self.history[-1] == 'C':
            return 'D'
        return 'C'

    def __repr__(self):
        """
        The string method for the strategy:
        """
        return 'Alternator'
{% endhighlight %}

This just inherits from a `Player` class I have created previously and all it really requires are two methods:

- `strategy`: this takes in the player itself (`self`) and the opponent and must return either `C` or `D`.
    Take a look through the other strategies to see how this can be written.
- `__repr__`: this just returns what we want the strategy to look like when printed out.

After writing the code itself we also need to modify the `__init__.py` file in the `strategies` directory.
Here I have added the relevant lines:

{% highlight python %}
from cooperator import *
from defector import *
from grudger import *
from rand import *
from titfortat import *
from gobymajority import *
from alternator import *  # <- Adding this line


strategies = [
        Defector,
        Cooperator,
        TitForTat,
        Grudger,
        GoByMajority,
        Random,
        Alternator,  # And adding this line
        ]
{% endhighlight %}

Now if you want to be super awesome you can also add a test for your strategy (this helps keep things organised and working but do not let this be an obstacle to contributing a strategy).
If you want to see what the test for the alternator looks like you can find it [here](https://github.com/drvinceknight/Axelrod/blob/master/axelrod/tests/test_alternator.py) (the README has info as to how to run the tests).

The latest results (which as of the time of writing now only include the alternator as an extra strategy - **EDIT** Just before publishing this Geraint sent me a pull request for another strategy: this image is the live one from the github repo so will have more and more strategies) can be found seen here:

![](https://github.com/drvinceknight/Axelrod/raw/master/results.png)

If you clone [this repository](https://github.com/drvinceknight/Axelrod) you can obtain that plot by running:

{% highlight bash %}
$ python run_tournament.py
{% endhighlight %}

**TLDR**: Please contribute a strategy to this Python based version of Axelrod's tournament on github: [https://github.com/drvinceknight/Axelrod](https://github.com/drvinceknight/Axelrod).

This would hopefully be of interest if:

- You are slightly interested in Axelrod's work
- You like Python
- You like Game Theory
- You have never had a pull request accepted before

Here is a short video showing exactly how to contribute using nothing else than the github web interface (the first 3 minutes are all you really need to do):

<div class="video">
    <figure>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/5kOUVdktxAo" frameborder="0" allowfullscreen></iframe>
    </figure>
</div>
