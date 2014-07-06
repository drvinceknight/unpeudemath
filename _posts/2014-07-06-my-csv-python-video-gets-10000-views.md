---
layout: post
title:  "My CSV python video gets 10000 views"
categories: code
tags:
- code
- python
- csv
comments: true
---

So the other day I got the following notification on my phone:

![]({{site.baseurl}}/assets/images/10000_views_notification.png)

This both terrified me and made me smile. It's nice to think that a bunch of people have (hopefully) been helped with what I put together but also slightly worrying as I think I would be able to put together a much better video if I did it now.

Here it is:

<iframe width="560" height="315" src="//www.youtube.com/embed/jQ9aDyBWCXI" frameborder="0" allowfullscreen></iframe>

The basic code I use in the video is:

{% highlight python %}
import csv

out = open('data.csv', 'r')  # Open a file in read mode
data = csv.reader(out)  # Initiate a csv reader object which will parse the data
data = [[row[0], eval(row[1]), eval(row[2])] for row in data]  # Read in the data and convert certain entries of each row
out.close()  # Close the file

new_data = [[row[0], row[1] + row[2]] for row in data]  # Create some new data

out = open('new_data.csv', 'w')  # Open a file in write mode
output = csv.writer(out)  # Initiate a csv writer object which will write the data in the correct format (csv)

for row in new_data:  # Loop through the data
    output.writerow(row)  # Write the row to file

out.close()  # Close the file
{% endhighlight %}

There are a couple of other videos that are getting near that landmark, this is possibly my favourite of them:

<iframe width="560" height="315" src="//www.youtube.com/embed/WEA8m3j-Jqk" frameborder="0" allowfullscreen></iframe>

The above video shows how to simulate a basic queue in Python.
My Summer student [James Campbell](https://plus.google.com/103944008095354003273/posts) and I are working on something related at the moment.
