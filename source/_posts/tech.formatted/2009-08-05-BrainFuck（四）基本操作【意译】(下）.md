---
layout: post
title: "BrainFuck（四）基本操作【意译】(下）"
date: 2009-08-05  09:59
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 524388269617881e8b82a1bb.html
_baiduhi_category: 算法
---

<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 18pt; "><font size="3">(hplonline)2009.8.5</font><br/></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><strong><span style="font-size: 18pt; ">逻辑操作<span/></span></strong></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">首先，作逻辑真值的定义，非<span>0</span>为真，<span>0</span>为假。<span/></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">或运算，把两个操作数都移动到同一格即可<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>or(s1,s2,d)</em> <strong>=</strong> <em>move(s1,d) move(s2,d)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">与运算要依靠<span>if</span>分支结构<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>and(s1,s2,d)</em> <strong>=</strong> <em>if(s1) move(s2,d) endif(s1) zero(s2) </em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; ">zero(s2)</span></em><span style="font-size: 12pt; "> </span><span style="font-size: 12pt; ">用来当<span>s1</span>为<span>0</span>的时候对<span>s2</span>清零<span>.</span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">（这个清零也是这些宏的默认特性，即在操作之后源格清零）<span> </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">非操作<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>not(s,d)</em> <strong>=</strong> <em>inc(d) if(s) dec(d) endif(s)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><strong><span style="font-size: 18pt; ">比较<span/></span></strong></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">首先实现一个宏，他把<span>x1,x2</span>中的小者减到<span>0</span>，另一个减到<span>|x1-x2|: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span></span><em><span style="font-size: 12pt; ">subtractMinimum(x1,x2,t1,t2,t3)</span></em><span style="font-size: 12pt; "> <strong>=</strong></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>      </span><em>copy(x1,t1,t3) copy(x2,t2,t3) and(t1,t2,t3)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>      </span>to(t3)</span></em><span style="font-size: 12pt; "> [</span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>        </span><em>zero(t3)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>dec(x1) dec(x2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>copy(x1,t1,t3) copy(x2,t2,t3) and(t1,t2,t3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>      </span></span></em><em><span style="font-size: 12pt; ">to(t3)</span></em><span style="font-size: 12pt; "> ]</span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">(</span><span style="font-size: 12pt; ">这个定义的源格也就是目的格，结果返回在<span>x1</span>和<span>x2</span>里面<span>) </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">使用这个宏，可以定义各种比较<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span></span><em><span style="font-size: 12pt; ">notEqual(x1,x2,d,t1,t2)</span></em><span style="font-size: 12pt; "> <strong>=</strong> <em>subtractMinimum(x1,x2,d,t1,t2) or(x1,x2,d)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>Equal(x1,x2,d,t1,t2)</em> <strong>=</strong> <em>NotEqual(x1,x2,t1,d,t2) not(t1,d)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>Greater(x1,x2,d,t1,t2)</em> <strong>=</strong> <em>subtractMinimum(x1,x2,d,t1,t2) zero(x2) move(x1,d)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>Less(x1,x2,d,t1,t2)</em> <strong>=</strong> <em>subtractMinimum(x1,x2,d,t1,t2) zero(x1) move(x2,d)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>GreaterOrEqual(x1,x2,d,t1,t2)</em> <strong>=</strong> <em>inc(x1) Greater(x1,x2,d,t1,t2)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>LessOrEqual(x1,x2,d,t1,t2)</em> <strong>=</strong> <em>inc(x2) Less(x1,x2,d,t1,t2)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">上面的<em><span>subtractMinimum</span></em><span> </span>阅读起来很短，但展开后很长。展开后更短的版本如下<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>subtractMinimum(x1,x2,t1,t2,t3)</em> <strong>=</strong></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>      </span></span><em><span style="font-size: 12pt; ">for(x1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>         </span>copy(x2,t1,t2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>         </span>ifelse(t1,t2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>           </span>dec(x2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>         </span>else(t1,t2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>          </span><span> </span>inc(t3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>         </span></span></em><em><span style="font-size: 12pt; ">endelse(t2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>      </span>next(x1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>      </span>move(t3,x1)</span></em><span style="font-size: 12pt; "/></p>
<p align="left" style="text-align: left;" class="MsoNormal"><strong><span style="font-size: 18pt; ">和小常数比较<span/></span></strong></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">使用逻辑运算和<span>if</span>结构，递归定义<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>isZero(s,d)</em> <strong>=</strong> <em>not(s,d)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>isOne(s,d)</em> <strong>=</strong> <em>if(s) dec(s) isZero(s,d) endif(s)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>isTwo(s,d)</em> <strong>=</strong> <em>if(s) dec(s) isOne(s,d) endif(s)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>isThree(s,d)</em> <strong>=</strong> <em>if(s) dec(s) isTwo(s,d) endif(s)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span>....</span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">（<span>hplonline</span>：其实可以牺牲一个临时格，先用来生成常数，然后使用上一节的比较，可避免递归）<span/></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><strong><span style="font-size: 18pt; ">常数<span/></span></strong></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">给一个格加上特定的常数，可以直接使用需要数量的<span>’+’</span>，也可以参考作者的大数生成：<span><a href="http://www.iwriteiam.nl/Ha_bf_numb.html">Big numbers in BF</a>. </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><strong><span style="font-size: 18pt; ">数组<span/></span></strong></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">这里的数组为一系列无穷长度的数组，一开始应该确定下需要多少数组（<span>n</span>）和这些数组开始的地方（<span>b</span>），实现数组即实现获取（<span>get</span>）和存储（<span>set</span>）<span/></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">为了实现先作如下定义<span>: </span></span></p>
<ul type="disc"><li style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; ">b</span></em><span style="font-size: 12pt; ">: </span><span style="font-size: 12pt; ">数组区域的开始<span>. </span></span></li>
    <li style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; ">n</span></em><span style="font-size: 12pt; ">: </span><span style="font-size: 12pt; ">数组的个数<span>. </span></span></li>
    <li style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; ">a</span></em><span style="font-size: 12pt; ">: </span><span style="font-size: 12pt; ">指出使用的数组是哪个（<span>0</span>开始）<span> </span></span></li>
    <li style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; ">i</span></em><span style="font-size: 12pt; ">: </span><span style="font-size: 12pt; ">指出该数组中的下标（<span>0</span>开始）<span> </span></span></li>
    <li style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; ">v</span></em><span style="font-size: 12pt; ">: get</span><span style="font-size: 12pt; ">方法中，代表把值放入的格，<span>set</span>方法中，代表把待放入的值所在的格<span>. </span></span></li>
</ul><p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; ">Set</span><span style="font-size: 12pt; ">和<span>get</span>方法的定义如下<span>: </span></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>setarray(b,n,a,i,v)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span>= <em>copy(i,b+1,b)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>copy(v,b+2,b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>for(b+1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b,b+n+3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b+1,b+n+4)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b+2,b+n+5)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>right(n+3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>inc(b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>next(b+1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>zero(a)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>move(b+2,a)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>for(b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>left(n+3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b+n+3,b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>next(b)</span></em><span style="font-size: 12pt; "/></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span><em>getarray(b,n,a,i,v)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "><span>  </span>= <em>copy(i,b+1,b)</em></span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>for(b+1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b,b+n+3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b+1,b+n+4)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>right(n+3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>inc(b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>next(b+1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>copy(a,b+1,b+2)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>for(b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>left(n+3)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b+n+3,b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>        </span>move(b+n+4,b+1)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>next(b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><em><span style="font-size: 12pt; "><span>     </span>move(b+1,v,b)</span></em></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p class="MsoNormal"><span style="font-size: 12pt; ">其中 <em><span>right(n)</span></em><span> </span>代表<em><span>n</span></em><span> </span>个<span>'&gt;'</span>符号， <em><span>left(n)</span></em><span> </span>代表 <em><span>n</span></em><span> </span>个<span>'&lt;'</span>符号。<span/></span></p>
<p class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p class="MsoNormal"><span style="font-size: 12pt; ">（<span>hplonline</span>：<span/></span></p>
<p class="MsoNormal"><span style="font-size: 12pt; ">这里数组的结构是这样的：<span/></span></p>
<p class="MsoNormal"><span style="font-size: 12pt; ">b b+1 b+2 b+3 b+4 … b+n+2 b+n+3 b+n+4 b+n+5 b+n+6 b+n+7 … </span></p>
<p class="MsoNormal"><span style="font-size: 12pt; ">t1 t2<span>  </span>t<chmetcnv tcsc="0" numbertype="1" negative="False" hasspace="True" sourcevalue="3" unitname="a">3 a</chmetcnv><chmetcnv tcsc="0" numbertype="1" negative="False" hasspace="True" sourcevalue="11" unitname="a">11 a</chmetcnv>21<span>      </span>an1<span>    </span>t1<span>      </span>t2<span>     </span>t<chmetcnv tcsc="0" numbertype="1" negative="False" hasspace="True" sourcevalue="3" unitname="a">3<span>    </span>a</chmetcnv><chmetcnv tcsc="0" numbertype="1" negative="False" hasspace="True" sourcevalue="12" unitname="a">12<span>  </span>a</chmetcnv>22</span></p>
<p class="MsoNormal"><span style="font-size: 12pt; "> </span></p>
<p class="MsoNormal"><span>aij</span><span>代表的是第</span><span>i</span><span>个数组的第</span><span>j</span><span>个元素。</span><span>t</span><span>代表的是临时单元。</span><span/></p>
<p class="MsoNormal"><span>即先排上所有数组的第一个元素，再排上所有数组的第二个元素，再是所有数组的第三个元素。。。</span><span/></p>
<p class="MsoNormal"><span> </span></p>
<p class="MsoNormal"><span>这个设计确实很巧妙，以</span><span>set</span><span>方法来说。先把待存入数值放入</span><span>t3</span><span>，把下标放入</span><span>t2</span><span>。</span><span/></p>
<p class="MsoNormal"><span>然后不断循环，每次把</span><span>t3</span><span>，</span><span>t2</span><span>，</span><span>t1</span><span>搬移</span><span>n</span><span>位，并且把</span><span>t2</span><span>减</span><span>1</span><span>，</span><span>t1</span><span>加</span><span>1</span><span>。</span><span/></p>
<p class="MsoNormal"><span>这样，到</span><span>t2</span><span>为</span><span>0</span><span>的时候就是该元素应该存放的段了，然后加上数组的偏移即可。</span><span/></p>
<p class="MsoNormal"><span>退回来的时候，只要找到</span><span>t1</span><span>为</span><span>0</span><span>的地方就行了。</span><span/></p>
<p class="MsoNormal"><span>为什么要退回来，也是这套宏的一致性定义，</span><span/></p>
<p class="MsoNormal"><span>要保证操作之后，除了指定的格的值被改变外，指针不动，</span><span/></p>
<p class="MsoNormal"><span>这样才能在更大的程序段中调用他们而不出错。</span><span/></p>
<span>）</span>
