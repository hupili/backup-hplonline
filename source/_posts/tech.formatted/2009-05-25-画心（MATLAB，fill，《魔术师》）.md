---
layout: post
title: "画心（MATLAB，fill，《魔术师》）"
date: 2009-05-25  13:56
comments: true
categories: tech
tags: ["Math"]
_baiduhi_id: 96aee1f871588107d8f9fd63.html
_baiduhi_category: Math
---

(hplonline)2009.5.25<br/><br/>
记得微积分的最后有个讲心形线的东西。<br/>
看了那个图，只能觉得，大致上算吧，总体上看去还是很别扭。<br/><br/>
今天看到用旋转的椭圆来拼成一个心，感觉很逼真。<br/><br/>
matlab的eaplot真的是很easy，表达式一上去就出来了。<br/><font color="#ff6600">ezplot('24*x*x-20*abs(x)*y+15*y*y=225') ;</font><br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/c0b2c6bfb8c8452e18d81f3c.jpg" small="0" class="blogimg"/><br/><br/>
貌似也没看到有啥好方法，据说还在百度知道上搜到这种“<a href="http://zhidao.baidu.com/question/52524620.html" target="_blank">不会</a>”为最佳答案的东西。。</div>
<br/>
瞟了一下，matlab里面有fill和fill3两个函数。<br/>
fill是对给出的点的序列描出的多边形画图。<br/>
于是就想把这个心上的点顺次生成，用fill画出来。<br/><br/>
因为表达式：24*x*x-20*abs(x)*y+15*y*y=225<br/>
的长相问题，在直角坐标下，很难找到一个办法来描述“顺次”这个意思。<br/><br/>
故转化到极坐标下。<br/>
当然，算出theta对应的r后，plot画图前还是得转回直角坐标来的。<br/><br/>
这里由于图像左右对称，所以theta只取[-0.5pi,0.5pi]。<br/>
把得到的点翻转一下就是了：<br/><br/><font color="#ff6600">theta = -pi/2:0.01:pi/2 ;<br/>
r = (225 ./ (24 .* cos(theta).^2 - 20 .* cos(theta).*sin(theta) + 15 .* sin(theta).^2 )) ;<br/>
x = r .* cos(theta) ;<br/>
y = r .* sin(theta) ;<br/>
fill([x -fliplr(x)] , [y fliplr(y)] , 'r') ;</font><br/><br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/f11493257878994435a80f3c.jpg" small="0" class="blogimg"/></div>
<br/>
不过有个问题，貌似和上面的函数式ezplot出来的轮廓不一样。<br/>
从某种意义上来说，这个图还是很像心的。但为啥不一样呢。。囧。。<br/><br/>
yhsa678同学用他那犀利的眼神发现了问题所在：<br/><font color="#ff0000">r = sqrt(225 ./ (24 .* cos(theta).^2 - 20 .* cos(theta).*sin(theta) + 15 .* sin(theta).^2 )) ;</font><br/>
就是推极坐标表达的时候搞忘对r开方了。<br/>
这下弄出来就是这个样子了。<br/><br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/b605c41b255f38deae51333c.jpg" small="0" class="blogimg"/></div>
<br/>
关于上面提到的fill要顺次连接的问题，可以改一点来观察。<br/><div forimg="1"><font color="#ff6600">theta = -pi/2:0.01:pi/2 ;<br/>
r = sqrt(225 ./ (24 .* cos(theta).^2 - 20 .* cos(theta).*sin(theta) + 15 .* sin(theta).^2 )) ;<br/>
x = r .* cos(theta) ;<br/>
y = r .* sin(theta) ;<br/>
%fill([x -fliplr(x)] , [y fliplr(y)] , 'r') ;</font><br/><font color="#ff0000">fill([x -x] , [y y] , 'r') ;</font></div>
<div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/450d3cd183677c1c9a50273c.jpg" small="0" class="blogimg"/></div>
<div forimg="1"><br/>
这两句：</div>
<div forimg="1">fill([x -fliplr(x)] , [y fliplr(y)] , 'r') ;<br/>
fill([x -x] , [y y] , 'r') ;</div>
<div forimg="1"><br/>
区别就在第一个先把相关序列翻转了，画出来的就没有中间的黑线。<br/>
第二个的话，fill从最下面延逆时针画到上方x=0处，<br/>
然后瞬间跑到最下方，延顺时针画，这就导致图形有问题。<br/><br/>
所以<font color="#ff0000">fill对点的顺次连接有要求</font></div>
<br/>
不知道那个24*x*x-20*abs(x)*y+15*y*y=225的式子是哪来的。。<br/><br/>
想了一下，可以看成是一个椭圆，先做旋转，然后取正半截，再翻转。见下图：<br/><br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/6a1e00d12d9037f7562c843c.jpg" small="0" class="blogimg"/></div>
<br/>
关于向量的旋转，可以参考：<a href="http://www.box.net/shared/casqylxr01" target="_blank">向量的旋转</a><br/><br/>
这样的话，就可以改变长轴a，短轴b，和转角phi来完成各种参数的心形。<br/><br/><font color="#ff6600"><font color="#ff0000">a = 3 ;<br/>
b = 3 ;<br/>
phi = 20 * pi / 180 ;</font><br/>
rotate = [cos(phi) -sin(phi) ; sin(phi) -cos(phi)] ;%旋转矩阵<br/>
theta = -pi:0.01:pi ;<br/>
x0 = a * cos(theta) ;<br/>
y0 = b * sin(theta) ;%标准椭圆的点序列<br/>
pt = rotate * [x0 ; y0] ;<br/>
x1 = pt(1,:) ;<br/>
y1 = pt(2,:) ;%旋转后的序列<br/>
pos = ( x1 &gt;= 0 ) ;<br/>
x = x1(pos) ;<br/>
y = y1(pos) ;%提取正半截<br/>
axis equal<br/>
hold on<br/>
fill([x -fliplr(x)] , [y fliplr(y)] , 'r') ;%翻转加绘图<br/>
plot(x0,y0,x1,y1) ;%打印出参考线</font><br/><br/>
那这个旋转椭圆画心又是怎么想到的呢。。<br/>
我也不知道，不过电影《魔术师》里面有类似的情节：<br/><br/>
（男主送给女主的礼物）<br/><br/>
1.看起来虽然不是很椭圆，也有那个意思<br/><div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/c8d9c295c489686fd0135ebc.jpg" small="0" class="blogimg"/><br/><br/>
2.好家伙，可以掰开的。。</div>
<div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/0ba65b0fa133120e6159f3bd.jpg" small="0" class="blogimg"/><br/><br/>
3.哇，转一圈过来是个心哦。。</div>
<div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/04243cd351f373243bf3cfbd.jpg" small="0" class="blogimg"/><br/><br/>
4.还可以这样。。。<img src="http://img.baidu.com/hi/jx/j_0016.gif"/>。。？？</div>
<div forimg="1"><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/42a9f1f23cdb5637b17ec5bd.jpg" small="0" class="blogimg"/></div>
<br/>
