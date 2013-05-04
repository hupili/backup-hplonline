---
layout: post
title: "C++中placement new在VC6中的实现"
date: 2010-06-17  10:03
comments: true
categories: tech
tags: ["Asm"]
_baiduhi_id: 96aee1f811036102d8f9fd22.html
_baiduhi_category: Asm
---

(hplonline)2010.6.17<br/><br/>
昨天研究了一个题，于是认识了所谓的<a href="http://hi.baidu.com/hplonline/blog/item/0a3fa76e45727fd780cb4ac9.html" target="_blank">placement new</a>。<br/><br/>
虽然做几个实验，<br/>
从现象上可以确定什么是placement new，<br/>
但总对其实现耿耿于怀。<br/><font color="#0000ff"><br/>
》》代码：（上篇的程序，只贴主要部分）</font><br/><br/>
int main(){<br/>
int *p ;<br/>
cls1 *p1 = new cls1 ;<br/>
p1-&gt;print() ;<br/>
p = (int*)p1 ;<br/>
cout&lt;&lt;"cookie:"&lt;&lt;p[-4]&lt;&lt;endl ;<br/><br/>
cls2 *p2 ;<br/><font color="#ff0000">p2 = new(p1) cls2 ;</font><br/>
p2-&gt;print() ;<br/>
p1-&gt;print() ;<br/>
p = (int*)p2 ;<br/>
cout&lt;&lt;"cookie:"&lt;&lt;p[-4]&lt;&lt;endl ;<br/><br/>
return 0 ;<br/>
}<br/><br/>
主要就是想看一些红色这句会产生什么样的目标代码。<br/><br/>
因为通过之前打印cookie的实验，<br/>
可以知道空间并没有重新分配，<br/>
但是当两个类的大小不一样的时候，<br/>
编译器是否会给new传入这个信息呢？<br/><br/><font color="#0000ff">》》debug方式的目标代码</font><br/><br/>
main函数：<br/><br/>
00401658   .  8B55 EC       mov     edx, dword ptr [ebp-14]<br/>
0040165B   .  52            push    edx<br/>
0040165C   .  6A 08       <font color="#ff0000">  push    8</font><br/>
0040165E   .  E8 F2F9FFFF   call    00401055<br/><br/>
可以看到，第二种类的信息是传入了的！！<br/>
那为什么不根据这个重新分配空间呢？<br/><br/>
operator new函数（placement new的版本）：<br/><br/>
00401B90 &gt;/&gt; \55            push    ebp<br/>
00401B91  |.  8BEC          mov     ebp, esp<br/>
00401B93  |.  83EC 40       sub     esp, 40<br/>
00401B96  |.  53            push    ebx<br/>
00401B97  |.  56            push    esi<br/>
00401B98  |.  57            push    edi<br/>
00401B99  |.  8D7D C0       lea     edi, dword ptr [ebp-40]<br/>
00401B9C  |.  B9 10000000   mov     ecx, 10<br/>
00401BA1  |.  B8 CCCCCCCC   mov     eax, CCCCCCCC<br/>
00401BA6  |.  F3:AB         rep     stos dword ptr es:[edi]<br/><font color="#ff0000">00401BA8  |.  8B45 0C       mov     eax, dword ptr [ebp+C]</font><br/>
00401BAB  |.  5F            pop     edi                              ;  0012FF3C<br/>
00401BAC  |.  5E            pop     esi<br/>
00401BAD  |.  5B            pop     ebx<br/>
00401BAE  |.  8BE5          mov     esp, ebp<br/>
00401BB0  |.  5D            pop     ebp<br/>
00401BB1  \.  C3            retn<br/><br/>
[epb+C]就是我们push的第一个参数，也就是new括号中的那个指针。<br/>
从红色这句可以看到，程序赤裸裸地把这个指针原样返回了。<br/><br/>
这么大一个过程，其实一个mov就可以解决，怎么会这么扭曲。。<br/><br/><font color="#0000ff">》》release方式编译</font><br/><br/>
怀疑是不是debug方式编译器不知道优化，<br/>
故使用release来看一下。<br/><br/>
main：<br/><br/>
0040165B   .  52            push    edx<br/>
0040165C   .  6A 08         push    8<br/>
0040165E   .  E8 F2F9FFFF   call    00401055<br/><br/>
operator new：<br/><br/>
00401B90 &gt;/&gt; \55            push    ebp<br/>
00401B91  |.  8BEC          mov     ebp, esp<br/>
00401B93  |.  83EC 40       sub     esp, 40<br/>
00401B96  |.  53            push    ebx<br/>
00401B97  |.  56            push    esi<br/>
00401B98  |.  57            push    edi<br/>
00401B99  |.  8D7D C0       lea     edi, dword ptr [ebp-40]<br/>
00401B9C  |.  B9 10000000   mov     ecx, 10<br/>
00401BA1  |.  B8 CCCCCCCC   mov     eax, CCCCCCCC<br/>
00401BA6  |.  F3:AB         rep     stos dword ptr es:[edi]<br/>
00401BA8  |.  8B45 0C       mov     eax, dword ptr [ebp+C]<br/>
00401BAB  |.  5F            pop     edi<br/>
00401BAC  |.  5E            pop     esi<br/>
00401BAD  |.  5B            pop     ebx<br/>
00401BAE  |.  8BE5          mov     esp, ebp<br/>
00401BB0  |.  5D            pop     ebp<br/>
00401BB1  \.  C3            retn<br/><br/>
可以看到，简化的只是main函数里面的一些冗余赋值语句。<br/>
本质上的调用<font color="#ff0000">operator new(size , pointer)</font>的框架没有改变。<br/><br/><font color="#ff00ff">附记：</font><br/><br/>
release方式下没有源码信息，故定位比较麻烦，只有手动跟踪。<br/>
从代码入口开始，找到三次特征的压栈操作即可，<br/>
并且main的入口在调用exit之前。<br/><br/>
00422490  |.  8B15 E0D34700 mov     edx, dword ptr [_environ]<br/>
00422496  |.  52          <font color="#ff0000">  push    edx</font><br/>
00422497  |.  A1 D8D34700   mov     eax, dword ptr<font color="#ff0000"> [__argv]</font><br/>
0042249C  |.  50       <font color="#ff0000">     push    eax</font><br/>
0042249D  |.  8B0D D4D34700 mov     ecx, dword ptr<font color="#ff0000"> [__argc]</font><br/>
004224A3  |.  51        <font color="#ff0000">    push    ecx</font><br/>
004224A4  |.  E8 91EDFDFF   call    0040123A<br/>
004224A9  |.  83C4 0C       add     esp, 0C<br/>
004224AC  |.  8945 E4       mov     dword ptr [ebp-1C], eax<br/>
004224AF  |.  8B55 E4       mov     edx, dword ptr [ebp-1C]<br/>
004224B2  |.  52            push    edx                              ; /status<br/>
004224B3  |.  E8 E8400000   <font color="#ff0000">call    exit                             ; \exit</font><br/><br/><font color="#0000ff">》》结论</font><br/><br/>
从表面上看，这个placement new着实有种脱了裤子放屁的感觉。<br/>
不过为什么要这样设计，前人也许有他们自己的原因。<br/>
麻烦知道的同学告诉一声。<br/><br/>
