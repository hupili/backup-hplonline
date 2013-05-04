---
layout: post
title: "不要YY：if和switch的那么些事情（C)"
date: 2009-05-04  19:50
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: 68db0055fd7f77ccb645ae3d.html
_baiduhi_category: c&c++
---

(hplonline)2009.5.4<br/><br/>
今天看到有个老外写了下面这段话：<br/><title>C Optimisation tutorial</title><h3>switch() instead of if...else...</h3>
For large decisions  involving if...else...else..., like this:
<pre>if( val == 1)        <br/>dostuff1();<br/> else if (val == 2)        <br/>dostuff2();<br/> else if (val == 3)        <br/>dostuff3();</pre>
it may be faster to use a switch:
<pre>switch( val ) {       <br/> case 1: dostuff1(); break;        <br/> case 2: dostuff2(); break;         <br/>case 3: dostuff3(); break; <br/>}</pre>
In the if() statement, if the last case is required, all the previous  ones will be tested first. The switch lets us cut out this extra work. If you  have to use a big if..else.. statement, test the most likely cases first. <br/><br/>
=====注意从这开始是我写的了。。<br/><br/><font color="#0000ff">啥都不说，写代码测试：</font><br/>
#include &lt;stdio.h&gt;<br/><br/>
void f1(){}<br/>
void f2(){}<br/>
void f3(){}<br/><br/>
int main()<br/>
{<br/>
       int val ;<br/>
       val = 0x1111 ;       <br/>
       if( val == 1)<br/>
              f1();<br/>
       else if (val == 2)<br/>
              f2();<br/>
       else if (val == 3)<br/>
              f3();<br/>
       <br/>
       //       it may be faster to use a switch:<br/>
       <br/>
       val = 0x2222 ;<br/>
       switch( val )<br/>
       {<br/>
       case 1: f1(); break;              <br/>
       case 2: f2(); break;              <br/>
       case 3: f3(); break;<br/>
       }<br/>
       return 0;<br/>
}<br/><font color="#0000ff"><br/>
然后，看汇编：</font><br/><br/><font color="#ff6600">这是对应if的那一组：</font><br/>
004010D8  |.  C745 FC 11110&gt;mov        dword ptr [ebp-4], 1111<br/>
004010DF  |.  837D FC 01       cmp        dword ptr [ebp-4], 1<br/>
004010E3  |.  75 07            jnz        short 004010EC<br/>
004010E5  |.  E8 25FFFFFF      call       0040100F<br/>
004010EA  |.  EB 18            jmp        short 00401104<br/>
004010EC  |&gt;  837D FC 02       cmp        dword ptr [ebp-4], 2<br/>
004010F0  |.  75 07            jnz        short 004010F9<br/>
004010F2  |.  E8 13FFFFFF      call       0040100A<br/>
004010F7  |.  EB 0B            jmp        short 00401104<br/>
004010F9  |&gt;  837D FC 03       cmp        dword ptr [ebp-4], 3<br/>
004010FD  |.  75 05            jnz        short 00401104<br/>
004010FF  |.  E8 01FFFFFF      call       00401005<br/><br/><font color="#ff6600">这是对应switch的那一组：</font><br/>
00401104  |&gt;  C745 FC 22220&gt;mov        dword ptr [ebp-4], 2222<br/>
0040110B  |.  8B45 FC          mov        eax, dword ptr [ebp-4]<br/>
0040110E  |.  8945 F8          mov        dword ptr [ebp-8], eax<br/>
00401111  |.  837D F8 01       cmp        dword ptr [ebp-8], 1<br/>
00401115  |.  74 0E            je         short 00401125<br/>
00401117  |.  837D F8 02       cmp        dword ptr [ebp-8], 2<br/>
0040111B  |.  74 0F            je         short 0040112C<br/>
0040111D  |.  837D F8 03       cmp        dword ptr [ebp-8], 3<br/>
00401121  |.  74 10            je         short 00401133<br/>
00401123  |.  EB 13            jmp        short 00401138<br/>
00401125  |&gt;  E8 E5FEFFFF      call       0040100F<br/>
0040112A  |.  EB 0C            jmp        short 00401138<br/>
0040112C  |&gt;  E8 D9FEFFFF      call       0040100A<br/>
00401131  |.  EB 05            jmp        short 00401138<br/>
00401133  |&gt;  E8 CDFEFFFF      call       00401005<br/><br/>
我想。。视力正常的人都看出来谁长谁短了。。。<br/><br/>
很明显，<font color="#ff0000">switch还要多几句话。不过比较次数是一样的。</font><br/><br/>
从高级语言的层面上来看，switch给人的感觉确实是:<br/>
一次switch，直接到相应的case。貌似很快<br/><br/>
而用if却要不断地if,else,if,else。。。。<br/><br/>
不过，上面的代码充分说明那是YY出来的。<br/><font color="#ff0000">实际上，switch有多少case就要cmp,je多少次。</font><br/><br/>
所以，当我们痛恨国内教材的时候，也要清醒地认识到，<br/>
其实老外也会YY的。<br/>
不过出于严谨的措辞：<br/>
it may be faster to use a switch: <br/>
这个“may”很关键<br/><br/>
话又说回来，最后一句：<br/><font color="#ff0000">test the most likely cases first</font><br/><br/>
倒是真的，能随时记着最好。
