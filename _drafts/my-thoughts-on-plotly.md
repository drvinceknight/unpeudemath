---
layout     : post
title      : "My thoughts on plotly ('the github for plots')"
categories : code
tags       :
- python
comments   : false
---

A while ago I saw [plotly](https://plot.ly/) appear on my G+ stream.
People seemed excited about it but I was too busy to look at it properly and just assumed: _must be some sort of new matplotlib_:

![](http://i0.kym-cdn.com/photos/images/newsfeed/000/284/529/e65.gif)

Then, one of the guys from plotly reached out saying I should take a look.
I took a brief glance and realise this was **nothing like a new matplotlib** and in fact looked pretty cool.
So I dutifully put it on my to do list but very much near the bottom.

I'm writing this sat in between sessions at [PyconUK 2014](http://pyconuk.org/).
One of the talks on the first day was by Chris from plotly.
He gave a great talk (which once the video link is up I'll share here) and I immediately threw 'check out plotly' to the top of my to do list.

**How I got started**

- I created an account at [https://plot.ly/](https://plot.ly/);
- I copied and pasted the code from the ['getting started guide'](https://plot.ly/python/getting-started/) which takes you threw setting up your plotly credentials etc...
- I ran the matplotlib code [https://plot.ly/matplotlib/](https://plot.ly/matplotlib/). Which if you look carefully basically is just matplotlib code with an added line `plot_url = py.plot_mpl(fig)`:

{% highlight python %}
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import plotly.plotly as py

n = 50
x, y, z, s, ew = np.random.rand(5, n)
c, ec = np.random.rand(2, n, 4)
area_scale, width_scale = 500, 5

fig, ax = plt.subplots()
sc = ax.scatter(x, y, c=c,
                s=np.square(s)*area_scale,
                edgecolor=ec,
                linewidth=ew*width_scale)
ax.grid()

plot_url = py.plot_mpl(fig)
{% endhighlight %}

That code automatically creates the following plotly plot (which you can edit, zoom in etc...):

<iframe width="460" height="345" frameborder="0" seamless="seamless" scrolling="no" src="https://plot.ly/~drvinceknight/1.embed?width=460&height=345"></iframe>

**Doing something of my own**

In [my previous post]({{site.baseurl}}/code/2014/09/19/the-expected-waiting-time-in-a-tandem-queue-with-blocking-using-sage/) I wrote about ...
