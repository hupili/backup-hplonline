---
layout: post
title: "关于CALL（绝对CALL？相对CALL？)"
date: 2009-02-13  14:06
comments: true
categories: tech
tags: ["Asm"]
_baiduhi_id: e6e99b8f9f88d7fd503d9232.html
_baiduhi_category: Asm
---

(hplonline)2009.2.13<br/><br/>
先是有同学讨论绝对的CALL<br/>
网上搜了下，啥都没搜到。<br/><br/>
有人说了用FF15。不过里面还有点小东西，后面跟的不是地址。<br/>
就把我论坛发言COPY下来了<br/><br/><font color="#0000ff">------------------第一份</font><br/><br/>
貌似FF15 后面跟的也不是绝对的地址，应该是一个DWORD的地址，<br/>
而这个地址正好存了你要CALL的地方<br/><br/>
.data<br/>
n DWORD m<br/>
.CODE<br/>
m proc<br/>
ret<br/>
m endp<br/>
START:<br/>
call DWORD PTR [n]<br/>
ret<br/>
end start<br/><br/>
然后就这长相，<br/><br/>
00401000  /$  C3            retn<br/>
00401001 &gt;|.  FF15 00304000 call    dword ptr [403000]               ;  CONSOLE.00401000<br/><br/><font color="#0000ff">----------------------第二份</font><br/><br/>
像下面这样，后面跟的就是过程地址，然后执行就挂掉<br/><br/>
.data<br/>
n DWORD m<br/>
.CODE<br/>
m proc<br/>
ret<br/>
m endp<br/>
START:<br/>
call DWORD PTR [m]<br/>
ret<br/>
----------------<br/>
00401000  /$  C3            retn<br/>
00401001 &gt;|.  FF15 00104000 call    dword ptr [401000]<br/><br/><font color="#0000ff">-------------------第三份</font><br/><br/>
然后给一组对比<br/>
.data<br/>
n DWORD m<br/>
.CODE<br/>
m proc<br/>
ret<br/>
m endp<br/>
START:<br/>
call DWORD PTR[n]<br/>
call NEAR PTR [n]<br/>
call DWORD PTR[m]<br/>
call NEAR PTR [m]<br/>
ret<br/>
----------------<br/>
00401001 &gt;|.  FF15 00304000 call    dword ptr [403000]               ;  CONSOLE.00401000<br/>
00401007  |?  E8 F41F0000   call    00403000<br/>
0040100C  |.  FF15 00104000 call    dword ptr [401000]               ; [getchar<br/>
00401012  /$  E8 E9FFFFFF   call    00401000<br/><br/>
其中第一个和第四个用法是可以的，中间两个用了程序要挂掉。<br/>
然后，默认的写法<br/>
call n == call DWORD PTR[n]<br/>
call m == call NEAR PTR [m]<br/><br/><font color="#0000ff">---------------------第四份</font><br/><h6 class="quote">Quote:</h6>
<blockquote>引用第24楼依然随意于2009-02-13 11:57发表的  :<br/><br/>
一个是相对偏移量，一个是绝对地址<br/>
call DWORD PTR[xxx]：其中的xxx处存放着要call的指令的地址<br/>
call NEAR       PTR [xxx]：最终要运行到的地址也是根据当前EIP和xxx联合计算出来的<br/><br/>
.......</blockquote><br/><br/>
不知道吧。呵呵，不过FF15那个可以变相实现还是可以。<br/><br/>
调用许多系统API的时候就是用的那个<br/><br/>
call DWORD PTR [thunk VA]<br/><br/>
thunk VA，是叫这个吧。。？<br/><br/>
------------------------------------<br/><br/>
想在网上搜一份详细的机器码表的，但是没有找到。。<br/><br/>
有人在他的BLOG上上传了一套，但是分了好几十个页面。。<br/><br/>
要弄下来太累了。。<br/><br/>
