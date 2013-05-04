---
layout: post
title: "SplayTree(伸展操作的一个演示）"
date: 2009-06-01  16:55
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 3c1feafe3f1c5e395d600848.html
_baiduhi_category: 算法
---

(hplonline)2009.6.1<br/><br/>
上篇给出了一个SplayTree的完整实现。<br/>
可以看到，一旦有了splay操作，那么其他的事情就很好办了。<br/><br/>
不过我看到的这份splay操作实在是很费解。<br/>
于是一边看一边拿visio画图。<br/>
其实我也不杂理解，拿出来大家一起看一下玩。<br/><br/><font color="#0000ff">伸展代码如下：</font><br/><br/>
PSNode SplayTree::_splay(ElemType d , PSNode p){<br/>
      //(1)left:待完成的树左子树，他的右子树为空<br/>
      //(2)通过移动，可以把left视为右子树为空的树串成的链表<br/>
      //left为左子树中的最大值（因为右子树为空）<br/>
      PSNode left , right ;<br/>
      //为了满足(1)，设置一个header，他初始的时候左右均空<br/>
      SNode header ;<br/>
      header.left = nil ;<br/>
      header.right = nil ;<br/>
      //而left和right均从header开始出发<br/>
      //(3)当left离开header的时候，left的右端挂上的肯定是当前树的左端<br/>
      left = &amp;header ;<br/>
      right = &amp;header ;<br/><br/>
      nil-&gt;data = d ;//(4)避免在空节点处发生双旋<br/><br/>
      while ( p-&gt;data != d ){<br/>
            if ( d &lt; p-&gt;data ){<br/>
                  if ( d &lt; p-&gt;left-&gt;data ) { // 当p-&gt;left为nil时，条件自动不成立，见(4)<br/>
                        p = _rotate_right(p) ; //同个方向前进，应该双旋<br/>
                  }<br/>
                  if ( p-&gt;left == nil ) break ;//节点查找失败，但p已经为新节点应当的插入点了。<br/>
                  right-&gt;left = p ;<br/>
                  right = p ;<br/>
                  p = p-&gt;left ;<br/>
            }else{<br/>
                  if ( p-&gt;right-&gt;data &lt; d ) {<br/>
                        p = _rotate_left(p) ;<br/>
                  }<br/>
                  if ( p-&gt;right == nil ) break ;<br/>
                  left-&gt;right = p ;<br/>
                  left = p ;<br/>
                  p = p-&gt;right ;<br/>
            }<br/>
      }<br/><br/>
      //p已经是我们要的节点了。他为新的根<br/>
      left-&gt;right = p-&gt;left ;//left的右端是空的,见(1)<br/>
      right-&gt;left = p-&gt;right ;<br/>
      //将header左右子树链接到p上面<br/>
      p-&gt;left = header.right ;//head的右端是新根的左端，见(3)<br/>
      p-&gt;right = header.left ;<br/>
      return p ;<br/>
}<br/><br/><font color="#0000ff">下图是关于双旋的演示：</font><br/><div forimg="1"><br/><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/c0f979f03064768aa50f5211.jpg"/><br/><br/>
下面的这个可以看作是中间状态。<br/><br/><br/><font color="#0000ff">1。初始的时候，令空节点的值为splay操作的值。</font><br/>
把header做成一个左右均空的节点。<br/>
让left和right都指向header</div>
<div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/a2f3e1c477236f8c8326ac12.jpg"/><br/><br/><br/><font color="#0000ff">2。第一次比较，应该向左移动两次。</font></div>
<div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/a2f1ba51367faa3d377abe12.jpg"/><br/><br/><br/><font color="#0000ff">3。先对X右旋一次。</font></div>
<div forimg="1"><br/><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/cb5e40edfd15a7f1b21cb112.jpg"/><br/><br/><br/><br/><font color="#0000ff">4。将X的右枝挂到right的左枝，同时移动right向新的左枝<br/><br/></font></div>
<div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/8fc50d08f45e3315e8248812.jpg"/><br/><br/><font color="#0000ff">5。应该向X的右端插入，但已经为空，于是停止。</font><br/><br/>
将X的左枝挂到left的右枝上。<br/>
将X的右枝挂到right的左枝上。</div>
<div forimg="1"><br/><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/7fec1795ee1d2e2d7af48012.jpg"/><br/><br/><font color="#0000ff">6。最后一步合并操作。</font><br/><br/>
将header的右枝挂给X的左枝<br/>
将header的左枝挂给X的右枝</div>
<div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/612531c71b5ad4f9d0006012.jpg"/></div>
<div forimg="1"><br/><font color="#0000ff">7。将元素4在树根的位置插入</font><br/><br/><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/c0eab0a145765eae46106412.jpg"/></div>
