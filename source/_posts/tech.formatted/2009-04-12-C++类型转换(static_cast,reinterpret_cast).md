---
layout: post
title: "C++类型转换(static_cast,reinterpret_cast)"
date: 2009-04-12  15:33
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: a8f8c2fc9100a4f5fd037fa4.html
_baiduhi_category: c&c++
---

(hplonline)2009.4.12<br/><br/><font color="#0000ff">先来个实验</font>。<br/>
定义如下三个类。<br/><br/>
class ca{<br/>
public:<br/>
     int ia ;<br/>
};<br/><br/>
class cb{<br/>
public:<br/>
     int ib1,ib2 ;<br/>
};<br/><br/>
class cc:public ca,public cb{<br/>
public:<br/>
};<br/><br/>
然后打印出一组数据:<br/><br/>
     cc c ;<br/>
     cc *pc = &amp;c ;<br/>
     cb *pb1 = pc ;<br/>
     cb *pb2 = static_cast&lt;cb*&gt;(pc);<br/>
     cb *pb3 = (cb*)(void*)pc ;<br/>
     cout&lt;&lt;pc&lt;&lt;endl;<br/>
     cout&lt;&lt;pb1&lt;&lt;endl;<br/>
     cout&lt;&lt;pb2&lt;&lt;endl;<br/>
     cout&lt;&lt;pb3&lt;&lt;endl;<br/><br/><font color="#0000ff">结果为：</font><br/><br/>
0012FF3C<br/>
0012FF40<br/>
0012FF40<br/>
0012FF3C<br/><br/>
可以发现 。<br/>
pb1 = pc + sizeof(ca)<br/>
pb2 = pc + sizeof(ca)<br/>
pb3 = pc<br/><br/>
由于cc是从ca和cb派生出来的，安排数据元素的时候，ca在cb之前。<br/>
所以得到了一个cc的指针之后（pc），<br/>
把他转换成cb的指针，自然后移一个ca的长度。<br/>
     cb *pb1 = pc ;<br/>
相当于隐式的static_cast。所以结果和<br/>
     cb *pb2 = static_cast&lt;cb*&gt;(pc);<br/>
是一样的。<br/>
这一点对有多重派生的类很重要。可见指针包含的信息很丰富：<br/><font color="#ff0000">1。地址。我们最初认识指针的时候，就知道<br/>
2。长度信息。比如int*一次前进4个字节，double*一次前进8个字节<br/>
3。类型的相对位置。就好比这里的cc中  cb放在ca之后 。=号赋值的时候引发相对移动。</font><br/>
（这点我一直没有关注到）<br/><br/>
而<br/>
cb *pb3 = (cb*)(void*)pc ;<br/>
用了void进行中转。于是编译器无法知道(void*)pc处放的是个cc。<br/>
只能机械地把地址给pb3。<br/><br/><font color="#0000ff">第二个实验：</font><br/><br/>
     float f = 1.2 ;<br/>
     float *pf = &amp;f ;<br/>
     int i = static_cast&lt;int&gt;(f);<br/>
    // i = f ;<br/>
     int *pi = reinterpret_cast&lt;int*&gt;(pf);<br/>
    // pi = (int*)pf ;<br/>
     cout&lt;&lt;i&lt;&lt;endl;<br/>
     cout&lt;&lt;*pi&lt;&lt;endl;<br/>
     cout&lt;&lt;*(float*)pi&lt;&lt;endl;<br/><br/><font color="#0000ff">结果：</font><br/><br/>
1<br/>
1067030938<br/>
1.2<br/><br/>
第一个i，经过转换后，把float变成了int<br/><br/>
int *pi = reinterpret_cast&lt;int*&gt;(pf);<br/>
这句如果用static_cast就编译不过。因为两种指针指向的东西就不一致。<br/>
但是可以使用reinterpret重新解释，强制转换这样一种指针。<br/>
输出*pi。可见是没有意义的。因为里面是按照float的标准存放的数据。<br/>
cout&lt;&lt;*(float*)pi&lt;&lt;endl;<br/>
这句又做个强制转换回float的指针，再dereference。于是可以输出pi所指内存的原本值。<br/><br/>
其中注释了两句话，如果用他们去替换对应的语句，结果也是一样的。<br/><br/>
所以，可以看出，“=”本身具有static_cast意思。<br/>
int     i = f ;这句是成功的<br/>
int* pi = pf ;这句是失败的<br/>
这里和static_cast是相应的。<br/><br/>
而强制指针类型转换，有reinterpret_cast的意思。<br/>
int* pi = (int*)pf ;<br/>
int *pi = reinterpret_cast&lt;int*&gt;(pf);<br/>
以上两句的功能是相同的。<br/><br/>
但同时强制指针类型转换，也有static_cast的意思。<br/>
cb *pb2 = reinterpret_cast&lt;cb*&gt;(pc); //0012FF3C<br/>
cb *pb2 = static_cast&lt;cb*&gt;(pc);//0012FF40<br/>
cb *pb3 = (cb*)pc ;//0012FF40
