---
layout: post
title: "Boson NetSim仿真RIP的一段DEBUG分析"
date: 2010-04-06  18:32
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: a8eb4090453b3281a877a44b.html
_baiduhi_category: Network
---

(hplonline)2010.4.6<br/><br/>
在用Boson Netsim仿真配置rip的时候，遇到比较奇怪的现象。<br/>
命令就是按照他的<font color="#ff0000">sequential lab</font>敲的，但是到后面没有完全通。<br/><br/>
在各个设备上检查了一遍之后，发现其中一台的debug信息比较奇怪。<br/>
下面是截取的一次周期到时，s0和s1口收发的rip报文情况。<br/><br/><font color="#ff0000">从这段DEBUG信息，<br/>
应该可以在不知道具体拓扑的情况下推出不少东西。</font><br/><br/>
=========<br/>
RIP: received update from 175.10.1.1 on Serial0<br/>
160.10.1.0 in 1 hops<br/><br/>
RIP: received update from 180.10.1.2 on Serial1<br/><span style="color: rgb(0, 128, 0);">     195.10.1.0 in 1 hops</span><br/><br/>
RIP: sending update to 255.255.255.255 via Serial0 (175.10.1.2)<br/><span style="color: rgb(255, 0, 255);"> subnet 180.10.1.0, metric 1</span><br/><span style="color: rgb(255, 0, 0);"> subnet 197.10.1.0, metric 1</span><br/><span style="color: rgb(0, 128, 0);"> subnet 195.10.1.0, metric 2</span><br style="color: rgb(0, 128, 0);"/><br/>
RIP: sending update to 255.255.255.255 via Serial1 (180.10.1.1)<br/><span style="color: rgb(255, 0, 255);"> subnet 175.10.1.0, metric 1</span><br/><span style="color: rgb(255, 0, 0);"> subnet 197.10.1.0, metric 1</span><br/>
===========<br/><br/><font color="#0000ff">下面是分析：</font><br/><br/>
红色的是两个接口发出都有的报文，并且metric为1，可以判断是该路由直连的一个子网。<br/>
紫色分别是s1和s0接口所在的子网，也是直连。<br/>
绿色是从s1口收到的条目，可以看到更新路由表之后从s0发出去了。<br/>
剩下一个从s0收到的条目，并没有从s1发出去。<br/><br/>
show ip route可以看到160.10.1.0已经添加到路由表了。<br/>
rip的过滤表也没有设置。<br/><br/><font color="#0000ff">结论：</font><br/><br/>
根据以上现象，个人认为是该模拟软件的问题。<br/><br/>
mail了老师一下，也是这个意思。<br/><br/>
（<br/><font color="#ff0000">如果有同学知道出现这种现象可能的原因，<br/>
麻烦跟我说一下，好检查检查</font><br/>
）<br/><br/><font color="#0000ff">感受：</font><br/><br/>
其实在这些网络设备上，<br/>
debug可以看到很多信息的，<br/>
善于观察，可以黑箱出不少有价值的东西。<br/><br/><font color="#ff0000">并且debug不是在有bug的时候才用的，<br/>
恰恰是在一切都正常时候用。</font><br/><br/>
当一切正常的时候，常常瞟一下debug会是什么样，<br/>
那么当不正常的时候，才能很快反映过来是什么问题。<br/>
否则，当这正bug出现的时候，<br/>
面对刷版似的debug信息，直接就懵了。<br/><br/>
