---
layout: post
title: "使用MATLAB Engine实现与C混合编程"
date: 2009-11-15  11:33
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: 2b6de350ab3576561138c270.html
_baiduhi_category: Vc
---

<p>(hplonline)2009.11.10</p>
<p><font color="#0000ff">》》目的：</font></p>
<p>1.实现快速结果验证<br/>
2.方便的矩阵运算<br/>
3.方便的绘图模块</p>
<p><font color="#0000ff">》》环境：</font></p>
<p>VISTA+MATLAB2009a+VC6.0</p>
<p><font color="#0000ff">》》资料：</font></p>
<p>以安装路径“E:\Program Files\MATLAB\R2009a\”为例</p>
<p>MATLAB外部支持文件夹：<br/>
E:\Program Files\MATLAB\R2009a\extern<br/>
matlab自带的c例程：<br/>
E:\Program Files\MATLAB\R2009a\extern\examples\eng_mat</p>
<p>engine.h的位置：<br/>
E:\Program Files\MATLAB\R2009a\extern\include</p>
<p>各种lib的位置：<br/>
E:\Program Files\MATLAB\R2009a\extern\lib\win32\microsoft</p>
<p>在matlab帮助中输入“C language”即可找到有关MATLAB Engine的一个页面。<br/>
从这个页面开始，学习各种关键词，<br/>
就能够找到一切你需要的资料。</p>
<p>使用MATLAB Engine一般用两套函数就可以了。<br/><font color="#ff0000">1.engXXXX，关于Engine本身的操作，包括打开/关闭，设置/取得变量，执行语句等等。<br/>
2.mxXXXX，关于数据类型mxArray的操作，与MATLAB交互的左右类型全部为mxArray。</font></p>
<p><font color="#0000ff">》》一个搭建实例</font></p>
<p>先在VC6的tools-&gt;options-&gt;directories里添加相关目录</p>
<p><font color="#ff0000">include files:<br/>
E:\Program Files\MATLAB\R2009a\extern\include</font></p>
<p><font color="#ff0000">library files:<br/>
E:\Program Files\MATLAB\R2009a\extern\lib\win32\microsoft</font></p>
<p>做好这些后，如果我们环境一样，<br/>
下面的代码应该能够编通并且正常执行，<br/>
其中包含了常用的一些函数，<br/>
一般来说使用Engine的时候也就用这些了。</p>
<p>#include &lt;stdlib.h&gt;<br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;string.h&gt;</p>
<p>#include "engine.h"<br/>
#include "matrix.h"</p>
<p>#pragma comment(lib,"libeng.lib") <br/>
#pragma comment(lib,"libmx.lib")</p>
<p>int main()<br/>
{<br/>
     Engine *ep;<br/>
     int i , j ;</p>
<p>     //show how to open MATLAB engine<br/>
     //for remote ones:<br/>
     //engOpen( ADDRESS OF REMOTE SYSTEM ) ;</p>
<p>     if (!(ep = engOpen("\0"))){<br/>
         fprintf(stderr, "\nCan't start MATLAB engine\n");<br/>
         return EXIT_FAILURE;<br/>
     }</p>
<p>     //show how to create matrix<br/>
     mxArray *Y = mxCreateDoubleMatrix(1 , 3 , mxREAL) ;<br/>
     <br/>
     //show how to put data in matrix<br/>
     double tmp[3] = {1.0 , 2.0 , 3.0} ;<br/>
     memcpy(mxGetPr(Y) , tmp , sizeof(tmp)) ;</p>
<p>     //show how to put variables in the Engine<br/>
     engPutVariable(ep , "Y" , Y) ;</p>
<p>     //show how to execute commands in MATLAB<br/>
     engEvalString(ep, "X = ones(5,1) * Y");<br/>
     <br/>
     //show how to get variables from the Engine<br/>
     mxArray *X = engGetVariable(ep , "X") ;<br/>
     <br/>
     //show how to manipulate dimensions<br/>
     int dims[10] ;<br/>
     int ndims ;<br/>
     ndims = mxGetNumberOfDimensions(X) ;<br/>
     printf("total number of dimensions is %d\n" , ndims) ;<br/>
     memcpy(dims , mxGetDimensions(X) , ndims * sizeof(int)) ;<br/>
     for ( i = 0 ; i &lt; ndims ; i ++ ){<br/>
         printf("dimension %d : %d\n" , i , dims[i]) ;<br/>
     }<br/>
     printf("\n") ;</p>
<p>     //show how the data is stored in the memory<br/>
     double *p = (double*)mxGetData(X) ;     <br/>
     for ( i = 0 ; i &lt; dims[0] ; i ++ ){<br/>
         for ( j = 0 ; j &lt; dims[1] ; j ++ ){<br/>
             printf("%8.2f" , p[j * dims[0] + i]) ;<br/>
         }<br/>
         printf("\n") ;<br/>
     }</p>
<p>     //---important, to release resources<br/>
     mxDestroyArray(X) ;<br/>
     mxDestroyArray(Y) ;</p>
<p>     //show how to hide and unhide MATLAB command window<br/>
     printf("type RETURN to hide the MATLAB command window...\n") ;<br/>
     getchar() ;<br/>
     engSetVisible(ep , false) ;<br/>
     printf("type RETURN to unhide the MATLAB command window...\n") ;<br/>
     getchar() ;<br/>
     engSetVisible(ep , true) ;</p>
<p>     printf("type RETURN to END this program...\n") ;<br/>
     getchar() ;     <br/>
     //remembering to close it is important .<br/>
     //but if you are debugging your programs , <br/>
     //annotate the following line will save you a lot of time ,<br/>
     //for you needn't to restart the Engine .<br/>
     engClose(ep) ;<br/>
     <br/>
     //when your work is accomplished , type "exit" in MATLAB command window</p>
<p>     return EXIT_SUCCESS;<br/>
}</p>
<p> </p>
<p><br/><font color="#0000ff">》》某些问题</font></p>
<p>如果出现这个：</p>
<p>engdemo.obj : error LNK2001: unresolved external symbol _engClose<br/>
engdemo.obj : error LNK2001: unresolved external symbol _engSetVisible<br/>
engdemo.obj : error LNK2001: unresolved external symbol _mxDestroyArray<br/>
engdemo.obj : error LNK2001: unresolved external symbol _mxGetData<br/>
engdemo.obj : error LNK2001: unresolved external symbol _mxGetDimensions_730<br/>
engdemo.obj : error LNK2001: unresolved external symbol _mxGetNumberOfDimensions_730<br/>
engdemo.obj : error LNK2001: unresolved external symbol _engGetVariable<br/>
engdemo.obj : error LNK2001: unresolved external symbol _engEvalString<br/>
engdemo.obj : error LNK2001: unresolved external symbol _engPutVariable<br/>
engdemo.obj : error LNK2001: unresolved external symbol _mxGetPr<br/>
engdemo.obj : error LNK2001: unresolved external symbol _mxCreateDoubleMatrix_730<br/>
engdemo.obj : error LNK2001: unresolved external symbol _engOpen</p>
<p>其实就是lib没有添加好。</p>
<p>在代码中写上：<br/>
#pragma comment(lib,"libeng.lib") <br/>
#pragma comment(lib,"libmx.lib")<br/>
就可以了。</p>
<p>或者可以在工程的连接设置里面添加这两个库。<br/>
不过我倾向于前者，这样在发布源码的同时，<br/>
就尽最大可能地保证能够编译，<br/>
而不用其他人学习的时候再去设置。</p>
<p>当然，由于#pragma是由编译器自己决定的，<br/>
所以代码的可移植性存在一些问题。</p>
<p>如果还是报上面的错误，估计是没有将lib的路径添加对。<br/>
具体参考上面的那个实例，然后注意把路径换成自己机器上的。</p>
<p><font color="#0000ff">》》小结</font></p>
<p>前几天围观了一个人用MATCOM混编，<br/>
发现确实很混。。。<br/>
比如调用rand的时候，直接就被MATLAB的rand给覆盖了。<br/>
因为他的头文件里面有类似<br/>
#define rand randM ?????<br/>
这样的东西，<br/>
于是在编译器接到代码之前，该代码已经被预处理替换了。<br/>
这样根本不会出现函数重复的编译或者连接错误。<br/>
这在某种意义上带来了一些隐患，影响调试。<br/>
（当时帮他看了半天才反映过来。。。）</p>
<p>使用MATLAB Engine的话，双方代码的隔离性很好。<br/>
由于使用字符串进行代码交互，开发效率可能会低一点。<br/>
另外在数据交互上比较麻烦一点，需要mxXXX系列的函数。<br/>
（<br/>
用MATCOM的时候甚至可以直接写出<br/>
mVar = CVar ;<br/>
这样的赋值。。。<br/>
由已经实现好的强大的类库来完成底层的转换。<br/>
）</p>
