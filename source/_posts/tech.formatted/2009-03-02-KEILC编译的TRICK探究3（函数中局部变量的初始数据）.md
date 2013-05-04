---
layout: post
title: "KEIL C 编译的TRICK探究3（函数中局部变量的初始数据）"
date: 2009-03-02  17:27
comments: true
categories: tech
tags: ["Scm"]
_baiduhi_id: cb5e40edd67c8cdcb21cb166.html
_baiduhi_category: Scm
---

毕竟单片机平台与我们PC有很大的不同，<br/><br/>
比较突出的就是，我们的PC上跑的程序，<br/>
代码和数据都是在RAM里面，从物理上来说是一起的，<br/>
所以，很多东西实现起来可以比较随意。<br/>
比如<br/>
void main(){<br/>
       uchar a[] = {1,2,3,4};<br/>
       ....<br/>
}<br/>
就可以用DB 把a[]直接放在代码段里面。然后用到的时候直接引就可以了。<br/><br/>
但是单片机的代码是放在ROM里面的，通常有一个内部256B的RAM，来存放临时数据，<br/>
当然还可以外挂比较大的64K RAM。<br/>
从指令上就可以看出是很有区别的：<br/><font color="#ff6600">rom: movc ...<br/>
内部ram:mov...<br/>
外部ram:movx</font>...<br/><br/>
那么，像上面那样一个函数，a[]的数据应该放在哪呢？<br/><br/><font color="#0000ff">实验程序：</font><br/>
#include &lt;reg51.h&gt;<br/>
typedef unsigned char uchar ;<br/>
uchar table1[]={1,2,3,4,5};<br/>
void main(){<br/>
      uchar table2[] = {6,7,8,9,10};<br/>
      uchar i,j;<br/>
      P1 = 1 ;<br/>
      j = P1 ;<br/>
      i = table1[j];<br/>
      P2 = i ;<br/>
      i = table2[j];<br/>
      P3 = i ;<br/>
      while (1) ;<br/>
}<br/><br/>
至于代码为啥要这样写，是经过多次尝试的，因为KEIL也会优化。<br/>
如果太简单的话，比如只有i=table[0]，<br/>
你可能看到的就只有mov R7 , 1这样一句话。。<br/><br/>
虽然从执行上来说没有区别，对我们的普遍性分析造成了障碍。<br/><br/><font color="#ff0000">而一般的原则是，尽可能用到P0..P3这些东西，<br/>
因为这些东西的值是编译期无法确定的，所以KEIL只有老实点了，哈哈</font><br/><br/>
那么先看上面这个程序的汇编情况：<br/><br/>
C:0x0982      780D       MOV        R0,#0x0D<br/>
C:0x0984      7C00       MOV        R4,#0x00<br/>
C:0x0986      7D00       MOV        R5,#0x00<br/>
C:0x0988      7BFF       MOV        R3,#0xFF<br/>
C:0x098A      7A09       MOV        R2,#0x09<br/>
C:0x098C      79B2       MOV        R1,#0xB2<br/>
C:0x098E      7E00       MOV        R6,#0x00<br/>
C:0x0990      7F05       MOV        R7,#0x05<br/><font color="#ff0000">C:0x0992      1208D0     LCALL      C?COPY(C:08D0)</font><br/>
      10:           P1 = 1 ; <br/>
C:0x0995      759001     MOV        P1(0x90),#0x01<br/>
      11:           j = P1 ; <br/>
C:0x0998      AF90       MOV        R7,P1(0x90)<br/>
      12:           i = table1[j]; <br/>
C:0x099A      7408       MOV        A,#table1(0x08)<br/>
C:0x099C      2F         ADD        A,R7<br/>
C:0x099D      F8         MOV        R0,A<br/>
C:0x099E      E6         MOV        A,@R0<br/>
      13:           P2 = i ; <br/>
C:0x099F      F5A0       MOV        PPAGE_SFR(0xA0),A<br/>
      14:           i = table2[j]; <br/>
C:0x09A1      740D       MOV        A,#0x0D<br/>
C:0x09A3      2F         ADD        A,R7<br/>
C:0x09A4      F8         MOV        R0,A<br/>
C:0x09A5      E6         MOV        A,@R0<br/>
      15:           P3 = i ; <br/>
