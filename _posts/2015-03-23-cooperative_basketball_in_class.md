---
layout     : post
title      : "Cooperative basketball in class"
categories : pedagogy
tags       :
- gametheory
- sage
comments   : true
---

Today in class we repeated the game we played [last year](http://drvinceknight.blogspot.co.uk/2014/03/basketball-and-cooperative-games-in.html).
3 teams of 3 students took part this year and here is a photo of the aftermath:

![]({{site.baseurl}}/assets/images/basketball.jpg)

As a class we watched the three teams attempt to free-throw as many crumpled up pieces of paper in to the bin as possible.

Based on the total number we then tried to come up with how many each subset/coalition of players would have gotten in.
So for example, 2 out of 3 of the teams had one student crumple paper while the other 2 took shots.
So whilst that individual did not get any in, they contributed an important part to the team effort.

Here are the characteristic functions that show what each team did:

![]({{site.baseurl}}/assets/images/basketball-characteristic-functions.jpg)

Here is some [Sage](http://sagemath.org/) code that gives the Shapley value for each game ([take a look at my class notes](http://vincent-knight.com/Year_3_game_theory_course/Content/Chapter_16_Cooperative_games/) or at [last years post](http://drvinceknight.blogspot.co.uk/2014/03/basketball-and-cooperative-games-in.html) to see how to calculate this):

Let us define the first game:

<div class="compute"><script type="text/x-sage">
f_1 = {(): 0,
       ('H'): 2,
       ('G'): 3,
       ('S'): 1,
       ('H', 'G'): 6,
       ('H', 'S'): 3,
       ('G', 'S'): 4,
       ('H', 'G', 'S'): 6}
game_1 = CooperativeGame(integer_function)
game_1.shapley_value()
</script></div>

If you click `Evaluate` above you see that the Shapley value is given by:

$$
\phi = (13/6, 19/6, 2/3)
$$

(This one we calculated in class)

By changing the numbers above we get the following for the other two games.

- Game 2:

    $$
    \phi = (3/2, 7/2, 4)
    $$

- Game 3:

    $$
    \phi = (17/6, 4/3, 23/6)
    $$

This was a bit of fun and most importantly from a class point of view gave us some nice numbers to work from and calculate the Shapley value together.

If anyone would like to read about the Shapley value a bit more take a look at the [Sage documentation](http://www.sagemath.org/doc/reference/game_theory/sage/game_theory/cooperative_game.html) which not only shows how to calculate it using Sage but also goes over some of the mathematics (including another formulation).
