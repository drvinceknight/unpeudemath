---
layout     : post
title      : "My 5 reasons why jekyll is a terrible teaching tool."
categories : pedagogy
tags       :
- jekyll
comments   : false
---

For the past year or so I have been using [jekyll](http://jekyllrb.com/) for all
my courses.
If you do not know, in a nutshell, jekyll is a ruby framework that lets you
write templates for pages and build nice websites using static markdown files
for your content.
Here I will describe what I think of jekyll from a pedagogic point of view, in 5 main points.

## 1. Jekyll is terrible because the tutorial is too well written and easy to follow.

First of all, as an academic I enjoy when things are difficult to read and
follow.
The Jekyll tutorial can get you up and running with a jekyll site in less than 5
minutes.
It is far too clear and easy to follow.
This sort of clear and to the point
explanation is very dangerous from a pedagogic point of view as students might
stumble upon it and raise their expectations of the educational process they are
going through.

In all seriousness, the tutorial is well written and clear, with a basic
knowledge of the command line you can modify the base site and have a website
deployed in less than 10 minutes.

## 2. Jekyll is terrible because it works too seamlessly with github.

First of all gh-pages takes care of the hosting.
Not having to use a complicated server saves far too much time.
As academics we have too much free time already, I do not like getting bored.

Github promotes the sharing and openness of code, resources and processes.
Using a jekyll site in conjunction with github means that others can
easily see and comment on all the materials as well as potentially
improve them.
This openness is dangerous as it ensures that courses are living and breathing
things as opposed to a set of notes/problem sheets that sit safely in a drawer
somewhere.

The fact that jekyll uses markdown is also a problem.
On github anyone can easily read and send a pull request (which improves things)
without really knowing markdown (let alone git).
This is very terrible indeed, [here for example is a pull request sent to me by a
student](https://github.com/drvinceknight/Computing_for_mathematics/commit/c9370a3e2880e0d6d2d3a0f4e3bb90a306783787).
The student in question found a mistake in a question sheet and asked me about it,
right there in the lab I just said 'go ahead and fix it :)' (and they did).
Involving students in the process of fixing/improving their course materials
has the potential for utter chaos.
Furthermore normalising mistakes is another big problem: all students should be
terrified of making a mistake and/or trying things.

Finally, having a personal site as a github project gives you a site at the
following url:

    username.github.io

By simply having a `gh-pages` branch for each class site, this will
automatically be served at:

    username.github.io/class-site

This is far too sensible and flexible.
Furthermore the promotion of decentralisation of content is dangerous.
If one of my class sites breaks: none of my others will be affected!!!
How can I expect any free time with such a robust system?
This is dangerously efficient.

## 3. Jekyll is terrible because it is too flexible.

You can (if you want to) include:

- [A disqus.com](https://disqus.com/) board to a template for a page which means
  that students can easily comment and talk to you about materials.
  Furthermore you can also use this to add things to your materials in a
  discussion based way, for example I have been able to far too easily to add a
  picture of a whiteboard explaining something students have asked.

- [Mathjax](https://www.mathjax.org/). With some escaping this works out of the
  box. Being able to include nicely rendered mathematics misaligns students'
  expectations as to what is on the web.

- [Sage cells](https://sagecell.sagemath.org/) can be easily popped in to
  worksheets allowing students to immediately use code to illustrate/explain a
  concept.

and various others: you can just include any html/javascript etc...

This promotion of interactive and modern resources by Jekyll is truly terrible
as it gets students away from what teaching materials should really be about:
dusty notes in the bottom of a drawer (worked fine for me).

The flexibility of Jekyll is also really terrible as it makes me forget the
restrictions imposed on me by whatever VLE we are supposed to use.
This is making me weak and soft, when someone takes the choice away from me and
I am forced to use the VLE, I most probably won't be ready.

(A jekyll + github setup also implis that a wiki immediately exists for a page
and I am also experimenting with a [gitter.im](https://gitter.im) room for each class).

## 4. Jekyll is terrible because it gives a responsive site out of the box.

Students should consume their materials exactly when and how we want them to.
The base jekyll site cames with a basic responsive framework, here is a photo of
one of my class sheets (which also again shows the disgustingly beautifully
rendered mathematics):

![]({{site.baseurl}}/assets/images/jekyll_site.png)

This responsive framework works right out of the box (you can also obviously use
further frameworks if you want to, see my point about flexibility) from the tutorial and this
encourages students to have access to the materials on whatever platform they
want whenever they want.
This cannot be a good thing.

## 5. Jekyll is terrible because it saves me too much time.

The main point that is truly worrying about jekyll is how much time it saves me.
I have mentioned this before, as academics we need to constantly make sure we do
not get bored.
Jekyll does not help with this.

I can edit my files using whatever system I want (I can even do this on github
directly if I wanted to), I push and the website is up to date.

In the past I would have a lot of time taken up by compiling a LaTeX document
and uploading to our VLE.
I would sit back and worry about being bored before realising (thankfully) that
I had a typo and so needed to write, delete and upload again.

Furthermore, I can easily use the github issue tracker to keep on top of to do
lists etc... (which I am actually beginning to do for more or less every aspect
of my life).
TAs can also easily fix/improve minor things without asking me to upload
whatever it is they wrote.

Github + Jekyll works seamlessly and ensures that I have more time to respond to
student queries and think.
This time for reflection on teaching practice is dangerous: I might choose to do
things differently than how they have been done for the past 100 years.
