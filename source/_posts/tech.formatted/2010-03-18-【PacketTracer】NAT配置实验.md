---
layout: post
title: "【PacketTracer】NAT配置实验"
date: 2010-03-18  22:15
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 7333f8d35b261bd3a8ec9a64.html
_baiduhi_category: Network
---

(hplonline)2010.3.18<br/><br/>
用PT来配了下NAT。<br/>
关键的几个问题为：<br/><br/><font color="#0000ff">1.测试NAT起作用</font><br/><br/>
网络连好之后，选一台路由开放virtual terminal，<br/>
其他主机telnet进来，可以用show users查看用户地址。<br/><br/>
根据用户地址就知道是NAT之前还是之后的了。<br/><br/><font color="#0000ff">2.模拟Internet环境</font><br/><br/>
这里的模拟要达到的效果是，<br/>
路由器对“Internet”方向的端口可以正常收发包，<br/>
但带有路由器对“内网”方向地址的包无法通过。<br/><br/>
可以配置ACL来模拟。<br/><br/><font color="#0000ff">拓扑</font><br/><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/97f23c7a981df1d82f73b3ad.jpg" small="0" class="blogimg"/></span><br/>
子网0：功能性子网，放台服务器和开了VT的路由，PC是用来测试保证本地正常访问的。<br/>
子网1：假设的Internet环境<br/>
子网2：用来实验静态NAT的子网<br/>
子网3：用来实验动态NAT的子网<br/><font color="#0000ff"><br/>
实验配置过程</font><br/><br/><br/><font color="#ff9900">1.各设备连接好，按设计分配IP</font><br/><br/><font color="#ff9900">2.启动路由协议</font><br/><br/>
route rip<br/>
net xxxxx<br/>
net xxxxx<br/><br/><font color="#ff9900">3.测试连通</font><br/><br/>
各设备之间都能ping通。<br/>
由于PT模拟的问题，<br/>
一般每截链路的第一个包会失败。<br/><br/><font color="#ff9900">4.配置R0的virtual terminal</font><br/><br/>
line vty 0 15<br/>
password 123<br/>
login<br/><br/><font color="#ff9900">5.测试vt的正常</font><br/><br/>
各设备<br/>
telnet 192.168.0.4 <br/><br/>
R0<br/>
show users<br/>
可以看到登陆的用户地址。<br/><br/><font color="#ff9900">6.用ACL来把子网1模拟成internet环境</font><br/><br/>
R1：<br/>
access-list 1 permit 192.168.1.0 0.0.0.255 <br/>
access-list 1 deny any<br/><br/>
int f0/1<br/>
ip acc 1 in<br/><br/>
只允许来自子网1的IP包通过。<br/><br/><font color="#ff9900">7.从子网2和子网3的主机测试连通性。</font><br/><br/>
对于子网0不可达<br/><font color="#ff9900"><br/>
8.静态NAT配置</font><br/><br/>
配置映射表<br/>
ip nat inside source static 192.168.2.2 192.168.1.102<br/><br/>
配置内外接口<br/>
int f0/0<br/>
ip nat out<br/>
exit<br/>
int f1/0<br/>
ip nat in <br/>
exit<br/><br/><font color="#ff9900">9.测试静态NAT</font><br/><br/>
PC1能够连上R0，<br/>
在R0上show users可以看到<br/>
192.168.1.102连接<br/>
（地址已被转换）<br/><font color="#ff9900"><br/>
10.动态NAT配置（multi-to-1 NAT)</font><br/><br/>
access-list 1 permit 192.168.3.0 0.0.0.255 <br/>
ip nat inside source list 1 interface fastEthernet 0/0 overload<br/><br/>
int f0/0<br/>
ip nat out<br/>
exit<br/>
int f1/0<br/>
ip nat in<br/>
exit<br/><br/><font color="#ff9900">11.动态NAT测试</font><br/><br/>
用PC2和PC3同时连R0，成功。<br/><br/>
从R0上show users，可以看到两个192.168.1.3（R3地址）<br/><br/><font color="#0000ff">成品下载：</font><br/><br/><a href="http://www.box.net/shared/8eseq8rrej" target="_blank">这里</a>
