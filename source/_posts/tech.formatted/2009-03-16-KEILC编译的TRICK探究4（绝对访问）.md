---
layout: post
title: "KEIL C 编译的TRICK探究4（绝对访问）"
date: 2009-03-16  21:32
comments: true
categories: tech
tags: ["Scm"]
_baiduhi_id: 2410eccdd0f2b6590eb34509.html
_baiduhi_category: Scm
---

因为隔了有这么远了，所以给个第3回的传送门。<br/><a href="http://hi.baidu.com/hplonline/blog/item/cb5e40edd67c8cdcb21cb166.html" target="_blank">hi.baidu.com/hplonline/blog/item/cb5e40edd67c8cdcb21cb166.html</a><br/>
前三篇都是连在一起的，比较好找。<br/><br/>
==================================================================<br/><br/>
(hplonline)2009.3.16<br/><br/>
从汇编上手的人，可能对KEIL C的一些东西感到疑惑。<br/>
因为我们汇编里面用<font color="#ff0000">MOV,MOVC,MOVX</font>来区分访问的内存区域。<br/>
而C里面隐藏很多内存相关的细节。<br/>
虽然有指针这个东西，但是如果我定义一个char *p，那么他究竟指向哪呢？<br/>
内部RAM，ROM，外部RAM？这一下就没了个统一的标准。<br/><br/>
那么要叙述这个事情，就直接用前面8255A的练习图了。<br/><a href="http://hi.baidu.com/hplonline/blog/item/cc2e5bda324f2cd3b7fd4812.html" target="_blank">hi.baidu.com/hplonline/blog/item/cc2e5bda324f2cd3b7fd4812.html</a><br/><br/>
这回用C程序：<br/><br/>
#include &lt;reg51.h&gt;<br/>
#include &lt;absacc.h&gt;<br/><br/>
#define PORTA 0x73fc<br/>
#define PORTB 0x77fd<br/>
#define PORTC 0x7bfe<br/>
#define CONTROL 0x7fff<br/>
#define MOD_AoutBin 0x82<br/><br/>
void main(){<br/>
       unsigned char tmp ;<br/><br/>
       XBYTE[CONTROL] = MOD_AoutBin ;       <br/>
       while (1){<br/>
              tmp = XBYTE[PORTB] ;<br/>
              XBYTE[PORTA] = tmp ;<br/>
       };<br/>
}<br/><br/>
看起来可谓简单。不过这里不讲8255A的东西。要看的就是这个XBYTE<br/><br/>
这个东西在<font color="#ff0000">#include &lt;absacc.h&gt;</font>里面有。<br/><font color="#0000ff">absolute access（绝对访问）</font><br/><br/>
其中的定义：<br/><font color="#ff0000">#define XBYTE ((unsigned char volatile xdata *) 0)</font><br/><br/>
这个宏返回的相当于就是一指针，而类似于<br/><font color="#ff0000">XBYTE[XXX] = YYY </font><br/>
的用法。则是都很熟悉的脱指针引用了。<br/><br/>
unsigned char volatile 这个应该是很常见的。<br/>
前面是无符号字符型，<br/><font color="#ff0000">volatile是多变的意思，用这个修饰变量以避免编译器优化。</font><br/>
具体的网上的介绍颇多。<br/><br/>
那么关键的地方其实就是xdata *，他表达的是这个指向的变量放在xdata区域。<br/><br/>
比如写一句下面的话<br/>
       unsigned char xdata  p ;<br/>
       p = 1 ;<br/>
编译过后<br/>
C:0x0803       7401        MOV         A,#0x01<br/>
C:0x0805       F0          MOVX        @DPTR,A<br/>
看到了吧，这里就是很熟悉的汇编访问外部RAM的方法了。<br/><br/>
那么如果直接一个xdata p = 1，是什么情况呢？<br/>
C:0x0800       900000      MOV         DPTR,#C_STARTUP(0x0000)<br/>
C:0x0803       E4          CLR         A<br/>
C:0x0804       F0          MOVX        @DPTR,A<br/>
C:0x0805       A3          INC         DPTR<br/>
C:0x0806       04          INC         A<br/>
C:0x0807       F0          MOVX        @DPTR,A<br/>
可见这里是一个short int的操作，分了两次赋值。<br/>
说明默认的变量类型是short int。<br/><br/>
嗯，差不多就这样吧。<br/><br/>
同时还有data , pdata , code 等 ，所有含义摘抄如下：<br/><br/><font color="#ff6600">data       可以直接存取的片内数据存储区（128字节）<br/>
bdata       可以位寻址（Bit Addressable）的片内存储区，允许位与字节混合访问（16字节）<br/>
idata       以 Mov @Rn 存取的片内数据存储区（256字节）<br/>
pdata       以 MOVX @Rn 存取的外部数据存储区，分页寻址，（256字节）<br/>
xdata       以 MOVX @DPTR 存取的外部数据存储区（64KB）<br/>
code       以 MOVC @A+DPTR 读取的程序内存，程序代码存储区（64KB）</font>
