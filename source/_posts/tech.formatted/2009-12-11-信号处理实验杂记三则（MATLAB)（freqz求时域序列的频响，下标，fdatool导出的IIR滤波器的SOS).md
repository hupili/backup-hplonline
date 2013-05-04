---
layout: post
title: "信号处理实验杂记三则（MATLAB)（freqz求时域序列的频响，下标，fdatool导出的IIR滤波器的SOS)"
date: 2009-12-11  22:30
comments: true
categories: tech
tags: ["Matlab"]
_baiduhi_id: 6d3387106e81c20b203f2e39.html
_baiduhi_category: Matlab
---

(hplonline)2009.12.11<br/><br/><font color="#0000ff">freqz求时域序列的频响</font><br/><br/>
help freqz看到的帮助说是求这种形式的频响<br/>
|                jw               -jw              -jmw <br/>
|         jw  B(e)    b(1) + b(2)e + .... + b(m+1)e<br/>
|      H(e) = ---- = ------------------------------------<br/>
|                jw               -jw              -jnw<br/>
|             A(e)    a(1) + a(2)e + .... + a(n+1)e<br/>
参数中要求的b，a既是该系统z域上的分子和分母。<br/><br/>
而很多时候是拿到个信号的时域序列，<br/>
这个时候要分析其频域特性就不知道该怎么办了，<br/>
于是用fft加plot自己来完成这个图：<br/><font color="#ff9900">t = linspace(0 , 2 * pi , 100) ;<br/>
x = sin(t) ;<br/>
X = fft(x) ;<br/>
absX = abs(X) ;<br/>
plot([absX(50:end),absX(1:49)]) ;</font><br/>
纠结了很久才反映过来这样就可以了：<br/><font color="#ff9900">N = 100 ;<br/>
w = 2 * pi * (0:N -1) / N ;<br/>
h = freqz(x ,[1] , 100 ) ;<br/>
plot(w , abs(h)) ;</font><br/>
直接把分母a令为1。则系数b和时域序列是一样的。<br/>
把有限长时域序列按照z变换的定义式写出来，<br/>
对比freqz提供的形式就知道了。。<br/>
这样比自己fft再频移要方便很多。<br/><br/><font color="#0000ff"><br/>
下标</font><br/><br/>
写一个升采样函数，写成了这样：<br/><font color="#ff9900">function y = inter(x , L)<br/>
N = length(x) ;<br/>
y = zeros(1 , L * N) ;<br/>
y(L * (0:(N-1))) = x ;<br/>
return </font><br/>
结果报错：<br/><font color="#ff0000">??? Subscript indices must either be real positive integers or logicals.</font><br/>
很多时候出这种问题就是因为下标不是整数，<br/>
而我看了L * (0:(N-1))生成的序列确实是整数啊，<br/>
就算不是，后来把他round一下，都还是不可以。。<br/>
郁闷了很久想起matlab是从1开始的，于是整个序列加1就搞定了。。。<br/>
y(L * (0:(N-1))) = x ;<br/>
其实报错说得很明确了<font color="#ff0000">positive</font>和<font color="#ff0000">integer</font>。<br/>
但是由于经常是integer把我们卡住，于是直接把重心偏移了过去。<br/>
想起了一篇<a target="_blank" href="http://www.matrix67.com/blog/archives/2571">文章</a>。<br/>
是不是这句要这么说呢。。：<br/><font color="#ff0000">??? Subscript indices must either be real god damned positive integers or logicals.</font><br/><br/><font color="#0000ff">fdatool导出的IIR滤波器的SOS</font><br/><br/>
由于<font color="#ff0000">课前没预习，上课栽瞌睡，课后没复习</font>。。<br/>
发现看不懂那个矩阵是什么意思。。<br/>
像FIR设计出来就很直观，只有个Numberator。<br/>
而IIR出来的SOS是个六列的矩阵。。<br/><br/>
后来问了<font color="#ff0000">研究生（<img src="http://img.baidu.com/hi/tsj/t_0027.gif"/>）</font>，才知道这个设计是按照级联型的方式做出来的。<br/>
一横行就是一个模块，左边三是分子，右边三是分母。<br/>
各行乘起来的就是直接型方式设计出来的系数了。<br/><br/>
悲剧。。
