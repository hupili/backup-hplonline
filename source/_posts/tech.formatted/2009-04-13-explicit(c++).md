---
layout: post
title: "explicit(c++)"
date: 2009-04-13  20:03
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: 89c8780ec95dbdc27acbe1c5.html
_baiduhi_category: c&c++
---

(hplonline)2009.4.13<br/><br/>
这个关键字可以用来限制类的构造函数要<font color="#ff0000">显式调用</font>。<br/><br/>
如下例子：<br/><br/>
class cls{<br/>
     int data ;<br/>
public :<br/>
     cls(){} ;<br/>
     cls(int x){data = x ;} ;<br/>
};<br/><br/>
int main(){<br/>
     cls c1(1) ;<br/>
     cls c2 = 1 ;<br/>
     return 0 ;<br/>
}<br/><br/>
有了 cls(int x)之后，cls c2 = 1  也是成立的。<br/>
相当于<font color="#ff0000">隐式调用</font>了c2.cls(1)。（我说相当于，因为直接这样写是通不过的）<br/><br/>
那么现在加一个explicit看下。<br/><br/>
class cls{<br/>
     int data ;<br/>
public :<br/>
     cls(){} ;<br/>
     <font color="#ff0000">explicit </font>cls(int x){data = x ;} ;<br/>
};<br/><br/>
int main(){<br/>
     cls c1(1) ;<br/>
     cls c2 = 1 ;<br/>
     return 0 ;<br/>
}<br/><br/>
于是报错了：<br/><br/>
cannot convert from 'const int' to 'class cls'<br/>
         No constructor could take the source type, or constructor overload resolution was ambiguous<br/><br/>
把第二句改一下。<br/>
cls c2 = cls(1) ;<br/>
于是又可以了。<br/>
等号右边就是一个显示的调用构造函数。<br/><br/>
那么做这样的限制有什么实际意义呢，我想还是在具体的工程中去体会。<br/><br/>
我现在暂时也没感受到，不过STL的源码里面出现很多这个东西。
