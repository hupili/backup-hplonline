---
layout: post
title: "linux shell+C++暴力24点"
date: 2010-01-16  19:01
comments: true
categories: tech
tags: ["Linux"]
_baiduhi_id: 4f3587b1e0002a5f0823026c.html
_baiduhi_category: Linux
---

<p>(hplonline)2010.1.16</p>
<p>24点的程序可以说很多人都写过，<br/>
用不同的语言，不同的思路。<br/>
即使都是全枚举，很多细节也会不一样。</p>
<p>写了一天的文档，累得不行了。。<br/>
以前没写过，正好最近搞linux，就用SHELL和C++来暴力一个24点。</p>
<p><font color="#0000ff">思路：</font></p>
<p>linux的shell有个好处就是可以直接按整形算符计算表达式。<br/>
于是可以把表达式构造好，然后交给shell就行了。<br/>
虽然直接用shell也可以构造表达式，<br/>
但毕竟对C熟悉一点，觉得shell的语法很别扭，<br/>
故就用C++来产生表达式。</p>
<p>我用的方法会产生出重复的，<br/>
但实际上是<font color="#ff0000">交换律、结合律、括号法则等意义下的重复</font>，<br/>
比如，3+4，4+3在我这里就认为是两个表达式。<br/>
要达到绝对化的不重复，写起来就很烦了。<br/>
再说，所有合法的表达式都是在四则运算意义下的重复。<br/>
24=(4-2)*(3+9)<br/>
24=((2*4)*9)/3<br/>
就像上面两个式子整体看上去都是一个意思，怎么能说没重复呢？<br/>
如果我用手把他们的细节遮住，你只可能看到两个24。</p>
<p>首先，对四个数进行全排列。<br/>
1 2 3 4 <br/>
1 2 4 3 <br/>
....<br/>
4 3 2 1 <br/>
这个用<font color="#ff0000">next_permutation</font>就出来了。</p>
<p>然后归纳模式，我觉得应该只有下面这几种吧：<br/><font color="#ff9900">     "((%d%c%d)%c%d)%c%d" ,<br/>
     "(%d%c%d)%c(%d%c%d)" ,<br/>
     "(%d%c(%d%c%d))%c%d" ,<br/>
     "%d%c((%d%c%d)%c%d)" ,<br/>
     "%d%c(%d%c(%d%c%d))" ,</font><br/>
