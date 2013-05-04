---
layout: post
title: "最小生成树（KRUSCAL,PRIM思想及SOLLIN实现)"
date: 2009-04-16  20:46
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 8d68db58eb0e1d89810a18c7.html
_baiduhi_category: 算法
---

(hplonline)2009.4.16<br/><br/>
很早听说过SOLLIN这个算法，虽然说起来有那么点意思，<br/>
但是总觉得实现上常数会很大，也就一直没动。<br/><br/>
另外在OI界和ACM界，MST的应用很广泛的，但很很少看到人用这个算法。<br/><br/>
最近的图论课要做PROJECT，老师上课也提到了这个算法。<br/>
于是搞了个出来，总得来说，这个实现只是描述了算法的意思，<br/>
其常数非常非常大，而且相关的数据都用STL来组织，偷点懒。<br/><br/>
KRUSCAL和PRIM相信网上到处都是，就只提思想了。<br/>
SOLLIN因为第一次写，给一个CP的实现（没有交过题，不确定正确性和效率）<br/><br/><font color="#0000ff">一。最小生成树的条件</font><br/><br/>
树上边：在最小生成树上的边<br/><br/>
非树上边：不在最小生成树上的边<br/><br/>
树上路径：最小生成树上两点间的唯一路径<br/><br/><font color="#ff0000">路径最优：任一非树上边的权重都大于它所对应的树上路径上的每条边的权重。<br/>
（否则用该边形成的生成树权重更小）</font><br/><br/>
割边：任意树上边把树分为两部分，连接该两部分的边为割边<br/><br/><font color="#ff0000">割最优：任一树上边的权重都小于它所对应的割集中每条边的权重。<br/>
（否则用比该边小的割边来连接成的生成树更小）</font><br/><div class="O">
<div style="text-align: center;"> </div>
</div>
<br/><font color="#0000ff">二。KRUSCAL</font><br/><br/><font color="#ff6600">KRUSCAL：根据路径最优构造。</font><br/><br/><font color="#0000ff">算法1</font>：（直观）<br/>
先随便构造一个树，依次检查非树上边，<br/>
如果发现破坏路径最优条件，即用该边替换一个比他大的树上边。<br/><br/>
这个算法，可以描述，但是写出来很慢。要改进<br/><br/><font color="#0000ff">算法2</font>：（换个角度，即KRUSCAL）<br/>
把所有边从小到大排序，依次加入边集。<br/>
如果某边加入后成环了（非树），则PASS掉。<br/><br/>
这样在加边的时候，因为从小到大，自然保证了路径最优。<br/><font color="#0000ff"><br/>
三。PRIM</font><br/><br/><font color="#ff6600">PRIM：根据割最优</font><br/><br/><font color="#0000ff">算法3</font>：（就是PRIM）<br/><br/>
假设现在已经有了一棵包含某些点的树了，<br/>
要把它和剩下的点连起来，从该树有许多割边指出，<br/>
那么根据割最优条件，选取最小的一个，一定在树上，<br/>
同时该树上的点增加一个。<br/><br/>
初始的时候随便选一个点就可以了。<br/><br/><font color="#0000ff">四。SOLLIN</font><br/><br/><font color="#0000ff">算法4：其实还是根据割最优</font><br/><br/>
该算法的核心在于。不是像PRIM选择一颗树，逐步扩大。<br/>
他一开始把所有的点做成独立的树，形成一个森林。<br/>
根据割最优条件，从这些树指出的割边一定是在MST上的。<br/>
于是把这些边都加入MST的边集，同时合并相连的树。<br/>
重复到只有一棵树为止。<br/><br/>
思想上感觉很有前途。实现的时候要考虑不少东西。<br/>
比如怎样表示树？怎样表示森林？<br/>
每次搜索出来的最小割边集有重复的，怎样避免多次加入？<br/>
。。。<br/><br/><font color="#ff6600">当然，我捡懒不想了，用了很庞大的一堆STL的组件来做。<br/>
下面这个代码显然没有实用价值，他只能表达一种意思。</font><br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;set&gt;<br/>
#include &lt;vector&gt;<br/>
#include &lt;list&gt;<br/>
#include &lt;algorithm&gt;<br/>
#include &lt;fstream&gt;<br/><br/>
#pragma warning(disable: 4786)<br/><br/>
using namespace std;<br/><br/>
const int MAX = 10000000 ;<br/><br/>
typedef set&lt;int&gt; TREE ;<br/>
typedef set&lt;TREE&gt; FOREST ;<br/>
typedef list&lt;int&gt; ADJEDGE ;//邻接边，记录的是vedges中该边的下标<br/>
typedef vector&lt;ADJEDGE&gt; ADJLIST ;//邻接表<br/><br/>
typedef struct _edge_type{<br/>
      int a ;<br/>
      int b ;<br/>
      int w ;<br/>
}EDGE ;<br/><br/>
int n , m ;<br/>
vector&lt;EDGE&gt; vedges ;<br/><br/>
/*<br/>
边的比较，未用到<br/>
struct cmp_edge{<br/>
      bool operator()(const int &amp;ie1 , const int &amp;ie2)const {<br/>
            return vedges[ie1].w &lt; vedges[ie2].w ;<br/>
      };<br/>
};<br/>
*/<br/><br/>
FOREST::iterator find_tree( FOREST &amp;f , int v){<br/>
      FOREST::iterator ifr ;<br/>
      for ( ifr = f.begin() ; ifr != f.end() ; ifr ++ ){<br/>
            if ( (*ifr).count(v) ) return ifr ;<br/>
      }<br/>
//      cout&lt;&lt;"eee"&lt;&lt;endl;<br/>
}<br/><br/>
void output(FOREST &amp;f){<br/>
      FOREST::iterator it ;<br/>
      int i = 0 ;<br/>
      for ( it = f.begin() ; it != f.end() ; it ++ ){<br/>
            cout&lt;&lt;"tree "&lt;&lt;++i&lt;&lt;endl;<br/>
            TREE::iterator ii ;<br/>
            TREE &amp;ct = (*it) ;<br/>
            for ( ii = ct.begin() ; ii != ct.end() ; ii ++ ){<br/>
                  cout&lt;&lt;(*ii)&lt;&lt;' ' ;<br/>
            }<br/>
            cout&lt;&lt;endl;<br/>
      }<br/>
}<br/><br/>
int main(){<br/>
      int i;<br/>
      FOREST forest ;<br/>
      ADJLIST adjlist ;<br/>
      set&lt;int&gt; mst_edges ;<br/><br/>
      ifstream fin("test.txt");<br/><br/>
      fin&gt;&gt;n&gt;&gt;m ;<br/>
      <br/>
      adjlist.clear() ;<br/>
      for ( i = 0 ; i &lt; n ; i ++ ){<br/>
            adjlist.push_back(ADJEDGE());<br/>
      }<br/><br/>
      vedges.clear() ;<br/>
      for ( i = 0 ; i &lt; m ; i ++ ){<br/>
            EDGE t;<br/>
            fin&gt;&gt;t.a&gt;&gt;t.b&gt;&gt;t.w ;<br/>
            vedges.push_back(t) ;<br/>
            adjlist[t.a].push_back(i);<br/>
            adjlist[t.b].push_back(i);<br/>
      }<br/>
      <br/>
      for ( i = 0 ; i &lt; n ; i ++ ){<br/>
            TREE t ;<br/>
            t.clear() ;<br/>
            t.insert(i);<br/>
            forest.insert(t);<br/>
      }<br/><br/>
      mst_edges.clear() ;<br/>
      while ( forest.size() != 1 ){<br/>
            set&lt;int&gt; minedges ;<br/>
            FOREST::iterator iforest ;<br/>
            minedges.clear();<br/>
            for ( iforest = forest.begin() ; iforest != forest.end() ; iforest ++ ){<br/>
                  TREE &amp;curtree = *iforest ;<br/>
                  TREE::iterator itree ;<br/>
                  int min_weight = MAX ;<br/>
                  int min_edge ;<br/>
                  //找到该树最小割边<br/>
                  for ( itree = curtree.begin() ; itree != curtree.end() ; itree ++ ){<br/>
                        ADJEDGE &amp;curedge = adjlist[*itree] ;<br/>
                        ADJEDGE::iterator iedge ;<br/>
                        for ( iedge = curedge.begin() ; iedge != curedge.end() ; iedge ++ ){<br/>
                              if ( curtree.count(vedges[(*iedge)].a) <br/>
                                    &amp;&amp; curtree.count(vedges[(*iedge)].b) ){<br/>
                                    continue ;//该边在同一树内      <br/>
                              }<br/>
                              if ( vedges[*iedge].w &lt; min_weight ){<br/>
                                    min_weight = vedges[*iedge].w ;<br/>
                                    min_edge = *iedge ;<br/>
                              }<br/>
                        }<br/>
                  }<br/>
                  minedges.insert(min_edge);<br/>
            }<br/><br/>
            set&lt;int&gt;::iterator iminedge ;<br/>
            for ( iminedge = minedges.begin() ; iminedge != minedges.end() ; iminedge ++ ){<br/>
            //      output(forest) ;<br/>
                  int a = vedges[*iminedge].a ;<br/>
                  int b = vedges[*iminedge].b ;<br/>
                  FOREST::iterator ita = find_tree( forest , a ) ;<br/>
                  FOREST::iterator itb = find_tree( forest , b ) ;<br/>
                  if ( ita == itb ) continue ;<br/>
                  mst_edges.insert(*iminedge) ;<br/>
            //      set_union((*ita).begin() , (*ita).end() , (*itb).begin() , (*itb).end() , (*ita).end() ) ;<br/>
                  TREE::iterator itr ;<br/>
                  for ( itr = (*itb).begin() ; itr != (*itb).end() ; itr ++ ){<br/>
                        (*ita).insert(*itr) ;<br/>
                  }<br/>
            //      cout&lt;&lt;(*ita).size()&lt;&lt;endl;<br/>
                  forest.erase(itb);<br/>
            }<br/>
      }<br/>
      <br/>
      set&lt;int&gt;::iterator it ;<br/>
      int mst_weight = 0 ;<br/>
      cout&lt;&lt;"the edges:"&lt;&lt;endl;<br/>
      for ( it = mst_edges.begin() ; it != mst_edges.end() ; it ++ ){<br/>
            cout&lt;&lt;vedges[*it].a&lt;&lt;' '&lt;&lt;vedges[*it].b&lt;&lt;' '&lt;&lt;vedges[*it].w&lt;&lt;endl;<br/>
            mst_weight += vedges[*it].w ;<br/>
      }<br/>
      cout&lt;&lt;"mst weight:"&lt;&lt;mst_weight&lt;&lt;endl;<br/>
      return 0 ;<br/>
}<br/><br/><font color="#0000ff">用到的test.txt文件内容如下组织：</font><br/><br/>
5 7<br/>
0 1 35<br/>
0 2 40<br/>
1 2 25<br/>
1 3 10<br/>
2 3 20<br/>
3 4 30<br/>
2 4 15 <br/><br/>
格式：<br/>
顶点数 边数<br/>
｛点a 点b 权重｝（边数行）<br/>
顶点从0开始编号<br/><br/><font color="#ff0000">PS：我没有充分检查，谁发现BUG了麻烦说一声</font>
