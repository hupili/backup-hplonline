---
layout: post
title: "多维迷宫的降维解法（POJ3454 Hypertheseus)"
date: 2009-03-25  12:49
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 52fc6722a32d1cac4723e83e.html
_baiduhi_category: 算法
---

(hplonline)2009.3.25<br/><br/>
题目应该说是意思很明了。<br/>
就是走一个高维的迷宫。<br/><br/>
走二维的迷宫是此类问题中最直接接触的。<br/>
一般的BFS可以很轻松的搞定。<br/><br/>
我们用dx[4] ={...},dy[4] = {...}这样的东西来记录一个增量。<br/>
对当前点依次按照各个增量来走。<br/>
判断新产生的点是否在地图外面，等等。<br/><br/>
当遇到三维的时候，我们习惯性地移植这种方法。加一个dz[4]就可以搞定了。<br/><br/>
有一个事实：每增加一个维度，可以走的方向增加两个。<br/><br/>
但是，当真正的多维迷宫出现的时候。上面的方法显然没法实现。<br/><br/>
就好比，你可以a = 1 , a = 1 + 2 , a = 1 + 2 + 3 <br/>
但是a = 1 + 2 + ... + 100 写起来就很臃肿了。<br/><br/>
对于一个n维迷宫，不至于写n个dXX[]来记录增量嘛。。<br/><br/>
所以，比较简洁的做法就是<font color="#ff0000">降维</font>。这个东西听起来很像个意思。<br/>
写起来还是比较囧的一个事情。<br/><br/><font color="#0000ff">一。思路描述</font><br/><br/>
d，总共的维度数目<br/><br/>
space[i]记录的是迷宫中第i个位置的情况。<br/>
迷宫按照第一个维度，第二个维度。。。这样排成一行，就降成一维了。<br/><br/>
n[i]为第i个维度的长度,i = 0..d<br/><br/>
mv[i]是一个移动矢量，表示在第i个维度上移动一个单位，在space中实际上产生的距离<br/>
那么mv[0] = 1 ;mv[i] = mv[i-1] * n[i-1] ;<br/>
其中mv[d]表达的就是这个图中总共的点数。<br/><br/>
所以，当BFS的时候，对当前点curp依次加减每个维度上的增量。<br/>
就可以得到新点的位置了。<br/><br/>
基本问题是解决了。但是还有一个更重要的问题：<br/>
就是关于新点有效性的判定。<br/><br/>
在做二维的时候，习惯上是生成nx,ny然后看<br/><br/>
if ( nx &gt;= 0 &amp;&amp; nx &lt; sx  &amp;&amp; ny &gt;= 0 &amp;&amp; ny &lt; sy ){...}<br/>
sx和sy是x和y维度的大小。<br/><br/>
那么，到n维的时候，这样就不行了。举个例子：<br/><br/>
有3*3的矩阵。排成0..8。当前点是2（即第0行的第2列）。<br/>
如果现在先按照维度移动。可以得到点3（即第1行的第0列）。<br/>
3点显然是在我们空间里面的，但这个移动又显然是不成立的。<br/><br/><font color="#ff0000">所以，要在移动之前判断。</font>而这个判断说起来就比较绕口了。<br/>
（<font color="#ff6600">感觉属于挑战表达能力的极限，那么我开始了。。</font>）<br/><br/>
假设我们要在第i个维度上移动。我们就把前面的所有维度压缩成一个点。<br/>
在i个维度上的移动一次的距离是mv[i]，这个已经求得。<br/>
那么在移动之前我们要检查：<br/><font color="#ff0000">1.如果该点在于第k个i+1维度上，离第k个i+1维度的第一个i维度的距离是0，<br/>
则不能进行减mv[i]的操作。<br/>
2.如果该点在于第k个i+1维度上，离第k个i+1维度的第一个i维度的距离是n[i] - 1 ， <br/>
则不能进行加mv[i]的操作。</font><br/><br/>
拿第一个说一下：<br/>
curp / mv[i] 可以得到curp是总共的第几个i维度<br/>
那么再 % n[i]  就算出离第k个i+1维度的第一个i维度的距离<br/>
跟着判断就行了。<br/><br/>
关键的代码就是：<br/>
  <font color="#ff6600">            if ( ( curp / mv[i] ) % n[i] != n[i] - 1 ){<br/>
                    newp = curp + mv[i] ;<br/>
                    visit(newp);<br/>
               }<br/>
               if ( ( curp / mv[i] ) % n[i] != 0 ){<br/>
                    newp = curp - mv[i] ;<br/>
                    visit(newp);<br/>
               }</font><br/><br/><font color="#0000ff">二。代码</font><br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;string.h&gt;<br/><br/>
