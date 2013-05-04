---
layout: post
title: "TCP的TIME-WAIT状态"
date: 2010-04-01  13:19
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 1b3b68d911cf652010df9b77.html
_baiduhi_category: Network
---

(hplonline)2010.4.1<br/><br/>
以前也用过SOCKET编程，<br/>
不过拖拖控件，或者只用点简单的功能，<br/>
并没注意过这个状态的问题。<br/><br/>
前天水个课程实验，被一个现象囧了一下。<br/><br/><span style="color: rgb(255, 153, 0);">环境：VISTA+VC6+VM（XP SP2）</span><br/>
程序是在主机上编的，然后拖到虚拟机里面测试。<br/>
（因为在VISTA下面现象不一样）<br/>
虚拟机使用bridge模式联网，replicate选项勾上了的。<br/><br/><span style="color: rgb(0, 0, 255);">一。原任务</span><br/><br/>
做个C/S的一问一答式聊天，<br/>
客户输入“exit”的时候，退出。<br/><br/>
服务器的基本流程：<br/>
WSAStartup-&gt;socket-&gt;bind-&gt;listen-&gt;{accept-&gt;{recv-&gt;send}-&gt;close}-&gt;close-&gt;WSACleanup<br/><br/>
客户机的基本流程：<br/>
WSAStartup-&gt;socket-&gt;bind-&gt;connect-&gt;{send-&gt;recv}-&gt;close-&gt;WSACleanup<br/><br/>
{}表示循环动作。<br/><br/><span style="color: rgb(0, 0, 255);">二。现象</span><br/><br/>
要求的功能其实很简单就达到了，<br/>
而且客户输入“exit”从两边的回显信息来看，<br/>
都应该是正常结束了的。<br/><br/>
不过客户端再次连接服务器端的时候会出问题，<br/>
由connect函数返回失败信息。<br/><br/>
debug服务器，可以发现上一轮循环正常结束，<br/>
并且服务器已经阻塞在了新一轮的accept上面。<br/><br/>
然后过一定的时间（没有具体测，至少有好几十秒），<br/>
就又可以正常通信了。<br/><br/>
这个期间，服务器端程序并没有退出，一直在listen。<br/><br/>
（用vista无这现象，直接重连即可）<br/><br/><span style="color: rgb(0, 0, 255);">三。分析</span><br/><br/>
根据上面的现象，基本确定问题出在客户端。<br/><br/>
在客户端，netstat -a 查看连接，<br/>
可以看到相应的连接处于TIME-WAIT状态。<br/><br/>
在服务端，同样查看，<br/>
可以看到，相关的端口是在正常listen的。<br/><br/>
这个时候，还是把TCP的状态转移图翻出来<br/><br/><span><img src="http://hiphotos.baidu.com/hplonline/pic/item/d97fdb4396f7712572f05db8.jpg" small="0" class="blogimg" border="0"/></span><br/><br/>
可以看到，这是主动关闭连接方，回到CLOSE之前的最后一个状态。<br/>
同时，这个状态转移过去的唯一条件为time-out。<br/>
（<span style="color: rgb(255, 0, 0);">RST也可以，不过图上没有标出来；<br/>
RFC1337中详细分析了这个问题，<br/>
并建议在该状态下忽略RST，【Page 7】；<br/>
RFC1122也提到可以直接接收SYN建立新连接</span>）<br/><br/>
正因为这个time-out的存在，<br/>
所以会有一定的时间，无法使用这个端口重连。<br/><br/><span style="color: rgb(0, 0, 255);">四。解决方案（一）被动关闭</span><br/><br/>
从TCP状态转移图上已经看得很明显了，<br/>
主动关闭方才会存在等这个时间。<br/><br/>
于是改下程序：<br/>
服务器仍然在收到“exit”的时候立即closesocket，<br/>
客户机在用户输入“exit”的时候等上一点时间。<br/>
（在同一台机器上测试，毫秒级的时间就够了）<br/><br/>
这样测试一下，<br/>
客户exit之后，马上重连，正常。<br/><br/>
（<span style="color: rgb(255, 0, 0);">为什么服务器主动关闭，但重连的时候，还是可以？</span><br/><span style="color: rgb(255, 0, 0);">服务器主动的话，应该仍然有个TIME-WAIT状态啊</span>）<br/><br/><span style="color: rgb(255, 153, 0);">》》》rfc1122,Page88</span><br/><br/>
When a connection is closed actively, it MUST linger in<br/>
TIME-WAIT state for a time 2xMSL (Maximum Segment Lifetime).<br/>
However,<span style="color: rgb(255, 0, 0);">it MAY accept a new SYN</span> from the remote TCP to<br/>
reopen the connection directly from TIME-WAIT state, if it:<br/><br/>
(1) assigns its initial sequence number for the new<br/>
connection to be larger than the largest sequence<br/>
number it used on the previous connection incarnation,<br/>
and<br/>
(2) returns to TIME-WAIT state if the SYN turns out to be<br/>
an old duplicate.<br/><br/>
虽然服务器在TIME-WAIT状态，<br/>
他此时发起连接应该也会像客户那样失败，<br/>
但连接都是由客户发起的，<br/>
所以从现象上看，<br/><span style="color: rgb(255, 0, 0);">让服务器主动关闭连接，<br/>
可以解决客户端由于TIME-WAIT导致端口占用的问题。</span><br/><br/><span style="color: rgb(0, 0, 255);">五。解决方案（二）隐式绑定</span><br/><br/>
既然主动关闭方不得不等这个时间，<br/>
那么就是惹不起但躲得起的问题，<br/>
这个端口不能用，就换一个来用。<br/><br/>
再看一下之前的流程：<br/>
客户机的基本流程：<br/>
WSAStartup-&gt;socket-&gt;<span style="color: rgb(255, 0, 0);">bind</span>-&gt;connect-&gt;{send-&gt;recv}-&gt;close-&gt;WSACleanup<br/><br/>
问题就出在bind上，这里使用了显式绑定。<br/><br/>
把相关的语句注释掉，测试，正常。<br/><br/>
这时，由于没有指定端口 ，<br/>
那么每次系统随机给一个没有占用的端口，<br/>
当然，一切都正常了。<br/><br/><span style="color: rgb(0, 0, 255);">六。为什么客户机是connect出错而不是bind？</span><br/><br/>
当客户机处于TIME-WAIT状态的时候，<br/>
实际上，最明显的反映是用netstat -a 看到相应端口是这状态。<br/><br/>
既然该端口不可用，那么bind该端口的时候就应该出错吧。<br/>
但我们可以看到bind正常了，而connect出错了。<br/><br/><span style="color: rgb(255, 153, 0);">猜测如下：</span><br/><br/>
bind仅仅是给socket提供本地端口的一些信息，<br/>
并没有涉及到与TCP实体的交互。<br/>
（因为在SOCK_DGRAM的套接字上仍然可以bind，<br/>
而且几套收发函数都可以混合使用。）<br/>
所以bind仅仅是告诉socket，我准备用这个端口，<br/>
并不是告诉TCP实体，我准备用这个端口。<br/><br/>
而connect不一样，将产生三次握手的动作，<br/>
socket是个接口，只有交给TCP实体完成，<br/>
这个时候TCP实体发现该端口还在TIME_WAIT状态，不让使用。<br/><br/><span style="color: rgb(0, 0, 255);">七。为什么要有TIME-WAIT状态？</span><br/><br/>
从TCP的状态转移图可以看到，<br/><span style="color: rgb(255, 0, 0);">不管经过哪条途径到达TIME-WAIT状态，<br/>
都是己方已经发送FIN和ACK，<br/>
并且收到对方ACK和FIN的时候</span>。<br/><br/>
也就是说从自己这边看起来，<br/>
关闭连接的四次握手已经完成了。<br/>
那么为什么要等，就是个很困惑的问题。<br/><br/><span style="color: rgb(255, 153, 0);">UNIX.Network.Programming.Volume.1</span> 的<span style="color: rgb(255, 153, 0);">2.7节</span>有描述，<br/>
摘抄并翻译几句：<br/><br/><span style="color: rgb(255, 153, 0);">There are two reasons for the TIME_WAIT state:<br/><br/>
To implement TCP's full-duplex connection termination reliably<br/>
To allow old duplicate segments to expire in the network</span><br/><br/>
一个为了可靠地实现TCP的全双工连接终止，<br/>
二是使得旧的重复分组能够在网络中超时。<br/><br/><span style="color: rgb(255, 153, 0);">The first reason can be explained by looking at Figure 2.5 and assuming that the final ACK is lost. The server will resend its final FIN, so the client must maintain state information, allowing it to resend the final ACK. If it did not maintain this information, it would respond with an RST (a different type of TCP segment), which would be interpreted by the server as an error. If TCP is performing all the work necessary to terminate both directions of data flow cleanly for a connection (its full-duplex close), then it must correctly handle the loss of any of these four segments. This example also shows why the end that performs the active close is the end that remains in the TIME_WAIT state: because that end is the one that might have to retransmit the final ACK.</span><br/><br/>
简述：<br/><br/>
主动关闭方（称客户）的最后一个ACK可能丢失，<br/>
被动关闭方（称服务器）会尝试重发FIN。<br/>
如果这时客户位于CLOSED状态，<br/>
根据状态转移图，是不应该收到FIN的，<br/>
于是TCP实体判断异常发生，回一个RST。<br/>
本来连接已经正常结束，服务器收到RST会也认为连接异常。<br/><br/>
总得来说就是没有做到雅致关闭。<br/><br/>
讨论：<br/><br/>
我认为，这里所谓的异常，其实并不影响高层。<br/>
当客户到达TIME-WAIT的时候，<br/>
实际上双方的高层都已经确认了不再交互。<br/>
（两边的FIN都是在Close事件触发下的动作）<br/>
仅仅是TCP实体还有一些扫尾的工作没有完成。<br/>
即使TCP实体进行RST，这种异常也不会干扰到高层。<br/><br/>
就好比我最开始的例子，<br/>
如果我把服务器也改成收到“exit”立即退出。<br/>
那么将看到客户和服务器最后都退出了。<br/>
从应用的逻辑来看，整个交互已经正确完成了。<br/><br/>
不过下面这个情况倒是会影响到高层的。<br/>
（因为涉及到数据的混乱）<br/><br/><span style="color: rgb(255, 153, 0);">To understand the second reason for the TIME_WAIT state, assume we have a TCP connection between 12.106.32.254 port 1500 and 206.168.112.219 port 21. This connection is closed and then sometime later, we establish another connection between the same IP addresses and ports: 12.106.32.254 port 1500 and 206.168.112.219 port 21. This latter connection is called an incarnation of the previous connection since the IP addresses and ports are the same. TCP must prevent old duplicates from a connection from reappearing at some later time and being misinterpreted as belonging to a new incarnation of the same connection. To do this, TCP will not initiate a new incarnation of a connection that is currently in the TIME_WAIT state. Since the duration of the TIME_WAIT state is twice the MSL, this allows MSL seconds for a packet in one direction to be lost, and another MSL seconds for the reply to be lost. By enforcing this rule, we are guaranteed that when we successfully establish a TCP connection, all old duplicates from previous incarnations of the connection have expired in the network</span>.<br/><br/>
简述：<br/><br/>
就是说防止旧的重复分组被认为是新的分组中的数据。<br/><br/>
讨论：<br/><br/>
我觉得这种现象要发生，很依赖于人为制造。<br/>
首先TCP接收数据的时候是看窗口的，<br/>
由起点（SEQ）和长度（RECV.WND）决定。<br/>
旧有包要落在这个范围内才会被接收。<br/><br/>
同时，因为是网络中延迟的旧包，<br/>
对端肯定会发本次新连接应有的数据。<br/>
所以<span style="color: rgb(255, 0, 0);">取决于具体实现</span>时是丢弃老的还是丢弃新的，<br/>
当区间交叉时，使用何种聚合策略。<br/><br/>
然后，每次建立连接的时候SEQ都是重新随机的，<br/>
SEQ有4G的变动空间，而RECV.WND比起这个数字一般很小，<br/>
要想两次的窗口有重叠部分，应该是很困难的事。<br/>
（<span style="color: rgb(255, 0, 0);">在RFC1337,Page8,3.F3中提到了一个建议，<br/>
就是64-bit的SEQ值，这样的话，撞车就更难了</span>）<br/><br/>
======<br/><br/>
除了上面讨论的两点，在网上也看到了各种说法，<br/>
其实意思大同小异，也有部分说得很混乱的。<br/><br/>
我觉得这就是个在实际中虽然问题不大，<br/>
但从理论上分析，是存在的情况。<br/>
出于严谨的考虑，前人发明了TIME-WAIT。<br/>
这也算是设计协议有意思的地方吧，<br/>
越是基础，越是底层，则越要严谨。<br/><br/>
况且TCP出现的年代，硬件设施与现在完全无法相比。<br/>
那时经常性断线，丢包，延迟，乱序，等等。<br/>
而现在，用UDP都很可靠。。<br/><br/><span style="color: rgb(0, 0, 255);">八。扩展阅读</span><br/><br/>
shallway关于TCP连接关闭的两篇文章：<br/><span style="color: rgb(255, 0, 0);">（20110301,update，已内容死链，移除链接）</span><br/>
http://shallway.net/?p=157<br/>
http://shallway.net/?p=192<br/><br/><span style="color: rgb(255, 0, 0);">RFC793<br/>
RFC1122<br/>
RFC1337</span><br/><br/>
相关测试程序<a href="http://www.box.net/shared/o0bftubirn" target="_blank">下载</a><br/><br/><span style="color: rgb(255, 0, 0);">由于阅读量有限，没有充足时间做所有试验，<br/>
欢迎对文中YY的和理论分析的部分进行指正。</span><br/><br/><a href="http://hi.baidu.com/hplonline/blog/item/3f37a9ccc1a8261100e92839.html" target="_blank">关于转载（第三、四条）</a><br/><br/>
