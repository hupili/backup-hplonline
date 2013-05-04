---
layout: post
title: "简易字符串协议的C/S框架（SOCKET select）"
date: 2010-06-05  21:15
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: a23496824285c8b26d8119b0.html
_baiduhi_category: Network
---

(hplonline)2010.6.5<br/><br/><a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/181d9a52a8158f020df3e34a.html">上一篇</a>做了服务端引擎，这篇把客户端引擎也弄好了。<br/><br/>
下载地址：<br/><a target="_blank" href="http://www.box.net/shared/2gvt846unl">ThunderCS2010.6.5</a>。<br/>
SAMPLE中是一个交互式聊天的示例。<br/><br/>
运行效果：<br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/c022ad869226300266096e33.jpg"/></span><br/><br/><br/>
完成客户端编程框架。<br/>
由于引擎的主要难点在于底层的组装机制，<br/>
所以可以沿用服务器的代码。<br/>
而且客户端避免了管理多个套接字的麻烦，<br/>
从服务端代码简化即可得到。<br/><br/>
上层代码构建方式也类似服务端，<br/>
首先派生ThunderClient类，<br/>
然后对Process和Run进行定制。<br/><br/>
同样的，Process也会收到下层递交过来的完整PDU。<br/><br/>
客户端向服务端发送PDU使用函数：Request。<br/>
跟服务端的函数在名字上对偶：Request/Respond。<br/><br/>
服务端在编程的时候，一般不考虑退出的问题。<br/>
所以在最简框架中也没提供相关的机制。<br/>
如果检测到套接字失效，直接删除即可。<br/><br/>
客户端不同，根据用户的需要应该可以主动退出。<br/>
并且客户端检测到套接字失效的时候也需要有机制通知上层。<br/>
于是提供了两个额外的函数：<br/>
Exit()，先关闭套接字，然后转换为退出状态；<br/>
Exited()，可以检测当前是否为退出状态。<br/><br/>
于是客户端的循环框架可以变为：while ( !Exited() )<br/><br/>
服务器端一般只处理与网络有关事件，<br/>
故在大多数情况下，可以不重载Run函数。<br/><br/>
客户端除了处理网络事件外，<br/>
还需要处理用户的一些操作所产生的事件，<br/>
所以往往需要重载Run函数。<br/><br/><font color="#0000ff">》》样例代码：</font><br/><br/>
Proces函数直接显示收到的字符串。<br/><br/>
重载了Run函数。<br/>
使用kbhit来判断是否按键，然后进行处理。<br/>
这样不会因为等待SOCKET或者键盘事件而阻塞了。<br/><br/>
一般情况下，需要编写的仅为红色的部分。<br/><br/>
class MyClient : public ThunderClient{<br/>
public:<br/>
MyClient(std::string ipAddress , unsigned short uPort , int maxcheck)<br/>
:ThunderClient(ipAddress , uPort , maxcheck){} ;<br/><br/><font color="#ff0000">    int Process(std::string &amp;str){<br/>
printf("%s\n" , str.c_str()) ;<br/>
return 0 ;<br/>
}<br/><br/>
void Run(){<br/>
std::string str = "" ;<br/>
while ( !Exited() ){<br/>
MakeReadList() ;<br/>
MakeWriteList() ;<br/>
MakeExceptList() ;<br/>
Select(0 , 10000) ;<br/>
LaunchEvent() ;<br/>
if ( kbhit() ){<br/>
char ch = getch() ;<br/>
printf("%c" , ch) ;<br/>
if ( ch == '\n' || ch == '\r'){<br/>
printf("\n") ;<br/>
Request(str) ;<br/>
if ( str == "exit" ){<br/>
Exit() ;<br/>
}<br/>
fflush(stdin) ;<br/>
str = "" ;<br/>
} else {<br/>
str += ch ;<br/>
}<br/>
}<br/>
}<br/>
}</font><br/>
} ;<br/><br/><br/>
int main(){<br/><br/>
WORD wVersionRequested;<br/>
WSADATA wsaData;<br/>
int err;<br/><br/>
wVersionRequested = MAKEWORD( 1, 1 );<br/><br/>
err = WSAStartup( wVersionRequested, &amp;wsaData);<br/>
if (err!=0){<br/>
return err;<br/>
}<br/><br/>
if (LOBYTE ( wsaData.wVersion) != 1 ||<br/>
HIBYTE ( wsaData.wVersion) != 1){<br/>
WSACleanup();<br/>
return 0;<br/>
}<br/><br/><font color="#ff0000">    char buf[MaxBuf] ;<br/>
puts("input server's ip:") ;<br/>
gets(buf) ;<br/>
MyClient mc(buf , SERVER_PORT , 500) ;<br/>
mc.Connect() ;<br/>
mc.Run() ;</font><br/><br/><br/>
WSACleanup();<br/>
return 0 ;<br/>
}<br/><font color="#0000ff"><br/>
》》其他改进</font><br/><br/>
对服务端引擎也进行了一定改造。<br/>
提供FirstPeer()和NextPeer()组合函数，<br/>
用于对从套接字进行遍历。<br/><br/><font color="#ff0000">(2010.6.10)<br/><br/>
补充编写文档。</font><br/><br/>
含编写文档的ThunderCS2010.6.5<a href="http://www.box.net/shared/2oux4qshg5" target="_blank">：下载</a>。<br/>
