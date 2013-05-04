---
layout: post
title: "whu1412（Molecular Weight Calculator）递归下降？"
date: 2009-03-14  19:14
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 0a3fa76e7e9072d280cb4a22.html
_baiduhi_category: 算法
---

(hplonline)2009.3.14<br/><br/>
原题地址：<br/>
http://acm.whu.edu.cn/oak/problem/problem.jsp?problem_id=1412<br/><br/>
就是让求分子式的质量（是这么说吗。。丢了化学快两年了。。）<br/>
题意简单吧。。据说要用到递归下降+高精度。<br/><br/>
递归下降，暂时不清楚。。按照自己的想法写了个。<br/>
一个处理就是，所有数据乘100，即可整数运算。<br/>
然后就是扫描字符串的工作了，<font color="#ff6600">遇到左括号"("的时候递归<br/>
遇到右括号")"的时候回溯</font>。。。<br/><br/>
我这边写逻辑部分，留了个BIGINT给队友实现去。（不会JAVA就是惨啊。。）<br/>
下面这样就可以过样例了。<br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;stdio.h&gt;<br/><br/>
const int MAXN = 210 ;<br/><br/>
typedef int BIGINT ;<br/><br/>
typedef struct molecule_type{<br/>
       char name[3] ;<br/>
       int weight;<br/>
       BIGINT num ;<br/>
}MOLECULE;<br/><br/>
typedef struct formula_type{<br/>
       int num[MAXN];<br/>
}FORMULA;<br/><br/>
MOLECULE molecule[MAXN];<br/>
int n,m ;<br/><br/>
bool isBig(char ch){<br/>
       return ch &gt;= 'A' &amp;&amp; ch &lt;= 'Z' ;<br/>
}<br/><br/>
bool isSmall(char ch){<br/>
       return ch &gt;= 'a' &amp;&amp; ch &lt;= 'z' ;<br/>
}<br/><br/>
bool isNum(char ch){<br/>
       return ch &gt;= '0' &amp;&amp; ch &lt;= '9' ;<br/>
}<br/><br/>
int getId(char ch){<br/>
       int i ;<br/>
       for ( i = 0 ; i &lt; n ; i ++ ) <br/>
              if (molecule[i].name[0] == ch &amp;&amp; molecule[i].name[1] == 0 )break;<br/>
       return i;<br/>
}<br/><br/>
int getId(char ch1 , char ch2){<br/>
       int i ;<br/>
       for ( i = 0 ; i &lt; n ; i ++ ) <br/>
              if (molecule[i].name[0] == ch1 &amp;&amp; molecule[i].name[1] == ch2 )break;<br/>
       return i;<br/>
}<br/><br/>
char *pos;<br/><br/>
FORMULA recursion(){<br/>
       FORMULA ftmp , tt ;<br/>
       int id ;<br/>
       memset(ftmp.num,0,sizeof(ftmp.num));<br/>
       while (*pos&amp;&amp;*pos!=')'){<br/>
              if ( *pos == '(' ){<br/>
                     pos ++ ;<br/>
                     tt = recursion();<br/>
                     for ( id = 0 ; id &lt; n ; id ++ )ftmp.num[id] += tt.num[id] ;<br/>
                     continue ;<br/>
              }<br/>
              if (isBig(*pos)&amp;&amp;isSmall(pos[1])){<br/>
                     id = getId(*pos,pos[1]) ;<br/>
                     pos += 2 ;<br/>
              }else{<br/>
                     id = getId(*pos);<br/>
                     pos ++ ;<br/>
              }<br/>
              if ( isNum(*pos)){<br/>
                     ftmp.num[id] += *pos - '0' ;<br/>
                     pos ++ ;<br/>
              }else{<br/>
                     ftmp.num[id] ++ ;<br/>
              }<br/>
       }<br/>
       if ( *pos == ')' ){<br/>
              pos ++ ;<br/>
              if (isNum(*pos)){<br/>
                     for ( id = 0 ; id &lt; n ; id ++ )ftmp.num[id] = ftmp.num[id] * (*pos - '0');<br/>
                     pos ++ ;<br/>
              }<br/>
       }<br/>
       return ftmp; <br/>
}<br/><br/>
BIGINT cal(char *s){<br/>
       int i;<br/>
       BIGINT ans = 0 ;<br/>
       pos = s ;<br/>
       FORMULA f = recursion();<br/>
       for ( i = 0 ; i &lt; n ; i ++ ){<br/>
              molecule[i].num = f.num[i] ;<br/>
              ans = ans + f.num[i] * molecule[i].weight ;<br/>
       }<br/>
       return ans ;<br/>
}<br/><br/>
int main(){<br/>
       int T ;<br/>
       int i ;<br/>
       int tmp1,tmp2 ;<br/>
       char s[600];<br/>
       scanf("%d",&amp;T);<br/>
       while (T -- ){<br/>
              scanf("%d",&amp;n);<br/>
              for ( i = 0 ; i &lt; n ; i ++ ){<br/>
                     scanf("%s %d.%d",molecule[i].name,&amp;tmp1,&amp;tmp2);<br/>
                     molecule[i].weight = tmp1 * 100 + tmp2 ;<br/>
              }<br/>
//              for ( i = 0 ; i &lt; n ; i ++ )printf("%s %d\n",molecule[i].name,molecule[i].weight);<br/>
              scanf("%d",&amp;m);gets(s);<br/>
              while(m -- ){<br/>
                     gets(s);<br/>
                     BIGINT ans = cal(s);<br/>
                     printf("%d.%d ",ans/100,ans%100 );<br/>
                     for ( i = 0 ; i &lt; n ; i ++ )if ( molecule[i].num != 0 ){<br/>
                            printf("%s[%d] ",molecule[i].name,molecule[i].num);<br/>
                     }<br/>
                     putchar('\n');<br/>
              }<br/>
       }<br/>
       return 0 ;<br/>
}<br/><br/>
之后就是很怨念的整合。。<br/><br/>
因为这里做逻辑的时候用的int 来，随便怎么递归都没问题。<br/>
一换成高精度类。。一上就<font color="#ff0000">stack overflow</font>。。惨啊。。<br/><br/>
于是把所有高精度有关的都放到全局空间中去。。<br/><br/>
交一下。。MLE。。<br/><br/>
因为高精度按照每节一个十进制位来存的，空间利用不充分。。<br/><br/>
最后是用的MOD 100000 过的。。<br/>
应该说很险。。因为<font color="#ff0000">400*100*100000超过signed int 的值</font>了。<br/>
不过当时很忙，没空改成unsigned的就硬上了。<br/><br/>
唉。。最后1个半小时就在整合中度过。。。<br/>
居然在17：02的时候交上去了一个。。而且还过了。。<br/><br/>
上面的int写法能够表达思路了。。<br/>
整好的就不拿出来了，太丑陋了。。<br/><br/><font color="#ff6600">既然大牛提到了递归下降，那么啥时候也要去学下编译原理了，呵呵。<br/>
话说网上有很多的分子式计算工具，不过ACM的题就是数据搞得很大。。<br/></font>
