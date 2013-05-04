---
layout: post
title: "【PacketTracer】三层交换dhcp，vtp"
date: 2010-03-24  12:34
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 2410eccdc21d845d0eb345ee.html
_baiduhi_category: Network
---

(hplonline)2010.3.24<br/><br/><a href="../../sys/search?type=1&amp;sort=1&amp;entry=1&amp;region=4&amp;hi=hplonline&amp;word=PacketTracer" target="_blank">系列链接</a><br/><br/>
vtp，vlan trunk protocol。<br/>
可以传递vlan编号和名字的信息，<br/>
感觉在实践上好像省不了多少操作。<br/><br/>
首先，开通vtp，需要各种配置。<br/>
然后，开通vtp之后，只能在各个交换机间统一vlan的编号和名字。<br/>
具体的哪些端口属于哪些vlan还是需要手动配置的。<br/><br/>
有人说，当vlan数量多的时候有用。<br/>
确实，当vlan有100个的时候，一条一条手敲vlan是个很痛苦的事。<br/>
不过要把各种端口一个个弄到100个vlan里面显然更痛苦，<br/>
相比之下，trunk这些vlan所减省的工作量并不多。<br/><br/>
况且，有时候，并不是每个交换机都下接有所有的vlan。<br/>
用vtp之后，会在全网进行统一，造成一些冗余。<br/><br/><font color="#0000ff">拓扑：</font><br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/1d3d9b23d5a5b972ac34defc.jpg"/></span><br/>
三层交换用于dhcp，和vtp的server。<br/>
交换机间用交叉线连接的为trunk链路，<br/>
可以传递vtp的信息和trunk各个vlan的信息。<br/>
三个二层交换机为vtp的client。<br/><br/><font color="#0000ff">基本设定：</font><br/><br/>
PC0:VLAN2,192.168.2.0/24<br/>
PC2:VLAN3,192.168.3.0/24<br/>
PC1:VLAN4,192.168.4.0/24<br/><br/><font color="#0000ff">实验步骤：</font><br/><br/><font color="#ff9900">1.vtp的设置</font><br/><br/>
三层交换机：<br/><br/>
vtp domain mydomain<br/>
vtp mode server<br/><br/>
其他二层交换机：<br/><br/>
vtp domain mydomain<br/>
vtp mode client<br/><br/>
把交换机间连接的线路设置成trunk模式。<br/><br/><font color="#ff9900">2.vlan的设置</font><br/><br/>
三层交换机上建立vlan2，vlan3，vlan4<br/><br/>
交换机间的trunk链路允许中继vlan2-4<br/><br/><font color="#ff9900">3.查看各路由器上的vlan，vtp的工作情况</font><br/><br/>
sh vlan <br/><br/>
sh vtp status<br/><br/><font color="#ff9900">4.将各access端口划到相应vlan</font><br/><br/>
vtp只是在网络内传播vlan数据库，<br/>
但相应的哪些端口属于哪个vlan是需要配置的。<br/><br/><font color="#ff9900">5.给三层交换机的各vlan配置地址。</font><br/><br/>
交换机的vlan1的地址为其管理地址。<br/><br/>
三层交换机其他vlan可以拥有IP地址，<br/>
地位相当于该vlan的网关。<br/><br/><font color="#ff9900">6.针对三个子网，开启三个dhcp地址池</font><br/><br/><font color="#ff9900">7.PC使用dhcp获得地址</font><br/><br/>
三个主机都得到了自己网段的ip地址。<br/><br/>
-------<br/><br/>
三层交换机处理多地址池与路由类似。<br/>
不同在于<font color="#ff0000">路由按照接口IP来区分该选用的pool</font>，<br/>
而<font color="#ff0000">三层交换机使用vlan的IP来区分该选用的pool</font>。<br/><br/>
另外，这篇兼耍一下vtp。<br/><br/><a href="http://www.box.net/shared/l67vjsfdl4" target="_blank">pkt下载</a>
