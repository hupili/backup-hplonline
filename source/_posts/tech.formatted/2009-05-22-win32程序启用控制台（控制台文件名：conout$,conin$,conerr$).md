---
layout: post
title: "win32程序启用控制台（控制台文件名：conout$,conin$,conerr$)"
date: 2009-05-22  19:07
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: db6a6f389c0e592b96ddd8a8.html
_baiduhi_category: Vc
---

(hplonline)2009.5.22<br/><br/>
一个寻找很久，却得来全不费功夫的事情。<br/><br/>
做win32窗口程序的时候，有时还是希望在控制台下输入输出一些信息。<br/>
特别是VC的TRACE()宏虽然不错，但是输出在VC的debug窗口下。<br/>
里面有些杂乱的信息，看起来还是很不爽。<br/><br/><font color="#0000ff">1。最原始的分配控制台，获得句柄，再输出</font><br/><br/>
      AllocConsole() ;<br/>
      HANDLE hd = GetStdHandle(STD_OUTPUT_HANDLE) ;<br/>
      WriteConsole(hd , "hello hplonline" , sizeof("hello hplonline") , NULL , NULL );<br/>
      CloseHandle(hd) ;<br/><br/>
这个方法是我最早知道的，但毕竟不直观。<br/>
每次都要调用一个WriteConsole才搞定。<br/>
自己写个函数来包装他的话，虽然做新的项目可以。<br/>
但是想要利用一些以前已经做好的控制台下的东西就囧了。<br/>
如果有个方法能够让我们还是方便地使用printf这样的函数就完美了。<br/><br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/f114932552aec74435a80fca.jpg" small="0" class="blogimg"/></div>
<br/><br/><font color="#0000ff">2。对stdin,stdout,stderr重新打开</font><br/><br/>
      AllocConsole();<br/>
      freopen("conout$","w",stdout) ;<br/>
      printf("hello hplonline!-_-\n") ;<br/>
      std::cout&lt;&lt;"i'm cout"&lt;&lt;std::endl;<br/>
      freopen("conout$","w",stderr) ;<br/>
      std::cerr&lt;&lt;"i'm cerr"&lt;&lt;std::endl;<br/><br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/ccbe5c4e6ac74a2db2de05ca.jpg" small="0" class="blogimg"/></div>
<br/><br/>
这个用起来就很方便了，昨天在论坛上看到的。<br/>
另外就是三个特殊的文件名：<br/><font color="#ff0000">conout$,conin$,conerr$</font><br/>
我想他们的意思已经在他们的名字里的。结合上面的例子就很显然的。<br/><br/><font color="#0000ff">3。修改subsystem</font><br/><br/>
这个方法我就没试过了。<br/>
上学期做AISnake的时候就在想，选手调试起来很不方便。<br/>
但是不知道怎么把控制台搞出来，只有建议大家用文件输出。<br/><br/>
后来看到xsjs的改造版，问之，说直接改subsystem。<br/>
不过他改的那个版本在我这里也是没法输出东西，不知道怎么回事。<br/>
谁去试一下，记得来说说这方法哈，
