---
layout: post
title: "简易字符串服务器框架（SOCKET select）"
date: 2010-06-03  21:25
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 181d9a52a8158f020df3e34a.html
_baiduhi_category: Network
---

(hplonline)2010.6.3<br/><br/><font color="#0000ff">》》需求</font><br/><br/>
做一套字符串的协议，为简化上层开发，先做一个服务器的框架。<br/><br/>
这里的字符串还是C风格的标准，使用'\0'结尾。<br/>
既然是基于字符串的协议，那么一个完整的字符串即可作为一个PDU。<br/>
一个完整PDU联合服务器记录的状态信息，应该是可以进行解释的。<br/><br/>
而SOCKET层的收发是不能保证一次性整字符串的传输 。<br/>
对于接收动作来说，可能对方的PDU被分片，<br/>
或者己方给recv函数的接受缓存过小 ，需多次接收。<br/>
对于发送动作来说，可能系统准备的缓冲区有限，<br/>
一个PDU还没有发完，send就会引发WSAEWOULDBLOCK错误，<br/>
这就要求在下一次继续发送。<br/><br/>
当我们在编写高层逻辑的时候，还得随时将这些装在脑子里，会比较累。<br/>
做的这个引擎和高层使用STL的string进行交互：<br/>
递交高层处理的是完整字符串，为一个独立的语义单元；<br/>
高层向引擎直接派发完整字符串，不会阻塞，由引擎负责发送。<br/><br/>
框架和样例：<a href="http://www.box.net/shared/0t2ibv9udj" target="_blank">下载地址</a><br/>
sample中的server使用该框架编写。<br/><br/><font color="#0000ff">》》使用方法</font><br/><br/>
1。包含头文件ThunderCS.h<br/><br/>
2。从类ThunderServer派生出MyServer<br/>
3。编写Process虚函数<br/>
4。如果有必要可以编写Run虚函数<br/><br/>
5。初始化环境（比如windows下的WSAStartup之类）<br/>
6。MyServer.Initialize()<br/>
7。Myserver.Run()<br/><br/><font color="#0000ff">》》Process编写方法</font><br/><br/>
int Process(std::string &amp;str , SOCKET sock)<br/>
从str可以得到一个完整的字符串，也就是PDU，可以进行解读并决定下一步操作。<br/>
sock是收到该字符串套接字，用于更复杂编写时关联状态信息。<br/><br/>
GetAddress()函数可以得到与套接字相关的地址<br/>
Respond()函数可以向客户发送字符串，非阻塞<br/>
RemovePeerSocket()函数用于结束对某套接字的服务<br/><br/><font color="#0000ff">》》样例代码</font><br/><br/>
需要手写的部分用红色标注。<br/>
详情见下载文件中的sample，有详细注释。<br/><br/>
class MyServer : public ThunderServer{<br/>
public:<br/>
MyServer(int BackLog , unsigned short ListeningPort)<br/>
: ThunderServer(BackLog , ListeningPort){}<br/>
int Process(std::string &amp;str , SOCKET sock){<br/><font color="#ff0000">        std::string ServerResponse = "" ;<br/>
ServerResponse = "I received your \"" + str + "\"" ;<br/>
Respond(ServerResponse , sock) ;<br/>
SOCKADDR_IN addr ;<br/>
addr = GetAddress(sock) ;<br/>
printf("(%s:%u):%s\n" , inet_ntoa(addr.sin_addr) , ntohs(addr.sin_port) , str.c_str()) ;<br/>
if ( str == "exit" ){<br/>
RemovePeerSocket(sock) ;<br/>
}</font><br/>
return 0 ;<br/>
}<br/>
} ;<br/><br/>
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
}<br/><font color="#ff0000"><br/>
MyServer ms(5 , SERVER_PORT) ;<br/>
ms.Initialize() ;<br/>
ms.Run() ;</font><br/><br/>
WSACleanup();<br/>
return 0 ;<br/>
}<br/><br/>
运行效果：<br/><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/ea07a164c9c462ccf63654d5.jpg" small="0" class="blogimg"/></span><br/><br/><br/><font color="#0000ff">》》设计大体思路</font><br/><br/>
使用select来做事件引擎。<br/><br/>
接收缓存：<br/>
std::map&lt;SOCKET , std::string&gt; mRecvBuf ;<br/>
使用map来关联和特定套接字相关的string。<br/>
在select触发的read事件中，向该string中拼接收到的内容。<br/>
如果发现已经收到一个完整的字符串（发现'\0'），<br/>
则递交Process处理。<br/><br/>
发送缓存：<br/>
std::map&lt;SOCKET , std::list&lt;std::string&gt; &gt; mSendBuf ;<br/>
上层调用Respond的时候，将PDU（即一字符串）插入到关联的list最后。<br/>
每一轮select会先将mSendBuf中，list不为空的套接字放发writefds里面。<br/>
一旦某套接字可以进行发送，则会触发write事件。<br/>
在write事件中，提取list中的第一条字符串。<br/>
尽力发送该字符串，如果发送完，则删除该字符串，<br/>
如果没有发送完，则将残余字符串放到list首部。<br/><br/><font color="#0000ff">》》下一步</font><br/><br/>
sample里的client写得很土，而且是非多路复用的，<br/>
client只能一收一发，而无法应对多次接收的情况。<br/><br/>
有时间也整个字符串客户机的框架。
