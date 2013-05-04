---
layout: post
title: "【PacketTracer】IPsec实验，连接子网的VPN"
date: 2010-03-20  21:11
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 56fab3126100ccc2c2fd7896.html
_baiduhi_category: Network
---

(hplonline)2010.3.20<br/><br/><a href="http://hi.baidu.com/sys/search?type=1&amp;sort=1&amp;entry=1&amp;region=4&amp;hi=hplonline&amp;word=PacketTracer" target="_blank">系列链接</a><br/><br/>
读了锐捷的手册，<br/>
有些东西不一样，没试成功。<br/><br/>
在网上找了份100+页的英文文档，<br/>
讲得很详细，终于通了。<br/><br/>
折腾了半天的东西，整理一下，结果就只有几句话。<br/><br/>
PT在观察包的加封和解封方面是很方便的，<br/>
所以可以直接在Simulation模式下观察IPsec是否成功。<br/><br/>
我主要是为了寻求一种不依赖于模拟环境的测试方法，<br/>
由于不了解一些细节，折腾了半天，后面会详细分析。<br/><br/><font color="#0000ff">拓扑图：</font><br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/4d8a3ea8f1315084c9130c6a.jpg"/></span><br/>
子网1，子网2：需要用VPN连接的两个私有网<br/>
子网3，子网4：模拟的Internet<br/>
R0，R1：两个私有网的边界路由，需要进行IPsec配置<br/>
R2：Internet路由，使用ACL限制两个私有网地址的包通过<br/><br/><font color="#0000ff">实验步骤：</font><br/><br/>
1.<br/><br/>
配置设备地址，开启rip。<br/>
第x个子网的网段为：192.168.x.0。<br/><br/>
（属于基本配置，就不贴命令了）<br/><br/>
2.<br/><br/>
测试各设备连通性<br/><br/>
3.<br/><br/>
R2上配置ACL，将子网3,4模拟成Internet环境<br/><br/>
Router2(config)#acc 1 permit 192.168.3.0 0.0.0.255<br/>
Router2(config)#acc 1 deny any <br/>
Router2(config)#acc 2 permit 192.168.4.0 0.0.0.255<br/>
Router2(config)#acc 2 deny any <br/>
Router2(config)#int f0/0<br/>
Router2(config-if)#ip acc 1 in<br/>
Router2(config-if)#exit<br/>
Router2(config)#int f0/1<br/>
Router2(config-if)#ip acc 2 in<br/>
Router2(config-if)#exit<br/><br/>
4.<br/><br/>
测试PC0和PC1不可达性。<br/><br/>
但是子网3和4之间的各接口都可以相互ping通。<br/><br/>
5.<br/><br/>
认证策略，预共享的密钥：<br/><br/>
crypto isakmp policy 1<br/>
authentication pre-share<br/>
group 2<br/><br/>
配置密钥：<br/><br/>
crypto isakmp key mykey address 192.168.0.2<br/><br/>
&lt;mykey&gt;：密钥<br/>
&lt;192.168.0.2&gt;：对方实体地址<br/><br/>
访问控制列表：<br/><br/>
acc 101 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255<br/><br/>
变换集：<br/><br/>
crypto ipsec transform-set myset esp-3des esp-sha-hmac <br/><br/>
创建加密图：<br/><br/>
crypto map mymap 10 ipsec-isakmp <br/>
match address 101<br/>
set transform-set myset<br/>
set peer 192.168.0.2<br/><br/>
在接口上应用：<br/><br/>
int f0/1<br/>
crypto map mymap<br/><br/>
5.<br/><br/>
测试连通性。<br/>
PC0和PC1能相互ping通。<br/><br/><font color="#0000ff">失败拓扑：</font><br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/f437ed110c01abf3a5ef3f6a.jpg"/></span><br/>
最初希望使用子网0来模拟Internet，<br/>
具体方法为在R0和R1上用ACL来限制带私网地址的包通过。<br/><br/>
结果不论是在接口上做in还是out的控制，都有问题。<br/><br/><font color="#0000ff">在R0和R1的Internet端配置in的ACL的问题</font><br/><br/><font color="#ff9900">配置为：允许地址为子网0的包，并且禁掉其他的包。</font><br/><br/>
关于IPsec的解包，摘录PT自己Simulation给出的操作：<br/>
（对方路由正确加封并发包，己方收到加封包的响应）<br/><br/>
1. The receiving port has an inbound traffic access-list with an ID of 3. The router checks the packet against the access-list.<br/>
2. The packet matches the criteria of the following statement: permit 192.168.0.0 0.0.0.255. <font color="#ff0000">The packet is permitted.</font><br/>
3. The destination IP address matches the IP address of one of the interfaces. The router dispatches the packet to the <font color="#ff0000">upper layer.</font><br/>
4. ESP receives a ESP PDU which requires to be authenticated and <font color="#ff0000">decrypted.</font><br/>
5. ESP finds a matching SPI for the encrypted packet and decrypts it.<br/>
6. The receiving port has an inbound traffic access-list with an ID of 3. The router checks the packet against the access-list.<br/>
7. The packet matches the criteria of the following statement: deny any. The packet is <font color="#ff0000">denied and dropped.</font><br/><br/>
IPsec包的形式：<br/><font color="#ff0000">IP(1)|IPsec|IP(2)</font><br/><br/>
上面英文段所干的事情简述为：<br/>
先脱去IP(1)，查ACL，放行。<br/>
交ESP脱去IPsec的信息，<br/>
ESP将IP(2)从相同接口“<font color="#ff0000">再次交入”</font>，<br/>
查ACL，发现失败。<br/><br/>
关键就在于“再次交入”这个动作。<br/>
我最初的设想是，脱去IPsec的报头之后，直接查表转发。<br/><br/>
想了一下，觉得这个动作其实也有道理：<br/><br/>
1.简化程序设计，这样脱掉IPsec的普通IP包该怎么路由，和其他包一样<br/><br/>
2.这个“再次交入”的动作并不在物理上存在，只是内部的一些调用，<br/>
这样也不会将无保护的数据泄漏到外网上面。<br/><br/><font color="#0000ff">在R0和R1的Internet端配置out的ACL的问题</font><br/><br/><font color="#ff9900">配置为：不允许地址为私网的包出去，允许其他的</font><br/><br/>
路由的处理过程：<br/><br/>
1.入端口正确接收<br/>
2.查路由表<br/>
3.向出端口转发<br/>
4.发现ACL匹配deny项，失败<br/><font color="#ff0000"><br/>
可见IPsec过程是在决定向出端口转发后，<br/>
交给ESP模块加封的</font>。<br/><br/>
后来也想了一下，这个顺序是有道理的。。。<br/>
主要在于，先IPsec再由出端口ACL判断，减弱控制粒度。<br/><br/>
虽然在配置IPsec的过程中，需要设定一个ACL，<br/>
但这个ACL其实只有第一个命中的permit是有效的。<br/>
再进一步说，其实这个设计只是工程上的一个重用而已，<br/>
因为扩展的ACL可以指定源和目的地址。<br/>
如果是我来写这段程序，这个时候ACL已经在各设备上都有了，<br/>
那么有两种选择，在用户看起来可能是这样两类命令：<br/><br/>
a. <br/><br/>
......<br/>
source 192.168.1.0 255.255.255.0<br/>
destination 192.168.2.0 255.255.255.0<br/>
......<br/><br/>
b.<br/><br/>
access-list 101 ......<br/>
...<br/>
match address 101<br/><br/>
我会比较倾向于后面这样，用户可以复用关于ACL的知识。<br/><br/>
确定了IPsec配置过程中的ACL并非一个“控制”目的之后，<br/>
当然就需要有额外的东西来进行控制。<br/>
如果先IPsec加封，再ACL，则加封过后的包一定是符合出端口规则的。<br/>
（否则IPsec本身就无法正常工作。。已经没有配置的意义）<br/>
所以要先用ACL判断，准出了之后，再交由IPsec加封。<br/><br/><font color="#0000ff">收获：</font><br/><br/>
在失败拓扑上折腾，得知了一些设备上的细节问题。<br/><br/>
发现用PT来找问题确实很方便，他会列出路由处理的过程。<br/>
不过用设备自己的debug和抓包来分析还需要练习，<br/>
实际操作中，可不会有个东西这么详细还图形化地告诉你数据是怎样的。<br/><br/>
阅读了一份英文文档。<font color="#0000ff"><br/><br/></font>下一次做主机到网络的VPN。<font color="#0000ff"><br/><br/>
成品下载：</font><br/><br/><a target="_blank" href="http://www.box.net/shared/0npqs9lqds">这里</a>
