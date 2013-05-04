---
layout: post
title: "An Interesting &#34;Hello World&#34; in C++"
date: 2010-03-13  13:54
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: 01d25943a2534b1a9213c6f3.html
_baiduhi_category: c&c++
---

(hplonline)2010.3.13<br/><br/>
given a piece of code :<br/><br/><font color="#ff9900">#include "stdio.h"<br/>
void print()<br/>
{<br/>
*<br/>
}<br/><br/>
void main()<br/>
{<br/>
}</font><br/><br/>
place your code around the asterisk (*)<br/>
to make the programme output "hello world".<br/><br/>
any idea ??<br/><br/>
=move<br/>
=downwards<br/><br/><br/>
=and<br/><br/>
=downwards<br/><br/><br/>
=<br/><br/><br/><br/><br/>
=<br/><br/><br/><br/><br/>
=<br/><br/><br/><br/><br/><br/>
=<br/><br/><br/><br/><br/><br/><br/><br/>
=<br/><br/><br/><br/><br/><br/><br/><br/><br/>
=<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
=<br/><br/><br/><br/><br/><br/><br/>
I had no ideas until <a href="http://shallway.net/" target="_blank">Shallway</a> reminded me of constructor in C++.<br/>
It's a common sense that constructors of global objects are called before main().<br/>
However, this is not always in our mind. <br/><br/>
Knowing the concept of using constructors, things become easy.<br/>
Substitute the asterisk by the following lines:<br/><br/><font color="#ff9900">}<br/>
class cls{<br/>
public:<br/>
cls(){<br/>
printf("hello world\n") ;<br/>
}<br/>
} ;<br/>
cls mycls ;<br/>
void fun(){</font><br/><br/>