在四个%d的地方，依次填上四个数。<br/>
在有%c的地方填上运算符。<br/>
只考虑了+-*/四种，就依次带入就行了。</p>
<p>够暴力吧，哈哈。</p>
<p><font color="#0000ff">用来计算表达式的shell脚本：cal24.sh</font></p>
<p>#!/bin/bash<br/>
#created by hpl<br/>
#2010.1.16<br/>
#take advantage of linux shell to caculate 24 points</p>
<p>function eval_exp(){<br/>
#     echo $1<br/>
declare -i re=$1<br/>
if [ "$re" == "24" ] ; then<br/>
echo "24=$1"<br/>
fi<br/>
}</p>
<p>eval_exp $1</p>
<p><font color="#0000ff">生成表达式的C++程序：</font></p>
<p><br/>
#include &lt;iostream&gt;<br/>
#include &lt;algorithm&gt;<br/>
#include &lt;stdio.h&gt;</p>
<p>using namespace std ;</p>
<p>char *patterns[] = {<br/>
     "((%d%c%d)%c%d)%c%d" ,<br/>
     "(%d%c%d)%c(%d%c%d)" ,<br/>
     "(%d%c(%d%c%d))%c%d" ,<br/>
     "%d%c((%d%c%d)%c%d)" ,<br/>
     "%d%c(%d%c(%d%c%d))" ,<br/>
} ;<br/>
const int P_NUM = 5 ;</p>
<p>void brute_force(int *a){<br/>
     const char c[] = "+-*/" ;<br/>
     char i[3] , j ;<br/>
     char buffer[100] , cmd[150] ;<br/>
     <br/>
     for ( i[0] = 0 ; i[0] &lt; 4 ; i[0] ++ ){<br/>
         for ( i[1] = 0 ; i[1] &lt; 4 ; i[1] ++){<br/>
             for ( i[2] = 0 ; i[2] &lt; 4 ; i[2] ++){<br/>
                 for ( j = 0 ; j &lt; P_NUM ; j ++ ) {<br/>
                     sprintf(buffer , patterns[j] , a[0] , c[i[0]] ,<br/>
                         a[1] , c[i[1]] , a[2] , c[i[2]] , a[3] , c[i[3]]) ;<br/>
                     sprintf(cmd , "./cal24.sh \"%s\" 2&gt; /dev/null" , buffer) ;<br/>
                     //printf(cmd) ;<br/>
                     system(cmd) ;<br/>
                 }                <br/>
             }<br/>
         }<br/>
     }<br/>
}</p>
<p>int main(){<br/>
     int a[4] ;<br/>
     int i ;<br/>
     printf("please input 4 numbers , seperate by blanks:\n") ;<br/>
     for ( i = 0 ; i &lt; 4 ; i ++ ){<br/>
         scanf("%d" , &amp;a[i]) ;<br/>
     }<br/>
     sort(a , a + 4) ;<br/>
     do{<br/>
         brute_force(a) ;        <br/>
         /*     for ( i = 0 ; i &lt; 4 ; i ++ ){<br/>
         printf("%d " , a[i]) ;<br/>
         }<br/>
         printf("\n") ;<br/>
         */<br/>
     }while ( next_permutation(a , a+4)) ;<br/>
     return 0 ;<br/>
}</p>
<p><br/><font color="#0000ff">运行示例：</font></p>
<p>please input 4 numbers , seperate by blanks:<br/>
4 2 3 9<br/>
24=((2*4)*9)/3<br/>
24=(2*4)*(9/3)<br/>
24=(2*(4*9))/3<br/>
24=2*((4*9)/3)<br/>
24=2*(4*(9/3))<br/>
24=((2*9)/3)*4<br/>
24=(2*(9/3))*4<br/>
24=2*((9/3)*4)<br/>
24=((2*9)*4)/3<br/>
24=(2*(9*4))/3<br/>
24=2*((9*4)/3)<br/>
24=3*(4+(9/2))<br/>
24=((3+9)/2)*4<br/>
24=3*((9/2)+4)<br/>
24=(3+9)*(4-2)<br/>
24=((3+9)*4)/2<br/>
24=(3+9)*(4/2)<br/>
24=(4-2)*(3+9)<br/>
24=(4/2)*(3+9)<br/>
24=(4-2)*(9+3)<br/>
24=((4*2)*9)/3<br/>
24=(4*2)*(9/3)<br/>
24=(4*(2*9))/3<br/>
24=4*((2*9)/3)<br/>
24=4*(2*(9/3))<br/>
24=(4/2)*(9+3)<br/>
24=(4*(3+9))/2<br/>
24=4*((3+9)/2)<br/>
24=(4+(9/2))*3<br/>
24=((4*9)*2)/3<br/>
24=(4*(9*2))/3<br/>
24=4*((9*2)/3)<br/>
24=(4*(9+3))/2<br/>
24=4*((9+3)/2)<br/>
24=((4*9)/3)*2<br/>
24=(4*(9/3))*2<br/>
24=4*((9/3)*2)<br/>
24=((9*2)/3)*4<br/>
24=((9*2)*4)/3<br/>
24=(9*(2*4))/3<br/>
24=((9/2)+4)*3<br/>
24=((9+3)/2)*4<br/>
24=((9/3)*2)*4<br/>
24=(9/3)*(2*4)<br/>
24=(9+3)*(4-2)<br/>
24=((9+3)*4)/2<br/>
24=(9+3)*(4/2)<br/>
24=((9/3)*4)*2<br/>
24=(9/3)*(4*2)<br/>
24=((9*4)*2)/3<br/>
24=(9*(4*2))/3<br/>
24=((9*4)/3)*2</p>
<p><font color="#0000ff">遗留问题：</font></p>
<p>由C程序产生的表达式，有不少是可能出现错误的。像<br/><font color="#ff0000">declare -i k="1/(1-1)"</font><br/>
执行时就会报一个除0错误。</p>
<p>由于没有找到容错的方法，<br/>
只有在调用的时候来个 <font color="#ff0000">2&gt; /dev/null</font><br/>
。。。</p>
<p>还是vb系列的很好用。。<br/>
不管啥错误，<br/>
一句on error resume next 。<br/>
或者on error goto就解决了。</p>
<p>另外，这个程序会跑比较久才有结果，<br/>
毕竟写起来方便，用起来就慢了。。</p>
