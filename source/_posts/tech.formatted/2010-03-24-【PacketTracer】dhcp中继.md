---
layout: post
title: "【PacketTracer】dhcp中继"
date: 2010-03-24  20:50
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: e1f5302947f1fcf299250a9e.html
_baiduhi_category: Network
---

(hplonline)2010.3.24<br/><br/><a target="_blank" href="../../sys/search?type=1&amp;sort=1&amp;entry=1&amp;region=4&amp;hi=hplonline&amp;word=PacketTracer">系列链接</a><br/><br/>
dhcp中继适用的是dhcp服务器和客户机不在一个IP子网情况。<br/>
因为是在第三层做中继，所以是可以跨越多个IP子网的。<br/><br/>
在cisco路由上，进入接口模式，可以配置一个 ip help-address。<br/>
打问号后面也说明了，是 转发UDP广播报文的目的。<br/>
(DHCP的广播都是封在UDP里面的）<br/><br/><font color="#0000ff">练习点：</font><br/><br/>
dhcp<br/>
dhcp中继<br/>
子接口（见“单臂路由”）<br/><br/><font color="#0000ff">拓扑：</font><br/><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/0edae32452d488374d088d0a.jpg" small="0" class="blogimg"/></span><br/>
三层交换配置dhcp的地址池，<br/>
试验由路由和三层交换做dhcp中继。<br/><br/>
三层交换机的f0/2为三层口，<br/>
下接一个子网（.3)。<br/><br/>
路由下接两个vlan，分属两个子网。<br/><br/><font color="#0000ff">实验步骤：</font><br/><font color="#ff9900"><br/>
1.开启各接口，配置三层交换机和路由的IP。</font><br/><br/>
MS0:<br/>
f0/1:172.16.0.1/30<br/>
f0/2:172.16.0.5/30<br/><br/>
MS1:<br/>
f0/1:172.16.0.6/30<br/>
f0/2:172.16.3.1/24<br/><br/>
R0:<br/>
f0/0:172.16.0.2/30<br/>
f0/1.1:172.16.1.1/24 (vlan2)<br/>
f0/1.2:172.16.2.1/24 (vlan3)<br/><br/><font color="#ff9900">2.在MS0上配置dhcp地址池，</font><br/><br/>
与普通dhcp的配置一样。<br/><br/><font color="#ff9900">3.</font><br/><br/>
交换机S0上划分vlan，<br/>
应用到接口，并且设置到R0的trunk。<br/><br/><font color="#ff9900">4.添加各路由设备的路由。</font><br/><br/>
其中R0和MS1只需一条默认路由即可，<br/>
MS0可以手动添加三条路由。<br/><br/><font color="#ff9900">5.在R0上配置dhcp中继</font><br/><br/>
int f0/1.1 <br/>
ip helper-address 172.16.0.1<br/>
exit<br/><br/>
int f0/1.2<br/>
ip helper-address 172.16.0.1<br/>
exit<br/><br/><font color="#ff9900">6.在MS1上配置dhcp中继</font><br/><br/>
与路由类似<br/><font color="#ff9900"><br/>
7.检验<br/></font><br/>
各主机renew一下ip，相互ping下。<br/><br/>
------<br/><br/>
实际上MS1有更方便的解决方案，<br/>
就是把相关端口都用在2层。<br/>
MS0-MS1的链路设为一个trunk。<br/>
类似“<a href="http://hi.baidu.com/hplonline/blog/item/2410eccdc21d845d0eb345ee.html" target="_blank">三层交换dhcp</a>”。<br/><br/><a href="http://www.box.net/shared/ymry0ocx1h" target="_blank">pkt下载</a><br/><br/>
