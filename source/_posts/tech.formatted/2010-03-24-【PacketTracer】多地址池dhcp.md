---
layout: post
title: "【PacketTracer】多地址池dhcp"
date: 2010-03-24  11:45
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: c5c022341dec19375ab5f509.html
_baiduhi_category: Network
---

(hplonline)2010.3.24<br/><br/><a href="http://hi.baidu.com/sys/search?type=1&amp;sort=1&amp;entry=1&amp;region=4&amp;hi=hplonline&amp;word=PacketTracer" target="_blank">系列链接</a><br/><br/>
以前只试过单地址池，<br/>
不清楚多地址池会是什么状况。<br/><br/>
这个小测试也算是最近一个大工程的building block。<br/><br/><font color="#0000ff">拓扑：<br/></font><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/a8d2915013bacd54843524fc.jpg" small="0" class="blogimg"/></span><br/><br/><br/><font color="#0000ff">操作步骤：</font><br/><br/><font color="#ff9900">1.接口基本配置</font><br/><br/>
将PC0和PC1划分到VLAN2和VLAN3中。<br/><br/>
交换机f0/3开启对2和3的trunk。<br/><br/>
路由配置子接口，对vlan2和vlan3，<br/>
地址分别为192.168.1.1和192.168.2.1。<br/><br/>
类似配置单臂路由。<br/><br/><font color="#ff9900">2.配置dhcp</font><br/><br/>
ip dhcp pool pool1<br/>
network 192.168.1.0 255.255.255.0<br/>
default-router 192.168.1.1<br/><br/>
ip dhcp pool pool2<br/>
network 192.168.2.0 255.255.255.0<br/>
default-router 192.168.2.1<br/><br/><font color="#ff9900">3.PC上申请地址</font><br/><br/>
ipconfig /renew<br/><br/>
=====<br/><br/><font color="#ff0000">目的只是验证一个路由是如何处理多地址池的情况。</font><br/><br/>
结论是当某个接口（子接口）收到DHCP请求的时候，<br/>
查找有无和该接口在同一子网的pool，有就分配。<br/><br/><a href="http://www.box.net/shared/t135a3rh8f" target="_blank">pkt下载</a>
