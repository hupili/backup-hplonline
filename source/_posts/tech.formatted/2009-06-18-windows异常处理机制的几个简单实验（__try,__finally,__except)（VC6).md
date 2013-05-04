---
layout: post
title: "windows异常处理机制的几个简单实验（__try , __finally , __except)（VC6)"
date: 2009-06-18  11:57
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: 2bc327f599e6972cbd31096f.html
_baiduhi_category: Vc
---

(hplonline)2009.6.18<br/><br/>
C++有标准的try,catch,throw，还没来得及深入体会。<br/>
先试试M$的windows异常处理机制__try , __finally , __except。<br/><font color="#0000ff"><br/>
一。观察时序</font><br/><br/>
这个例子是从MSDN里面抄下来的，只改了一小点地方<br/><br/>
// Example of try-except and try-finally statements<br/>
#include "stdio.h"<br/>
#include &lt;windows.h&gt;<br/>
#include &lt;excpt.h&gt;<br/><br/>
void main()<br/>
{<br/>
    int* p = 0x00000000;    // pointer to NULL<br/>
    puts("hello");<br/>
    __try{<br/>
       puts("in try1");<br/>
       __try{<br/>
          puts("in try2");<br/>
          *p = 13;     // causes an access violation exception;<br/>
       }__finally{<br/>
          puts("in finally");<br/>
       }<br/>
    }__except(puts("in filter"), 1){<br/>
       puts("in except");<br/>
    }<br/>
    puts("world");<br/>
}<br/><br/><font color="#ff6600">输出：</font><br/><br/>
hello<br/>
in try1<br/>
in try2<br/>
in filter<br/>
in finally<br/>
in except<br/>
world<br/><br/><font color="#ff6600">结论：</font><br/><br/>
根据输出的字符串，各个语句块的执行顺序一目了然。<br/>
要注意的就是finally是在对应的try块执行完之后（不管是正常还是异常结束）。<br/><br/>
__except(XXX){<br/>
       YYY<br/>
    }<br/>
