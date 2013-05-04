---
layout: post
title: "KEIL C 编译的TRICK探究1（条件跳转）"
date: 2009-03-01  15:58
comments: true
categories: tech
tags: ["Scm"]
_baiduhi_id: 57c903f7b8e29c2a730eecc6.html
_baiduhi_category: Scm
---

(hplonline)2009.3.1<br/><br/>
之前写的时候，用的都是C在写，感觉很顺手。。<br/><br/>
这几天看的是一个汇编的实验指导。。所以全部用的汇编。。<br/><br/>
这下问题就来了。。C51汇编的指令很少啊。有些东西就不知道是怎么实现的了。<br/><br/>
比如INTEL X86里面可以<br/>
cmp eax , ebx<br/>
jg XXX<br/>
来实现大于跳转<br/><br/>
而翻完了C51的指令集，也没发现类似jg的东西。。<br/><br/>
只有cjne a , b , c这个，当a不等于b的时候跳到c。<br/><br/>
所以比较好奇，看下KEIL是怎样办到的。<br/><br/><font color="#0000ff">一。实验代码</font><br/>
      uchar vc;<br/>
      uchar va , vb;<br/>
      va = 2  ;<br/>
      vb = 8 ; <br/>
      if ( va &gt; vb ) vc = va;<br/>
      else vc = vb ;<br/>
      while (1);<br/><br/><font color="#0000ff">二。直接在KEIL里面看反汇编</font><br/><br/>
C:0x0800      7E02       MOV        R6,#0x02<br/>
       9:           vb = 8 ;  <br/>
C:0x0802      7D08       MOV        R5,#0x08<br/>
      10:           if ( va &gt; vb ) vc = va; <br/>
C:0x0804      EE         MOV        A,R6<br/>
C:0x0805      D3         SETB       C<br/>
C:0x0806      9D         SUBB       A,R5<br/>
C:0x0807      4004       JC         C:080D<br/>
C:0x0809      7F02       MOV        R7,#0x02<br/>
C:0x080B      8002       SJMP       C:080F<br/>
      11:           else vc = vb ; <br/>
C:0x080D      AF05       MOV        R7,0x05<br/>
      12:           while (1); <br/>
C:0x080F      80FE       SJMP       C:080F<br/><br/>
这一点，我觉得KEIL做得不错，看起来很方便，源码与汇编对照。<br/><br/>
首先，通过几个赋值，知道在这里用的是寄存器变量<br/>
R6&lt;-&gt;va<br/>
R5&lt;-&gt;vb<br/>
R7&lt;-&gt;vc<br/><br/>
然后找到比较的核心：<br/>
C:0x0804      EE         MOV        A,R6<br/>
C:0x0805      D3         SETB       C<br/>
C:0x0806      9D         SUBB       A,R5<br/>
C:0x0807      4004       JC         C:080D<br/><br/>
这里就是编译器的TRICK了，你看没有用jg,jng之类，但是实现了这种功能<br/><br/>
其实前三句等于做了这样的一个运算<br/>
A = va - vb - 1<br/><br/>
如果va &gt; vb ， 那么将没有借位 <br/>
相反va &lt;= vb  ， 那么减的时候将设置借位，然后再根据情况跳转就行了。<br/><br/>
实际上，我么86汇编里面丰富的条件跳转也是靠判断这些标志位来的，<br/>
只不过硬件实现了，我们用起来很方便。<br/><br/>
如果把代码的 va &gt; vb改成 va &gt;= vb 呢<br/>
可以看到<br/>
C:0x0805      D3         SETB       C<br/>
被改成了<br/>
C:0x0805      D3        CLR       C<br/><br/>
相当于 A = va - vb<br/><br/>
到这里，条件跳转的问题基本就解决了。。<br/><br/>
顺便记一个事情。。就是51汇编里面只有SUBB，没有不带借位的减法。。<br/>
这个不知道是谁设计的，好囧。。。<br/><br/><font color="#ff6600">研究底层的东西并不表示我们一定要去用它，<br/>
至少让我们对编译器的作者产生感激之情吧。</font>
