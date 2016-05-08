---
layout     : post
title      : "A suggested directory structure for Academia"
categories : acdemia
tags       :
- academia
- general
comments   : true
---

I would say that I've been learning how to use a computer properly for about 5
years or so now. Once I started to understand things a bit more I realised I
wanted a good directory structure for keeping this neat and organised. I
searched for one but did not find any (which I found surprising!). So here is a
very brief description of how I organise my directories.

Some principles:

- I version control everything I can
- I want short names for directories

So here is what it looks like:

```bash
~
|---/tch  # All my teaching materials (mainly git repos that gh-pages serves)
|---/rsc  # All current research (papers)
|---/src  # All source code for software
|---/www  # Any purely web based things (like this blog)
|---/acv  # An archive (subdirectories for each year: 2014, 2015...)
|---/tmp  # For things I do not care about (mainly throway code gists)
|---/etc  # Anything else
|---/.dotfiles  # All my dot files (see below for some details)
|---/.bup  # Versioninig of my whole system (see below for some details)
|---/Dropbox  # You know: the cloud and stuff
```

**I'm writing this in the hope that someone actually points me to something better
than the above :)**

**Some minor details:**

I pay for a Dropbox account so any big binaries, shared projects with non
version control using collaborators or anything else that doesn't quite work
with version control goes in there. I also use it in conjunction with
[git-remote-dropbox](https://github.com/anishathalye/git-remote-dropbox) to in
essence have an infinite amount of private git repos.

I use [dotbot](https://github.com/anishathalye/dotbot) to keep all my dotfiles
organised and have them in [github
repository](https://github.com/drvinceknight/dotfiles) where the README.md is
basically a set of instructions to myself for setting up a new machines.

I use [bup](https://github.com/bup/bup) as a backup system (one of many,
including the tried and tested time machine on my Mac). I've got this setup with
[cron](https://en.wikipedia.org/wiki/Cron) to automatically run **when I start
my machine**. That means that it is automatically creating a snapshot of my
system when I start it up: so I can easily revert changes if need be. This is
basically a layer of redundancy on top of my use of version control but has
already proved useful.  **I'm going to write another blog post some time about
how I use that in conjunction with Dropbox for robust offsite backup.**
