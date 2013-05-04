---
layout: post
title: "格式化输入输出浮点数据的细微问题（C标准：printf,scanf)"
date: 2009-02-15  15:24
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: c0e3b9de2e24355fcdbf1afc.html
_baiduhi_category: c&c++
---

(hplonline)2009.2.15<br/><br/>
刚开始学C语言的时候，看到用<font color="#ff6600">scanf</font>输入浮点数据的对应字符串如下：<br/><font color="#ff0000">float : %f<br/>
double : %lf</font><br/>
而<font color="#ff6600">printf</font>输出的时候却都是统一的：<br/><font color="#ff0000">float / double : %f</font><br/><br/>
你也许曾经跟我一样，用%lf输出过double，<br/>
结果是正常的，因为%lf直接被当作了%f了。<br/><br/>
但是这时候问题就来了，<br/><font color="#ff0000">问题1.</font>C语言也算是强类型的语言，两种不同类型怎么能统一到同一种输出上呢？<br/><font color="#ff0000">问题2.</font>既然输出都可以统一，为什么输入必须用两种不同的格式串呢?<br/><br/><font color="#ff6600">实验一：确定以上结论</font><br/>
int main(){<br/>
          double d;<br/>
          scanf("%f",&amp;d);<br/>
          printf("%f\n",d);<br/>
          scanf("%lf",&amp;d);<br/>
          printf("%f\n",d);<br/>
          return 0 ;<br/>
}<br/>
两次都输入1，<br/>
我电脑上的输出为：<br/>
-92559604281615349000000000000000000000000000000000000000000000.000000<br/>
1.000000<br/><br/>
可见用%f输入double型是不正确的，还有很多类似实验，就不一一列举了。<br/>
输入两种格式*输出两种格式*两种类型变量 = 8 组 。<br/><br/><font color="#ff6600">实验二：规范的输入输出，以及汇编分析</font><br/>
int main(){<br/>
          float f;<br/>
          double d;<br/>
          scanf("%f",&amp;f);<br/>
          scanf("%lf",&amp;d);<br/>
          printf("%f\n",f);<br/>
          printf("%f\n",d);<br/>
          return 0 ;<br/>
}<br/><br/>
这个实验的写法是符合标准的，两次输入1，能够输出正确的结果。<br/>
现在要解决的就是提出的两个问题。<br/>
我把汇编代码放在最后。这里挑关键说明一下。<br/>
截取部分就是四个函数的调用，四块大致上是长这样：<br/><font color="#0000ff">push ...<br/>
push ...<br/>
call ...<br/>
add esp , ?</font><br/>
（关于C调用约定，查一下就清楚了）<br/>
第二个push的是格式字符串的地址，<br/>
所以我们关心的在于第一个push，那里进去的是我们的变量<br/><br/>
第一个：<br/><font color="#0000ff">lea           eax, dword ptr [ebp-4]<br/>
push          eax</font><br/>
先获取变量的有效地址，然后直接push<br/>
第二个：<br/><font color="#0000ff">lea           ecx, dword ptr [ebp-C]<br/>
push          ecx</font><br/>
除了地址外，其他和第一个一样。<br/><br/><font color="#ff0000">既然传给scanf 的都是变量的地址，我们当然就要用不同的格式字符串来区分了。</font><br/><br/>
第四个：先看第四个因为它更简单<br/><font color="#0000ff">mov          edx, dword ptr [ebp-8]<br/>
push         edx<br/>
mov          eax, dword ptr [ebp-C]<br/>
push         eax</font><br/>
ebp-C就是我们d变量的地址，<br/>
这里先让高双字[ebp - 8]入栈，<br/>
然后再是低双字[ebp - C]。<br/>
这些是由平台的字节顺序规定的，我的机器是<font color="#ff0000">小尾顺序</font>，<br/>
而esp的增长方向是向下的，所以这样 push进去的东西依然是小尾的。<br/><br/>
第三个：很猫腻的就在这里了<br/><font color="#0000ff">fld          dword ptr [ebp-4]<br/>
sub          esp, 8<br/>
fstp         qword ptr [esp]</font><br/>
[ebp - 4]是我们的变量f。<br/>
第一条指令，f入浮点栈<br/>
第二条指令，把esp减掉8，相当于在栈顶“腾"出了8字节的空间<br/>
第三条指令，从浮点栈弹出一个数到指定内存。<br/>
后面的esp由 qword修饰 ， 即8字节。<br/><br/><font color="#ff0000">简要的说 ，就是利用机器本身的浮点指令完成了<br/>
从float到double型的转换<br/>
而我们传给printf的始终是一个double型。</font><br/><br/><font color="#ff0000">既然我们传给函数的都是同一种类型，当然没必要区分格式字符串了！</font><br/><br/>
至此，前面提出的两个问题算是有了一个说法。<br/><br/><font color="#ff0000">问题3：</font><br/>
也许你也跟我一样，想到了既然传给scanf的都是一个地址，<br/>
那我们给了一个double的地址，用了%f输入，<br/>
但是机器不知道那是double的地址啊！一定会正确的输入一个浮点数的！<br/>
就像下面这样<br/>
        double d;<br/>
        scanf("%f",&amp;d);<br/>
