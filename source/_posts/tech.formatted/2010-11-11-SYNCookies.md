---
layout: post
title: "SYN Cookies"
date: 2010-11-11  23:57
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 6ed46d09962f3edf3ac76368.html
_baiduhi_category: Network
---

(hplonline)2010.11.11<br/><br/>
前天上课的时候听到了这个东西，还是有点意思。<br/><font color="#0000ff"><br/>
》》相关知识回顾</font><br/><br/>
SOCKET中有两个队列，<br/>
姑且一个叫syn队列，一个叫accept队列。<br/>
对于TCP来说，对方发起连接的时候，会建立一个SOCKET放到syn队列里面。<br/>
当连接建立好的时候，就从syn队列到accept队列。<br/>
当然，syn“队列”这个叫法不一定科学，<br/>
因为有网络延迟的差异，连接不总是先到的就先建立好。<br/>
当我们调用SOCKET的accept接口时，<br/>
实际上连接早已建立好，并且放在accept队列中了。<br/><br/>
这两个队列都有最大的长度。<br/>
在服务器调用listen的时候可以设定一个backlog值，<br/>
但该值具体对应的是哪个队列还需要再考察，和实现有关。<br/>
另外，除了backlog之外，系统本身也会加上限。<br/><br/><font color="#ff0000">(update,2010.11.15)<br/>
在linux下，accept队列的最大长度由/proc/sys/net/core/somaxconn指定。<br/>
listen参数的backlog对应的也是该队列，调用listen的时候系统会检查。<br/>
默认的accept队列最大长度是128，许多服务器需要修改增大。<br/>
syn队列的最大长度由/proc/sys/net/ipv4/tcp_max_syn_backlog指定。<br/>
没有用户接口去设定，其默认值是1024。</font><br/><br/>
既然是队列，那就有充满的那么一天。<br/>
这样新的连接无法进来，造成服务的拒绝。<br/><br/>
对于accept队列，一般有三种处理：<br/>
增大backlog，修改系统上限，提高accept的处理速度。<br/>
由于这个队列只依赖本地的处理，<br/>
我们可以尽量快地从系统接管其中的SOCKET资源，<br/>
这样，就可以最大可能地保证其非满。<br/><br/>
但syn队列会依赖网络对端，很容易被半开的连接充满。<br/>
特别是当syn flood发生的时候，服务器会维护一大堆没有用的连接信息。<br/>
正常的连接过来的时候，会由于syn队列满而无法建立。<br/>
此时，就算服务器还有很多闲散资源，也无法为客户提供服务。<br/>
SYN Cookies即可解决这种问题。<br/><br/><font color="#0000ff">》》SYN Cookies</font><br/><br/>
在我们设计程序的过程中，经常考虑的就是时间和空间的折衷。<br/>
syn队列本质消耗的是空间，而拒绝服务也是由于队列空间耗尽所致。<br/>
这样，可以想一种办法，把本来需要存储的信息进行“编码”，<br/>
交给客户端，下次返回的时候，花点时间“解码”即可。<br/>
这个思路很像服务器和浏览器之间交换的cookies。<br/><br/>
但最早的TCP协议并没有作出类似的规范，<br/>
所以我们无法在DATA域中放入这些信息，并让客户端乖乖传回。<br/>
好在TCP有规定一个SEQ值，初始的时候可以由服务器选定，<br/>
但客户在回送的时候，其ACK_client=SEQ_server+1。<br/>
服务器设计一种只有自己能读懂的SEQ值就行了。<br/><br/>
一般的实现会考虑这几个部分：<br/>
timestamp，用于判断连接是否超时。<br/>
sign = f(time, ip_src, port_src, ip_dst, port_dst)，用于签名防伪。<br/><br/>
f()的实现是服务器保密的，并且只要bit数足够，多个客户撞车的可能性也很小。<br/>
timestamp需要选取一个较大的粒度，以便能在32-bit的SEQ中的一部分中存下。<br/>
很不幸的是，为了保证签名的安全，留给timestamp的bit数量肯定很少。<br/>
一个可选的实现是：timestamp=(time()&gt;&gt;6)&amp;0x1f<br/>
这样，服务器对时间的分辨率可以达到64秒，数值循环周期大概半小时。<br/><br/>
到目前为止，一个SYN Cookies已经可用了，但还有个细节：<br/>
TCP有个MSS的选项，该选项只能在初始的数据包中设定。<br/>
如果客户发送了MSS，而我们不在syn队列中维护这个信息，就直接搞丢了。<br/>
所以还有个需求，就是把MSS也编码进SYN Cookies中。。。<br/>
真是艰苦卓绝，原先的timestamp和sign还得匀出点空间给MSS。<br/><br/>
由于MSS只能用少数几个bit表达，所以支持的种类是很少的。<br/>
好在目前基本是ethernet+ip一统天下，大部分的MSS都是经典的1460。<br/>
根据不同的环境，配置几种MSS也就够应付大部分需求了。<br/>
而一个正常的客户，应该不大可能手动设定一个非主流的MSS。<br/><br/>
除了MSS之外，TCP还有其他的选项，就姑且不考虑了，<br/>
毕竟这些选项在之后的交互中还可以再协商。<br/>
总得来说，回送的SEQ中有下面三个必要的部分：<br/>
timestamp,sign,MSS<br/>
可以自行设计分配他们的空间和签名的算法。<br/><br/>
参考资料：<a target="_blank" href="http://en.wikipedia.org/wiki/SYN_cookies">http://en.wikipedia.org/wiki/SYN_cookies</a>
