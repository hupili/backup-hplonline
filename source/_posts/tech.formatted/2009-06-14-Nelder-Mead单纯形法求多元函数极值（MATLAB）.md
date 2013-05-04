---
layout: post
title: "Nelder-Mead单纯形法求多元函数极值（MATLAB）"
date: 2009-06-14  19:34
comments: true
categories: tech
tags: ["Math"]
_baiduhi_id: a2f3e1c45fa147a08326acbc.html
_baiduhi_category: Math
---

(hplonline)2009.6.14<br/><br/><font color="#0000ff">简介：</font><br/><br/>
n维空间中，由n+1个顶点，可以组成“最简单”的图形，叫单纯形。<br/>
NM法就是先构造一个初始的，包含给定点的单纯形。<br/>
然后使用可能的三种手段（<font color="#ff0000">反射，扩展，压缩</font>）去替换函数值最差的顶点。<br/>
在以上三种手段失效的时候，使用<font color="#ff0000">收缩</font>。<br/>
直到该单纯形的半径足够的小。<br/>
（半径的定义可以有很多，比如两两点的距离，<br/>
两两点构成的向量中最大的维度的值，<br/>
只要当“半径”趋于0的时候，该单纯形趋于一个点即可）<br/><br/><font color="#0000ff">相关资料：</font><br/><br/><a href="http://www.box.net/shared/14o1dy0f5d" target="_blank">NelderMeadProof.pdf</a><br/>
这篇文章讲解比较详细。<br/>
虽然只提到二维的情况，不过可以推广到n维。<br/>
主要通过上面的几个图例，知道四种手段即可：<br/><font color="#ff0000">反射(reflection)，扩展(expasion)，压缩(contraction)，</font><font color="#ff0000">收缩(shrink)</font><br/><br/>
看懂了这四个基本手段后，就不用去搜其他资料了。<br/>
感觉网上很多写得十分别扭。<br/>
最好的方法就是直接找matlab里面的fminsearch函数。<br/>
写得漂亮而且通用。<br/>
这套代码里面，允许对以上四种操作的尺寸做定制。<br/>
（比如一般的文献讲的扩展是从反射点再走一倍反射点到中心的距离，<br/>
这个距离在fminsearch里面可以手工定制：<br/>
% Initialize parameters<br/>
rho = 1;<font color="#ff0000"> chi = 2;</font> psi = 0.5; sigma = 0.5;<br/>
同理还可以改变其他几个代码)<br/><font color="#0000ff"><br/>
单纯形变换流程：</font><br/><br/>
看流程之前，先确保一提到上面四个操作，就能反映出相关的点之间的关系。<br/><br/>
最好点：best<br/>
次差点：soso<br/>
最差点：worst<br/>
反射点：r<br/>
扩展点：e<br/>
内压缩点：c1(center和worst之间）<br/>
外压缩点：c2(center和r之间）<br/><br/>
1。如果反射点值小于best，那么考虑扩展点e，选r和e中小者去替换worst<br/>
2。如果反射点值小于soso，用r如替换worst<br/>
3。非以上两种情况，考虑压缩点<br/>
3.1。worst比r小，那么考虑c1，如果c1比worst小，选c1替换，否则考虑收缩<br/>
3.2。r比worst小，那么考虑c2，如果c2比r小，选c2替换，否则考虑收缩<br/>
4。如果在第3步中确定需要收缩，那么将所有点向best方向按比例收缩<br/><br/>
剩下的内容代码里面比较详细了。<br/><br/><font color="#0000ff">代码：</font><br/><br/>
下面这个就是看了matlab实现的fminsearch之后，稍加改写的一个版本。<br/>
去掉了一些通用性的定制变量，一些繁琐的参数判断，尽量写了详细的注释。<br/><br/>
function [x , fval , flag] = nm_min(fun , x0 , max_time , eps)<br/>
%realization of Nelder-Mead Simplex<br/>
%[x fval flag] = nm_min(f , x0 , max_time , eps)<br/>
%max_time:最大迭代次数，默认10000<br/>
%eps:精度，默认1e-5<br/><br/>
%参数检查<br/>
if nargin &lt; 2, <br/>
       error('请至少传入函数和初始点'); <br/>
end<br/><br/>
%默认值设置<br/>
if nargin &lt; 3<br/>
        max_time = 10000 ;<br/>
end<br/>
if nargin &lt; 4<br/>
        eps = 1e-5 ;        <br/>
end<br/><br/>
n = length(x0) ;%变量个数<br/>
x0 = x0(:) ;%把x0变成列向量<br/><br/>
%vx是单纯形矩阵，n行n+1列<br/>
%即n维空间中的n+1个点<br/>
vx = x0 ;<br/>
%vf是函数值，对应每个列向量<br/>
vf = feval(fun , x0) ;<br/><br/>
%构造初始单纯形<br/>
%分别对每个维度按一定比例扩张，以形成一个高维体<br/>
for i = 1:n         <br/>
        x = x0 ;<br/>
        if abs(x(i)) &lt; eps<br/>
            x(i) = x(i) + 0.005 ;%该维度上为0时，人工指定加上一定值<br/>
        else<br/>
            x(i) = x(i) * 1.05 ;<br/>
        end<br/>
        vx = [vx , x] ;<br/>
        vf = [vf , feval(fun , x)] ;<br/>
end<br/><br/>
%排序，做迭代准备<br/>
[vf index] = sort(vf) ;<br/>
vx = vx(:,index) ;<br/><br/>
%开始迭代<br/>
while max_time &gt; 0 <br/>
        %各个点在各维度上的差值足够小<br/>
        if max(max(abs(vx(:,2:n+1)-vx(:,1:n)))) &lt; eps <br/>
            break<br/>
        end<br/>
        %三个考察点，最优，次差，最差<br/>
        best = vx(: , 1) ;<br/>
        fbest = vf(1) ;<br/>
        soso = vx(: , n) ;<br/>
        fsoso = vf(n) ;<br/>
        worst = vx(: , n+1) ;<br/>
        fworst = vf(n+1) ;            <br/>
        center = sum(vx(: , 1:n) , 2) ./ n ;<br/>
        r = 2 * center - worst ;%反射点<br/>
        fr = feval(fun , r) ;<br/>
        if fr &lt; fbest<br/>
            %比最好的结果还好，说明方向正确，考察扩展点，以期望更多的下降<br/>
            e = 2 * r - center ; %扩展点<br/>
            fe = feval(fun , e) ;<br/>
            %在扩展点和反射点中选择较优者去替换最差点<br/>
            if fe &lt; fr<br/>
                vx(: , n+1) = e ;<br/>
                f(: , n+1) = fe ;<br/>
            else<br/>
                vx(: , n+1) = r ;<br/>
                vf(: , n+1) = fr ;<br/>
            end<br/>
        else<br/>
            if fr &lt; fsoso<br/>
                %比次差结果好，能够改进<br/>
                vx(: , n+1) = r ;<br/>
                vf(: , n+1) = fr ;                <br/>
            else<br/>
                %比次差结果坏，应该考察压缩点<br/>
                %当压缩点无法得到更优值的时候，考虑收缩<br/>
                shrink = 0 ;<br/>
                if fr &lt; fworst<br/>
                    %由于r点更优所以<br/>
                    %向r点的方向找压缩点 <br/>
                    c = ( r + center ) ./ 2 ;<br/>
                    fc = feval(fun , c) ;<br/>
                    if fc &lt; fr<br/>
                        %确定从r压缩向c可以改进 <br/>
                        vx(: , n+1) = c ;<br/>
                        vf(: , n+1) = fc ;<br/>
                    else<br/>
                        %否则的话，准备进行收缩<br/>
                        shrink = true ;<br/>
                    end<br/>
                else<br/>
                    c = (worst + center) ./ 2 ;<br/>
                    fc = feval(fun , c) ;<br/>
                    if fc &lt; fr<br/>
                        %确定从r压缩向c可以改进 <br/><font color="#ff0000">%（2009.7.22标注，这里应该是搞错了，回去再认真看一下）</font><br/>
                        vx(: , n+1) = c ;<br/>
                        vf(: , n+1) = fc ;<br/>
                    else<br/>
                        %否则的话，准备进行收缩<br/>
                        shrink = 1 ;<br/>
                    end                    <br/>
                end%fr &lt; fworst<br/>
                if shrink<br/>
                    %压缩点并非更优，考虑所有点向best收缩<br/>
                    for i = 2:n+1<br/>
                        vx(: , i) = ( vx(i) + best ) ./ 2 ;<br/>
                        vf(: , i) = feval(fun , vx(: , i)) ;<br/>
                    end<br/>
                end%shrink<br/>
            end%fr &lt; fsoso<br/>
        end%fr &lt; fbest<br/>
        [vf index] = sort(vf) ;<br/>
        vx = vx(:,index) ;        <br/>
        max_time = max_time - 1 ;<br/>
end%while max_time &gt; 0 <br/><br/>
x = vx(: , 1) ;<br/>
fval = vf(: , 1);<br/><br/>
if max_time &gt; 0<br/>
        flag = 1 ;<br/>
else <br/>
        flag = 0 ;<br/>
end<br/><font color="#0000ff"><br/>
示例：</font><br/><br/>
f = inline('x(1).^2+(x(2)-2).^2')<br/>
[x fval flag] = nm_min(f , [0;0])<br/><br/>
x =<br/>
           0<br/>
      2.0000<br/>
fval =<br/>
8.0779e-028<br/>
flag =<br/>
       1<br/><br/>
flag=1表示找到解，[0;2.0000]，相应的函数值为8.0779e-028(即0）<br/>
和解析计算吻合。<br/><br/><font color="#0000ff">图形化演示：</font><br/><br/>
对于上面的示例，修改一下程序，画出先10次迭代的轨迹如下：<br/><br/><div forimg="1"><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/2210888b1e1140f6fc1f107b.jpg"/></div>
此方法的精髓在于不断向最优点进发。<br/>
而在最优点附近的时候，围绕最优点旋转，并不断收缩，<br/>
直到所掌握的单纯形近似收缩到一个点为止。<br/><br/><font color="#0000ff">关于matlab的一点事：</font><br/><br/>
在看fminsearch时才发现<br/>
x(:)这个表达式，无论x是列向量还是行向量，都会返回列向量<br/><br/>
维度的指定相当重要 。<br/>
%排序，做迭代准备<br/>
[vf index] = sort(vf) ;<br/>
vx =<font color="#ff0000"> vx(:,index) ;</font><br/><br/>
最初写的是vx = vx(index)<br/>
直接导致vx中不是按照列提取的结果。。。<br/><br/>
还有<br/>
max(max(abs(vx(:,2:n+1)-vx(:,1:n))))<br/><font color="#ff0000">vx(:,2:n+1)</font>里面的冒号开始也写掉了。<br/>
当达到极值的时候，反而搞得分量间可能相差较大。<br/>
所以每次都跑慢max_time。。。
