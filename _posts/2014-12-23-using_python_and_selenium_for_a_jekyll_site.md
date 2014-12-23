---
layout     : post
title      : "Using Python and Selenium to write functional tests for a Jekyll site"
categories : code
tags       :
- jekyll
- python
- selenium
comments   : true
---

Over the past six months or so I've become a huge Jekyll fan.
In this post I'll briefly show how to write functional tests using Selenium for a Jekyll site.

### What are functional tests?

This is all extremely well described in [Test Driven Development with Python](http://chimera.labs.oreilly.com/books/1234000000754/ch01.html).
Functional tests are one aspect of test driven development (TDD).
They concentrate on testing that software works as it is expected to when used by the user.
TDD is the (awesome) framework in which the first thing one should do when writing code is to write a test, then check that it fails and then write code that makes it pass.
Or to put it simple "Obey the Testing Goat! Do Nothing Until You Have a Test" (that is a direct quote from the book I mentioned above).

Testing takes various forms, two of which are (the hyper links there go to the corresponding Python library):

- [Doctests](https://docs.python.org/2/library/doctest.html): this involves writing tests directly in the documentation of the code you are writing.
- [Unittests](https://docs.python.org/2/library/unittest.html): this involves writing more robust tests in a separate script.

### Let us fire up a Jekyll site (skip this if you are a jekyll regular)

This is very easy to do, after installing jekyll (see [jekyll installation instructions](http://jekyllrb.com/docs/installation/)), the following will create a base site:

{% highlight bash %}
$ jekyll new site_for_tests
New jekyll site installed in /Users/vince/site_for_tests.
{% endhighlight %}

Simply navigate to that new folder and run the following jekyll command to fire up the base site:

{% highlight bash %}
$ jekyll serve
Configuration file: /Users/vince/site_for_tests/_config.yml
            Source: /Users/vince/site_for_tests
       Destination: /Users/vince/site_for_tests/_site
      Generating...
                    done.
 Auto-regeneration: disabled. Use --watch to enable.
Configuration file: /Users/vince/site_for_tests/_config.yml
    Server address: http://0.0.0.0:4000/
  Server running... press ctrl-c to stop.
{% endhighlight %}

Then open up a browser and throw `http://0.0.0.0:4000/` in to the url, the base site will come up:

![]({{site.baseurl}}/assets/images/base_jekyll.png)

Now we are ready to write a Selenium testing framework

### Writing an initial Selenium test

So now we are going to write a test that indeed checks that the website acts like we expect.
First of all let us install the Python selenium library:

{% highlight bash %}
$ pip install selenium
{% endhighlight %}

Now let us write some tests!
Open up a file called `functional_tests.py` and fill it with this:

{% gist drvinceknight/d2494432ba5b284869ae %}

Run the tests:

{% highlight bash %}
$ python functional_tests.py
{% endhighlight %}

This will open up Firefox and (assuming all is well) return nothing in the shell.

So now let us modify the test file:

{% gist drvinceknight/b9a80c84418f750a632f %}

Note that I am getting ready to change the base jekyll template and build my site about writing tests.
Run the tests:

{% highlight bash %}
$ python new_functional_tests.py
File "new_functional_tests.py", line 6, in <module>
    assert 'How to write tests' in browser.title  # This checks that the required title is in browser title
AssertionError
{% endhighlight %}

This time around we get an assertion error :)

Now we can go about changing our site (we are doing some TDD right now).
Here is the new config file (note I have only changed the `title` field):

{% gist drvinceknight/a5d7e0d311bb0ce7f050 %}

Now when we run the tests we get no assertion error:

{% highlight bash %}
$ python new_functional_tests.py
{% endhighlight %}

This frees us up to write another test and then write another feature etc...

### Taking things further

The above is an extremely simple example of what Selenium can do and also of how to write tests.

1. If you know how to write unit tests but are not sure about Selenium take a look at [the Selenium site](http://docs.seleniumhq.org/docs/03_webdriver.jsp) (you can click on a button for Python or indeed whatever interface you would like to use). That site has a good collection of what Selenium can do (check what happens when clicking on links, checking content etc...). This is also helpful: [https://selenium-python.readthedocs.org/](https://selenium-python.readthedocs.org/).
2. If you are happy with Selenium but not unit tests then there are a variety of great tutorials around but to be honest I cannot recommend the [Test Driven Development with Python Book](http://chimera.labs.oreilly.com/books/1234000000754/ch01.html) enough. [Harry Percival](https://twitter.com/hjwp) did a great job.

Here are some tests I wrote today for the site my students have put together for [Code Club](http://cardiffmathematicscodeclub.github.io/): [https://github.com/CardiffMathematicsCodeClub/CardiffMathematicsCodeClub.github.io/blob/tests/functional_tests.py](https://github.com/CardiffMathematicsCodeClub/CardiffMathematicsCodeClub.github.io/blob/tests/functional_tests.py)

In there you can see examples of all of the above (clicking on links, checking content etc...) but also the way I document the code (using what is called a 'User Story' which explains what a user should/would see).
You can also see the way to properly 'tear down' the tests (so that Firefox closes).

I hope this is helpful for some: in essence you can use Selenium via Python for any site, to use it with jekyll all you need to do is have the local server running.
