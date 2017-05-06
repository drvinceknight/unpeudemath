---
layout     : post
title      : "(Re)scheduling a conference with linear programming and Python"
categories : Python
tags       :
- python
- pycon
- math
comments   : true
---

Scheduling conferences can be a time consuming tricky affair with a lot of
moving parts. This is often done in practice with committee members staring at
the various events that need to be scheduled and forcing them in to the various
rooms and times available until everything fits. In this blog post I'll describe
and illustrate a Python library that [Owen
Campbell](https://twitter.com/opcampbell), [Alex
Chan](https://twitter.com/alexwlchan) and I have written over the past week that
uses Integer Linear Programming to automatically schedule a conference:
[`conference_scheduler`](https://github.com/PyconUK/ConferenceScheduler). As an
example to illustrate this I am going to (re) schedule last year's PyCon UK:
[2016.pyconuk.org/programme/](http://2016.pyconuk.org/programme/).

## Some background

There are a number of constraints to keep track off:

- All events must actually be scheduled;
- No more than one event can be in a given slot at a given time;
- Events are only scheduled in slots for which they are available;
- Two events are scheduled at the same time only if they are available to do so;
- Talks in a given session have something in common;

This is all going to be handled mathematically by letting a schedule be
represented by a matrix of size \\(M\times N\\) where \\(M\\) is the number of
events and \\(N\\) is the number of slots in which those events can go (a slot
representing both a time and a location):

$$
X = \begin{pmatrix}
1 & 0 & 0 & 0 & 0\\
0 & 0 & 1 & 0 & 0\\
0 & 1 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 1\\
\end{pmatrix}
$$

So in that example, we have:

- The 1st event is in the first slot;
- The 2nd event is in the third slot;
- The 3rd event is in the second slot;
- The 4th event is in the fifth slot;

and the fourth slot is not used. Once we have that representation of a schedule
it is possible to represent all our constraints mathematically.

For example we want to ensure that all events (rows) are scheduled:

$$
\sum_{j=1}^NX_{ij}=1
$$

If you would
like to read a full mathematical formulation of these things take a look at the
library documentation:
http://conference-scheduler.readthedocs.io/en/latest/background/mathematical_model.html

Once we have that mathematical formulation, **integer linear programming**, a
mathematical technique for optimising problems with a lot of linearity (like
scheduling a conference!) can be used.

Linear programming is a beautiful area of mathematics with a lot of elegance
that makes use of linear algebra without anyone ever needing
to know about it.

Python has a few nice libraries for
linear programming:

- PyOmo
- Cvxopt (this does more than linear programming: it tackles convex programming)
- Pulp


In `conference_scheduler`, we have gone with
[Pulp](https://pythonhosted.org/PuLP/index.html) and what
`conference_scheduler` does is essentially wrap Pulp to transform all the
constraints on events and slots in to the mathematical constraints in the
background.

## Rescheduling PyCon Uk 2016

Looking at last year's schedule, it was over five days:

- an open day,
- three days of talks and workshops
- a final day of sprints and more workshops

For the purpose of this blog post I'll just schedule
the three days of talks.

I'll be using version 1.1.0 of `conference_scheduler` which is pip installable
(but only supports Python 3.6).

```python
$ pip install conference_scheduler
$ python
>>> import conference_scheduler
>>> assert conference_scheduler.__version__ == "1.1.0"
```

As you can see if you were to follow along with the `conference_scheduler`
tutorial:
[conference-scheduler.readthedocs.io/en/latest/tutorial/index.html](http://conference-scheduler.readthedocs.io/en/latest/tutorial/index.html) we need to build up 2 things:

- A collection of slots;
- A collection of events.

First let us build up the slots, I'm going to dynamically generate these but we
could read them in from a csv file or otherwise. (In fact, there are issues open
on the github repo about writing documentation for how to do this as I write
this:
[github.com/PyconUK/ConferenceScheduler/issues](https://github.com/PyconUK/ConferenceScheduler/issues)).

```python
>>> from conference_scheduler.resources import Slot
>>> import itertools

>>> rooms = ["Assembly room", "Room D", "Ferrier Hall", "Room C"]
>>> days = ['16-Sep-2016', '17-Sep-2016', '18-Sep-2016']
>>> times_and_durations = [('10:15', 30), ('11:15', 45), ('12:00', 30), ('12:30', 30), ('14:30', 30),
...                        ('15:00', 30), ('15:30', 30), ('16:30', 30), ('17:00', 30)]
>>> day_period = {('10:15', 30) : "Morning",
...               ('11:15', 45) : "Morning",
...               ('12:00', 30) : "Morning",
...               ('12:30', 30) : "Afternoon",
...               ('14:30', 30) : "Afternoon",
...               ('15:00', 30) : "Afternoon",
...               ('15:30', 30) : "Afternoon",
...               ('16:30', 30) : "Evening",
...               ('17:00', 30) : "Evening"}

>>> room_capacity = {"Assembly room": 500,
...                  "Room D": 100,
...                  "Ferrier Hall": 200,
...                  "Room C": 80}
```

Now to build the `Slot` instances for talks:

```python
>>> talk_slots = []
>>> for room, day, time_and_duration in itertools.product(rooms, days, times_and_durations):
...     if (room, day) not in [("Room C", '16-Sep-2016'),
...                            ("Room C", '18-Sep-2016')]: # Rooms, Days used for workshops
...         time, duration = time_and_duration
...         session = f"Talks: {day} {day_period[time_and_duration]}"
...         starts_at = f"{day} {time}"
...         capacity = room_capacity[room]
...         talk_slots.append(Slot(venue=room, starts_at=starts_at, duration=duration, session=session, capacity=capacity))
>>> len(talk_slots)
90
```

Now for some specific slots for workshops:

```python
>>> rooms = ["Room C", "Room A"]
>>> days = ['18-Sep-2016']
>>> times_and_durations = [('10:15', 90), ('11:15', 105), ('14:30', 90), ('16:30', 60)]
>>> workshop_slots = []

>>> for room, day, time_and_duration in itertools.product(rooms, days, times_and_durations):
... 	time, duration = time_and_duration
...     session = f"Workshop: {day} {time}"
...     starts_at = f"{day} {time}"
...     capacity = 80
...     workshop_slots.append(Slot(venue=room, starts_at=starts_at, duration=duration, session=session, capacity=capacity))
>>> len(workshop_slots)
8
```

There are a couple of other special slots: on each day the conference is opened with a plenary session:

```python
>>> plenary_slots = [Slot(venue="Assembly Room", starts_at='16-Sep-2016 09:10', duration=50, session="Plenary: 16-Sep-2016", capacity=500),
...                  Slot(venue="Assembly Room", starts_at='17-Sep-2016 09:10', duration=50, session="Plenary: 17-Sep-2016", capacity=500),
...                  Slot(venue="Assembly Room", starts_at='18-Sep-2016 09:10', duration=50, session="Plenary: 18-Sep-2016", capacity=500)]
```

Now let us create all our events. To do this I've used a [csv
file]({{site.baseurl}}/assets/data/pycon_2016_talks.csv) which is just the talk
title, duration and a tag. I've tagged 3 of the Education talks.
Here I'll read that in and also set that all talks are unavailable to take place
during the plenary slot:

```python
>>> talks = []
>>> for row in raw_talks:
...     name = row[0]
...     duration = int(row[1])
...     tags = [row[2]] if row[2] != '' else []
...     talks.append(Event(name=name, duration=duration, tags=tags,
...                        unavailability=plenary_slots[:], demand=None))
>>> len(talks)
69
```

We want to be a bit specific with out Education talks, first of all we want them
on the last day and we also don't want any of them to take place at the same
time as each other:

```python
>>> education_talks = [talk for talk in talks if "Education" in talk.tags]
>>> slots_not_on_last_day = [slot for slot in talk_slots if ('16-Sep-2016' in  slot.starts_at) or ('17-Sep-2016' in slot.starts_at)]
>>> for talk in education_talks:
...     talk.unavailability.extend(education_talks[:])
...     talk.unavailability.extend(slots_not_on_last_day)
```

We also have the plenary talks:

```python

>>> plenary_talks = [Event(name="Python and the Glories of the UNIX Tradition",
...                        duration=50, tags=[], unavailability=talk_slots[:] + workshop_slots[:], demand=None),
...                  Event(name="Folklore and fantasy in the information age",
...                        duration=50, tags=[], unavailability=talk_slots[:] + workshop_slots[:], demand=None),
...                  Event(name="An Arabish lesson: Introducing Django to the foreign world",
...                        duration=50, tags=[], unavailability=talk_slots[:] + workshop_slots[:], demand=None)]
```

Finally, we also have the workshops:

```python
>>> workshops = [Event(name="Open Data projects with Python", duration=90, tags=[],
...                    unavailability=talk_slots[:] + plenary_slots[:],
...                    demand=None),
...              Event(name="Dive Into Object-oriented Python", duration=90, tags=[],
...                    unavailability=talk_slots[:] + plenary_slots[:],
...                    demand=None),
...              Event(name="An introduction to deep learning", duration=105, tags=[],
...                   unavailability=talk_slots[:] + plenary_slots[:],
...                   demand=None),
...              Event(name="Dive Into Object-oriented Python (cont.)", duration=105, tags=[],
...                    unavailability=talk_slots[:] + plenary_slots[:],
...                    demand=None),
...              Event(name="Python for Scientists (feat. Software Carpentry)", duration=120, tags=[],
...                    unavailability=talk_slots[:] + plenary_slots[:],
...                    demand=None),
...              Event(name="Data Wrangling with Python", duration=120, tags=[],
...                    unavailability=talk_slots[:] + plenary_slots[:],
...                    demand=None),
...              Event(name="Users are not the only people", duration=60, tags=[],
...                    unavailability=talk_slots[:] + plenary_slots[:],
...                    demand=None)]
```

Let us concatenate all our events:and slots:

```python
>>> events = talks + plenary_talks + workshops
>>> slots = talk_slots + plenary_slots + workshop_slots
```

Now we can re schedule PyCon 2016, note that this can take a little time as the
underlying mathematical problem is being solved (it took 24 seconds using the
`GPLK` solver on my low
spec laptop)

```python

>>> from conference_scheduler import scheduler
>>> schedule = scheduler.schedule(events, slots, solver=GPLK())
```

The output of `scheduler.schedule` is a generator of schedule items (a named
tuple of event and slots). Let us put that in a sorted list:

```python

schedule = sorted(schedule, key=lambda item: item.slot.starts_at)
```

Now let us see where each of the workshops has been scheduled:

```python
>>> for item in schedule:
... 	if item.event in workshops:
...         print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
Open Data projects with Python at 18-Sep-2016 10:15 in Room C
An introduction to deep learning at 18-Sep-2016 11:15 in Room C
Dive Into Object-oriented Python (cont.) at 18-Sep-2016 11:15 in Room A
Python for Scientists (feat. Software Carpentry) at 18-Sep-2016 14:30 in Room C
Data Wrangling with Python at 18-Sep-2016 14:30 in Room A
Dive Into Object-oriented Python at 18-Sep-2016 16:30 in Room C
Users are not the only people at 18-Sep-2016 16:30 in Room A
```

What about our plenaries:

```python
>>> for item in schedule:
... 	if item.event in plenary:
...         print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
Python and the Glories of the UNIX Tradition at 16-Sep-2016 09:10 in Assembly Room
Folklore and fantasy in the information age at 17-Sep-2016 09:10 in Assembly Room
An Arabish lesson: Introducing Django to the foreign world at 18-Sep-2016 09:10 in Assembly Room
```

And finally each and every one of our talks:

```python
>>> for item in schedule:
... 	if item.event in talks:
...         print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
Transforming the government’s Digital Marketplace from portal to platform at 16-Sep-2016 10:15 in Assembly room
The state of PyPy at 16-Sep-2016 11:15 in Room D
An Introduction to Deep Learning with TensorFlow at 16-Sep-2016 11:15 in Ferrier Hall
Simulating a CPU with Python or: surprising programs you might have thought were better written in C at 16-Sep-2016 11:15 in Assembly room
Distributed systems from scratch: lessons learned the hard way! at 16-Sep-2016 12:00 in Assembly room
Taking control of your Bluetooth devices at 16-Sep-2016 12:00 in Room D
Assessing performance of Support Vector Machine kernels to detect interactions in genotyped data at 16-Sep-2016 12:00 in Ferrier Hall
An Introduction to web scraping using Python at 16-Sep-2016 12:30 in Assembly room
A data processing toolbox for agile scientific research at 16-Sep-2016 12:30 in Room D
Lessons learned from organizing SciPy Latin America 2016 at 16-Sep-2016 12:30 in Ferrier Hall
Timezones: A tale of (more than) two cities at 16-Sep-2016 14:30 in Assembly room
Scripting across hosts with Chopsticks at 16-Sep-2016 14:30 in Room D
High School Pythonistas: What PYNAM did next. at 16-Sep-2016 14:30 in Ferrier Hall
I love being Pythonic, you? at 16-Sep-2016 15:00 in Room D
The Art of Doing Nothing – Using profiling to speed up your code at 16-Sep-2016 15:00 in Ferrier Hall
Introducing type hints - challenges and lessons at 16-Sep-2016 15:00 in Assembly room
Python, Locales and Writing Systems at 16-Sep-2016 15:30 in Assembly room
Declarative user interfaces in Python using ENAML at 16-Sep-2016 15:30 in Room D
So you "want" to maintain a Python legacy code base? at 16-Sep-2016 15:30 in Ferrier Hall
My journey from wxPython to PyQt at 16-Sep-2016 16:30 in Room D
An introduction to property-based testing and Hypothesis at 16-Sep-2016 16:30 in Ferrier Hall
Using Machine Learning to solve a classification problem with scikit-learn - a practical walkthrough at 16-Sep-2016 17:00 in Assembly room
The Breakup: Monolith to Microservices at 16-Sep-2016 17:00 in Room D
Building a Python Cake: Testing The Layers of Your Application at 17-Sep-2016 10:15 in Room D
Test-Driven Data Analysis at 17-Sep-2016 10:15 in Ferrier Hall
The CSD Python API – Helping the world’s structural chemists innovate at 17-Sep-2016 10:15 in Room C
recipy: completely effortless provenance for Python at 17-Sep-2016 10:15 in Assembly room
Django REST framework: Schemas, Hypermedia & Client libraries. at 17-Sep-2016 11:15 in Ferrier Hall
Python in Medicine: ventilator data at 17-Sep-2016 11:15 in Assembly room
How to Automate your Data Cleanup with Python at 17-Sep-2016 11:15 in Room C
Developing a Zero boilerplate library for Raspberry Pi GPIO at 17-Sep-2016 11:15 in Room D
Behind the scenes: writing tutorials at 17-Sep-2016 12:00 in Assembly room
From QA to UX - Learning how to accommodate developers at 17-Sep-2016 12:00 in Room D
Python and static types: Let's use mypy! at 17-Sep-2016 12:00 in Ferrier Hall
Ancient Greek Philosophy, Medieval Mental Models and 21st Century Technology at 17-Sep-2016 12:00 in Room C
PiNet - A project that was never intended to be... at 17-Sep-2016 12:30 in Assembly room
Type checking - Whose responsibility is it? at 17-Sep-2016 12:30 in Room D
Form Follows Functions at 17-Sep-2016 12:30 in Ferrier Hall
Some challenges in automatic English text correction at 17-Sep-2016 12:30 in Room C
Creating a reproducible more secure python application at 17-Sep-2016 14:30 in Room D
Addition: well, that escalated quickly! at 17-Sep-2016 14:30 in Assembly room
Chat bots: What is AI? at 17-Sep-2016 15:00 in Assembly room
Getting started with requests HTTP library at 17-Sep-2016 15:00 in Room D
Why /dev/random is a horrible idea and other problems you didn't know you had yet at 17-Sep-2016 15:30 in Assembly room
Symbolic Computation with Python using SymPy at 17-Sep-2016 15:30 in Room D
5 mistakes you will make building a Python Software House at 17-Sep-2016 16:30 in Ferrier Hall
Introducing MetaClasses at 17-Sep-2016 16:30 in Room D
Avoiding the "left-pad" problem: How to secure your pip install process at 17-Sep-2016 16:30 in Room C
Attempting to Win at Blackjack at 17-Sep-2016 16:30 in Assembly room
Lessons learned from PHP at 17-Sep-2016 17:00 in Room C
Life as the Sourcerer's Apprentice at 17-Sep-2016 17:00 in Assembly room
Tech interviews that don't suck at 17-Sep-2016 17:00 in Room D
Rewriting without rewriting - porting an ATC radar display to Python/Qt without starting from scratch at 17-Sep-2016 17:00 in Ferrier Hall
Cerberus - Data Validation for Humans at 18-Sep-2016 10:15 in Assembly room
An adventure in exploitation with Python at 18-Sep-2016 10:15 in Room A
Cleaner unit testing with the Arrange Act Assert pattern at 18-Sep-2016 10:15 in Room D
Developing CS education - how can you help at 18-Sep-2016 11:15 in Assembly room
Why do kids need to code and how can we help? at 18-Sep-2016 12:00 in Assembly room
Children's Day Show and Tell at 18-Sep-2016 12:30 in Room D
django CMS in the real time web: how to mix CMS, websockets, REST for a fully real time experience at 18-Sep-2016 14:30 in Room D
Neurodiversity in Technology at 18-Sep-2016 14:30 in Assembly room
Build your Microservices with ZeroMQ at 18-Sep-2016 15:00 in Assembly room
Easy solutions to hard problems at 18-Sep-2016 15:00 in Room D
Using Python for National Cipher Challenge at 18-Sep-2016 15:30 in Assembly room
Queueing and Python: pip install ciw at 18-Sep-2016 15:30 in Room D
Fast Python? Don't Bother! at 18-Sep-2016 16:30 in Assembly room
Euler's Key to Cryptography at 18-Sep-2016 16:30 in Room D
Python Library Development at 18-Sep-2016 17:00 in Assembly room
Prisoners, Cooperation and Spatial Structure at 18-Sep-2016 17:00 in Room D
```

**That could then be exported to whatever format is prefferable and used
to populate the conference website for example.**

Let us also take a closer look at the education talks:

```python
>>> for item in schedule:
... 	if item.event in talks and "Education" in item.event.tags:
...         print(f"{item.event.name} at {item.slot.starts_at} in {item.slot.venue}")
```

This is a very basic use of the library, you'll note for example that I've
ignored the capacity of the slots and the demand for talks. This can be used as
an objective function to try and put popular talks in large rooms. Similarly, we
can also use tags to enforce that talks that are in the same session share a
tag.

We can also use the library to check if any given schedule is valid: for example
we can make manual changes and quickly check if this is breaking something. We
can also create a new schedule with as few changes as possible from an old one
(perhaps when a speaker lets us know of a last minute constraint).

You can see an example of how to do all this at the library's documentation:
[conference-scheduler.readthedocs.io/en/latest/tutorial/index.html](http://conference-scheduler.readthedocs.io/en/latest/tutorial/index.html).

**This is a nice example of using mathematics and computer code to make our
things easier.**

One word of warning: whilst the problem I've solved here was solved very
cheaply on my machine it is possible that through the addition of a number of
constraints it becomes a lot more time consuming.

The library is still very young and we're planning on using it to schedule
[PyCon UK 2017](http://2017.pyconuk.org/) (26th to the 30th of October 2017 in
Cardiff) but you can find it all at this github repo:
[github.com/PyconUK/ConferenceScheduler](https://github.com/PyconUK/ConferenceScheduler)
and you can `pip install conference_scheduler`.

[Here is a notebook version of the code used in this blog post.]({{site.baseurl}}/assets/code/(Re) Scheduling PyCon uk.ipynb)
