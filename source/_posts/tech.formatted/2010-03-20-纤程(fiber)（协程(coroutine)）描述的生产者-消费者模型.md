---
layout: post
title: "纤程(fiber)（协程(coroutine)）描述的生产者-消费者模型"
date: 2010-03-20  11:48
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: 96ebab8b71e129739f2fb44a.html
_baiduhi_category: Vc
---

<p>(hplonline)2010.3.20<br/><br/>
貌似fiber出现也是很久以前的事情了，<br/>
看的书实在太少，没遇到哪里提一下，<br/>
最近听到了这个东西，试下。<br/><br/>
我觉得fiber这个名字很形象，<br/>
因为比它更重一点的解决方案是thread。<br/><br/>
VC6的头文件和库都没有带上，用VS2008实验的。<br/><br/><font color="#0000ff">语言描述的模型：</font><br/><br/>
1.生产者不断生产<br/>
2.消费者不断消费<br/>
3.仓库（队列）只有有限容量<br/>
4.仓库满了生产者必须停止生产<br/>
5.仓库空了消费者必须停止消费<br/>
6.生产者的原材料用完了整个过程也结束<br/><br/><font color="#0000ff">程序描述：</font><br/><br/><br/>
#include "stdafx.h"</p>
<p>#include &lt;windows.h&gt;<br/>
#include &lt;stdio.h&gt;</p>
<p>LPVOID fProducer , fConsumer , fMain;</p>
<p>int RawMaterial ;<br/>
int Queue ;<br/>
int MaxQueue ;</p>
<p>VOID CALLBACK FiberProc_Producer( PVOID lpParameter ){<br/>
     while ( RawMaterial &gt; 0 ){<br/>
         while ( Queue &lt; MaxQueue &amp;&amp; RawMaterial &gt; 0 ) {<br/>
             Queue ++ ;<br/>
             RawMaterial -- ;         <br/>
             puts("produce") ;<br/>
         }<br/>
         SwitchToFiber(fConsumer) ;<br/>
     }<br/>
     puts("raw material used up") ;<br/>
     SwitchToFiber(fMain) ;<br/>
}</p>
<p>VOID CALLBACK FiberProc_Consumer( PVOID lpParameter ){<br/>
     while (1){<br/>
         while ( Queue &gt; 0 ) {<br/>
             Queue -- ;<br/>
             puts("consume") ;<br/>
         }<br/>
         SwitchToFiber(fProducer) ;<br/>
     }<br/>
}</p>
<p><br/>
int _tmain(int argc, _TCHAR* argv[])<br/>
{<br/>
     Queue = 0 ;<br/>
     MaxQueue = 3 ;<br/>
     RawMaterial = 10 ;</p>
<p>     fProducer = CreateFiber(0 , FiberProc_Producer , NULL) ;<br/>
     fConsumer = CreateFiber(0 , FiberProc_Consumer , NULL) ;</p>
<p>     fMain = ConvertThreadToFiber(NULL) ;</p>
<p>     SwitchToFiber(fConsumer) ;<br/>
     <br/>
     puts("returned to main fiber") ;</p>
<p>     return 0;<br/>
}<br/><br/><font color="#0000ff">fiber的特点：</font><br/><br/>
1.fiber需要手动切换，而thread中不出现“切换”的动作<br/>
2.fiber不需要做“等待-加锁-释放”这样一套动作<br/>
3.各个fiber是串行的，无法利用多核的资源<br/><br/>
从程序输出也可以明显看到，<br/>
队列被消费者一次耗尽，<br/>
然后交给生产者一次填满，<br/>
如此来回，直到原材料耗尽。<br/>
如果是thread来描述这个问题，<br/>
可能生产两个，消耗一个，又生产一个，消耗两个。<br/><br/>
根据这些特点，<br/>
其实fiber并不是像thread那样用来改善性能的，<br/>
最大的作用应该是提供一种描述逻辑的方法。<br/><br/>
下次可以试下FSM。<br/>
把每个fiber和一个state对应，<br/>
接受输入（事件）之后，做相应的动作，<br/>
然后SwitchToFiber到下一个state。<br/><br/><font color="#0000ff">相关函数：</font><br/><br/>
ConvertThreadToFiber<br/>
CreateFiber<br/>
GetCurrentFiber<br/>
GetFiberData<br/>
SwitchToFiber</p>
