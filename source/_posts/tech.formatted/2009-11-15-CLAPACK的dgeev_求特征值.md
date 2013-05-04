---
layout: post
title: "CLAPACK的dgeev_求特征值"
date: 2009-11-15  16:07
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: 0832b63e5cd883f0838b1386.html
_baiduhi_category: c&c++
---

<p>(hplonline)2009.11.15</p>
<p>CLAPACK在<a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/ede99845db316435869473c9.html">上一篇</a>介绍过了。<br/>
虽然这个库很强大，<br/>
但是参数太冏了，<br/>
看了很久才搞定。。</p>
<p>这篇讲解dgeev_函数的用法，<br/>
从这一个函数也可以认识LAPACK的一些习惯问题，<br/>
进而可以使用其他的函数。</p>
<p><font color="#0000ff">》》特征值和特征向量</font></p>
<p>我们平时使用的一般都是右特征向量，定义为：<br/>
A*alpha = lamda * alpha<br/>
另外还有一种定义的左特征向量：<br/>
beta*A = lamda * beta</p>
<p>而该函数被设计为可以选择求出：<br/>
只有特征值，左边特征向量，右边特征向量</p>
<p><font color="#0000ff">》》关于参数的解释</font></p>
<p>从头文件里面直接摘录的原型如下：</p>
<p>int dgeev_(char *jobvl, char *jobvr, integer *n, doublereal *<br/>
     a, integer *lda, doublereal *wr,</p>
<p>doublereal *wi, doublereal *vl, <br/>
     integer *ldvl, doublereal *vr, integer *ldvr, doublereal *work, <br/></p>
<p>  integer *lwork, integer *info);</p>
<p>首先，最明显的是，所有参数都按照指针传入。<br/>
然后这套函数库有个共同的习惯，<br/>
即要求调用者来处理空间，<br/>
包括提供返回值的空间，<br/>
用来计算的临时空间。</p>
<p><font color="#ff9900">函数命名：</font></p>
<p>d表示double。<br/>
ge表示general，说明是普通矩阵，按照列主序存储。<br/>
ev表示eigenvector吧（疑问语气），表达的是函数的功能。</p>
<p><font color="#ff9900">用到的类型解释：</font></p>
<p>char*，是字符串类型，但LAPACK的函数只关注该字符串的第一个字符<br/>
integer,就是C里面的int，一般用来指定维度<br/>
doublereal，就是C里面的double，参数类型和函数前缀统一（这里是d）</p>
<p><font color="#ff9900">各个参数：</font></p>
<p>char *jobvl, 第一个字符为'N'，表示不求左特征向量，为'V'表示要求<br/>
char *jobvr, 同上，是对右特征向量的选项<br/>
integer *n, 矩阵的列数<br/>
doublereal *<br/>
a, 存储A矩阵的空间（列主序！！）<br/>
integer *lda, A矩阵的行数<br/>
doublereal *wr, 返回的特征值，实部<br/>
doublereal *wi, 返回的特征值，虚部<br/>
doublereal *vl, 左特征向量的存储空间，大小为ldvl*n<br/>
integer *ldvl, 左特征向量存储空间的行数<br/>
doublereal *vr, 右特征向量的存储空间，大小为ldvr*n<br/>
integer *ldvr, 右特征向量存储空间的行数<br/>
doublereal *work, 工作空间，一般至少要4*n<br/>
integer *lwork, 工作空间的大小<br/>
integer *info，返回信息，0表示成功，-i表示第i个参数有问题，+i表示执行错误</p>
<p>具体的看一下代码就明白了，<br/>
实在觉得恼火的，照搬着用也行。。</p>
<p><font color="#ff9900">示例代码：</font></p>
<p>#include &lt; stdio.h&gt;</p>
<p>#pragma comment(lib , "blas.lib") <br/>
#pragma comment(lib , "clapack.lib")</p>
<p>void *malloc(size_t n) ;</p>
<p>#include "f2c.h"<br/>
#include "clapack.h"</p>
<p>int main(void)<br/>
{<br/>
     /* 3x3 matrix A<br/>
      * 76 25 11<br/>
      * 27 89 51<br/>
      * 18 60 32<br/>
      */<br/>
     doublereal A[9] = {76, 27, 18, 25, 89, 60, 11, 51, 32};</p>
<p>     integer info ;<br/>
     int i , j ;</p>
<p>     char jobvl = 'V' ;<br/>
     char jobvr = 'V' ;<br/>
     integer n = 3 ;<br/>
     doublereal *a = A ;<br/>
     integer lda = 3 ;<br/>
     <br/>
     doublereal* wr = (doublereal*)malloc( sizeof(doublereal) * n) ;<br/>
     doublereal* wi = (doublereal*)malloc( sizeof(doublereal) * n) ;   </p>
<p>     integer ldvr = 3 ;<br/>
     doublereal* vr = (doublereal*)malloc( sizeof(doublereal) * n * ldvr) ;</p>
<p>     integer ldvl = 3 ;<br/>
     doublereal* vl = (doublereal*)malloc( sizeof(doublereal) * n * ldvl) ;</p>
<p>     integer lwork = n * 4 ;<br/>
     doublereal *work = (doublereal*)malloc( sizeof(doublereal) * lwork) ;</p>
<p>     dgeev_(&amp;jobvl, &amp;jobvr, &amp;n, a,  &amp;lda, wr, wi, vl , &amp;ldvl , vr, &amp;ldvr, work, &amp;lwork, &amp;info) ;</p>
<p>     printf("info:%d\n" , info) ;<br/>
     printf("D = \n") ;<br/>
     for ( i = 0 ; i &lt; n ; i ++ ){<br/>
         for ( j = 0 ; j &lt; n ; j ++ ){<br/>
             if ( i == j ) printf("%10.5f" , wr[i]) ;<br/>
             else printf("%10.5f" , 0.0) ;<br/>
         }<br/>
         printf("\n") ;<br/>
     }<br/>
     printf("Vl = \n") ;<br/>
     for ( i = 0 ; i &lt; n ; i ++ ){<br/>
         for ( j = 0 ; j &lt; n ; j ++ ){<br/>
             printf("%10.5f" , vl[n * j + i]) ;<br/>
         }<br/>
         printf("\n") ;<br/>
     }<br/>
     printf("Vr = \n") ;<br/>
     for ( i = 0 ; i &lt; n ; i ++ ){<br/>
         for ( j = 0 ; j &lt; n ; j ++ ){<br/>
             printf("%10.5f" , vr[n * j + i]) ;<br/>
         }<br/>
         printf("\n") ;<br/>
     }<br/>
     return info;<br/>
}</p>
