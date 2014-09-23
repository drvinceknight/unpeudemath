---
layout: post
title:  "Greyscale graphs in sage"
categories: code
tags:
- sage
comments : false
---

{% highlight python %}
from sage.graphs.graph_coloring import chromatic_number
from sage.graphs.graph_coloring import vertex_coloring
from sage.graphs.graph_coloring import number_of_n_colorings
from sage.graphs.graph_coloring import edge_coloring
{% endhighlight %}

{% highlight python %}
def grey_rainbow(n, black=False):
    """
    Return n greyscale colors
    """
    if black:
        clrs = [0.299*clr[0] + 0.587 * clr[1] + 0.114 * clr[2] for clr in rainbow(n-2,'rgbtuple')]
    else:
        clrs = [0.299*clr[0] + 0.587 * clr[1] + 0.114 * clr[2] for clr in rainbow(n-1,'rgbtuple')]
    output = ['white']
    for c in clrs:
        if c <= 0.0031308:
            rgb = 12.92 * c
        else:
            rgb = (1.055*c^(1/2.4)-0.055)
        output.append((rgb,rgb,rgb))
    if black:
        output.append('black')
    return output
{% endhighlight %}

{% highlight python %}
def grey_coloring(G, black=False):
    chromatic_nbr = chromatic_number(G)
    coloring = vertex_coloring(G)
    grey_colors = grey_rainbow(chromatic_nbr, black)
    d = {}
    for i, c in enumerate(grey_colors):
        d[c] = coloring[i]
    return P.graphplot( vertex_colors=d)
{% endhighlight %}

{% highlight python %}
P = graphs.PetersenGraph()
p = grey_coloring(P,black=True)
p.show()
{% endhighlight %}

{% highlight python %}
P = graphs.PetersenGraph()
p = grey_coloring(P)
p.show()
{% endhighlight %}

[Random stack overflow question](http://stackoverflow.com/questions/12201577/convert-rgb-image-to-grayscale-in-python)
[wiki page](http://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale)
