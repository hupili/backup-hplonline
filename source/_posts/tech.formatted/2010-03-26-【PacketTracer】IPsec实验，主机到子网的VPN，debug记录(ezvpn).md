---
layout: post
title: "【PacketTracer】IPsec实验，主机到子网的VPN，debug记录(ezvpn)"
date: 2010-03-26  12:23
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 438cda16a4448b14962b4332.html
_baiduhi_category: Network
---

(hplonline)2010.3.26<br/><br/><a href="../../sys/search?type=1&amp;sort=1&amp;entry=1&amp;region=4&amp;hi=hplonline&amp;word=PacketTracer" target="_blank">系列链接</a><br/><br/>
关于实验本身，HEXEC的<a href="http://www.chenhuan.net/pt-easyvpn-simulation.html" target="_blank">这篇文章</a>已经写得很清晰了。<br/><br/>
这周二中午，我也在网上碰到了有关EZVPN的资料，<br/>
不过敲了很久，可能是敲晕了，怎么都不通。<br/><br/>
前天看同学敲出来了，想必是能行的通的。<br/>
先照着敲了一遍，发现可以跑，<br/>
于是把之前的失败文件拿出来，一点点debug。<br/>
折腾了一天之后，发现连有哪些命令都差不多记住了。。。。<br/><br/><font color="#0000ff">一。大致过程</font><br/><br/>
配置aaa新模式，创建本地认证和授权的list。(aaa new, aaa authen, aaa autho)<br/><br/>
在本地添加若干账户（用户名和密码）。(user xxx pass xxx)<br/><br/>
配置本地地址池。(ip local pool)<br/><br/>
创建isakmp的组。<br/>
组中指明地址池，和组密码。<br/><font color="#ff9900">（还可以指定掩码，见诸网上的资料一般都没做这一步了）</font><br/><br/>
创建isakmp的策略。<br/>
指明hash算法，和认证方式(pre-share)。<br/><br/>
创建变换集，transform-set。<br/><br/>
创建动态加密图(dynamic-map)，<br/>
选择变换集，开启反向路由注入。<br/><br/>
创建静态加密图，<br/>
把前面aaa的认证和授权list配上去，<br/>
开启地址响应，<br/>
与动态加密图绑定。<br/><br/>
将静态图应用到出口接口上。<br/><br/><font color="#0000ff">二。配置完全正确不通</font><br/><br/>
据说是模拟ARP的问题，<br/>
就像平时ping的时候，<br/>
可能第一个不通，后面的就通了。<br/><br/>
可以先用PC ping 下网关，确保网络是通的。<br/>
如果配置都正确，应该就行了。<br/><br/><font color="#0000ff">三 。connect之后，PC会卡住，也不报告timeout。</font><br/><br/><font color="#ff0000">使用PT的Simulation模式，<br/>
每个包在端点的处理都会显示出来。</font><br/><br/>
直接查看最上层isakmp的信息如下：<br/><br/>
===<br/><br/>
1. Server received first aggressive mode message.<br/>
2. ISAKMP matching policy found.<br/>
3. Group and key match found on server.<br/>
1. Server sends second message of aggressive mode<br/><br/>
1. Client received second message of aggressive mode from server.<br/>
1. Client sends configuration request PDU.<br/><br/>
1. IKE PDU received. Client needs configuration information from server.<br/>
2. User authentication is required.<br/>
1. Server sends request for username and password.<br/><br/>
1. Client process receives username and password query by server.<br/>
1. Client process sends username and password response packet.<br/><br/>
1. Username and password packet received on server. Server requests authentication from AAA server<br/><br/>
1. Client receives configuration packet which has IP/Subnet for its Tunnel. It processes the packet.<br/><br/>
=====<br/><br/>
后检查为ip local pool 配置的问题，改正确就行了。<br/><br/>
可能isakmp的组中，指定了一个就不存在的地址池。<br/><br/>
PS一句，在PT里面想查看一下本地地址池，猜想的命令是：<br/><font color="#ff0000">show ip local pool </font><br/>
没有用起，跑<a href="https://supportforums.cisco.com" target="_blank">Cisco网站</a>上去问了下，<br/>
说<font color="#ff0000">实体机上是可以的，PT没有模拟完</font>。<br/><br/>
那边回答问题的速度还是比较快的，毕竟是面向全球的。<br/>
所以当你身边人打dota，睡午觉，睡晚觉的时候，<br/>
网上总有人是醒着的，而且老外用英语很流利。<br/><br/><font color="#0000ff">四。输入信息完全正确，点connect，立即显示disconnect。</font><br/><br/>
输入信息完全正确的意思是：<br/>
服务器地址错，会报timeout；<br/>
组名或组密码错，也会针对性地报；<br/>
用户名或密码错，也会针对性的报。<br/>
所以当这些都没报，表示这些信息应该是正确提供的。<br/><br/>
包跟踪过程：<br/><br/>
==========<br/><br/>
1. Server received first aggressive mode message.<br/>
2. ISAKMP matching policy found.<br/>
3. Group and key match found on server.<br/>
1. Server sends second message of aggressive mode<br/><br/>
1. Client received second message of aggressive mode from server.<br/>
1. Client sends configuration request PDU.<br/><br/>
1. IKE PDU received. Client needs configuration information from server.<br/>
2. User authentication is required.<br/>
1. Server sends request for username and password.<br/><br/>
1. Client process receives username and password query by server.<br/>
1. Client process sends username and password response packet.<br/><br/>
1. Username and password packet received on server. Server requests authentication from AAA server<br/><br/>
1. Client receives configuration packet which has IP/Subnet for its Tunnel. It processes the packet.<br/>
2. Client sets its Tunnel interface IP and Mask.<br/>
1. Client sends Acknowledgement to the server.<br/><br/>
1. Server received acknowledgement from the client.<br/><font color="#ff0000">2. Server is not configured to respond</font>. It drops the received PDU.<br/><br/>
1. Client VPN is disconnected.<br/><br/>
===<br/><br/>
倒数第二条已经说得很明确了，服务器不对地址进行响应。<br/>
相应的配置命令为：<br/><br/>
cry map <font color="#ff9900">&lt;mymap&gt;</font> isa client conf add res<br/><br/><font color="#0000ff">五。加密图名字空间的问题</font><br/><br/>
动态图和静态图是分开的，<br/>
所以当已经配置mymap为动态图的时候，<br/>
下面这些命令还是被全部接收了。<br/><br/>
crypto map mymap client authentication list eza<br/>
crypto map mymap isakmp authorization list ezo<br/>
crypto map mymap client configuration address respond<br/>
crypto map mymap 1 ipsec-isakmp dynamic mymap<br/><br/>
没有具体的负面影响，就是多了个图。<br/>
不过很可能由于手抖，用了之前配的动态图的名字，<br/>
于是后来加在端口上的静态图就缺少配置了。<br/><br/>
像第四点估计就是这样弄出来的连锁问题。。<br/><br/><font color="#0000ff">六。登陆的观察</font><br/><br/>
多台主机可以用同一个帐号登陆。<br/><br/>
连接成功之后，使用<br/>
sh cry map<br/>
可以看到若干<font color="#ff9900">peer=xxxx</font>的条目，xxxx为客户机的地址。<br/><br/><br/>
==================<br/><br/>
整个过程感觉对PT提供的包跟踪特性依赖比较大，<br/>
主要是debug开启isakmp和ipsec，会显示太多的信息。<br/>
在并不熟悉整个流程的情况下，找不到是哪里的问题。<br/><br/>
