---
layout: post
title: "【PacketTracer】单臂路由"
date: 2010-03-24  11:40
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 377d53ee341e4ff7b3fb950d.html
_baiduhi_category: Network
---

(hplonline)2010.3.24<br/><br/><a href="http://hi.baidu.com/sys/search?type=1&amp;sort=1&amp;entry=1&amp;region=4&amp;hi=hplonline&amp;word=PacketTracer" target="_blank">系列链接</a><br/><br/>
去年夏天用<a href="http://hi.baidu.com/hplonline/blog/item/8cfcf7fa610942d7b58f3128.html" target="_blank">Boson把Stand Alone Lab敲完</a>了。<br/><br/>
听说了单臂路由这个名字，也在网上搜了些东西，结果就是没整出来。<br/><br/>
上学期上LAN/MAN，从把原理想清楚了，<br/>
感觉其实是个比较清晰的事情，<br/>
最近用PT模拟比较多，再试一下。<br/><br/><font color="#0000ff">拓扑：</font><br/><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/6d33871053912137203f2efc.jpg" small="0" class="blogimg"/></span><br/><br/><font color="#0000ff">配置过程：</font><br/><br/><br/><font color="#ff9900">1.模拟用户擅自修改的IP地址</font><br/><br/>
本来应该是255.255.255.128的掩码，<br/>
由于用户擅自修改IP地址，使得可以通信。<br/><br/>
pc0:<br/>
ipconfig 192.168.1.2 255.255.255.0 192.168.1.1<br/><br/>
pc1:<br/>
ipconfig 192.168.1.130 255.255.255.0 192.168.1.129<br/><br/><font color="#ff9900">2.配置VLAN，使用户隔离</font><br/><br/>
将PC0放到vlan2内<br/><br/>
vlan 2<br/>
int f1/0<br/>
sw acc vlan 2<br/><br/>
PC1放到vlan3内<br/><br/><font color="#ff9900">3.交换机端trunk链路</font><br/><br/>
链路模式<br/>
sw mode tr<br/>
允许中继的vlan<br/>
sw tr allowed vlan 2,3<br/><br/><font color="#ff9900">4.路由配置</font><br/><br/>
开启端口<br/>
int f0/0<br/>
no shut<br/>
ex<br/><br/>
子接口1：<br/>
int f0/0.1<br/>
enc dot 2<br/>
ip add 192.168.1.1 255.255.255.128<br/><br/>
子接口2：<br/>
int f0/0.2<br/>
enc dot 3<br/>
ip add 192.168.1.129 255.255.255.128<br/><br/><font color="#ff0000">给子接口配置IP地址前必须封装802.1Q或者ISL等加标协议。</font><br/>
分析一下，还是很容易理解。<br/>
所有的子接口在物理上都是同一个实体，<br/>
如果没有加标的话，该实体收到了帧，无法判断是给哪一个子接口。<br/><br/><font color="#ff9900">5.测试</font><br/><br/>
PC0可以ping通路由的两个子接口，<br/>
但是无法ping通PC1。<br/><br/>
原因是用户擅自修改了IP地址的掩码，<br/><font color="#ff0000">PC判断目的在同一子网内，<br/>
于是直接进行arp，</font>显然是无法得到回应的。<br/><br/><font color="#ff9900">6.用户更改回网管员分配的IP</font><br/><br/>
PC0:<br/>
ipconfig 192.168.1.2 255.255.255.128 192.168.1.1<br/><br/>
PC1:<br/>
ipconfig 192.168.1.130 255.255.255.128 192.168.1.129<br/><br/><font color="#ff9900">7.测试</font><br/><br/>
PC0和PC1可以ping通<br/><br/><br/>
====<br/><br/>
整个过程简单得让我都不知道以前是为啥没配通了。<br/><br/><font color="#ff0000">PS:在PT5.2中用三层交换机配子接口，提示不支持。</font><br/><br/>
不过用三层交换机实现的时候，似乎更简洁，<br/>
因为可以给vlan 2-1005配ip地址，已经不需要子接口这个东西了。<br/><br/><a target="_blank" href="http://www.box.net/shared/9yx617d6ip">pkt下载</a>
