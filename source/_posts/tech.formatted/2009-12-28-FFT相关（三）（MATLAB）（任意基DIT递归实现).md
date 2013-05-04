---
layout: post
title: "FFT相关（三）（MATLAB）（任意基DIT递归实现)"
date: 2009-12-28  20:22
comments: true
categories: tech
tags: ["Matlab"]
_baiduhi_id: e936db003d99e11a738b6549.html
_baiduhi_category: Matlab
---

<p>(hplonline)2009.12.28</p>
<p>其实有了前面基2，基4的原理。。。<br/>
任意基的FFT也就是那个样子。</p>
<p>详细推导和程序文件<a target="_blank" href="http://www.box.net/shared/s4tcp5rpvg">下载</a>。</p>
<p><font color="#0000ff">简要说明：</font></p>
<p>任意基就是把长度作因子分解：<br/>
N=a*b<br/>
于是可以通过计算a个长度为b的子序列，<br/>
然后再把结果整合得到N点的DFT。<br/>
（话说虽然DSP的期末貌似不考FFT，<br/>
但是这个任意基的原理在某课后题出现过，<br/>
只是没有点名可以用来做FFT而已）</p>
<p>这个过程可以递归下去，<br/>
直到b=1，就可以直接算得X=x。</p>
<p>详细的推导还是见下载的包吧。</p>
<p>另外，作为原理模拟，<br/>
像分解因数等部分写得就很土鳖了，<br/>
反正意思是到了。</p>
<p><font color="#0000ff">关键程序段：</font></p>
<p>function X = ditany(x)<br/>
     N = length(x) ;<br/>
     if N == 1<br/>
         X = x ;<br/>
     else <br/>
         %factorize N = a * b<br/>
         flag = 0 ;<br/>
         for a = 2:fix(sqrt(N))<br/>
             if fix(N / a) == N / a<br/>
                flag = 1 ;<br/>
                break ;<br/>
             end<br/>
         end<br/>
         if ~flag<br/>
            a = N ; <br/>
         end<br/>
         b = N / a ;<br/>
         %start caculation of length b dft <br/>
         %and assemble the a sequences<br/>
         W = exp(-1j * 2 * pi / N * (0:a-1)'*(0:b-1)) ;<br/>
         %preallocation of space will be needed here<br/>
         %to accelerate the programme<br/>
         XX = [] ;<br/>
         for ii = 1:a<br/>
            XX = [XX ; ditany(x(ii:a:N))] ; <br/>
         end<br/>
         X = [] ;<br/>
         XX = XX .* W ;<br/>
         for jj = 1:a<br/>
             tmp = exp(-j * 2 * pi / N * (0:a-1) * b * (jj - 1)) * XX ;<br/>
             X = [X , tmp] ;<br/>
         end<br/>
     end<br/>
return ;</p>
<p><font color="#0000ff">一些比较:</font></p>
<p>其实我们比较关心的是这个任意基的算法究竟能改进多少时间。<br/>
基准采用的是矩阵定义的DFT变换：<br/>
X1 = x * exp(-j * 2 * pi / N * (0:N-1)'*(0:N-1)) ;</p>
<p>以点数为横坐标，<br/>
加速比为纵坐标。<br/>
加速比的定义为DIT_any的耗时比上矩阵DFT的耗时。<br/>
画出散点图，并标注基准线y=1来观察。</p>
<p>首先来看从1到200点的散点图。</p>
<p><span><img class="blogimg" border="0" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/83afdc8802b56fa4a5c272c1.jpg"/></span><br/>
再看以2的方冪为点数的散点图。</p>
<p><span><img class="blogimg" border="0" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/46c61bdf99666223622798c1.jpg"/><br/></span><br/>
在观察各种自然数的时候，<br/>
发现这个任意基的算法大部分时候反而更戳。</p>
<p>专门把2的方冪提取出来观察，<br/>
发现效率有所改进，<br/>
但似乎并不是很明显的样子。</p>
<p>要仔细观察其中的差异，<br/>
还得用C来实现一下。<br/>
因为MATLAB隐藏了太多的细节，<br/>
让我们无法把握每一个消耗时间的地方。<br/>
不过作为粗糙的原理模拟，<br/>
以及简易对比来说是可以的。</p>
<p>出现这种现象也比较好理解，<br/>
因为任意基的算法的精华在于分解。<br/>
把大的序列分解成若干小的序列，分别计算。<br/>
随便选一个数，如果是质数，<br/>
则无法发挥任意基的能力，<br/>
甚至由于其他操作引入更多的时间。<br/>
即使不是质数，<br/>
如果其中有较大的质数因子也会导致耗时较多。</p>
<p>由于是任意基，exp(2 * pi / N * k)的计算是逃不掉的。<br/>
不像基2基4基8，出来的是如1,j,1+j这类比较好看的数字。</p>
<p> </p>
