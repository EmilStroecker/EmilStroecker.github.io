---
layout: page
permalink: /publications/
title: publications
nav: true
nav_order: 3
---

{% include bib_search.liquid %}

<div class="publications">

<h2 class="bibliography">Conference Abstracts</h2>

{% bibliography --query @inproceedings %}

<h2 class="bibliography">Web Articles</h2>

{% bibliography --query @misc %}

</div>
