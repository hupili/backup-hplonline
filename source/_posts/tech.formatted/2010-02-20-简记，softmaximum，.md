---
layout: post
title: "简记，soft maximum，"
date: 2010-02-20  14:00
comments: true
categories: tech
tags: ["Math"]
_baiduhi_id: d224c9fd02f12f4ed7887d8c.html
_baiduhi_category: Math
---

(hplonline)2010.2.20<br/><br/>
这几天本来不该写东西的，<br/>
但是不小心看到好东西，<br/>
没时间做，还是记几点想法。<br/><br/>
在matrix67这里看到的<a href="http://www.matrix67.com/blog/archives/2830" target="_blank">文章</a>。<br/><br/><font color="#0000ff">1.目的<br/></font><br/>
把不可导的max函数近似成为可导的指数对数函数，<br/>
是个很不错的事情。<br/>
用处是很显然的，<br/>
本来需要耗时的数值算法的地方，<br/>
可能直接推导出闭合的表达式。<br/>
在一些实际问题中，<br/>
满足一定精度就行了。<br/><br/><font color="#0000ff">2.改进精度调整<br/></font><br/>
想法是看到了地核maa04的留言后出来的。<br/>
“abs(0)的值和ln(exp(0)+exp(0))的距离有点远……”<br/><br/>
仿照原文中用k去调整精度的方法，<br/>
可以先对x、y加上某个大常数，最后再减去这个常数。<br/>
如果把原文的乘k视作正比放大，<br/>
这个改进的调整算是<font color="#ff0000">线性变换</font>。<br/><br/>
因为指数函数的目的在于放大差异，<br/>
所以想办法把指数部分弄大就行了。<br/>
当指数部分经过0的附近的时候，<br/>
通过找个大正数，总可以偏移到足够大的地方。<br/><br/>
反正就是想办法把x换成 k*x+b，<br/>
使得k*x+b是个很大的正数就行了。<br/><br/>
具体的效果有待以后在实践中绘图看看，这里就打住了。<br/><br/><font color="#0000ff">3.其他近似函数</font><br/><br/>
瞟了下<a href="http://www.johndcook.com/blog/2010/01/13/soft-maximum/" target="_blank">原文</a>，和下面的留言。<br/>
从wiki上得到了一点启示。<br/><br/>
用p-范数(p-norm)来说这个问题。<br/>
对于一个向量x，<br/>
2-norm(x)是它的模，<br/>
∞-norm(x)是它最大的分量的绝对值。<br/>
微积分里面也证过这个结论。<br/><br/>
于是可以用p-norm来提取最大的一个分量，让p足够大即可。<br/><br/>
注意到norm的表达式里面是有绝对值的，<br/>
这样使得近似max(,)以求可导的本意被破坏了。<br/><br/>
所以可以考虑给各个分量加上一个正大常数C，<br/>
这样就可以甩掉绝对值，<br/>
开了p次方之后再减去这个C即可。<br/><br/>
这里的p和C是经验性选取的，<br/>
如同前一条的k和b一样。<br/><br/><font color="#ff0000">未验证效果。</font><br/><br/><font color="#0000ff">4.理论比较</font><br/><br/>
这两个方法的核心思想在于扩大原各个比较项的差异，<br/>
使得在加法意义下，小项被忽略掉。<br/><br/>
而指数函数比幂函数更陡，<br/>
所以原文的指数函数应该比后面p-norm这方法逼近。<br/><br/>
p-norm这种方法在接近各项接近0的时候一样会有问题，<br/>
所以也需要对各项在处理前后调整下。<br/><br/>
