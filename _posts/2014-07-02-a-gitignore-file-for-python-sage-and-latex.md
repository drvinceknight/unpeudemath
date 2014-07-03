---
layout: post
title:  "A gitignore file for Python (Sage) and LaTeX"
categories: Mathematics
tags:
- Sage
- Python
- LaTeX
comments: true
---

The main tools I use on a day to day basis are Python/Sage and LaTeX.
Since learning to love git and even more so github my usual workflow when starting a new project is something like this:

{% highlight bash %}
$ git init
$ vim proof_that_there_are_a_finite_number_of_primes.py
...
$ vim application_for_fields_medal.tex
$ latexmk --xelatex application_for_fields_medal.tex
$ git status
{% endhighlight %}

Once I run the git status that's when I realise that I've now got a bunch of files I don't want to commit `.aux`, `.pyc` etc...

I then normally throw whatever those files are to a `.gitignore` file.
Despite teaching my students to never do anything twice and to always script whatever can be scripted: I have never actually put a `.gitignore` file together that has everything in it.

So here's my first attempt.

This is basically a modification of the Python github `.gitignore` and a slight tweak of [this gist](https://gist.github.com/kogakure/149016) (there doesn't seem to be a bespoke LaTeX .gitignore as an option when you create a repository).

{% highlight vim %}
# LaTeX Files
*.aux
*.glo
*.idx
*.log
*.toc
*.ist
*.acn
*.acr
*.alg
*.bbl
*.blg
*.dvi
*.glg
*.gls
*.ilg
*.ind
*.lof
*.lot
*.maf
*.mtc
*.mtc1
*.out
*.synctex.gz
*.fdb_latexmk
*.fls
*.nav
*.snm

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]

# C extensions
*.so

# Distribution / packaging
.Python
env/
bin/
build/
develop-eggs/
dist/
eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.cache
nosetests.xml
coverage.xml

# Translations
*.mo

# Mr Developer
.mr.developer.cfg
.project
.pydevproject

# Rope
.ropeproject

# Django stuff:
*.log
*.pot

# Sphinx documentation
docs/_build/
{% endhighlight %}

You can find this at [this gist](https://gist.github.com/drvinceknight/060f091a61b91e3b449b).

If anyone can suggest anything I'm missing it'd be great to hear it :)
