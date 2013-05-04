---
layout: post
title: "VB用DDE读取EXCEL里面的数据"
date: 2009-05-08  15:51
comments: true
categories: tech
tags: ["Vb"]
_baiduhi_id: 691afd36ec1cdd390b55a9b6.html
_baiduhi_category: Vb
---

(hplonline)2009.5.8<br/><br/>
话说DDE也是N早前的事情了。<br/>
都很久没看人提起过。。。<br/>
Dynamic Data Exchange。<br/><br/>
不过M$的的一套东西相互间做点猫腻的事情很方便。<br/><br/>
就好比用VB读取EXCEL里面的数据一样。<br/><br/>
打开EXCEL，在SHEET1中随便写点东西。<br/>
（<font color="#ff0000">不要把EXCEL关了，DDE是用于运行着的进程交换数据的</font>）<br/><br/>
然后通过下面的代码在VB里面把单元格A1打印出来。<br/><br/>
Private Sub Command1_Click()<br/>
Dim s As String<br/>
Text1.LinkMode = 0<br/>
Text1.LinkTopic = "Excel|Sheet1"<br/>
Text1.LinkItem = "R1C1"<br/>
Text1.LinkMode = 1<br/>
s = Text1.Text<br/>
Print s<br/>
End Sub<br/><br/>
代码很容易类比。。相信不需要多余的解释。<br/><br/>
LinkTopic指定运行的进程名，管道符"|"后面是form名<br/>
LinkItem指定的是form上控件的名字。<br/>
这里是根据EXCEL的命名规则。R行C列。<br/>
LinkMode，1是自动连接，<br/>
还有几个连接方式，可以随便找个控件，在属性窗口那里下拉了看。<br/><br/>
============<br/>
突然看到论坛上有人问久违的VB。。冲动了一下。。<br/>
继续搜集数据+上课去。。
