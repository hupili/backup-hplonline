---
layout: post
title: "Boson NetSim软件（附Stand Alone Lab笔记）"
date: 2009-08-13  19:26
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 8cfcf7fa610942d7b58f3128.html
_baiduhi_category: Network
---

(hplonline)2009.8.13<br/><br/><font color="#0000ff">Boson NetSim：</font><br/><br/>
相当好用的一个软件。<br/>
据说仿真从CCNA到CCNP的实验都足够了。<br/><br/><span><img class="blogimg" border="0" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/28eb2b3f38fe96c556e72360.jpg"/></span><br/><br/><br/>
软件带有图形界面的拓扑设计，比较方便。<br/>
仿真的时候，所有的运行过程都在这个软件内，<br/>
所以失真度还是比较大，<br/>
不过仿真二字的言下之意就是有失真。<br/><br/>
值得一提的是这个lab navigator，<br/>
按照难度分成了若干类。<br/><br/>
之前拿这个软件的时候，<br/>
同学给的包里顺带捎了一份国人做的入门教程。<br/>
拿到当天也就试了下，<br/>
不过除了照这一阵乱敲之外，<br/>
硬是没有懂起啥东西。<br/><br/>
而这个软件自带的lab view相当不错，<br/>
有不长不短的解释，<br/>
命令也很详细，不像国人的资料，<br/>
老是有很多缩写，<br/>
还得自己输进去来看全称。<br/><br/>
把里面的Stand Alone Labs做完，<br/>
就大致知道了交换机和路由的基本玩法，<br/>
然后可以适时进阶，或者找点更专业，<br/>
更逼真的仿真软件来玩玩。<br/>
或者这个时候，再看看一些市面流行的实验，<br/>
基本也能看懂。<br/><br/>
这几天把入门级的lab都做完了，<br/>
发现以前用的tp-link之类的路由器纯属家用型玩具。<br/>
cisco的货果然好玩，内容非常丰富。<br/>
要是有实物就更好玩了。<br/><br/><font color="#0000ff">Stand Alone Lab笔记：</font><br/><br/>
（仅仅是为了玩玩设备，并非为考试准备，<br/>
所以是在没有相关理论基础的情况下做的，<br/>
有的地方可能看起来很可笑<img src="http://img.baidu.com/hi/jx/j_0015.gif"/>）<br/><br/>
1.<br/>
配置好端口后，可以先ping一下自身该端口的地址，<br/>
确定该端口是否通畅。<br/>
或者show interfaces xxx yyy<br/><br/>
2.ppp+chap<br/><br/>
enable password<br/>
username ??? password ???<br/>
ppp authentication chap<br/>
encapsulation ppp<br/><br/>
当出现A端可以ping通自身，而B端连自身都无法ping通的时候。<br/>
在B端show int se0可以看到：<br/>
Serial0 is up, line protocol is down<br/>
表示se0已经被打开，但是没有得到对方的认证。<br/><br/>
这个时候试着在A端重设密码：<br/>
enable password ???<br/><br/>
或者在B端重设用户名+密码：<br/>
username xxx password yyy <br/><br/>
3.reload命令<br/>
感觉貌似有问题，<br/>
在配置过frame-relay的dlci之后，<br/>
reload并不清除。<br/>
而在之后的地方又没有找到删除该号的方法。<br/>
可能是仿真系统的问题。<br/><br/>
4.<br/>
show ip int e0<br/>
可以看到access-list有关的信息。<br/>
形如：<br/>
Outgoing access list is not set<br/>
Inbound  access list is not set<br/><br/>
show int e0<br/>
看不到<br/><br/>
5.<br/>
wildcar mask<br/>
通配符的掩码<br/>
为1的部分表示用来支持通配的位。<br/>
比如：<br/>
permit tcp 24.17.2.16 0.0.0.15 any eq telnet log<br/>
即是把24.17.2.16子网来的telnet包都放行。<br/>
这个通配符可以视作是子网掩码取反<br/>
如果通配符为0.0.0.0，即是要完全匹配地址，<br/>
他和host关键字是一个意思。<br/><br/>
6.访问控制表<br/>
在conf t状态下：<br/>
access-list创建的是无名字的表<br/>
ip access-list extended xxxxx创建的是有名字的表<br/><br/>
7.<br/>
access list 的最后有个隐含的阻止一切数据包的条目<br/><br/>
8.<br/>
switch 的 interfaces 命令后面，<br/>
可以跟vlan配置关于vlan的ip地址，<br/>
也可以跟range指定一个范围：<br/>
int range fa0/2-5<br/><br/>
但是这个模拟系统中？没有提示。<br/>
不知道是设备本身的问题，还是模拟系统的问题。<br/><br/>
9.<br/>
(switch)<br/>
在#提示下，可以vlan database进入vlan的配置。<br/>
在#(config)提示下，直接vlan也可以<br/><br/>
10.<br/>
貌似不同型号的交换机在端口配置的地方区别比较大。<br/>
高端型号有switchport项，里面可以配置若干内容。<br/><br/>
