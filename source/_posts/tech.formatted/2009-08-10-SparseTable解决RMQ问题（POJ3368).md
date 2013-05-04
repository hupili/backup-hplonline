---
layout: post
title: "Sparse Table解决RMQ问题（POJ3368)"
date: 2009-08-10  15:36
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: e3395d2c61c50ee58b13996a.html
_baiduhi_category: 算法
---

(hplonline)2009.8.10<br/><br/>
解决RMQ问题的方法还是相当多的。<br/>
今天终于尝试了一下Sparse Table。<br/>
这是一个时间上：<br/>
预处理n*log(n)，查询O(1)<br/>
空间上：<br/>
n*log(n)的方法。<br/><br/><font color="#0000ff">Sparse Table：</font><br/><br/>
用A[]来记原序列，用 M[i][j]来表示：<br/>
A[i] 到 A[i + 2^j - 1]这一段的最小值<font color="#ff0000">的下标</font>。<br/><br/>
有一个图示如下：<br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/01d259435bc100389213c623.jpg" small="0" class="blogimg"/></span><br/>
来自：<a href="http://www.topcoder.com/tc?module=Static&amp;d1=tutorials&amp;d2=lowestCommonAncestor#Sparse_Table_(ST)_algorithm" target="_blank">tc的这篇</a><br/><br/>
该数组的尺寸为M[max_n][max_logn]<br/>
max_logn=floor(log2(max_n))<br/><br/>
所以空间复杂度是显而易见的。<br/>
而对该数组的每个元素，能在O(1)的时间计算出来的话，<br/>
那么时间复杂度也就等同了。<br/>
O(nlogn)<br/><br/><font color="#0000ff">Sparse Table的计算：</font><br/><br/>
首先，含单个元素的区域最小值就是他本身：<br/>
M[i][0] = i ; <br/>
其他的值，按照j递增的顺序计算：<br/>
M[i][j] = index of max{ M[i][j - 1] , M[i + 2^(j-1)][j] }<br/><br/>
相当于是个区间长度倍增的过程。<br/>
每一层合并了两个较短区间的最值记录。<br/><br/><font color="#0000ff">Sparse Table的查询：</font><br/><br/>
对于查询rmq[i,j]<br/>
把该区间分成两段：<br/>
[i , i + 2^k - 1]和[j - 2^k + 1 , j]<br/>
则可以导出：<br/>
rmq[i,j] = max{ M[i][k] , M[j-2^k+1][k] }<br/><br/>
然后就是要确定k值。标准就是使得分成的两个区间能覆盖原来的区间[i,j]即可。<br/>
于是 j - 2^k + 1 &lt;= i + 2 ^k - 1 + 1<br/>
最终：k&gt;=log2(j-i+1)-1<br/><br/><font color="#0000ff">POJ3368：</font><br/><br/>
有了上面这个数据结构，刷这个题就先转化一下就行了。<br/><br/>
由于数据是有序的，<br/>
那么在读入的过程中就可以统计出一个频率来。<br/><br/>
比如：<br/>
-1 -1 1 1 1 1 3 10 10 10<br/>
统计为freq[]：<br/>
2 4 1 3<br/><br/>
要记录的信息是，这个数字的频率freq[]，左端left[]，右端right[]，<br/>
由于预处理后，数字本身是多少并不关心，所以其实可以不用记录数字num[]。<br/><br/>
给出统计[a,b]之间的频率后。<br/>
先要得到a,b对应的数字在freq[]里面的位置l,r。<br/>
可以用二分来完成。<br/><br/>
于是最终要输出的结果是<br/>
max{<br/>
right[l] - a + 1 ,<br/>
rmq(l+1 , r-1) ,<br/>
b - left[r] + 1,<br/>
}<br/><br/>
当然，对于l和r的差值要讨论相等，刚好等于1，以及其他这三种情况。<br/><br/><font color="#0000ff">POJ3368代码：</font><br/><font color="#ff0000"><br/>
关于排版，只能深表遗憾。<br/>
其实是有缩进的，粘上来就成这样了。<br/>
可以在VC中用全选，alt+f8解决。</font><br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;string.h&gt;<br/>
#include &lt;math.h&gt;<br/><br/>
const int MAXN = 100010 ;<br/>
const int MAXLOGN = 17 ;<br/><br/>
int num[MAXN] , left[MAXN] , right[MAXN] , freq[MAXN] ;<br/>
int rmq[MAXN][MAXLOGN] ;<br/>
int power2[MAXLOGN + 1] ;<br/>
int total ; <br/><br/>
void init(){<br/>
int i ;<br/>
power2[0] = 1 ;<br/>
for ( i = 1 ; i &lt;= MAXLOGN ; i ++ ){<br/>
power2[i] = power2[i - 1] * 2 ;<br/>
}<br/>
}<br/><br/>
int max_rmq(int i , int j){<br/>
if ( freq[i] &gt; freq[j] ) return i ;<br/>
else return j ;<br/>
}<br/><br/>
void init_st(){<br/>
int i , j ;<br/>
for ( i = 1 ; i &lt;= total ; i ++ ){<br/>
rmq[i][0] = i ;<br/>
}<br/>
int max_log2 = int (log(double(total)) / log(double(2))) ;<br/>
for ( j = 1 ; j &lt;= max_log2 ; j ++ ){<br/>
for ( i = 1 ; i &lt;= total ; i ++ ){<br/>
rmq[i][j] = max_rmq(rmq[i][j - 1] , rmq[i + power2[j-1]][j - 1]) ;<br/>
}<br/>
}<br/>
}<br/><br/>
int rmq_st(int i , int j){<br/>
int loglen = int(log(double(j - i + 1)) / log(double(2))) ;<br/>
return max_rmq(rmq[i][loglen] , rmq[j - power2[loglen] + 1][loglen]) ;<br/>
}<br/><br/>
int search(int x){<br/>
int l = 1 ;<br/>
int r = total + 1 ;<br/>
while ( l &lt; r ){<br/>
int mid = (l + r) / 2 ;<br/>
if ( x &gt; right[mid] ) l = mid + 1 ;<br/>
else r = mid ;<br/>
}<br/>
return l ;<br/>
}<br/><br/>
int max(int a , int b){<br/>
return a &gt; b ? a : b ;<br/>
}<br/><br/>
int max_freq(int a , int b){<br/>
int l = search(a) ;<br/>
int r = search(b) ;<br/><br/>
if ( l == r ){//same block<br/>
return b - a + 1 ;<br/>
}<br/><br/>
int t ;<br/>
if ( r - l &gt; 1 ){<br/>
t = freq[rmq_st(l + 1 , r - 1)];<br/>
}else t = -1 ;<br/><br/>
t = max(t , right[l] - a + 1) ;<br/>
t = max(t , b - left[r] + 1) ;<br/><br/>
return t ;<br/>
}<br/><br/>
int main(){<br/>
int n , q ;<br/>
int i ;<br/>
int curleft , curnum , tmp , count ;<br/>
init() ;<br/>
while ( 1 ){<br/>
scanf("%d" , &amp;n) ;<br/>
if ( n == 0 ) break ;<br/>
scanf("%d" , &amp;q) ;<br/>
total = 0 ;<br/>
curnum = 10000000 ; <br/>
for ( i = 1 ; i &lt;= n ; i ++ ){<br/>
scanf("%d" , &amp;tmp) ;<br/>
if ( tmp != curnum ) {<br/>
left[total] = curleft ;<br/>
right[total] = i - 1 ;<br/>
num[total] = curnum ;<br/>
freq[total] = count ;<br/>
curleft = i ;<br/>
curnum = tmp ;<br/>
count = 1 ;<br/>
total ++ ;<br/>
}else count ++ ;<br/>
}<br/>
left[total] = curleft ;<br/>
right[total] = i - 1 ;<br/>
num[total] = curnum ;<br/>
freq[total] = count ;<br/><br/>
init_st() ;<br/>
for ( i = 0 ; i &lt; q ; i ++ ){<br/>
int a , b ;<br/>
scanf("%d%d" , &amp;a , &amp;b) ;<br/>
printf("%d\n" , max_freq(a , b)) ;<br/>
}<br/>
}<br/>
return 0 ;<br/>
}<br/><br/><font color="#0000ff">其他问题：</font><br/><br/>
1.<font color="#ff0000">在算2的方幂的时候，使用移位比预计算后寻址来得更快。</font><br/>
这点在以前弄有关线段树的东西的时候也发现过类似情况。<br/><br/>
2.最初加外挂的时候，写了这样一句：<br/>
putint(max_freq(getint() , getint())) ;<br/><br/>
交WA了若干次，才反映过来，<font color="#ff0000">默认函数传参是从右边开始的</font>。<br/>
于是给max_freq的两个数刚好打颠倒了。<br/>
这个要严重的注意。。
