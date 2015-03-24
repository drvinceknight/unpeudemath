---
layout     : post
title      : "Marrying toys and students"
categories : pedagogy
tags       :
- gametheory
- sage
comments   : true
---

In class yesterday we took a look at matching games.
These are sometimes referred to as stable marriage problems.
To have some data for us to play with I asked for some volunteers to marry.
Sadly I apparently am not allowed to ask students to rank each other in class and I also do not have the authority to marry.
So, [like last year](http://drvinceknight.blogspot.co.uk/2014/03/matching-games-in-class.html) I used some of my office toys and asked students to rank them.

I brought three toys to class:

- The best ninja turtle: Donatello
- A tech deck
- A foam football

I asked 3 students to come down and rank them and in turn I let the toys rank the students.

We discussed possible matchings with some great questions such as:

> "Are we trying to make everyone as happy as possible?"

The answer to that is: no.
We are simply trying to ensure that no one has an incentive to deviate from their current matching by breaking their match for someone they prefer and who also prefers them.

Here is the stable matching we found together:

![]({{site.baseurl}}/assets/images/matching_game.jpg)

Note that we can run the Gale-Shapley value using Sage:

<div class="compute"><script type="text/x-sage">
suitr_pref = {'K': ('F', 'Td', 'D'),
              'Kr': ('D', 'F', 'Td'),
              'D': ('D', 'F', 'Td')}
reviewr_pref = {'D': ('K', 'D', 'Kr'),
                'F': ('Kr', 'K', 'D'),
                'Td': ('K', 'Kr', 'D')}
m = MatchingGame([suitr_pref, reviewr_pref])
m.solve()
</script></div>

The 3 students got to hold on to the toys for the hour and I was half expecting the football to be thrown around but sadly that did not happen.
Perhaps next year.
