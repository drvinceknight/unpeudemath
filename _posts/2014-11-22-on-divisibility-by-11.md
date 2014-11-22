---
layout     : post
title      : "Thinking about divisibility by 11"
categories : code
tags       :
- python
- mathematics
comments   : true
---

This post is based on a class meeting I had recently with my programming class.
It was based on trying to use code to help identify a condition that a number must obey for it to be divisible by 11.
Readers of this blog might be aware that the following is incorrect but stick with me.

### Exploring a statement

> A number is divisible by 11 if and only if the alternating (in sign) sum of the number's digits is 0.

To help with notation let us define \\(f:x\to\text{alternating sum of digits of x}\\) so for example we have:

$$f(27)=2-7=-5$$

and

$$f(27562)=2-7+5-2+4=4$$

It is immediate to note that for \\(N< 100\\) \\(f(N)=0\\) if and only if 11 divides \\(N\\) (\\(11\;\|\;N\\) for short).
Before trying to prove our statement we could check it for a few more numbers:

- \\(f(110)=0\\)
- \\(f(121)=0\\)
- \\(f(132)=0\\)
- \\(f(143)=0\\)
- \\(f(154)=0\\)
- \\(f(165)=0\\)
- \\(f(176)=0\\)
- \\(f(187)=0\\)
- \\(f(198)=0\\)

So things are looking good!
We could now rush off and try to prove that our statement is correct... **or** we could try more numbers.
The easiest way to 'try enough' is to write some simple code (the following is written in Python):

{% highlight python %}
class Experiment():
    """
    A class for an experiment
    """
    def __init__(self, N):
        """
    Initialisation method:
    inputs: N - the number for which we will check the conjecture
    """
        self.N = N
        self.divisible_by_11 = N % 11 == 0
        self.sum_of_consecutive_digits = sum([(-1) ** d *int(str(N)[d]) for d in range(len(str(N)))])
    def test_statement(self):
        """
        Returns True if 'A number is divisible by 11 iff the alternating sum digits is 0' holds for this particular number.
        """
        if self.divisible_by_11:
            return self.sum_of_consecutive_digits == 0
        return self.sum_of_consecutive_digits != 0
{% endhighlight %}

This creates a class for an `Experiment` for a given number, which has a couple of attributes relevant to what we're trying to do:

{% highlight python %}
>>> N = Experiment(121)
>>> N.divisible_by_11
True
>>> N.sum_of_consecutive_digits
0
{% endhighlight %}

There is also a method that checks the if and only if condition of our statement:

{% highlight python %}
...
        if self.divisible_by_11:
            return self.sum_of_consecutive_digits == 0
        return self.sum_of_consecutive_digits != 0
...
{% endhighlight %}

So if the number is divisible by 11 then the statement is true if the sum is 0.
If the number is however not divisible by 11 then the statement is true if the sum is **not** 0.

We can thus check for any given number if our statement is true:

{% highlight python %}
>>> N = Experiment(121)
>>> N.test_satement()  # 121 is divisible by 11 and 1-2+1==0
True
>>> N = Experiment(122)
>>> N.test_statement()  # 122 is not divisible by 11 and 1-2+2!=0
True
{% endhighlight %}

So before attempting to prove anything algebraically let's just check that it holds for the first 10000 numbers:

{% highlight python %}
>>> all(Experiment(N).test_statement() for N in range(10001))
False
{% endhighlight %}

**Disaster!** It looks like our statement is not quite right!

The following might help us identify where (outputting a list of numbers for which the statement is false):

