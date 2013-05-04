---
layout: post
title: "FFT相关（二）（MATLAB）（DIT4递归实现)"
date: 2009-12-27  13:01
comments: true
categories: tech
tags: ["Matlab"]
_baiduhi_id: bebbf9deed85a45f94ee379b.html
_baiduhi_category: Matlab
---

(hplonline)2009.12.27<br/><br/>
考了几天试，差点搞忘整这个了。<br/>
有了之前<a href="http://hi.baidu.com/hplonline/blog/item/6ed46d09534963c43ac7630d.html" target="_blank">基2的原理</a>，基4的算法可以顺便推出。<br/><font color="#0000ff"><br/>
程序：</font><br/><br/>
function test<br/>
x = rand(1 , 4 .^ 6) ;<br/>
tic<br/>
X1 = fft(x) ;<br/>
toc<br/>
tic<br/>
X2 = dit4(x) ;<br/>
toc<br/>
tic<br/>
X3 = dit2(x) ;<br/>
toc<br/>
max(abs(X1 - X2)) <br/>
max(abs(X1 - X3)) <br/>
return ;<br/><br/>
%precondition:<br/>
%length of x should be (4.^n) where n is an integer<br/>
function X = dit4(x)<br/>
N = length(x) ;<br/>
if N == 1<br/>
X = x ;<br/>
else <br/>
X1 = dit4(x(1:4:N)) ;<br/>
X2 = dit4(x(2:4:N)) ;<br/>
X3 = dit4(x(3:4:N)) ;<br/>
X4 = dit4(x(4:4:N)) ;<br/>
W2 = exp(-1j * 2 * pi / N * (0:(N/4-1))) ;<br/>
W3 = exp(-2j * 2 * pi / N * (0:(N/4-1))) ;<br/>
W4 = exp(-3j * 2 * pi / N * (0:(N/4-1))) ;<br/>
XX1 = X1 + 1 * W2 .* X2 + 1 * W3 .* X3 + 1 * W4 .* X4 ;<br/>
XX2 = X1 - j * W2 .* X2 - 1 * W3 .* X3 + j * W4 .* X4 ;<br/>
XX3 = X1 - 1 * W2 .* X2 + 1 * W3 .* X3 - 1 * W4 .* X4 ;<br/>
XX4 = X1 + j * W2 .* X2 - 1 * W3 .* X3 - j * W4 .* X4 ;<br/>
X = [XX1 , XX2 , XX3 , XX4] ;<br/>
end<br/>
return ;<br/><br/>
%precondition:<br/>
%length of x should be (2.^n) where n is an integer<br/>
function X = dit2(x)<br/>
N = length(x) ;<br/>
if N == 1<br/>
X = x ;<br/>
else <br/>
X1 = dit2(x(1:2:(N-1))) ;<br/>
X2 = dit2(x(2:2:N)) ;<br/>
W = exp(-1i * 2 * pi / N * (0:(N/2-1))) ;<br/>
X = [X1 + W .* X2 , X1 - W .* X2] ;<br/>
end<br/>
return ;<br/><font color="#0000ff"><br/>
结果：</font><br/><br/>
Elapsed time is 0.000149 seconds.<br/>
Elapsed time is 0.125514 seconds.<br/>
Elapsed time is 0.183247 seconds.<br/>
ans =<br/>
1.1369e-013<br/>
ans =<br/>
3.5527e-014<br/><br/><font color="#0000ff">小结：</font><br/><br/>
从理论上说基4的算法递归层数是基2的一半。<br/><font color="#ff0000">可以看到效率有所提高，但并没有到两倍。</font><br/>
主要原因在于每一层整合上层结果的消耗变大了。<br/><br/>
在用C实现的时候，即使还是用递归，<br/>
整合这一步仍然有提高的余地。<br/>
因为基4的算法中，旋转系数是0,-j,-1,j。<br/>
而与这几个特殊数字相乘，<br/>
可以直接用取反、交换虚实部等手段完成（最多两次MUL(与-1)及MOV），<br/>
而不是普通复数乘法（消耗4次MUL与2次ADD）。<br/><br/>
而再升基的话，在整合上就会出现麻烦了，<br/>
因为可能很难简化复数乘法。<br/>
（基2的W(N,N/2)为-1，可以只接取反相加）<br/><br/>
不过基8的时候还是有可能改进的，<br/>
相比基4的时候，多出来的为sqrt(2)/2*(1+j,1-j,-1+j,-1-j)等因子。<br/>
最多的时候，可能出现三次与-1相乘，一次与sqrt(2)/2相乘，<br/>
如果硬件上直接支持浮点取反，这里就可以改进不少。<br/><br/>
