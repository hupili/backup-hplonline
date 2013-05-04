---
layout: post
title: "拉格朗日松弛(SubGradient Method)"
date: 2009-10-18  14:10
comments: true
categories: tech
tags: ["Math"]
_baiduhi_id: 967eaec21c81b2110ff477f7.html
_baiduhi_category: Math
---

<p>(hplonline)2009.10.18</p>
<p>数学规划中常用拉格朗日松弛法来分解问题。<br/>
前段时间，曾经尝试用了一下这个方法来解带约束的最短路。<br/>
由于老师的课件中仅仅是一个原理性的介绍，<br/>
没有具体的操作办法，所以一直不理解要怎么更新乘子（u）。</p>
<p>当时直接把u拿来二分了，<br/>
其效果类似一个种加权，<br/>
后来想了下，即使是二分，<br/>
也应该在对数尺上做，<br/>
否则乘子的绝对值不一样的时候精度不一样。</p>
<p>前几天去找了上学期最优化的老师。<br/>
专业人士就是不一样，<br/>
手头有不少人类进步的电梯（电子书）。</p>
<p>其中，这本<br/>
《DECOMPosition techniques in math programming1》<br/>
讲得比较详细，又有例子，容易看懂。</p>
<p>这里按照书中描述的原理作一个<br/>
用subgradient(SG)法更新乘子的试验。<br/>
查词典叫“次梯度”，<br/>
我不知道怎么翻译，<br/>
也不知道其数学定义，<br/>
反正按照书中所述地使用就行了。</p>
<p>问题和算法都描述在了代码的注释里了。</p>
<p><font color="#0000ff">程序：</font></p>
<p>% &gt;&gt;1.primal problem:<br/>
% minimize f(x,y) = x^2 + y^2<br/>
% subject to:<br/>
%      -x - y &lt;= -4 <br/>
%      x &gt;= 0 <br/>
%      y &gt;= 0 <br/>
% &gt;&gt;2.Lagrangian function is<br/>
% L(x,y,u) = x^2 + y^2 + u(-x - y + 4)<br/>
% subject to x &gt;= 0 ,y &gt;= 0<br/>
% &gt;&gt;3.subproblem of L<br/>
% phi1(u) = minimize L1(u) = x^2 - u * x + 2 * u , s.t. x&gt;=0<br/>
% phi2(u) = minimize L2(u) = y^2 - u * y + 2 * u , s.t. y&gt;=0<br/>
% &gt;&gt;4.solving subproblem<br/>
% xc = u / 2 <br/>
% yc = u / 2<br/>
% &gt;&gt;5.s vector = [-x - y + 4] , (here only 1 component)<br/>
% <br/>
% &gt;&gt;SG method for LR multiplier updating (algorithm)<br/>
% 1).set u0 , a , b , v = 1 ,<br/>
% 2).get xc , yc from decomposed problem<br/>
% 3).u(v+1) = u(v) + 1/(a+b*v) * (s / abs(s))<br/>
% 4).convergence checking <br/>
%      if stop condition meeted , x_star = xc , y_star = yc<br/>
%      else v = v + 1 , goto 2 ,</p>
<p>clear ;<br/>
clc ;<br/>
close all ;</p>
<p>a = 1 ;<br/>
b = 0.1 ;<br/>
v = 1 ;<br/>
u = 3 ;<br/>
V = 2000 ;</p>
<p>%iteration begin<br/>
while v &lt; V <br/>
     xc(v) = u(v) / 2 ;<br/>
     yc(v) = u(v) / 2 ; % see &gt;&gt;4<br/>
     f(v) = xc(v).^2 + yc(v).^2 ;<br/>
     L(v) = xc(v).^2 + yc(v).^2 + u(v)*(-xc(v) - yc(v) + 4) ;<br/>
     k(v) = 1 / (a + b * v) ;<br/>
     s(v) = [-xc(v) - yc(v) + 4] ; % see &gt;&gt;5<br/>
     u(v + 1) = u(v) + k(v) * ( s(v) / abs(s(v))) ;<br/>
     %no convergence checking here<br/>
     v = v + 1 ;<br/>
end<br/>
[u(1:end-1)' , xc' , yc' , f' , L'] <br/>
xc(end) , yc(end)</p>
<p><font color="#0000ff">输出：</font></p>
<p>ans =<br/>
     2.0025<br/>
ans =<br/>
     2.0025</p>
<p>理论计算的最优答案是（2,2）<br/>
相差不大，还行</p>
