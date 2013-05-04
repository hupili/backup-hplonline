---
layout: post
title: "巩固一下ether_ip_tcp的格式"
date: 2009-11-25  19:40
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 6a639451076bc22e43a75ba8.html
_baiduhi_category: Network
---

<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman">(hplonline)2009.11.24</font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">由于手工填充</span><span><font face="Times New Roman">TCP</font></span><span style=" mso-ascii- mso-hansi-">的实验报告太繁琐了，所以尝试写了一个程序。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">数据是用</span><span><font face="Times New Roman">dinamips</font></span><span style=" mso-ascii- mso-hansi-">捕获的</span><span><font face="Times New Roman">.cap</font></span><span style=" mso-ascii- mso-hansi-">文件，用</span><span><font face="Times New Roman">wireshark</font></span><span style=" mso-ascii- mso-hansi-">打开，另存为</span><span><font face="Times New Roman">K12 TEXT FILE </font></span><span style=" mso-ascii- mso-hansi-">。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">其实</span><span><font face="Times New Roman">.cap</font></span><span style=" mso-ascii- mso-hansi-">也可以分析的，就是没时间去研究他的格式了。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">而导出的</span><span><font face="Times New Roman">txt</font></span><span style=" mso-ascii- mso-hansi-">文件，一看就明白文件结构是怎样的，</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">于是对着相关的几个课件试着弄了一下。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">之前看帧格式的时候，觉得也就那么回事，没多在意，</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">写了一下，发现还是有不少理解有出入的地方。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><font color="#0000ff"><span><font face="Times New Roman">ETHER</font></span><span style=" mso-ascii- mso-hansi-">帧：</span></font></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-"><span><img class="blogimg" border="0" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/1f1e11d5ca8583eb53da4b60.jpg"/><br/></span></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span/></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman">1.</font></span><span style=" mso-ascii- mso-hansi-">首先前面的</span><span><font face="Times New Roman">7BYTE</font></span><span style=" mso-ascii- mso-hansi-">的</span><span><font face="Times New Roman">preamble </font></span><span style=" mso-ascii- mso-hansi-">和</span><span><font face="Times New Roman">SFD</font></span><span style=" mso-ascii- mso-hansi-">在抓上来的包中是看不到的，他们是用来同步的交替</span><span><font face="Times New Roman">01</font></span><span style=" mso-ascii- mso-hansi-">序列和一个起始位。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman">2.</font></span><span style=" mso-ascii- mso-hansi-">我们平常说</span><span><font face="Times New Roman">MAC</font></span><span style=" mso-ascii- mso-hansi-">帧头长</span><span><font face="Times New Roman">18BYTE</font></span><span style=" mso-ascii- mso-hansi-">是包含了最后的</span><span><font face="Times New Roman">FCS</font></span><span style=" mso-ascii- mso-hansi-">的，不同于一般想到的“头”就一定是放在前面的部分。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman">3.DA</font></span><span style=" mso-ascii- mso-hansi-">放在</span><span><font face="Times New Roman">SA</font></span><span style=" mso-ascii- mso-hansi-">前面，应该是为了在链路层更高效的转发。这样收到</span><span><font face="Times New Roman">DA</font></span><span style=" mso-ascii- mso-hansi-">之后就可以将帧“直通”出去了。而</span><span><font face="Times New Roman">IP</font></span><span style=" mso-ascii- mso-hansi-">里面的顺序是先</span><span><font face="Times New Roman">SIP</font></span><span style=" mso-ascii- mso-hansi-">再</span><span><font face="Times New Roman">DIP</font></span><span style=" mso-ascii- mso-hansi-">，</span><span><font face="Times New Roman">TCP</font></span><span style=" mso-ascii- mso-hansi-">里面的顺序是</span><span><font face="Times New Roman">SPORT</font></span><span style=" mso-ascii- mso-hansi-">再</span><span><font face="Times New Roman">DPORT</font></span><span style=" mso-ascii- mso-hansi-">。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><font color="#0000ff"><span><font face="Times New Roman">IP</font></span><span style=" mso-ascii- mso-hansi-">分组：</span></font></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-"><span><img class="blogimg" border="0" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/4868b8b7d14f52db33add162.jpg"/><br/></span></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-">这里主要涉及的就是大小尾顺序的问题了。这些图都是从上到下，从左到右，地址值增加的。要在程序里面处理的时候，一般都是读成</span><span><font face="Times New Roman">BYTE,WORD,DWORD</font></span><span style=" mso-ascii- mso-hansi-">长度的变量，然后进行分析。当遇到不是</span><span><font face="Times New Roman">8bit</font></span><span style=" mso-ascii- mso-hansi-">整数倍的域时，理解就有问题了。比如我之前以为</span><span><font face="Times New Roman">VER</font></span><span style=" mso-ascii- mso-hansi-">既然放在</span><span><font face="Times New Roman">HLEN</font></span><span style=" mso-ascii- mso-hansi-">前面，那么我把</span><span><font face="Times New Roman">IP</font></span><span style=" mso-ascii- mso-hansi-">头读入一个字节，低位就是</span><span><font face="Times New Roman">VER</font></span><span style=" mso-ascii- mso-hansi-">，高位就是</span><span><font face="Times New Roman">HLEN</font></span><span style=" mso-ascii- mso-hansi-">，结果刚好是反着的。。后面用红框划了的</span><span><font face="Times New Roman">FLAGS</font></span><span style=" mso-ascii- mso-hansi-">和</span><span><font face="Times New Roman">Fragmentation offset</font></span><span style=" mso-ascii- mso-hansi-">也是这样的。</span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><font color="#0000ff"><span><font face="Times New Roman">TCP</font></span><span style=" mso-ascii- mso-hansi-">流：</span></font></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span style=" mso-ascii- mso-hansi-"><span><img class="blogimg" border="0" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/f437ed118b0028e9a5ef3f6c.jpg"/><br/></span></span></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"> </p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"><span style="mso-fareast-"><span style="mso-list: Ignore"><font face="Times New Roman">1.<span style="font: 7pt  Times New Roman ">        </span></font></span></span><span style=" mso-ascii- mso-hansi-">用红框划起来的一段和在上一节中说的问题一样。因为不是整字节，不方便直接处理，我是先按照</span><span><font face="Times New Roman">16bit</font></span><span style=" mso-ascii- mso-hansi-">读进来，然后高</span><span><font face="Times New Roman">4</font></span><span style=" mso-ascii- mso-hansi-">位</span><span><font face="Times New Roman">HLEN</font></span><span style=" mso-ascii- mso-hansi-">，中间</span><span><font face="Times New Roman">6</font></span><span style=" mso-ascii- mso-hansi-">位保留，其他的</span><span><font face="Times New Roman">FIN,SYN</font></span><span style=" mso-ascii- mso-hansi-">之类的标志放在最低位。一开始以为这些标志是放在该</span><span><font face="Times New Roman">16</font></span><span style=" mso-ascii- mso-hansi-">字节的最高位，导致结果不一致。</span></p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"><font face="Times New Roman"><span style="mso-fareast-"><span style="mso-list: Ignore">2.<span style="font: 7pt  Times New Roman ">        </span></span></span><span>TCP</span></font><span style=" mso-ascii- mso-hansi-">的数据长度没有直接写出来，用</span><span><font face="Times New Roman">IP</font></span><span style=" mso-ascii- mso-hansi-">的总长</span><span><font face="Times New Roman">-IP</font></span><span style=" mso-ascii- mso-hansi-">的头长</span><span><font face="Times New Roman">-TCP</font></span><span style=" mso-ascii- mso-hansi-">的头长即可。</span></p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"> </p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"> </p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"> </p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"><span style=" mso-ascii- mso-hansi-"><span><font face="Times New Roman">数据和程序文件：<a target="_blank" href="http://www.box.net/shared/b7focz9xdn">下载</a></font><font face="Times New Roman"> </font></span></span></p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"><span style=" mso-ascii- mso-hansi-">（不知道明年会不会有UESTC.NE的小朋友无意碰到这个东西。。）</span></p>
<p style="text-indent: -18pt; margin: 0cm 0cm 0pt 18pt; mso-list: l0 level1 lfo1; " class="MsoNormal"><span style=" mso-ascii- mso-hansi-"><span/></span> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span/> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span/></p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span/> </p>
<p style="margin: 0cm 0cm 0pt" class="MsoNormal"><span><font face="Times New Roman"> </font></span></p>
