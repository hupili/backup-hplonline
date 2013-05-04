---
layout: post
title: "尽量避免stack overflow的quick sort的一种写法"
date: 2009-04-24  21:39
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: a8d29150a0f2506a84352447.html
_baiduhi_category: 算法
---

(hplonline)2009.4.24<br/><br/>
关于quick sort，人类给出了不少讨论。<br/>
有讲median of three的，有讲蒙特卡罗优化的，有讲intro-sort的。<br/><br/>
而最近在STL里面淘宝。。很火星地发现了qsort的另外一种写法。<br/>
那一处候老师的批注是<font color="#ff0000">可读性较差</font>。。<br/>
我也这么认为，不过仔细一想，发现科学家毕竟就是科学家。。<br/>
问题考虑得如此之细致。<br/><br/>
这里我不会关注其他方面的优化，仅仅是说一下这个可以尽量<font color="#ff0000">避免stack overflow</font>的写法<br/><br/>
先给出一个以前很常用的写法。<br/><br/><font color="#ff6600">//对[first , last)区间排序<br/>
void qs( int *first , int *last ){<br/>
     int *i , *j ;<br/>
     i = first ; <br/>
     j = last - 1 ;<br/>
     if ( i &gt;= j ) return ;<br/>
     int t = *first ;<br/>
     while ( i &lt; j ){<br/>
          while ( i &lt; j &amp;&amp; t &lt;= *j ) j -- ;<br/>
          *i = *j ;<br/>
          while ( i &lt; j &amp;&amp; *i &lt;= t ) i ++ ;<br/>
          *j = *i ;<br/>
     }<br/>
     *i = t ;<br/>
     qs(first , i) ;<br/>
     qs(i + 1 , last) ;<br/>
}</font><br/><br/>
这个写法应该说很好懂的。估计搞OI和ACM的人都能瞬间拍出来。<br/><br/>
而提到qsort。人们常喜欢讨论的是在数据几乎有序的情况下，时间有多糟糕。<br/><br/>
其实，再怎么糟糕也是n^2的。而少有人提到的但更糟糕的其实是<font color="#ff0000">stack overflow</font>。<br/><br/>
比如在我机器上，跑10000的数组上面那算法就爆堆栈了。（跟具体环境有关系）<br/>
但是，下面将给出的改造的qsort，同样也是蜕化到n^2，瞬间出解。<br/><br/>
也就是，在某些情况下，爆堆栈比耗时间更严重。<br/>
于是要想办法改进。。<br/><br/>
那么，仿照STL中sort的写法，给出一个下面的版本：<br/>
（说仿照，因为STL的sort还有许多其他优化，而我这里关注的是其中一点，<br/>
于是就把核心思想提取出来了）<br/><br/><font color="#ff6600">//对[first , last)区间排序<br/>
void qs2( int *first , int *last ){<br/>
     int *i , *j ;<br/>
     while ( first &lt; last ){<br/>
          int t = *first ; <br/>
          i = first ; <br/>
          j = last - 1 ;<br/>
          while ( i &lt; j ){<br/>
               while ( i &lt; j &amp;&amp; t &lt;= *j ) j -- ;<br/>
               *i = *j ;<br/>
               while ( i &lt; j &amp;&amp; *i &lt;= t ) i ++ ;<br/>
               *j = *i ;<br/>
          }<br/>
          *i = t ;<br/>
          if ( i - first &lt; last - i ){<br/>
               qs2( first , i ) ;<br/>
               first = i + 1 ;<br/>
          }else{<br/>
               qs2( i + 1 , last ) ;<br/>
               last = i ;     <br/>
          }<br/>
     }<br/>
} </font><br/><br/>
其中的主要优化，就在于用：<br/><br/><font color="#ff6600">         if ( i - first &lt; last - i ){<br/>
               qs2( first , i ) ;<br/>
               first = i + 1 ;<br/>
          }else{<br/>
               qs2( i + 1 , last ) ;<br/>
               last = i ;     <br/>
          }</font><br/><br/>
去代替了原来的递归。<br/><br/>
优化前，是对分区后的左段和右段分别递归。<br/>
那么，数据有序时，会向右递归n层下去，显然是个很大的数字。<br/>
爆堆栈太正常了。<br/><br/>
改进的算法先进行判断，然后递归排序短的那一段，<br/>
同时修改原来标定的[first,last)区间，得以在同一层递归中再次对新区间排序。<br/>
因为选的是较小的一层递归，所以总层数一定不会超过log(n)的。<br/><br/>
所以有的时候，我们不仅要关注一个抽象级别的时间和空间复杂度。<br/>
也要注意编码上的优化，要考虑到机器的实际运行情况。。<br/><br/>
一点小小的改动，使得可以应对的数据增长了相当之多<br/>
（从耗栈的角度考察。。如果要从时间上说，当然还需要其他优化）<br/><br/>
再次膜拜科学家。。
