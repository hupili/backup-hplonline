---
layout: post
title: "解决TCP的TIME-WAIT状态导致的端口占用（四种方法）"
date: 2010-04-06  15:18
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 314e4c23e25fd05e9922edfb.html
_baiduhi_category: Network
---

(hplonline)2010.4.6<br/><br/>
之前讨论了一下<a href="http://hi.baidu.com/hplonline/blog/item/1b3b68d911cf652010df9b77.html" target="_blank">TCP的TIME-WAIT状态</a>，<br/>
主要是分析了原理，给出了两种解决方案。<br/><br/>
后面又搜集到了另外两种方案，<br/>
这篇对四种方法仅做简要描述，给点自己的评价。<br/><br/><font color="#0000ff">1。隐式绑定</font><br/><br/><font color="#ff9900">》》方法</font><br/><br/>
客户机不调用bind，交给系统分配端口。<br/><br/><font color="#ff9900">》》好处</font><br/><br/>
这是通常的做法，并且还可以少写几行代码。<br/>
这样的出来的交互不仅从高层看来是完善的，<br/>
（<br/>
上一篇分析过，<br/>
认为去掉TIME-WAIT对高层的本次通信是完善的，<br/>
并且影响下次通信的概率非常小<br/>
）<br/>
在TCP层看起来也是完善的。<br/><br/><font color="#ff9900">》》不足</font><br/><br/>
这里提到的其实不是什么真正的缺陷，<br/>
仅仅是一个比较BT的需求：<br/>
比如我的服务器只对确定的客户进行交流，<br/>
于是我要求指定IP和PORT。<br/><br/>
既然是隐式绑定，端口就无法确定了。<br/><br/><font color="#0000ff">2。重置连接（RST）</font><br/><br/><font color="#ff9900">》》方法</font><br/><br/>
TCP实体可以在任何状态通过RST到达CLOSED状态。<br/>
所以，只要客户端发RST就行了，<br/>
这样自己就不会进入TIME-WAIT状态。<br/><br/>
当然，通过socket提供的接口直接设置RST很不方便。<br/>
（用RAW SOCKET应该可以搞）<br/>
所以可以不用closesocket而直接退出程序，<br/>
这样，系统自行回收资源并发RST给对方。<br/><br/><font color="#ff9900">》》好处</font><br/><br/>
很快。RST重置连接只需要一个报文，<br/>
没有四次握手的正常关闭那么麻烦。<br/><br/>
另外GFW和IE中，RST都有不错的应用。<br/><font color="#ff9900"><br/>
》》不足</font><br/><br/>
服务器需要一定的检查机制，<br/>
异常结束的客户机可能有些数据还没发完。<br/>
如果像我上篇的例程，<br/>
服务器可能只收到个“e”就被RST了，<br/>
于是会一直阻塞在等待用户输入的地方。<br/><br/>
不过对服务器进行编程的时候，<br/>
考虑各种异常状况本来就是份内的事情。<br/><br/>
不过用RST，对完美主义者始终不爽。<br/><br/><font color="#0000ff">3。被动关闭</font><br/><br/><font color="#ff9900">》》方法</font><br/><br/>
让服务器主动关闭。<br/><br/>
上篇是实验性的，只给了一个延迟的方案。<br/>
在实际的网络中，延迟多久又会成为一个问题。<br/><br/>
严格一点的流程应该是：<br/>
客户机检测exit，进入退出状态；<br/>
服务器收到exit，立即closesocket；<br/>
客户机在退出状态不断recv，<br/>
通过返回值判断是否已经收到对方的FIN；<br/>
客户机检测到FIN已收，则自己也closesocket。<br/><br/><font color="#ff9900">》》好处</font><br/><br/>
这样的动作，是符合雅致关闭的。<br/>
也成功解决了端口占用的问题。<br/>
同时，还能满足上面提到的比较BT的需求。<br/>
（<br/>
实际中应该很难遇到这样的需求，<br/>
即使要求对客户身份进行验证，<br/>
可以在高层再交互一些信息来做。<br/>
）<br/><br/><font color="#ff9900">》》不足</font><br/><br/>
应该说除了客户端多写点代码，<br/>
貌似没有什么坏处。<br/><br/><font color="#0000ff">4。LINGER选项</font><br/><br/><font color="#ff9900">》》方法</font><br/><br/>
LINGER linger ;<br/>
linger.l_linger = 5 ;<br/>
linger.l_onoff = TRUE ;<br/>
setsockopt(clientSock , SOL_SOCKET , SO_LINGER , (const char *)&amp;linger , sizeof(linger)) ;<br/><br/>
onoff为非0，表示开启逗留。<br/>
linger值为超时时间。<br/><br/><font color="#ff9900">》》好处</font><br/><br/>
可以抓包看下，设置了这个选项之后，<br/>
是服务器先发的FIN，然后客户机才跟进。<br/>
其效果和第3个方法实际上是一样的。<br/><br/>
好处在于把等待这个动作交给下层完成，<br/>
客户调用了closesocket之后可以立即干别的事情。<br/><br/><font color="#ff9900">》》不足</font><br/><br/>
linger.l_linger = 5 ;<br/>
如果手抖把这个成员设成了0，<br/>
那么可以抓包看下，客户会发RST。<br/>
也就是退化成了第2种方法了。<br/><br/><font color="#0000ff">5。设置端口复用</font><font color="#ff0000">（？？）</font><br/><br/><font color="#ff9900">》》方法</font><br/><br/>
BOOL opt = TRUE ;<br/>
int optlen = sizeof(opt) ;<br/>
setsockopt(s , SOL_SOCKET , SO_REUSEADDR , (char*)&amp;opt , optlen) ;<br/><br/><font color="#ff9900">》》讨论</font><br/><br/>
记录这点的原因主要是看到网上很多人都在说，<br/>
不过经过试验，没有解决TIME-WAIT的问题。<br/><br/>
上一篇中，讨论过<font color="#ff0000">为什么是connect失败而非bind</font>。<br/><br/>
当两个程序bind同一端口时，会失败，<br/>
通过SO_REUSEADDR选项可以使得两者都成功绑定，<br/>
所以给很多人留下个印象说REUSEADDR可以解决端口占用问题。<br/><br/>
而当某个端口位于TIME-WAIT状态时，<br/>
其bind一般都是会成功的，<br/>
问题在于connect的时候失败，<br/>
这应该不是REUSEADDR能够管得到的事情。<br/><br/>
（<br/><font color="#ff0000">如果有用这个方法成功的同学，<br/>
麻烦给下例程，我好跑来试验下。<br/>
我在VISTA和VM.XP下都不行。</font><br/>
）<br/><br/><a target="_blank" href="../../hplonline/blog/item/3f37a9ccc1a8261100e92839.html">关于转载（第三、四条）</a><br/><br/><br/>
