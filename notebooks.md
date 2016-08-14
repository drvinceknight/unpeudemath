---
layout: page
title: Notebooks
permalink: /notebooks/
---

Here are notebooks used for a variety of posts:

{% for nb in site.static_files | reversed %}
    {% if nb.extname == ".ipynb" %}
1. [{{nb.path}}]({{site.baseurl}}{{nb.path}}) (modified: {{nb.modified_time}})
    {% endif %}
{% endfor %}
