---
layout: post
title: "FFT相关（一）（MATLAB）（DIT2,DIF2的递归实现，实序列fft计算)"
date: 2009-12-20  13:30
comments: true
categories: tech
tags: ["Matlab"]
_baiduhi_id: 6ed46d09534963c43ac7630d.html
_baiduhi_category: Matlab
---

(hplonline)2009.12.20<br/><br/>
虽然之前用C写过，<br/>
不过一直没有对原理进行比较好的把握，<br/>
正好最近的实验指导书上写得还行，<br/>
于是用递归实现了一下基2的运算。<br/><br/>
关于基2时间抽取和频率抽取在指导书里面讲得比较详细了。<br/><a href="http://www.box.net/shared/cleppvpyx2" target="_blank">指导书和m文件下载</a><br/><br/>
这里讨论另外两个主题：递归实现和实序列计算。<br/><font color="#0000ff"><br/>
递归实现：</font><br/><br/>
使用递归实现的话，只需要把原理部分读懂就行了，<br/>
至于蝶形运算，同址运算，位反序等高级操作则不用管了。<br/>
毕竟用matlab写东西往往关注的是一个算法的正确性，<br/>
需要大量使用之前再用C写出来 ，并大加优化。<br/><br/>
既然是递归，则有一个终止条件的问题，<br/>
实际上，可以递归到序列长度为1的时候：<br/>
X = x;则可<br/>
但不知道为啥看到好几个人写的都是递归到长度为2的时候。。<br/>
难道是老师这么说的。。<br/><br/>
用递归写出来了之后，<br/>
我也觉得很惊悚，<br/>
没想到用matlab可以做得这么短。。。<br/>
（代码见后，<font color="#ff0000">只能对2的次方的长度计算）</font><br/><br/><font color="#0000ff">实序列DFT：</font><br/><br/>
上面讨论的dit，dif都是处理复序列的。<br/>
而实序列本身就少一半的信息，<br/>
居然还要用同样多的运算量，<br/>
这就有点不合理了。<br/><br/>
关于DFT有如下结论：<br/><font color="#ff0000">x的实部的DFT是X的共轭对称部分(Xcs)<br/>
x的虚部的DFT是X的共轭反称部分(Xca)</font><br/><br/>
对于实序列来说，共轭反称部分为0，这就是很大的浪费。<br/><br/>
计算两个实序列的话，都知道可以组装起来。<br/>
x = x1 + 1i * x2；<br/>
得到X后再分离出Xcs和Xca，则对应X1和X2。<br/><br/>
计算一个实序列的话，方法类似。<br/><font color="#ff0000">唯一要考虑的是怎样拆成两个序列，<br/>
又怎样组装回原序列。</font><br/><br/>
答案也很显然，借用DIT或者DIF的思想就可以了。<br/>
比如我下面的实现中，按奇偶分裂原序列。<br/>
组装成新序列，并且调用任何一种DFT算法得到频域的序列。<br/>
根据共轭对称和反称关系得到奇偶序列对应的变换，<br/>
再用类似DIT的方法组装起来就行了。<br/><br/>
（代码见后，<font color="#ff0000">只能处理原序列是偶数的情况）</font><br/><br/><font color="#0000ff">代码：</font>（如果缩进有问题，那肯定是百度的问题。。）<br/><br/>
function test<br/>
x = rand(1 , 2 .^ 13) ;<br/>
tic<br/>
X1 = fft(x) ;<br/>
toc<br/>
tic<br/>
X2 = dit2(x) ;<br/>
toc<br/>
tic<br/>
X3 = dif2(x) ;<br/>
toc<br/>
tic<br/>
X4 = real_fft(x) ;<br/>
toc<br/>
max(abs(X1 - X2)) <br/>
max(abs(X1 - X3))<br/>
max(abs(X1 - X4))<br/>
return ;<br/><br/>
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
return ;<br/><br/>
function X = dif2(x)<br/>
N = length(x) ;<br/>
if N == 1<br/>
X = x ;<br/>
else<br/>
x1 = x(1:N/2) ;<br/>
x2 = x(N/2+1:N) ;<br/>
W = exp(-1i * 2 * pi / N * (0:(N/2-1))) ;<br/>
X = zeros(1 , N) ;<br/>
X(1:2:N-1) = dif2(x1 + x2) ;<br/>
X(2:2:N) = dif2((x1 - x2) .* W) ;<br/>
end<br/>
return ;<br/><br/>
function X = real_fft(x)<br/>
N = length(x) ;<br/>
xx = x(1:2:N) + 1j * x(2:2:N) ;<br/>
XX = dit2(xx) ; %can be changed to other realization of fft<br/>
XX_conj_rev = conj([XX(1) , fliplr(XX(2:end))]);<br/>
Xcs = (XX + XX_conj_rev) / 2 ;<br/>
Xca = (XX - XX_conj_rev) / 2 ;<br/>
W = exp(-1i * 2 * pi / N * (0:(N/2-1))) ;<br/>
X = [Xcs + W .* Xca / 1j , Xcs - W .* Xca / 1j] ;<br/>
return ;<br/><br/><font color="#0000ff">结果：</font><br/><br/>
Elapsed time is 0.000225 seconds.<br/>
Elapsed time is 0.349320 seconds.<br/>
Elapsed time is 0.326117 seconds.<br/>
Elapsed time is 0.154730 seconds.<br/><br/>
ans =<br/>
6.7032e-014<br/>
ans =<br/>
5.5153e-014<br/>
ans =<br/>
6.0396e-014<br/><br/>
1.可以看到字节写的和内置的fft时效相差很大，<br/>
不过作为原理模拟，这不是主要问题<br/>
2.通过实序列算法计算，效率是基础算法（这里用的dit2）的两倍<br/>
3.计算出的序列和内置fft有一定的误差，<br/>
这时由于不同路径产生的，<br/>
不过其量值很小，可以忽略。<br/><br/><font color="#0000ff">下一步：</font><br/><br/>
1.基4的算法<br/>
2.任意基的算法<br/>
3.质数长度的序列计算<br/>
