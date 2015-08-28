---
layout     : post
title      : "Natural language processing of new jokes from 2015"
categories : code
tags       :
- python
- natural language processing
- Edinburgh fringe festival
- jokes
comments   : true
---

This is a brief update to a previous post: ["Python, natural language processing
and predicting
funny"]({{site.baseurl}}/code/2015/06/14/natural-language-and-predicting-funny/).
In that post I carried out some basic natural language processing with Python to
predict whether or not a joke is funny. In this post I just update that with
some more data from this year's [Edinburgh Fringe
festival](http://www.bbc.co.uk/news/uk-scotland-edinburgh-east-fife-34039927).

Take a look at [the ipython
notebook](https://github.com/drvinceknight/EdinburghFringeJokes/blob/master/nlp-of-jokes-2015.ipynb) which shows graphics and outputs of all the jokes.
Interestingly this year's winning joke is not deemed funny by the basic model :)
but overall was 60% right this year (which is pretty good compared to last
year).

Here is a summary plot of the classifiers for different thresholds of 'funny':

![]({{site.baseurl}}/assets/images/joke_classification_moving_ratio_threshold-all.png)

The corresponding plot this year (with the new data):

![]({{site.baseurl}}/assets/images/joke_classification_moving_ratio_threshold-all-2015.png)

Take a look at the notebook file and by all means grab [the csv
file](https://github.com/drvinceknight/EdinburghFringeJokes/blob/master/jokes.csv) to
play (but do let me know how you get on :)).
