---
layout: post
title: "用ROM自制ALU（proteus，vc，27c512)"
date: 2009-06-07  12:56
comments: true
categories: tech
tags: ["Scm"]
_baiduhi_id: d916c9ce0ae70d0b93457e69.html
_baiduhi_category: Scm
---

(hplonline)2009.6.7<br/><br/>
完整作品下载：<a href="http://www.box.net/shared/1ogxc1lnyx" target="_blank">rom_caculator</a><br/><br/>
前些时候，学习数电，听说了74X181这个东西，<br/>
感觉功能还挺多的，结果在proteus里面仿真的时候，<br/>
只有一个空壳在那里，没有相关的模型，无法使用。（我是7.12版）<br/><br/>
这周数电结课，听到了一句近乎哲学的话（至少是相对这个学科而言），<br/>
一语惊醒梦中人啊：<br/><br/><font color="#ff0000">rom的本质就是一个n输入m输出组合逻辑电路。</font><br/>
（地址线有n位，数据线有m位）<br/>
在课上苦苦耗了一学期，听到的最有用的一句莫过于此<img src="http://img.baidu.com/hi/jx/j_0015.gif"/>。<br/>
我很喜欢这种，说出来地球人都知道，但是不说，大部分地球人都不知道的东西。。。<br/><br/>
那么接上面，比如这里选用的27c512就可以看作16输入，8输出的组合逻辑电路了。<br/><br/><font color="#0000ff">电路：</font><br/><br/><div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/1f1e11d5e16ba4e150da4b70.jpg"/></div>
<br/>
a和b是4bit的数据输入，上面为低位，直接接到了0--7的地址线上。<br/>
下面是运算符选择。四种运算符，用编码器编码后送到8，9两位。<br/><br/>
右边的D[0..7]就是数据输出，也是上面为低位。<br/><br/>
上图演示的就是a/b的结果（即：7/2=3）<br/><br/><font color="#0000ff">程序：</font><br/><br/>
程序就很简单了，随便拿个在pc上写c的工具就可以了。<br/><br/>
#include &lt;stdio.h&gt;<br/><br/>
int main(){<br/>
      FILE *fp = fopen("data_rom.bin" , "wb") ;<br/>
      unsigned int i , j ;<br/>
      unsigned char ch ;<br/><br/>
      for ( i = 0 ; i &lt; 16 ; i ++ ) {<br/>
            for ( j = 0 ; j &lt; 16 ; j ++ ){<br/>
                  ch = i + j ;<br/>
                  fwrite(&amp;ch , 1 , 1 , fp) ;<br/>
            }<br/>
      }<br/><br/>
      for ( i = 0 ; i &lt; 16 ; i ++ ) {<br/>
            for ( j = 0 ; j &lt; 16 ; j ++ ){<br/>
                  ch = (unsigned char)(j - i) ;<br/>
                  fwrite(&amp;ch , 1 , 1 , fp) ;<br/>
            }<br/>
      }<br/><br/>
      for ( i = 0 ; i &lt; 16 ; i ++ ) {<br/>
            for ( j = 0 ; j &lt; 16 ; j ++ ){<br/>
                  ch = i * j ;<br/>
                  fwrite(&amp;ch , 1 , 1 , fp) ;<br/>
            }<br/>
      }      <br/><br/>
      for ( i = 0 ; i &lt; 16 ; i ++ ) {<br/>
            for ( j = 0 ; j &lt; 16 ; j ++ ){<br/>
                  if ( i == 0 ) ch = 0xff ;<br/>
                  else ch = j / i ;<br/>
                  fwrite(&amp;ch , 1 , 1 , fp) ;<br/>
            }<br/>
      }<br/><br/>
      fclose(fp) ;<br/>
      return 0 ;<br/>
}<br/><br/><font color="#0000ff">加载：</font><br/><br/>
在proteus里面，为27c512指定数据文件，就选择上面生成的data_rom.bin。<br/>
然后就可以使用了。<br/><br/><font color="#0000ff">总结：</font><br/><br/>
一旦得知到rom的本质之后，可以用其来实现的逻辑即可获得大幅增长。<br/><br/>
一般的数电，微机原理之类的课程都会提到相应的<font color="#ff0000">字扩展，位扩展</font>的事情。<br/>
这样，就可以得到<font color="#ff0000">任意想要的输入个数和输出个数</font>。<br/><br/>
剩下的事情就是生成相应的数据，下载到rom里面这么简单。<br/><br/>
个把月前，当初次听说181，但又没找到相应的模型的时候，<br/>
真的是很纠结，当时想了两种：<br/><font color="#ff6600">1。用其他MSI来搭建。。。其复杂程度无法想象，作罢。<br/>
2。自己做个元件。。在网上找了很久的资料。。没找着有用的，也罢。。</font><br/><br/>
而现在，任何的组合逻辑都可以用一个小小的rom来实现，<br/>
可谓强大啊。。虽然上面只给了几个简单的四则运算。<br/>
但是，各位看官必然想到，用他来开方，求幂，控制数码管显示，等等，<br/>
都完全不在话下。。<br/><br/>
用C语言写段程序，生成相应的数据显然比用若干器件来搭建一个庞大的电路简单。<br/><font color="#ff0000">另外，对应于任何输入，获得稳定输出的时间都是一样的。</font><br/>
（这点是其他器件搭建出来的不容易做到的，<br/>
因为不同的输入途经的线路会不同，<br/>
比较典型的就是像ripple adder这种，<br/>
最小和最大延迟之间成倍数关系）<br/>
再换句话说，这种搞法有点<font color="#ff0000">打表</font>的味道。<img src="http://img.baidu.com/hi/jx/j_0015.gif"/><br/>
可见一个通用的思想，可以用在不同的地方。<br/>
（可参考：<a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/8fbb05b30fb894a0d8335ae9.html">编译器打表（MASM)</a>）<br/><br/>
rom。。。很邪恶，很暴力的通用解决方案。<img src="http://img.baidu.com/hi/jx/j_0003.gif"/>
