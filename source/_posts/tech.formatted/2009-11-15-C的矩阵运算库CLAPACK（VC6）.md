---
layout: post
title: "C的矩阵运算库CLAPACK（VC6）"
date: 2009-11-15  14:55
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: ede99845db316435869473c9.html
_baiduhi_category: c&c++
---

<p>(hplonline)2009.11.14</p>
<p><font color="#0000ff">》》各种资料和笔记</font></p>
<p>主页<br/><a href="http://www.netlib.org/clapack/">http://www.netlib.org/clapack/</a></p>
<p>一份简单的CLAPACK的hello world<br/><a href="http://www.cs.rochester.edu/~bh/cs400/using_lapack.html">http://www.cs.rochester.edu/~bh/cs400/using_lapack.html</a></p>
<p>vc6的工具包intro<br/><a href="http://www.netlib.org/clapack/readme.claw32">http://www.netlib.org/clapack/readme.claw32</a><br/>
（这个可以直接用）</p>
<p>winNT下安装一些hint<br/><a href="http://www.netlib.org/clapack/faq.html#1.10">http://www.netlib.org/clapack/faq.html#1.10</a></p>
<p>一篇比较详尽地从BLAS到LAPACK的方法<br/><a href="http://icl.cs.utk.edu/lapack-forum/viewtopic.php?f=2&amp;t=1595&amp;sid=0365ef1e599136085d9385ebb1a6c588">http://icl.cs.utk.edu/lapack-forum/viewtopic.php?f=2&amp;t=1595&amp;sid=0365ef1e599136085d9385ebb1a6c588</a></p>
<p>CLAPACK的readme<br/><a href="http://www.netlib.org/clapack/readme">http://www.netlib.org/clapack/readme</a></p>
<p><font color="#ff9900">1.命名方式</font></p>
<p>使用<br/>
#include "f2c.h"<br/>
其中包含一些变量类型和函数类型的定义</p>
<p>在fortran里面写作<br/>
call func(..)<br/>
在C里面写作<br/>
func_()</p>
<p><font color="#ff9900">2.参数传递方式</font></p>
<p>要求都以“引用”传递，<br/>
在C里面表现为全部是指针。</p>
<p><font color="#ff9900">3.字符（串）参数</font></p>
<p>在除了测试和定时代码(timing code)的所有地方，<br/>
函数关注的都仅仅是第一个字符。</p>
<p>引用readme里面的例子，</p>
<p>fortran：<br/>
#     call dpotrf( 'Upper', n, a, lda, info )</p>
<p>C：<br/>
#     char s = 'U';<br/>
#     dpotrf_(&amp;s, &amp;n, a, &amp;lda, &amp;info);</p>
<p><font color="#ff9900">4.矩阵的主序问题</font></p>
<p>在fortran里面是列主序，<br/>
C中是行主序。</p>
<p>C中调用的正确方法应该是，<br/>
申请一个一维数组，<br/>
然后按照列主序给元素赋值。</p>
<p>（原readme指出，<br/>
a[M][N]这样的二维定义，<br/>
可能被编译器实现为不连续的空间。<br/>
即Iliffle向量（ECP中的叫法）的方式。）</p>
<p><br/>
手册：<br/><a href="http://www.netlib.org/lapack/lug/">http://www.netlib.org/lapack/lug/</a></p>
<p>使用dgeev_的问题：<br/><a href="https://icl.cs.utk.edu/lapack-forum/viewtopic.php?f=2&amp;t=661">https://icl.cs.utk.edu/lapack-forum/viewtopic.php?f=2&amp;t=661</a></p>
<p>手册中关于参数的解释：<br/><a href="http://www.netlib.org/lapack/lug/node110.html">http://www.netlib.org/lapack/lug/node110.html</a></p>
<p>----------参数传递的习惯</p>
<p>N 问题的尺寸，也即列的数量<br/>
LD?? (Leading Dimension)，即行的数量<br/>
info 0表示成功，-i表示第i个参数错误，+i计算错误<br/>
work 工作空间<br/>
lwork 工作空间的大小，可以传入-1以从work返回需要的空间<br/>
(这个功能一直没有尝试成功喃。。。）</p>
<p>----------</p>
<p><font color="#0000ff">》》环境搭建和第一个简单程序（VC6)</font></p>
<p>我就直接用的下面这个编译好的库：<br/><a href="http://www.netlib.org/clapack/CLAw32.zip">http://www.netlib.org/clapack/CLAw32.zip</a><br/>
在对应的地方去把clapack.lib和blas.lib复制到工程目录下。</p>
<p>把clapack.h复制到工程目录下（从<a href="http://www.netlib.org/clapack/">http://www.netlib.org/clapack/</a>下载）</p>
<p><br/>
#include &lt; stdio.h&gt;</p>
<p>#pragma comment(lib , "blas.lib") <br/>
#pragma comment(lib , "clapack.lib")</p>
<p>#include "f2c.h"<br/>
#include "clapack.h"</p>
<p>int main(void)<br/>
{<br/>
     /* 3x3 matrix A<br/>
      * 76 25 11<br/>
      * 27 89 51<br/>
      * 18 60 32<br/>
      */<br/>
     double A[9] = {76, 27, 18, 25, 89, 60, 11, 51, 32};<br/>
     double b[3] = {10, 7, 43};</p>
<p>     int N = 3;<br/>
     int nrhs = 1;<br/>
     int lda = 3;<br/>
     int ipiv[3];<br/>
     int ldb = 3;<br/>
     int info;<br/>
     <br/>
     dgesv_(&amp;N, &amp;nrhs, A, &amp;lda, ipiv, b, &amp;ldb, &amp;info);</p>
<p>     if(info == 0) /*  succeed */ <br/>
 printf("The solution is %lf %lf %lf\n", b[0], b[1], b[2]);<br/>
     else<br/>
 fprintf(stderr, "dgesv_ fails %d\n", info);</p>
<p>     return info;<br/>
}</p>
<p><font color="#0000ff">》》遗留问题</font></p>
<p>直接下载的源码没有编译通，<br/>
搞不懂，据说是VS05的工程，<br/>
我在VS08下没有搞定。。</p>
<p>然后CLAPACK里面函数参数实在是太抽象了，<br/>
不符合通常的应用习惯，需要再次进行封装。</p>
