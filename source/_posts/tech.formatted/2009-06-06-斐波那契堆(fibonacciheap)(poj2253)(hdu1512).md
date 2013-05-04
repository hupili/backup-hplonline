---
layout: post
title: "斐波那契堆(fibonacci heap)(poj2253)(hdu1512)"
date: 2009-06-06  10:59
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: c0f979f073fcb7a7a50f5295.html
_baiduhi_category: 算法
---

(hplonline)2009.6.6<br/><br/>
我的参考代码和详细的资料在<a href="http://www.box.net/shared/mvvr4h2cyq" target="_blank">这里下载</a>。<br/>
其中写了导读了，于是我就不在这里说了。<br/><a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/c62071cb4d9b1917bf09e6b4.html">上一篇</a>中也有简单的提要，可以在最后看下。<br/><br/>
HDU1512，这个在前面的<a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/7a8a0633d33d0ef01b4cff08.html">左偏树</a>里面提到过了。<br/>
因为当时刷了下不是很快，于是想到有斐波那契堆这个东西，<br/>
结果用好不容易搞了个斐波那契堆出来，反而更慢，太失望了。<br/><br/><a href="http://www.box.net/shared/tyanmpcxiz" target="_blank">HDU1512.TXT</a><br/><br/>
POJ2253，求的是 Min Max路径，就是经过的边中最大值最小的路。<br/>
随便上一种最短路的算法就可以了。<br/>
刷这个题，只是为了测试一下用斐波那契堆实现可改点堆的正确性。<br/><br/><a href="http://www.box.net/shared/slixsfievu" target="_blank">POJ2253.TXT</a><br/><br/><font color="#0000ff">我的终极bug：</font><br/><br/>
1.bug版<br/>
//将l2放到l1的断开处<br/>
PFNode _list_merge(PFNode l1 , PFNode l2){<br/>
      if ( l1 == NULL ) return l2 ;<br/>
      if ( l2 == NULL ) return l1 ;<br/>
      PFNode l1_right = l1-&gt;right ;<br/>
      PFNode l2_right = l2-&gt;right ;<br/><font color="#ff0000">      l1-&gt;right = l2 ;<br/>
      l2-&gt;left = l1 ;<br/>
      l2_right-&gt;right = l1_right ;<br/>
      l1_right-&gt;left = l2_right ;</font><br/>
      return l1 ;<br/>
}<br/><br/>
2.正常版<br/>
//将l2放到l1的断开处<br/>
PFNode _list_merge(PFNode l1 , PFNode l2){<br/>
      if ( l1 == NULL ) return l2 ;<br/>
      if ( l2 == NULL ) return l1 ;<br/>
      PFNode l1_right = l1-&gt;right ;<br/>
      PFNode l2_right = l2-&gt;right ;<br/><font color="#ff0000">      l1-&gt;right = l2_right ;<br/>
      l2-&gt;right = l1_right ;<br/>
      l2_right-&gt;left = l1 ;<br/>
      l1_right-&gt;left = l2 ;/*here ...*/</font><br/>
      return l1 ;<br/>
}<br/><br/>
这就是我调了三天的最大的一个bug（当然期间也有不少小的bug）<br/>
仔细一看。。。其实就是把双向链表的合并写错了<img src="http://img.baidu.com/hi/jx/j_0012.gif"/>。<br/>
可见基础的数据结构都没过关，太浮躁了<img src="http://img.baidu.com/hi/jx/j_0004.gif"/>。。。。<br/><br/><font color="#0000ff">一点感想:</font><br/><br/>
有时候，花多少时间仅仅取决于对于一件事情的较真程度。<br/><br/>
写出第一版，仅花了两个小时。<br/>
随便写几个插入删除，看结果都很正常。<br/>
于是我身边的80%的人，会就此停住了。<br/>
（常年在纸上写程序，连能否编译通过都不知道，<br/>
还期望他们有闲心去测试什么吗？<br/>
对于他们来说，老师的红勾就是正确的代名词）<br/><br/>
接着我用大数据进行排序的测试。<br/>
发现了一些问题，调了之后，对于20000的数据排序都正常了。<br/>
这时候，不说别人了，连我自己都心满意足了。<br/>
直到这个时候，也才花了三小时左右。<br/><br/>
本来当天就想把我的东西发出来的，<br/>
又想了一下，还是去把HDU1512给刷了再说。<br/>
改了一下，把样例过了，交上去，TLE了。。。。。<br/><br/>
第二天又来搞，发现了TLE所在，一改，结果WA了。。<br/>
很想不通，于是自己生成了数据，跟前面用左偏树写一起测，<br/>
发现果然答案不同。。。<br/><br/>
第三天又找啊找。。才发现了原来是上面提到的链表操作失误。。<br/>
当时那个郁闷啊。。。因为这几天一直在想是不是对斐波那契堆的理解有误。<br/>
根本没有怀疑过会在这种基础结构上出问题。。。。<img src="http://img.baidu.com/hi/jx/j_0012.gif"/><br/><br/>
于是昨晚把HDU1512刷了，刚想发，想起减值操作还没测试。。。<br/>
于是又在POJ上找了道很水的最短路，来整个改点堆。。。<br/><br/>
好不容易。。终于可以放心地发了。。。<img src="http://img.baidu.com/hi/jx/j_0009.gif"/>。<br/>
（不过各位发现bug了，记得要跟我说哈）