const int MAXCUBE = 1048576 ;<br/><br/>
int d ;<br/>
int n[21] ;<br/>
int mv[21] ;<br/><br/>
char space[MAXCUBE] ;<br/>
int q[MAXCUBE] ;//队列<br/>
int stp[MAXCUBE] ;//到达space[i]的步数<br/>
int front , rear ;<br/>
bool vst[MAXCUBE] ;//判重<br/><br/>
int p ;<br/>
int s , m , t , curs;<br/><br/>
void visit(int pt){<br/>
     if ( !(pt &gt;= 0 &amp;&amp; pt &lt; mv[d]) ) {<br/>
          return ;<br/>
     }<br/>
     if ( vst[pt] || space[pt] ) return ;<br/>
     vst[pt] = true ;<br/>
     stp[pt] = curs ;<br/>
     q[rear] = pt ;<br/>
     rear ++ ;<br/>
}<br/><br/>
int bfs(int from , int to ){<br/>
     int curp , newp ;<br/>
     int i ;<br/>
     memset(vst , false , sizeof(vst)) ;<br/>
     front = 0 ;<br/>
     rear = 1 ;<br/>
     q[0] = from ;<br/>
     stp[from] = 0 ;<br/>
     vst[from] = true ;<br/>
     while ( front &lt; rear ){<br/>
          curp = q[front ++] ;<br/>
          curs = stp[curp] + 1;<br/>
          if ( curp == to ) {<br/>
               front -- ;<br/>
               break ;<br/>
          }<br/>
          for ( i = 0 ; i &lt; d ; i ++ ){<br/>
               if ( ( ( curp ) / mv[i] ) % n[i] != n[i] - 1 ){<br/>
                    newp = curp + mv[i] ;<br/>
                    visit(newp);<br/>
               }<br/>
               if ( ( ( curp ) / mv[i] ) % n[i] != 0 ){<br/>
                    newp = curp - mv[i] ;<br/>
                    visit(newp);<br/>
               }<br/>
          }<br/>
     }<br/>
     if ( front == rear ) return - 1;<br/>
     else return stp[curp] ;<br/>
}<br/><br/>
char nextchar(){<br/>
     char ch ;<br/>
     do{<br/>
          ch = getchar() ;<br/>
     }while ( ch != '#' &amp;&amp; ch != '.' &amp;&amp; ch != 'S' &amp;&amp; ch != 'M' &amp;&amp; ch != 'T' ) ;<br/>
     if ( ch == 'S' ) s = p ;<br/>
     if ( ch == 'M' ) m = p ;<br/>
     if ( ch == 'T' ) t = p ;<br/>
     if ( ch == '#' ) return 1 ;<br/>
     else return 0 ;<br/>
}<br/><br/>
void readmap(int layer){<br/>
     int i;<br/>
     if ( layer == 0 ){<br/>
          space[p ++ ] = nextchar() ;<br/>
          return ;<br/>
     }<br/>
     for ( i = 0 ; i &lt; n[layer - 1] ; i ++ ) readmap( layer - 1 ) ;<br/>
}<br/><br/>
int main(){<br/>
     int i ;<br/>
     int ans ;<br/>
     while (1){<br/>
          scanf("%d",&amp;d);<br/>
          if ( d == 0 ) break ;<br/>
          for ( i = 0 ; i &lt; d ; i ++ ){<br/>
               scanf("%d",n + i ) ;               <br/>
          }<br/>
          mv[0] = 1 ;<br/>
          for ( i = 1 ; i &lt;= d ; i ++ ){<br/>
               mv[i] = n[i - 1] * mv[i - 1] ;<br/>
          }<br/>
          p = 0 ;<br/>
          readmap(d) ;<br/>
          ans = 0 ;<br/>
          space[m] = 1 ;<br/>
          i = bfs(t,s) ;<br/>
          if ( i == -1 ){<br/>
               ans = -1 ;<br/>
          }else{<br/>
               space[m] = 0 ;<br/>
               ans += i ;<br/>
               i = bfs(s,m) ;<br/>
               if ( i == -1 ){<br/>
                    ans = -1 ;<br/>
               }else{<br/>
                    ans += i ;<br/>
                    i = bfs(m,t) ;<br/>
                    if ( i == -1 ){<br/>
                         ans = -1 ;<br/>
                    }else{<br/>
                         ans += i ;<br/>
                    }<br/>
               }<br/>
          }<br/>
          if ( ans == -1 )puts("No solution. Poor Theseus!");<br/>
          else{<br/>
               printf("Theseus needs %d steps.\n",ans);<br/>
          }<br/>
     }     <br/>
     return 0 ;<br/>
}<br/><br/><font color="#0000ff">三。后话</font><br/><br/>
这东西在POJ上用G++交不过。。于是很郁闷地去搜了数据。拿下来发现是对的。。<br/><br/>
无解中。。。于是换C++ 交。。。然后就过了。。不知道谁看出是哪的问题了。。求解。
