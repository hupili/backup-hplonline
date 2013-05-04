---
layout: post
title: "volatile(c++)"
date: 2009-04-13  18:37
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: baf29d2bb27a5ff2e7cd400b.html
_baiduhi_category: c&c++
---

(hplonline)2009.4.13<br/><br/>
曾经听说过也被人问过，就是没有试验过。那么今天来试一下。<br/><br/>
先做这样一个程序：<br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;windows.h&gt;<br/><br/>
using namespace std;<br/><br/>
DWORD WINAPI ThreadProc(<br/>
LPVOID lpParameter     // thread data<br/>
){<br/>
      Sleep(3000) ;<br/>
      *(int*)(lpParameter) = 1 ;<br/>
      return 0 ;<br/>
}<br/><br/>
void wait(int *p){<br/>
      while ( *p == 0 ) ;<br/>
}<br/><br/>
int main(){<br/>
      int n = 0 ;<br/>
      CreateThread(NULL , 0 , ThreadProc , &amp;n , NULL , NULL ) ;<br/>
      wait(&amp;n) ;<br/>
      cout&lt;&lt;"terminated normally"&lt;&lt;endl;<br/>
      return 0 ;<br/>
}<br/><br/>
wait函数就是一直读取变量n的状态，直到不为0就结束，然后输出<br/>
terminated normally<br/><br/>
在wait前，先把n设置为0，并且启动一个线程，把n的地址传给线程参数。<br/>
在该线程中，先等待3000毫秒，然后改变n的值为1。<br/><br/>
那么我们预计，这个程序三秒后将会出现<br/>
terminated normally<br/><br/>
现在使用最快速度优化编译。<br/><font color="#ff0000">VC6中直接build-&gt;set active configuration-&gt;release。</font><br/>
选择release方式编译，操作简单。<br/><br/>
可以看到程序一直不结束。（我只等了一会儿。。也许你可以等上若干年。。说不定就结束了。。-_-）<br/><br/>
这点与预期不同。<br/><br/>
于是看一下wait的汇编代码:<br/><br/>
00401090 mov       eax, dword ptr [esp+4]<br/>
00401094 cmp       dword ptr [eax], 0<br/>
00401097 jnz       short 0040109B<br/><font color="#ff0000">00401099 jmp       short 00401099</font><br/>
0040109B retn<br/><br/>
可见，该程序从变量p（[esp + 4])取出地址到eax，然后与0比较。<br/>
获得标志位Z的值。<br/>
然后判断，Z为0就一直死循环（00401099 jmp       short 00401099），不为0 就跳出。<br/><br/>
这个逻辑在单线程的时候确实是成立的。<br/>
所以编译器这样达到了最快速度优化。<br/>
可是在多线程的时候却有问题。因为我们的<font color="#ff0000">p<font color="#0000ff">所指向的内容</font>有可能在其他地方改变</font>。<br/><br/>
下面做一个修改。加上volatile关键字：即下面这行。<br/>
void wait(<font color="#ff0000">volatile </font>int *p){<br/><br/>
运行后，3秒延迟，然后程序正常结束。达到了我们的要求。<br/><br/>
再看一下wait的代码：<br/><br/>
00401090  mov       eax, dword ptr [esp+4]<br/><font color="#ff6600">00401094  cmp       dword ptr [eax], 0<br/>
00401097  jnz       short 0040109E</font><br/>
00401099  cmp       dword ptr [eax], 0<br/>
0040109C  je        short 00401099<br/>
0040109E  retn<br/><br/>
其中00401094 ，00401097 两句其实可以省去的。。<br/>
（看来编译器的行为确实很难理解...)<br/><br/>
现在代码就是先把，p的值放到eax里面。<br/>
然后不断对eax寻址得到的值与0比较。判断。<br/><br/>
那么这段代码存不存在<font color="#ff0000">隐患</font>呢？<br/><br/>
如果，我说如果，<font color="#ff0000">p<font color="#0000ff">的值</font>在运行过程中会改变，那么这段代码也有问题了</font>。<br/>
因为他先把p的值放入了eax中，如果这个时候，p的值变了。<br/>
即p指向了另一处内存，而此处内存完全可以是1。<br/>
但是我们用eax去寻址，导致一直读的是原来p指向的位置，他可能一直为0，导致无法退出。<br/><br/>
不过，<font color="#ff6600">这在正常编程时是不会出现的</font>。因为p所占据的是函数参数的空间。<br/>
一般，从C的层面上，我们没有办法去得到这个位置。（当然可以特殊构造）<br/>
所以在遇到这种多线程的时候，记得加一个volatile就OK了。<br/><br/>
那么，我上面既然说过特殊构造，我就来一段：<br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;windows.h&gt;<br/><br/>
using namespace std;<br/><br/>
DWORD v_esp ;<br/><br/>
int one = 1 ;<br/><br/>
DWORD WINAPI ThreadProc(<br/>
  LPVOID lpParameter    // thread data<br/>
  ){<br/>
     Sleep(3000) ;<br/>
     __asm{<br/>
          mov ebx , v_esp ;<br/>
          sub ebx , 4 ;<br/>
          mov eax , OFFSET one ;<br/>
          mov [ebx] , eax ;<br/>
     }<br/>
     return 0 ;<br/>
}<br/><br/>
void wait(<font color="#ff0000">volatile</font> int *p){<br/>
     while ( *p == 0 ) ;<br/>
}<br/><br/>
int main(){<br/>
     int n = 0 ;<br/>
     cout&lt;&lt;"begin"&lt;&lt;endl;<br/>
     CreateThread(NULL , 0 , ThreadProc , &amp;n , NULL , NULL ) ;<br/>
     cout&lt;&lt;"end"&lt;&lt;endl;<br/>
     __asm{<br/>
          mov v_esp , esp ;<br/>
     }<br/>
     wait(&amp;n) ;<br/>
     cout&lt;&lt;"terminated normally"&lt;&lt;endl;<br/>
     return 0 ;<br/>
}<br/><br/>
在VC6下测试，<font color="#ff6600">这个程序用release编译，就一直不结束。<br/>
用debug编译就会在3秒后正常结束。</font><br/>
（注意是写有volatile的）<br/><br/>
这就是我前面提过的，release下，虽然比较“<font color="#ff0000">老实"</font>了，他知道每次去取那一段内存。<br/>
但是还是<font color="#ff0000">“不够老实”</font>，我们看到了，编译器把p放在了eax里面。<br/><br/>
而<font color="#ff0000">debug下出来的东西就非常的“老实”</font>，我们看一下：<br/><br/>
004011F8  mov      eax, dword ptr [ebp+8]<br/>
004011FB  cmp      dword ptr [eax], 0<br/>
004011FE  jnz      short 00401202<br/>
00401200  jmp      short 004011F8<br/><br/>
每次都会从p处（参数所占空间）取得一个地址，然后再寻址。<br/>
这就对了哈，debug真是乖孩子。<br/><br/>
看来这是个危险的社会啊。。。<br/><br/>
不过像我最后给出的这种畸形的写法。。相信各位不会搞到自己的软里面。。<br/><br/>
所以说volatile足够了，该优化的时候还是放心让编译器去做。
