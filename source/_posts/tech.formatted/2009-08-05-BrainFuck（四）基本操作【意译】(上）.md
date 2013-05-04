---
layout: post
title: "BrainFuck（四）基本操作【意译】(上）"
date: 2009-08-05  09:58
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: c62071cb96ac6416bf09e6ba.html
_baiduhi_category: 算法
---

<p class="MsoNormal"><span>(hplonline)2009.8.4<br/><br/></span><span>原文：</span><span><br/><a href="http://www.iwriteiam.nl/Ha_bf_intro.html" target="_blank">http://www.iwriteiam.nl/Ha_bf_intro.html</a><br/><br/></span><span>（意译的标准在于本人能理解，</span><span><br/></span><span>知道大意后，详细内容还是要参考原文，</span><span><br/></span><span>这篇更类似摘要或者笔记）</span></p>
<p class="MsoNormal"><span> </span></p>
<p class="MsoNormal"><span>这篇的内容涉及到很多宏的定义，需要从头按顺序看，才能理解，要记住各个宏定义的时候的参数是什么意义。这篇在于给出一个功能上的完整集合，所以并非里面的宏是在具体使用时候的最优解决方案，很多时候，可以针对特殊情况进行改进的。但是通过这篇给出的宏的方式，比较容易构建程序，并且展开方便。</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><strong><span style="font-size: 18pt;"> </span></strong></p>
<p align="left" class="MsoNormal" style="text-align: left;"><strong><span style="font-size: 18pt;">移动，复制，加法</span></strong></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">最简单的程序，清零当前所指的格<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span>[-]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把当前格的数字移动到右边一格<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span>[ &gt; + &lt; - ]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">通用的移动数字的框架为<span>: </span></span></p>
<ul type="disc"><li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把指针移动到源点</span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">"["      command </span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把指针移动到目的点<span> </span></span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">"+"      command </span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">（这一步可能对多个目的点相加）</span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把指针移动到源点</span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">"-"      command </span></li>
    <li class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">"]"      command </span></li>
</ul><p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">定义 <em><span>to(m)</span></em><span> </span>为把指针移动到<em><span>m</span></em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><em><span style="font-size: 12pt;">move(s,d)</span></em><span style="font-size: 12pt;"> </span><span style="font-size: 12pt;">表示移动<span>s</span>的数字到<span>d, </span>可以写作<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>move(s,d)</em> <strong>=</strong> <em>to(s)</em> [ <em>to(d)</em> + <em>to(s) </em>- ]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">定义 <em><span>for(a)</span></em><span> </span>和 <em><span>next(a)</span></em><span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>for(a)</em> <strong>=</strong> <em>to(a)</em>[</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>next(a)</em> <strong>=</strong> <em>to(a)</em>-]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>move(s,d)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><strong>=</strong> <em>for(s)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>        </span><em>to(d)</em> +</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>      </span><em>next(s)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把一个源点移动到两个目的点<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>move2(s,d1,d2)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><strong>=</strong> <em>for(s)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>        </span><em>to(d1)</em> +</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>        </span><em>to(d2)</em> +</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>      </span><em>next(s)</em>-]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把<span>s</span>复制到<span>t</span>需要用到一个临时单元<span>t: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>copy(s,d,t)</em> <strong>=</strong> <em>move2(s,d,t) move(t,s)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">以上的操作都默认了各个格子在操作之前是空的。</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><strong><span style="font-size: 18pt;">乘法和幂</span></strong></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">把一个数变成两倍<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>double(s,d)</em> <strong>=</strong> <em>move2(s,d,d)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">用 <em><span>constant(n)</span></em><span> </span>表示在当前格设置常数<span>n</span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">那么<span>s</span>乘以常数<span>n</span>可以写作<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>multiplyconst(s,d,n)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><strong>=</strong> <em>for(s)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>        </span><em>to(d) constant(n)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>      </span><em>next(s)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">两个数相乘：<span> </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>times(s1,s2,d,t)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><strong>=</strong> <em>for(s1)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>        </span><em>copy(s2,d,t)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>      </span><em>next(s1)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>      </span><em>zero(s2)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">注意，在以上以及以后的定义中，都认为一个操作完成后源格被置零。</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">乘幂，就是重复乘法就行了<span>:</span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>power(x,p,d,t1,t2,t3)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span></span><strong><span style="font-size: 12pt;">=</span></strong><span style="font-size: 12pt;"> <em>to(d)</em> +</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>      </span><em>for(p)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><em><span style="font-size: 12pt;"><span>          </span>copy(x,t1,<span style="color: red;">t2</span>)</span></em></p>
<p align="left" class="MsoNormal" style="text-align: left;"><em><span style="font-size: 12pt;"><span>          </span></span></em><em><span style="font-size: 12pt;">times(d,t1,t2,t3)</span></em></p>
<p align="left" class="MsoNormal" style="text-align: left;"><em><span style="font-size: 12pt;"><span>          </span>move(t2,d)</span></em></p>
<p align="left" class="MsoNormal" style="text-align: left;"><em><span style="font-size: 12pt;"><span>      </span></span></em><em><span style="font-size: 12pt;">next(p)</span></em></p>
<p align="left" class="MsoNormal" style="text-align: left;"><em><span style="font-size: 12pt;"><span>      </span>zero(x)</span></em></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">（红色部分为<span>hplonline</span>更正，因为<span>copy</span>宏的定义要用到一个临时格）</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"> </p>
<p align="left" class="MsoNormal" style="text-align: left;"><strong><span style="font-size: 18pt;">If-then-else</span></strong><strong><span style="font-size: 18pt;">分支结构</span></strong></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">之前实现了循环，<span>[]</span>可以进行判断，而分支可以视作只执行一次的循环，所以按照循环的结构，在分支内部把控制循环真值的格清零即可。定义如下符号<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>zero(a)</em> <strong>=</strong> <em>to(a)</em> [-]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>if(a)</em> <strong>=</strong> <em>to(a)</em> [</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>endif(a)</em> <strong>=</strong> <em>zero(a)</em> ]</span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"> </span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">实现<span>else</span>结构，只需增加一个临时变量，首先置<span>1</span>，进入<span>if</span>分支的时候清零，则在下一次判断不进入<span>else</span>分枝<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>ifelse(a,t)</em> <strong>=</strong> <em>inc(t) if(a) dec(t)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>else(a,t)</em> <strong>=</strong> <em>endif(a) if(t)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>endelse(t)</em> <strong>=</strong> <em>endif(t)</em></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;">最后一个宏也可写作<span>: </span></span></p>
<p align="left" class="MsoNormal" style="text-align: left;"><span style="font-size: 12pt;"><span>  </span><em>endelse(t)</em> <strong>=</strong> <em>dec(t)</em> ]</span></p>
(百度说我太长了。。。只有分成两篇。。）<br/><p class="MsoNormal"> </p>
