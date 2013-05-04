---
layout: post
title: "LCD_AMPIRE12864的简单使用（PROTEUS）"
date: 2009-03-13  20:10
comments: true
categories: tech
tags: ["Scm"]
_baiduhi_id: 4d8a3ea83232adb9ca130cbb.html
_baiduhi_category: Scm
---

(hplonline)2009.3.13<br/><br/><font color="#0000ff">一。原因</font><br/><br/>
练习LCD，选的是PROTEUS里面的AMPIRE12864。<br/>
并没有实现什么复杂的功能，因为我只想<font color="#ff0000">给出几个常用接口</font>而已。<br/><font color="#ff0000">一旦知道了怎样在屏幕的指定位置画上一个点，<br/>
那么在屏幕上画任何的图形都只是简单的算法而已。</font><br/>
而网上搜了很久，居然没有找到AMPIRE12864的手册，郁闷。<br/>
搜出几个页面，上面也是条留言：<br/><font color="#ff6600">谁有AMPIRE12864的资料啊，能发我一份吗，我的邮箱：XXXXX。。。</font><br/><br/>
而乱逛中看到了一份成品，显示了若干文字，<br/>
因为找不到对应的手册，深究起来就有些吃力了。<br/>
于是拿想通了，花点时间，把基本功能<font color="#ff0000">黑箱</font>出来，<br/>
至少也给后来者留点简洁的上手资料。<br/><font color="#ff0000">（后面的内容属于分析结果，也许叙述上并不标准，这点各位斟酌采纳）</font><br/><br/><font color="#0000ff">二。电路</font><br/><br/><div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/4411b8fbaf2157034e4aea27.jpg"/></div>
<br/>
先说AMPIRE12864的组成：<br/>
可以看成是两个64*64的屏幕，<br/>
通过CS1,CS2两个片选信号来控制，这两个都是低有效（元件面板上没反映出来这一点）<br/><br/>
RST是低有效，所以直接连到电源了（开始因为没连这个整了半天没反映。。。）<br/>
实际应用的时候应该还是要像单片机那样做个复位电路。<br/><br/>
DBx，是并行的指令/数据输入/输出端。<br/><br/>
E是使能信号。控制时，应先置1，然后设置DB，最后E回0，结束一轮的信息交换。<br/><br/>
RW，低为写入，高为读出。<br/><br/>
RS ， 低为指令，高为数据。<br/><br/>
然后要说的就是坐标的问题：<br/><font color="#ff0000">对于每一片（左边和右边），分成8行*64列，这是光标（想成一根8位的竖线）的放置单位。<br/>
而每一行的高度为8位，从上到下对应的是DB的低位到高位</font><br/><br/><font color="#ff0000">每写一个数据，光标自动向后移动，到行末的时候返回下一行行首</font><br/>
（就跟平时用的控制台类似）<br/><br/>
有了这些之后，如果能拿到相应的手册，知道指令是怎么回事，就可以实现想要的功能了。<br/><br/><font color="#0000ff">三。程序</font><br/><br/>
//并行控制的AMPIRE12864<br/>
#include &lt;reg51.h&gt;<br/><br/>
sbit CS1 = P3 ^ 4 ;       //片选1<br/>
sbit CS2 = P3 ^ 3 ;       //片选2<br/>
sbit RW = P3 ^ 1 ;       //读写，高为读，低为写<br/>
sbit RS = P3 ^ 2 ;       //代码/数据，低为代码，高为数据<br/>
sbit E = P3 ^ 0 ;       //使能信号<br/>
sfr DB = 0xA0 ; //P2地址，数据端口<br/><br/>
typedef unsigned char uchar ;<br/><br/>
void busy_wait();<br/>
void select(uchar i);<br/>
void send(uchar type , uchar content);<br/>
#define send_cmd(x) send(0,(x))<br/>
#define send_data(x) send(1,(x))<br/>
void init();<br/>
void setpos(uchar row , uchar col);<br/><br/>
void main(){<br/>
       uchar i;<br/>
       <br/>
       select(2);<br/>
       init();<br/>
       //设置显示位置<br/>
        setpos(2,30);<br/>
       //连续输出32个字节<br/>
       for ( i = 0 ; i &lt; 32 ; i ++ )send_data(0x0f);<br/>
       setpos(3,30);<br/>
       for ( i = 0 ; i &lt; 32 ; i ++ )send_data(0xf0);              <br/>
       while(1);<br/>
}<br/><br/>
//片选，0为第一片，1为第2片<br/>
void select(uchar i){<br/>
       switch(i){<br/>
       case 0 : CS1 = 0 ; CS2 = 1 ;break;<br/>
       case 1 : CS1 = 1 ; CS2 = 0 ;break;<br/>
       case 2 : ;<br/>
       default: CS1 = 0 ; CS2 = 0 ;<br/>
       }<br/>
}<br/><br/>
//忙等待，直到LCD处理完为止<br/>
//每个命令前都应当调用<br/>
//以保证不会紊乱<br/>
void busy_wait(){<br/>
       uchar tmp;<br/>
       for (tmp = 0 ; tmp &lt; 200 ; tmp ++ );<br/><font color="#ff0000">//(2009.5.21补充，return前面是延迟，后面是读忙标志。<br/>
//正常的话，两种方式都可以达到效果的。<br/>
//只要在写命令前保证前面的命令已经执行完就行了。<br/>
//由于仿真的故障，这里就用了延迟。<br/>
//欢迎在硬件上做出来的同学更正下面的读忙标志代码段。</font><br/>
       return ;<br/>
       RS = 0 ;<br/>
       RW = 1 ;<br/>
       do{<br/>
              //因为读状态完成时间为0us，<br/>
              //所以可以连续不断地读<br/>
              DB = 0x00 ;<br/>
              E = 1 ;<br/>
              //最高位为BF,1为空闲，0为忙<br/><font color="#ff0000">//(2009.4.16补充，此处貌似跟手册不一致，以及proteus有点问题，回头来看 ）</font><br/>
              tmp = DB &amp; 0x80 ;<br/>
              E = 0 ;<br/>
       }while ( !tmp ) ;       <br/>
}<br/><br/>
void init(){<br/>
       send_cmd(0x3f);       //扩充指令集动作       <br/>
}<br/><br/>
//发送消息：<br/>
//type = 0 , 为命令消息<br/>
//type = 1 ，为数据消息<br/>
void send(uchar type , uchar content){<br/>
       switch(type){<br/>
       case 0:RS = 0 ;break;<br/>
       case 1:RS = 1 ;break;<br/>
       default:return ;<br/>
       }<br/>
       busy_wait();<br/>
       RW = 0 ;<br/>
       E = 1 ;<br/>
       DB = content ;<br/>
       E = 0 ;<br/>
}<br/><br/>
//设置显示位置<br/>
//row:0..7<br/>
//col:0..63<br/>
void setpos(uchar row , uchar col){<br/>
       if ( row &lt; 0 || row &gt;= 8 || col &lt; 0 || col &gt;= 64 ) return ;<br/>
       send_cmd(0xb8+row);<br/>
       send_cmd(0x40+col);       <br/>
}<br/><br/>
程序结合前面的说明应该能看懂了。。。<br/>
我也只能黑箱到这个程度了。<br/>
虽然一般LCD的指令，远远不只这些，但是我想基本功能已经够了。<br/>
就像前面说的，<font color="#ff0000">有了上面的这些函数之后，<br/>
就能在指定的地方画出一个点，</font><br/>
而要画任何形状的东西都很容易了。<br/>
把程序拿去，改改main函数里面的几条语句，<br/>
试试画点别的进去，就可以理解前面描述的坐标系统了。<br/><br/><font color="#0000ff">四。体会</font><br/><br/>
很多人到网上，一来就要别人做个功能强大的东西。<br/>
真不知道拿去干什么的。。或许想简单点交个作业还是啥的吧。。<br/><br/>
同时，网上很多资料。。有结果没过程，看起来很吃力。<br/><br/>
我喜欢的是一些<font color="#ff0000">简洁</font>的东西。<br/>
比如，你告诉我了怎样点亮和灭掉一个LED，<br/>
然后给我拿一排出来，要玩任何花样都可以；<br/>
你告诉我了怎样发一个音频，<br/>
我一定可以弄首歌出来。<br/><br/>
我觉得这些才是初学者应该得到的。<br/><br/>
而我看到的很多东西，一上来就把LED跑得天花乱坠的，<br/>
要不直接来首强大的歌，主要是又没注释，也没原理说明。。。<br/><br/>
这些东西，也许只有拿给喜欢捡懒的人用吧。。。拿到老师那里交差应该没问题。<br/>
对于想了解里面真正的内涵的人，乃是莫大的打击。。<br/><br/>
PS：谁有这东西的详细手册，发我一份吧^_^。。搜半天不到。。
