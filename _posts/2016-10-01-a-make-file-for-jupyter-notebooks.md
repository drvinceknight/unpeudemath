---
layout     : post
title      : "Make file to convert all Jupyter notebooks in a directory to pdfs"
categories : python
tags       :
- python
comments   : true
---

I'm going to be using Jupyter notebooks for the first time in a course I'm
teaching (previously I have been using Sage notebooks and python scripting). I'd
like to be able to share my notebooks with tutors and eventually students as
both notebook but also pdfs. Thankfully the `jupyter-nbconverte` command lets
you easily convert notebooks to more or less whatever you want. Below is a
`make` file that will automatically check if any notebook files have changed and
if they have convert them to pdf.

Save the following in a file called `makefile`:

```bash
nbs = $(wildcard *.ipynb)
pdfs = $(nbs:%.ipynb=%.pdf)

all: $(pdfs)

%.pdf: %.ipynb
        jupyter-nbconvert --to pdf $<;
```

[Here it is as a gist](https://gist.github.com/fa53cd64941a9314cbba0f03abd6b556)

To run that file simply type `make` and it'll convert all your notebooks to pdf.