{% highlight python %}
>>> [N for N in range(10001) if not Experiment(N).test_statement()]
[209, 308, 319, 407, 418, 429, 506, 517, 528, 539, 605, 616, 627, 638, 649, 704, 715, 726, 737, 748, 759, 803, 814, 825, 836, 847, 858, 869, 902, 913, 924, 935, 946, 957, 968, 979, 1309, 1408, 1419, 1507, 1518, 1529, 1606, 1617, 1628, 1639, 1705, 1716, 1727, 1738, 1749, 1804, 1815, 1826, 1837, 1848, 1859, 1903, 1914, 1925, 1936, 1947, 1958, 1969, 2090, 2409, 2508, 2519, 2607, 2618, 2629, 2706, 2717, 2728, 2739, 2805, 2816, 2827, 2838, 2849, 2904, 2915, 2926, 2937, 2948, 2959, 3080, 3091, 3190, 3509, 3608, 3619, 3707, 3718, 3729, 3806, 3817, 3828, 3839, 3905, 3916, 3927, 3938, 3949, 4070, 4081, 4092, 4180, 4191, 4290, 4609, 4708, 4719, 4807, 4818, 4829, 4906, 4917, 4928, 4939, 5060, 5071, 5082, 5093, 5170, 5181, 5192, 5280, 5291, 5390, 5709, 5808, 5819, 5907, 5918, 5929, 6050, 6061, 6072, 6083, 6094, 6160, 6171, 6182, 6193, 6270, 6281, 6292, 6380, 6391, 6490, 6809, 6908, 6919, 7040, 7051, 7062, 7073, 7084, 7095, 7150, 7161, 7172, 7183, 7194, 7260, 7271, 7282, 7293, 7370, 7381, 7392, 7480, 7491, 7590, 7909, 8030, 8041, 8052, 8063, 8074, 8085, 8096, 8140, 8151, 8162, 8173, 8184, 8195, 8250, 8261, 8272, 8283, 8294, 8360, 8371, 8382, 8393, 8470, 8481, 8492, 8580, 8591, 8690, 9020, 9031, 9042, 9053, 9064, 9075, 9086, 9097, 9130, 9141, 9152, 9163, 9174, 9185, 9196, 9240, 9251, 9262, 9273, 9284, 9295, 9350, 9361, 9372, 9383, 9394, 9460, 9471, 9482, 9493, 9570, 9581, 9592, 9680, 9691, 9790]
{% endhighlight %}

The first of those numbers is \\(209=11\times19\\) so it is divisible by 11 but \\(f(209)=2-0+9=11\\) and if we calculate \\(f\\) for a few more of the numbers in the above list we again get \\(11\\).
At this point in time it seems like we need to adjust our statement.

### Sufficient evidence for a conjecture

> A number is divisible by 11 if and only if the alternating (in sign) sum of the number's digits is divisible by 11.

A slight tweak of the `Experiment` code above gives:

{% highlight python %}
class Experiment():
    """
    A class for an experiment
    """
    def __init__(self, N):
        """
    Initialisation method:
    inputs: N - the number for which we will check the conjecture
    """
        self.N = N
        self.divisible_by_11 = N % 11 == 0
        self.sum_of_consecutive_digits = sum([(-1) ** d *int(str(N)[d]) for d in range(len(str(N)))])
    def test_conjecture(self):
        """
        Returns True if 'A number is divisible by 11 iff the alternating sum digits is 0' holds for this particular number.
        """
        if self.divisible_by_11:
            return self.sum_of_consecutive_digits % 11 == 0
        return self.sum_of_consecutive_digits % 11 != 0
{% endhighlight %}

Now let us check the first 100,000 numbers:

{% highlight python %}
>>> all(Experiment(N).test_conjecture() for N in range(100001))
True
{% endhighlight %}

When we have a lot of evidence for a mathematical statement we can (generally) start calling it a conjecture.
At this point we probably can attempt to prove that the conjecture is true:

### Proof

Let \(n_i\) be the \\(i\\)th digit of the \\(m\\) digit number \\(N\\), so we have \\(N=\sum_{i=1}^{m}n_i10^{i-1}\\).
Using arithmetic modulo \\(11\\) we have:

$$N\equiv \sum_{i=1}^{m}n_i10^{i-1} \mod 11$$

but:

$$
10^{i-1}\equiv\begin{cases}
1\mod 11,&\text{if }i\text{ odd}\\
-1\mod 11,&\text{if }i\text{ even}\\
\end{cases}
$$

thus:

$$N\equiv \sum_{i=1}^{m}n_i(-1)^{i-1} \mod 11$$

The right hand side of that is of course just \\(f(N)\\) so \\(11\;\|\;N\\) if and only iff \\(11\;\|\;f(N)\\) (as required).

---

This is how a lot of mathematics gets done nowadays.
Statements get made, then refined then checked and then finally (hopefully) proved.
A nice book that describes a conjecture that stayed a conjecture for a long time (until ultimately being proved) is [Proofs and Confirmations: The Story of the Alternating-Sign Matrix Conjecture](http://www.amazon.co.uk/Proofs-Confirmations-Alternating-Sign-Conjecture-Spectrum/dp/0521666465) by Bressoud.
