---
layout: post
title: "vista使用showwindow的一点问题"
date: 2010-02-18  14:58
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: 4868b8b77604b5ff30add1f8.html
_baiduhi_category: Vc
---

(hplonline)2010.2.18<br/><br/>
目的就是当某人打开某窗口的时候，<br/>
就把该窗口关掉，防止乱操作。<br/><br/>
代码如下：<br/><br/>
HWND hwnd = ::GetForegroundWindow() ;<br/>
const MAX_BUF = 100 ;<br/>
char buf[MAX_BUF] ;<br/>
::GetWindowText(hwnd , buf , MAX_BUF) ;<br/>
if ( strstr(buf , "CCProxy") ){<br/>
//MessageBox(buf) ;<br/>
::ShowWindow(hwnd , SW_HIDE) ;<br/>
//::CloseWindow(hwnd) ;<br/>
//::SendMessage(hwnd , WM_CLOSE , 0 , 0) ;<br/>
//::SendMessage(hwnd , WM_SHOWWINDOW , FALSE , SW_OTHERUNZOOM) ;<br/>
}<br/><br/>
把这段放到一个timer的处理函数中就可以反复地检测执行了。<br/><br/>
结果试了很久发现MessageBox都报出窗口名，<br/>
但CCProxy的窗口一直不被隐藏掉。<br/><br/>
最后发现的原因是之前CCProxy是用管理员打开的，<br/>
而这个隐藏程序是用普通权限执行的。<br/>
换成管理员后就有效果了。<br/><br/>
有几个函数有类似的现象，在if块的注释中。<br/><br/>
