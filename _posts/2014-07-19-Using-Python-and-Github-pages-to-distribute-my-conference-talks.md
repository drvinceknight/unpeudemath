---
layout: post
title:  "Using Github pages and Python to distribute my conference talks"
categories: Code
tags:
- Python
- Conference
- Github
comments: false
---

I'm very conscious about wanting to share as much of what I do as a research/instructor in as easy a way as possible.
One example of this is the slides/decks that I use for talks I give.
3 or 4 years ago I was doing this with a Dropbox link.
More recently this has lead to me putting everything on github but this wasn't ideal as I've started to accumulate a large number of repositories for the various talks I give.

**One of the great things about using github though is that for html presentations ([reveal.js](http://lab.hakim.se/reveal-js/#/) is the one I've used a couple of times), you can use the github deployement branch `gh-pages` to serve the files directly.**
A while back I put a video together showing how to do this:

<iframe width="560" height="315" src="//www.youtube.com/embed/bNVU82qP1n4" frameborder="0" allowfullscreen></iframe>

So there are positives and negatives.
After moving to a [jekyll](http://jekyllrb.com/) framework for my blog I started thinking of a way of getting all the positives without any negatives...

- I want to use a git+github workflow;
- I don't want to have a bunch of separate repositories anymore;
- I want to be able to just write my talks and they automatically appear online.

My immediate thought was to just use jekyll but **as far as I can tell** I'd have to hack it a bit to get blog posts be actual .pdf files (for my beamer slides) (**please tell me if I'm wrong!**).
I could of course write a short blog post with a link to the file but this was one extra step to just writing my talk that I didn't want to have to do.
Instead of hacking jekyll a bit I decided to write a very simple Python script.
You can see it [here](https://github.com/drvinceknight/Talks/blob/master/serve.py) but I'll use this blog post to just walk through how it works.

I have a `Talks` repository:

{% highlight bash %}
~$ cd Talks
Talks$ ls

2014-07-07-Using-a-flipped-classroom-in-a-large-programming-course-for-mathematicians
2014-07-09-Embedding-entrepreneurial-learning-through-the-teaching-of-programming-in-a-large-flipped-classroom
2014-07-25-Measuring-the-Price-of-Anarchy-in-Critical-Care-Unit-Interactions
README.md
favicon.ico
footer.html
head.html
header.html
index.html
main.css
reveal.js
serve.py
{% endhighlight %}

What you can see in there are 3 directories (each starting with a date) and various other files.
In each of the talk directories I just have normal files for those talks:

{% highlight bash %}
Talks$ cd 2014-07-25-Measuring-the-Price-of-Anarchy-in-Critical-Care-Unit-Interactions/
...$ ls

2014-07-25-Measuring-the-Price-of-Anarchy-in-Critical-Care-Unit-Interactions.nav    2014-07-25-Measuring-the-Price-of-Anarchy-in-Critical-Care-Unit-Interactions.snm
2014-07-25-Measuring-the-Price-of-Anarchy-in-Critical-Care-Unit-Interactions.pdf    2014-07-25-Measuring-the-Price-of-Anarchy-in-Critical-Care-Unit-Interactions.tex
{% endhighlight %}

I can work on those slides just as I normally would.
Once I'm ready I go back to the root of my Talks directory and run the `serve.py` script:

{% highlight bash %}
Talks$ python serve.py
{% endhighlight %}

This file automatically goes through my sub-directories reading the date from the directory names and identifying `.html` or `.pdf` files as talks.
This creates the `index.html` file which is an index of all my talks (sorted by date) with a link to the right file.
To get the site online you simply need to push it to the gh-pages branch of your github repository.

You can see the site here: [drvinceknight.github.io/Talks](http://drvinceknight.github.io/Talks/).
Clicking on relevant links brings up the live version of my talk, or at least as live as my latest push to the github gh-pages branch.

The python script itself is just:

{% highlight python linenos %}
#!/usr/bin/env python
"""
Script to index the talks in this repository and create an index.html file.
"""
import os
import glob
import re

root = "./"
directories = sorted([name for name in os.listdir(root) if os.path.isdir(os.path.join(root, name))], reverse=True)
talk_formats = ['.pdf', '.html']


index = open('index.html', 'w')
index.write(open('head.html', 'r').read())
index.write(open('header.html', 'r').read())

index.write("""
            <body>
            <div class="page-content">
            <div class="wrap">
            <div class="home">
            <ul class='posts'>""")

for dir in directories:
    if dir not in ['.git', 'reveal.js']:
        talk = [f for f in glob.glob(root + dir + "/" + dir[:10] + '*') if  os.path.splitext(f)[1] in talk_formats][0]
        date = talk[len(root+dir) + 1: len(root + dir) + 11]
        title, extension =  os.path.splitext(talk[len(root+dir)+11:].replace("-", " "))
        index.write("""
                    <li>
                    <span class="post-date">%s [%s]</span>
                    <a class="post-link" href="%s">%s</a>
                    <p>
                    <a href="%s">(Source files)</a>
                    </p>
                    </li>
                    """ % (date, extension[1:], talk, title, 'https://github.com/drvinceknight/Talks/tree/gh-pages/' + dir ))
index.write("""
            </ul>
            </div>
            </div>
            </div>
            """)
index.write(open('footer.html', 'r').read())
index.write("</body>")
index.close()
{% endhighlight %}

The main lines that do anything are lines 25-38, everything else just reads in the relevant header and footer files.

So now getting my talks written and online is hardly an effort at all:

{% highlight bash %}
# Write awesome talk
Talks$ git commit -am 'Finished talk on proof of finite number of primes'  # This I would do anyway
Talks$ python serve.py  # This is the 1 extra thing I need to do
Talks$ git push origin  # This I would do anyway
{% endhighlight %}

There are various things that could be done to improve this (including pushing via `serve.py` as an option) and I'm not completely convinced I can't just use `jekyll` for this but it was quicker to write that script then to figure it out (or at least that was my conclusion after googling twice).

If anyone has any fixes/improvements (including: "You idiot just run jekyll with the `build-academic-conference-talk-site` flag") that'd be super appreciated and if you want to see the Talk repository (with python script, css files, header.html etc...) it's here: [github.com/drvinceknight/Talks](https://github.com/drvinceknight/Talks).

Now to finish writing my talk for [ORAHS2014](http://www.orahs2014.fc.ul.pt/)...
