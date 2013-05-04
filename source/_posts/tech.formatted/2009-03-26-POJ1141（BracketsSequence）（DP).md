---
layout: post
title: "POJ1141（Brackets Sequence）（DP)"
date: 2009-03-26  20:23
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: a2f68d01653db8de267fb5cd.html
_baiduhi_category: 算法
---

(hplonline)2009.3.26<br/><br/>
就是给括号序列。<br/>
定义了一种regular brackets sequence。<br/>
求最少添加多少括号来形成这种序列。<br/><br/>
半年前怨念地<font color="#ff0000">WA</font>了此题。。今天跑回来，在<font color="#ff0000">WA</font>了两盘后，终于搞定了。。。<br/><br/>
那么说DP：<br/><br/>
s[]是读入的字符串<br/>
f[i][j]是i到j的最少的添加数<br/>
c[i][j]是对应的添加方案<br/><br/>
分几种情况<br/><font color="#ff6600"><br/>
s[i] == '[' 在右端添 ']' 并求解 s[i + 1][j]<br/>
s[i] == '('<br/>
s[j] == ')'<br/>
s[j] == ']'类似处理<br/>
s[i] == '[' &amp;&amp; s[j] == ']' ，求解s[i + 1][j - 1] <br/>
s[i] == '(' &amp;&amp; s[j] == ')'， 类似<br/><br/>
除了这些特殊情况外。<br/>
对 i &lt;= k &lt; j <br/>
分别求解s[i][k] 和 s[k + 1][j] </font><br/><br/>
实现上选取相应的记法来表达策略：<br/>
//least bracket num ;<br/>
int f[MAXN][MAXN] ;<br/><font color="#ff6600">//strategy:-1,-2,-3,-4,-5</font><br/>
//'[',']','(',')',choose middle<br/>
int c[MAXN][MAXN] ;<br/>
char s[MAXN] ;<br/><br/><font color="#ff6600">即为负的时候相当于上面的5种特殊情况，为非负的时候就是截成两段的一般情况时的分界点</font>。<br/><br/>
于是，程序：<br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;string.h&gt;<br/><br/>
const int MAXN = 110 ;<br/>
const int MAX = 100000000 ;<br/><br/>
//least bracket num ;<br/>
int f[MAXN][MAXN] ;<br/>
//strategy:-1,-2,-3,-4,-5<br/>
//'[',']','(',')',choose middle<br/>
int c[MAXN][MAXN] ;<br/>
char s[MAXN] ;<br/><br/>
void output(int l , int r ){<br/>
     if ( l &gt; r ) return ;<br/>
     switch(c[l][r]){<br/>
     case -5 : <br/>
          putchar(s[l]);<br/>
          output( l + 1 , r - 1 );<br/>
          putchar(s[r]);<br/>
          break;<br/>
     case -1 :<br/>
          putchar('[');<br/>
          output( l , r - 1 ) ;<br/>
          putchar(']');<br/>
          break;<br/>
     case -2 :<br/>
          putchar('[');<br/>
          output( l + 1 , r ) ;<br/>
          putchar(']');<br/>
          break;<br/>
     case -3 :<br/>
          putchar('(');<br/>
          output( l , r - 1 ) ;<br/>
          putchar(')');<br/>
          break;<br/>
     case -4 :<br/>
          putchar('(');<br/>
          output( l + 1, r ) ;<br/>
          putchar(')');<br/>
          break;<br/>
     default:<br/>
          output( l , c[l][r] ) ;<br/>
          output( c[l][r] + 1 , r ) ;<br/>
          break;<br/>
     }<br/>
}<br/><br/>
int main(){<br/>
     int i , j , k , l ; <br/>
     int p ;<br/>
     <br/>
     gets(s);<br/>
     l = strlen(s);<br/>
     for ( i = 0 ; i &lt; l ; i ++ ){<br/>
          f[i][i] = 1 ;<br/>
          switch(s[i]){<br/>
          case '[':c[i][i] = -2 ;break ;<br/>
          case ']':c[i][i] = -1 ;break ;<br/>
          case '(':c[i][i] = -4 ;break ;<br/>
          case ')':c[i][i] = -3 ;break ; <br/>
          }<br/>
     }<br/>
     for ( i = 1 ; i &lt; l ; i ++ ) f[i][i - 1] = -5 ;<br/><br/>
     for ( k = 1 ; k &lt; l ; k ++ ){<br/>
          for ( i = 0 ; i &lt; l - k ; i ++ ){<br/>
               j = i + k ;<br/>
               f[i][j] = MAX ;<br/>
               if ( s[i] == '(' &amp;&amp; s[j] == ')' || s[i] == '[' &amp;&amp; s[j] == ']' ){<br/>
                    f[i][j] = f[i + 1][j - 1] ;<br/>
                    c[i][j] = -5 ;<br/>
               }<br/>
               if ( s[i] == '[' &amp;&amp; f[i + 1][j] + 1 &lt; f[i][j] ){<br/>
                    f[i][j] = f[i + 1][j] + 1 ;<br/>
                    c[i][j] = -2 ;<br/>
               }<br/>
               if ( s[j] == ']' &amp;&amp; f[i][j - 1] + 1 &lt; f[i][j] ){<br/>
                    f[i][j] = f[i][j - 1] + 1 ; <br/>
                    c[i][j] = -1 ;<br/>
               }<br/>
               if ( s[i] == '(' &amp;&amp; f[i + 1][j] + 1 &lt; f[i][j] ){<br/>
                    f[i][j] = f[i + 1][j] + 1 ;<br/>
                    c[i][j] = -4 ;<br/>
               }<br/>
               if ( s[j] == ')' &amp;&amp; f[i][j - 1] + 1 &lt; f[i][j] ){<br/>
                    f[i][j] = f[i][j - 1] + 1 ; <br/>
                    c[i][j] = -3 ;<br/>
               }<br/>
               for ( p = i ; p &lt; j ; p ++ ){<br/>
                    if ( f[i][p] + f[p + 1][j] &lt; f[i][j]){<br/>
                         f[i][j] = f[i][p] + f[p + 1][j] ;<br/>
                         c[i][j] = p ;<br/>
                    }<br/>
               }<br/>
          }     <br/>
     }<br/><br/>
     output(0,l - 1) ;<br/>
   <font color="#ff0000"> putchar('\n');</font><br/>
     <br/>
     return 0 ;<br/>
}<br/><br/>
最后那句红的putchar是很关键的。。因为是SPJ。。所以没有PE的说法。。<br/>
于是我今天又<font color="#ff0000">WA</font>了两盘。。<br/>