C:0x09A6      F5B0       MOV        P3(0xB0),A<br/>
      16:           while (1) ; <br/>
C:0x09A8      80FE       SJMP       C:09A8<br/><br/>
KEIL已经分割好了，很容易找到对应C的汇编<br/><br/>
可以看出R7就是我们的j，<br/>
C:0x099A      7408       MOV        A,#table1(0x08)<br/>
C:0x099C      2F         ADD        A,R7<br/>
C:0x099D      F8         MOV        R0,A<br/>
C:0x099E      E6         MOV        A,@R0<br/>
这里就是用哦个table的始地址加上j，放到R0里面供寻址用。<br/><br/>
可以看到table1 的地址是0x08<br/>
同理，table2的地址是0x0d<br/><br/><font color="#ff0000">他们都是用的MOV ，所以数据是放在内部RAM里面的！</font><br/><br/>
这里有一个原则性的东西，<font color="#ff6600">我们写的程序全部在ROM里面，<br/>
包括指定的这些初始数据，那么他们一定在某个时候跑到了RAM里面。</font><br/><br/>
本来准备了table1和table2的，但是时间不够，这次就先分析table2的形成。<br/><br/>
进去KEIL的反汇编，停下来的时候，可以看到，<br/>
table1对应的位置已经有值了，而table2对应的地方还是空的<br/><br/>
然后单步，当执行了：<br/>
C:0x0992      1208D0     LCALL      C?COPY(C:08D0)<br/>
的时候，可以看到，table2对应的地方就有值了。<br/><br/>
嗯，顺带提一句，免得下回我也忘了，就是查内存。<br/>
view -&gt; memory window<br/>
在地址框填写：  <br/>
C:0000     ;查看     CODE     区  <br/>
D:0000     ;查看     DATA     区  <br/>
I:0000    ;查看     IDATA     区  <br/>
X:0000     ;查看     XDATA     区<br/>
这里我们查看的是DATA区<br/><br/>
从C?COPY这个名字，也就能想到他的功能了。<br/><br/>
那么我们的数据其实还是放在ROM里面，运行时copy到RAM里的。<br/>
从我们开始的main函数的代码往下拉<br/><br/>
C:0x09B2      06         INC        @R0<br/>
C:0x09B3      07         INC        @R1<br/>
C:0x09B4      08         INC        R0<br/>
C:0x09B5      09         INC        R1<br/>
C:0x09B6      0A         INC        R2<br/><br/>
这一串看起来就很熟悉了。。不用看后面的指令，实际上就是我们的6,7,8,9,10<br/><br/>
然后回去改一下，比如7,7,7,7,7。。可以看到这里跟着改了，那就没错了。<br/><br/>
不过在调用COPY前，有一大堆东西看起来很迥异，<br/>
也不用急。。比如，现在让我写一个COPY函数，应该怎么写呢？<br/><br/><font color="#ff6600">显然，你要告诉我的COPY函数，从哪开始COPY，要COPY多少字节，等等。</font><br/><br/>
在PC上，一般是push XXX 来传递，这里没有，可见一定是通过前面的寄存器来传递的。<br/><br/><font color="#ff6600">比较容易看到R2R1，组合成的16位地址刚好是我们刚才找到的<br/>
ROM里面存放6,7,8,9,10的地方。<br/><br/>
R7里面的值（5）正好是数据的个数。</font><br/><br/>
不过这是猜测，那么就验证他。<br/>
我们不用跟进COPY函数，那样太麻烦，看得比较不爽。<br/><br/>
直接改数组就行了，比如增加数据个数，看到R7对应增长。<br/><br/>
然后增加代码数量，看到R2R1始终是数据位置的地址。<br/><br/>
至于其他几个寄存器呢？因为我改的过程中没有发现变化，<br/>
所以也不知道有什么用，<br/><br/>
而且这东西在网上搜老半天也没看谁说。。。<br/>
看来大家都不屑于研究这些东西，呵呵。<br/><br/>
下次研究一下全局变量的初始化。
