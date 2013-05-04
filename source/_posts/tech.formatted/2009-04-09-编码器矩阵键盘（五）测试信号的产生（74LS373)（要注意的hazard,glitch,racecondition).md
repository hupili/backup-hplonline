---
layout: post
title: "编码器矩阵键盘（五）测试信号的产生（74LS373)（要注意的hazard,glitch,race condition)"
date: 2009-04-09  20:27
comments: true
categories: tech
tags: ["Scm"]
_baiduhi_id: 8d68db58fbb80d89800a189d.html
_baiduhi_category: Scm
---

(hplonline)2009.4.9<br/><br/><font color="#0000ff">需求分析：</font><br/><br/>
前面把大量的工作做好了。这里来收一下尾。我们还差一个test信号。<br/><br/>
这一块要干的事：<br/><font color="#ff6600">1.使所有行线为1，所有测试信号与列线相接的端口为高阻态<br/>
2.使能列编码器，禁止行编码器</font><br/>
（反之也有）<br/><br/><font color="#0000ff">电路：</font><br/><br/><div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/5e28df627b979dffe6113acb.jpg"/><br/><br/>
有了这些需求后，自然想到74LS373。这东西真的好用。<br/><br/>
先用一个非门，产生test的反信号itest。<br/><br/>
test有效的时候，是行为1，测试列线，所以ecol和itest为同一电平。<br/>
erow和test为同一电平。<br/><br/>
然后看U10<br/><br/>
test为1的时候row0和row1要为1.<br/>
所以使d0，d1为test，OE为itest。<br/><br/>
另一边正好相反，所以成高阻。这些都是很好想到的。<br/><font color="#0000ff"><br/>
关于test_d的解释。：</font><br/><br/><font color="#ff0000">各位注意U11的下面OE端是test_d。</font>。。<br/><br/>
再看U16，把itest取反，其实其值就是test。那么这个d仅仅是为了延迟（delay之意）<br/><br/>
这就涉及到数电里面提到的hazard（危害，冒险)了，有的地方也叫glitch（电路尖峰）。<br/>
按照正常的来说，先学数电，再学单片机，会认为这些都是很熟悉的内容。。。<br/>
只有我这样先学单片机。。才开始学数电的发现了才觉得很囧。。。<br/>
（这个问题找了很久。。。其中乱改一通，<br/>
有时proteus报告：race condition detected。<br/>
不以为然，继续乱改，后来终于看到这里来了。。。<br/>
果然是竞争状态。。唉。。。）<br/><br/>
首先，要搞清楚373的工作。<br/><br/>
如果把test直接接到OE上。<br/>
假设这时test为1。该373是高阻的。<br/>
然后我们把test变为0 。<br/>
这个时候itest由于非门延迟，还么有变为1。而OE端成了0，输出有效。<br/>
于是Q0Q1成了0 。<br/>
非门延迟过后，itest成了1。<br/><br/>
以前只考虑静态逻辑，想到反正OE是低，输入为1，输出也就1。<br/>
可以373的动态逻辑是，在OE的下降延来输出的。<br/><br/>
所以输出0之后，虽然itest成了1，但是我们的373已经不理他了。<br/><br/>
这样，不管怎么按键，读到的行线都是低，反向为高，不进行编码。。。<br/><br/>
所以，把itest再次反向，形成test_d，让使能信号与数据信号之后跳变。这个问题就解决了。<br/><font color="#ff6600"><br/>
没想到一个proteus这么五脏俱全。一点hazard都不放过，厉害。。</font><br/>
囧了我这么久才囧出来。。</div>