其中XX部分M$叫他filter，在捕获到异常的时候执行。<br/>
YYY部分叫except 。在异常位置对应的finally之后执行。<br/><br/>
设置finally这一机制的目的在于，异常处理完之后，还有机会去释放一些资源等等。<br/><br/><font color="#0000ff">二。异常处理相关的结构</font><br/><br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;EXCPT.H&gt;<br/>
#include &lt;windows.h&gt;<br/>
#include &lt;winnt.h&gt;<br/><br/>
int myhandler(int code , PEXCEPTION_POINTERS p){<br/>
     printf("error but corrected %x\n" , code) ;<br/>
     printf("%x,%x\n" , p-&gt;ContextRecord , p-&gt;ExceptionRecord) ;<br/>
     CONTEXT *c = p-&gt;ContextRecord  ;<br/>
     printf("%x,%x,%x,%x\n",c-&gt;Eax , c-&gt;Ebx , c-&gt;Ecx , c-&gt;Edx ) ;<br/>
     printf("%x\n",&amp;c);<br/>
     return 1;<br/>
}<br/><br/>
int main(){<br/>
     __try{<br/>
          __asm{<br/>
               mov eax , 1 ;<br/>
               mov ebx , 2 ;<br/>
               mov ecx , 3 ;<br/>
               mov edx , 4 ;<br/>
               mov [eax] , 1 ; cause exception <br/>
          }<br/>
     }__except(myhandler(_exception_code() , (PEXCEPTION_POINTERS)_exception_info())){} ;<br/>
     return 0 ;<br/>
}<br/><br/><font color="#ff6600">__except()</font><br/><br/>
其中如果要执行复杂的操作，可以封装一个函数完成。<br/>
这个函数应该返回如下值：<br/><strong>EXCEPTION_CONTINUE_EXECUTION (–1)</strong>  <br/>
表示异常已经消除，从异常地址处<font color="#ff0000">继续执行</font><br/><strong>EXCEPTION_CONTINUE_SEARCH (0)</strong> <br/>
表示无法处理这个异常，叫给后一级处理<br/><strong>EXCEPTION_EXECUTE_HANDLER (1)</strong> <br/>
表示异常数理完，<font color="#ff0000">结束程序</font><br/><br/>
在int myhandler(函数中，把 return 1;<br/>
改为 <font color="#ff0000">return -1</font>，可以看到不断打印出信息，<br/>
因为还没有消除这个异常，于是返回执行时马上又进入异常处理函数<br/>
改为 <font color="#ff0000">return 0</font>，可以看到windows的报错框，然后程序结束了。<br/>
因为表示没法处理这个异常，而之后我们又没有其他的处理函数了，<br/>
于是交给了系统，系统一般都是弹个出错框，然后结束程序。<br/><br/><font color="#ff6600">_exception_code()，_exception_info()</font><br/><br/>
前者返回错误代码，后者返回EXCEPTION_POINTERS结构的一个指针，<br/>
只能在<font color="#ff0000">filter</font>的位置使用这个函数。<br/>
定义如下：<br/>
typedef struct _EXCEPTION_POINTERS {<br/>
     PEXCEPTION_RECORD ExceptionRecord;<br/>
     PCONTEXT ContextRecord;<br/>
} EXCEPTION_POINTERS, *PEXCEPTION_POINTERS;<br/>
这个结构里面包含两个指针。<br/>
他们的定义都可以在 <font color="#ff0000">winnt.h</font>中看到，比较长，就不抄出来的了。<br/><br/>
通过ExceptionRecord可以取得比如异常地址，异常代码，之类的信息。<br/>
通过ContextRecord可以取得异常时的CPU现场。<br/>
（示例中打印出了几个寄存器的值供观察）<br/><font color="#ff6600"><br/>
ExceptionRecord，ContextRecord指向的地址</font><br/><br/>
他们都是放在栈区的，<br/>
根据打印出的地址和局部变量的地址比较可得，<br/>
printf("%x\n",&amp;c);<br/><br/><font color="#0000ff">三。修正现场继续执行</font><br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;EXCPT.H&gt;<br/>
#include &lt;windows.h&gt;<br/>
#include &lt;winnt.h&gt;<br/><br/>
int myerror(int code , PEXCEPTION_POINTERS p){<br/>
     printf("error but corrected %x\n" , code) ;<br/>
     CONTEXT *c = p-&gt;ContextRecord ;<br/>
     c-&gt;Ebx = 1 ;<br/>
     return -1;<br/>
}<br/><br/>
int main(){<br/>
     __try{<br/>
          __asm{<br/>
               mov ebx , 0 ;<br/>
               mov eax , 0 ;<br/>
               cdq ;<br/>
               div ebx ;<br/>
          }<br/>
     }__except(myerror(_exception_code() , (PEXCEPTION_POINTERS)_exception_info())){<br/>
     <br/>
     }<br/>
     return 0 ;<br/>
}<br/><br/>
这里制造了一个除0的异常。<br/>
在异常处理中，把EBX的值修改过后，返回-1，<br/>
告知继续执行，可以看到程序正常结束。<br/><br/>
如果把  c-&gt;Ebx = 1 ;注释掉，就像前面例子中一样，<br/>
异常不断地被触发，导致不停地打印信息。。<br/><br/><font color="#0000ff">其他:</font><br/><br/>
EXCPT.H这个头文件名让我觉得很梗塞。。。<br/>
这是哪门子的缩写啊。。。那个E很有必要省略吗。。<br/><br/>
windows异常处理机制的详细资料（看0day推荐的）：<br/><a href="http://www.microsoft.com/msj/0197/exception/exception.aspx" target="_blank"><font face="verdana, arial, helvetica" color="#000080" size="3">A Crash Course on the Depths of Win32™ Structured Exception Handling</font></a><br/><br/>