那么输出呢？<br/><br/><font color="#ff6600">实验三：</font><br/>
int main(){<br/>
        double d;<br/>
        scanf("%f",&amp;d);<br/>
        printf("%f\n",d);<br/>
        printf("%f\n",float(d));<br/>
        printf("%f\n",*(float*)&amp;d);<br/>
        return 0 ;<br/>
}<br/><br/>
在我电脑上的输出为：<br/>
-92559604281615349000000000000000000000000000000000000000000000.000000<br/>
-92559604281615349000000000000000000000000000000000000000000000.000000<br/>
1.000000<br/><br/>
第一个只是说明这样输出是错的。<br/>
也许有人会说，既然正确输入了一个float，那么我来个强制转换吧。<br/>
这就是第二个结果，其实也是错的。<br/>
因为float(d)将产生double -&gt; float 的类型转换。<br/>
是按值转换，所以还是和上面一样的一个东西。<br/>
那第三个呢？从结果看，显然是对的。<br/>
这句话比较绕口，从右向左看：<br/>
先取了d的地址，这里是double*的类型，<br/>
然后指针类型转换，这里就是float*的类型了，<br/>
最后脱指针引用，得到的就是一个float类型。<br/><br/>
呵呵，这个玩得稍微大了一点。<br/><font color="#ff0000">只是想说明，虽然用scanf 和printf的格式串有细微的规定，<br/>
但并不是一种八股，只要知道原理怎么来都行。</font><br/><br/>
有兴趣可以试下用%lf输入float，再输出也是可以的。<br/>
不过注意，假设你输入输出用的是变量f，要这样：<br/>
int main(){<br/>
        float fspace;<br/>
        float f;<br/>
       。。。<br/>
试试把fspace去掉，即把float f放在main的第一行会出现什么！<br/>
有意思吧。。。<br/><br/>
========================实验二的汇编代码：<br/>
scanf("%f",&amp;f);<br/>
00412BA8            8D45 FC             lea           eax, dword ptr [ebp-4]<br/>
00412BAB            50                  push          eax<br/>
00412BAC            68 2C614200         push          0042612C                               ;  ASCII "%f"<br/>
00412BB1            E8 7AFFFFFF         call          scanf<br/>
00412BB6            83C4 08             add           esp, 8<br/><br/>
scanf("%lf",&amp;d);<br/>
00412BB9            8D4D F4             lea           ecx, dword ptr [ebp-C]<br/>
00412BBC            51                  push          ecx<br/>
00412BBD            68 1C604200         push          0042601C                               ;  ASCII "%lf"<br/>
00412BC2            E8 69FFFFFF         call          scanf<br/>
00412BC7            83C4 08             add           esp, 8<br/><br/>
printf("%f\n",f);<br/>
00412BCA            D945 FC             fld           dword ptr [ebp-4]<br/>
00412BCD            83EC 08             sub           esp, 8<br/>
00412BD0            DD1C24              fstp          qword ptr [esp]<br/>
00412BD3            68 08704200         push          00427008                               ;  ASCII "%f",LF<br/>
00412BD8            E8 93E4FEFF         call          printf<br/>
00412BDD            83C4 0C             add           esp, 0C<br/><br/>
printf("%f\n",d);<br/>
00412BE0            8B55 F8             mov           edx, dword ptr [ebp-8]<br/>
00412BE3            52                  push          edx<br/>
00412BE4            8B45 F4             mov           eax, dword ptr [ebp-C]<br/>
00412BE7            50                  push          eax<br/>
00412BE8            68 08704200         push          00427008                               ;  ASCII "%f",LF<br/>
00412BED            E8 7EE4FEFF         call          printf<br/>
00412BF2            83C4 0C             add           esp, 0C<br/><br/>
===============================
