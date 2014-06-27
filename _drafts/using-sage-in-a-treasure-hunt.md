---
layout: post
title:  "Using Sage in a Treasure hunt"
categories: Mathematics
tags:
- Sage
- Python
- Treasure Hunt
- Operational Research
- ESI
---

Here is my first post using [jekyll](http://jekyllrb.com/), I'll see how this goes and potentially migrate my blog completely to here.

This past year I've had a very minor role helping to organise the [EURO Summer Institute for Healthcare](http://orahs.di.unito.it/eswi.html).
This took part from June 11 to 20 and it was really cool with 20 (ish) young academics (from first year PhD student to early years of Post Doc) coming together to present a paper they're working on and get bespoke feedback from peers and an expert in the field.

The academic activities are really valuable but arguably of more value is the fact that everyone comes together and has a good time.
One such 'good time' was a treasure hunt that because of some people dropping out of I was lucky enough to take part in.
This was really great fun and in this post I'll describe the problems as well as the [Sage](http://sagemath.org/) code my team used to __almost__ win!

Here's a photo of Pieter, Omar, Jenny and I:

![]()

So I finally decided to try out `jekyll`. I mist say that I'm really impressed: it's so light weight!

I looked at various tutorials and as I'm planning on deploying this (and possibly moving my [blog](http://drvinceknight.blogspot.co.uk/)) using github I took a look at theirs *but* it seemed a little tricky so I just followed the actual [`jekyll` tutorial](http://jekyllrb.com/docs/quickstart/).

The first step was to install `jekyll`:

{% highlight bash %}
$ gem install jekyll
{% endhighlight %}

Then I created the base site for my blog:

{% highlight bash %}
$ jekyll unpeudemath
{% endhighlight %}

[Here is another post]({{site.baseurl}}{% post_url 2014-06-26-welcome-to-jekyll %}).

Here is a picture:

![some text]({{site.baseurl}}/assets/waterfall.jpg)

Here is some mathematics \\(x^2=1\\):

\\[x=\pm 1\\]
