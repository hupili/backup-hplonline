---
layout: post
title: "贴一个BST（BinarySearchTree）"
date: 2009-05-11  21:34
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 6267a37773b21e13b151b9f7.html
_baiduhi_category: 算法
---

hplonline(2009.5.11)<br/><br/>
写过这么多程序了，貌似还没<font color="#ff6600">正式</font>写过这个结构。<br/>
毕竟以后可能会用到这些东西。<br/>
老是小打小闹地遇到特殊问题时写一篇特殊的代码，<br/>
编码效率上会很吃亏的，<br/>
还是写得像模像样一点，<br/>
标准就是自己在若干天后用起来比较方便就行了。<br/><br/>
由于学习STL的最后一部分被RBTree卡到了。。<br/>
得先学下这个结构。<br/>
而他的近亲AVLTree也要学一下。<br/>
当然AVL的老爹应该先搞定，于是从BST开始。<br/><br/>
我这个版本就有两点稍微可以说的：<br/><br/><font color="#ff0000">1.除了Clear()外没有用递归。</font><br/>
因为像Find，Insert之类的，当前指针p在树上跑的路线都是单边的。<br/>
这样大可不必递归。<br/>
但Clear() 由于要先清除左右子树，自己写栈来消除递归显然更臃肿，就算了。<br/><br/><font color="#ff0000">2.空间分配方面留了三个宏</font><br/>
#define _BST_initspace <br/>
#define _BST_allocate() (BNode *)malloc(sizeof(BNode))<br/>
#define _BST_deallocate(p) free(p) <br/><br/>
长期做工程的同学可能不理解这个用意。<br/>
但是长期刷题的同学应该知道这写猥琐的手脚。。。<br/><br/>
比如，刷题的时候换成下面一组：<br/>
//BNode space[1000] , *spacehead ;<br/>
//#define _BST_initspace spacehead = space <br/>
//#define _BST_allocate() spacehead++ ;<br/>
//#define _BST_deallocate(p) <br/><br/>
一般来说刷题可以先估计要用的内存大小，<br/>
这样搞可以提高速度。<br/>
而且把释放内存的宏定义为空。<br/>
因为开在全局区的空间，随程序结束自动释放。<br/><br/>
总得来说，这一手脚有的时候可以让TLE的变AC。<br/><br/>
记得曾经有一道题：<br/>
用new和delete<font color="#ff0000">超时</font>，<br/>
搞了半天，决定不delete了，<font color="#ff0000">300ms</font>过了。<br/>
把new换成malloc，<font color="#ff0000">200ms</font>过了。<br/>
换成静态分配，<font color="#ff0000">100ms</font>过了。<br/><br/><font color="#0000ff">源码：</font>包含测试部分<br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;stdlib.h&gt;<br/><br/>
//元素类型<br/>
typedef int ElemType ;<br/><br/>
//树的节点<br/>
struct BNode{<br/>
     ElemType data ;<br/>
     BNode *left , *right , *parent ;<br/>
     BNode(){<br/>
          left = NULL ;<br/>
          right = NULL ; <br/>
          parent = NULL ;<br/>
     }<br/>
     BNode(ElemType d){<br/>
          data = d ;<br/>
          left = NULL ;<br/>
          right = NULL ; <br/>
          parent = NULL ;<br/>
     }<br/>
     void init(ElemType d){<br/>
          data = d ;<br/>
          left = NULL ;<br/>
          right = NULL ; <br/>
          parent = NULL ;          <br/>
     }<br/>
};<br/>
typedef BNode *PBNode ;<br/><br/>
//空间分配宏，便于实现其他配置方式<br/>
#define _BST_initspace <br/>
#define _BST_allocate() (BNode *)malloc(sizeof(BNode))<br/>
#define _BST_deallocate(p) free(p) <br/>
//BNode space[1000] , *spacehead ;<br/>
//#define _BST_initspace spacehead = space <br/>
//#define _BST_allocate() spacehead++ ;<br/>
//#define _BST_deallocate(p) <br/><br/>
//BST<br/>
class BinarySearchTree{<br/>
private:<br/>
     PBNode root ;<br/>
     void _delete_node(PBNode p) ;<br/>
     PBNode _find_subs(PBNode pos) ;//寻找删除时用于替换的节点<br/>
public:<br/>
     BinarySearchTree() ;<br/>
     PBNode Find(ElemType d) ;<br/>
     PBNode FindMax() ;<br/>
     PBNode FindMin() ;<br/>
     ElemType&amp; Retrieve(PBNode p) ;<br/>
     PBNode Insert(ElemType d) ;<br/>
     void Delete(ElemType d) ;//按元素删除<br/>
     void Erase(PBNode p) ;//按节点位置删除<br/>
     void Clear() ;<br/>
     static void Sort(ElemType a[] , int n , int d = 1) ;//利用BST进行排序，静态函数<br/>
} ;<br/><br/>
//d：1，从小到大，0，从大到小<br/>
void BinarySearchTree::Sort(ElemType a[] , int n , int d){<br/>
     BinarySearchTree tree ;<br/>
     int i ;<br/>
     for ( i = 0 ; i &lt;n ; i ++ ){<br/>
          tree.Insert(a[i]) ;<br/>
     }<br/>
     for ( i = 0 ; i &lt; n ; i ++ ){<br/>
          PBNode p ;<br/>
          if ( d ) {<br/>
               p = tree.FindMin() ;<br/>
          }else{<br/>
               p = tree.FindMax() ;     <br/>
          }<br/>
          a[i] = tree.Retrieve(p) ;<br/>
          tree.Erase(p) ;<br/>
     }<br/>
}<br/><br/>
BinarySearchTree::BinarySearchTree(){<br/>
     root = NULL ;<br/>
}<br/><br/>
PBNode BinarySearchTree::Find(ElemType d){<br/>
     PBNode p = root ;<br/>
     while ( p &amp;&amp; p-&gt;data != d ){<br/>
          if ( d &lt; p-&gt;data ) p = p-&gt;left ;<br/>
          else p = p-&gt;right ;<br/>
     }     <br/>
     return p ;<br/>
}<br/><br/>
PBNode BinarySearchTree::FindMax(){<br/>
     if ( root == NULL ) return NULL ;<br/>
     PBNode p = root ;<br/>
     while ( p-&gt;right ){<br/>
          p = p-&gt;right ;<br/>
     }<br/>
     return p ;<br/>
}<br/><br/>
PBNode BinarySearchTree::FindMin(){<br/>
     if ( root == NULL ) return NULL ;<br/>
     PBNode p = root ;<br/>
     while ( p-&gt;left ){<br/>
          p = p-&gt;left ;<br/>
     }<br/>
     return p ;<br/>
}<br/><br/>
ElemType&amp; BinarySearchTree::Retrieve(PBNode p){<br/>
     return p-&gt;data ;<br/>
}<br/><br/>
PBNode BinarySearchTree::Insert(ElemType d){<br/>
     //根为空特殊处理<br/>
     if ( root == NULL ) {<br/>
          root = _BST_allocate() ;<br/>
          root-&gt;init(d) ;          <br/>
          return root ;<br/>
     }<br/>
     PBNode p = root ;<br/>
     PBNode q = NULL ;<br/>
     while ( p &amp;&amp; p-&gt;data != d ){<br/>
          q = p ;<br/>
          if ( d &lt; p-&gt;data ) p = p-&gt;left ;<br/>
          else p = p-&gt;right ;<br/>
     }<br/>
     //该节点存在,直接返回<br/>
     if ( p ) {<br/>
          return p ;<br/>
     }<br/>
     //不存在,q为插入点<br/>
     p = _BST_allocate() ;<br/>
     p-&gt;init(d) ;<br/>
     p-&gt;parent = q ;<br/>
     if ( d &lt; q-&gt;data ){<br/>
          q-&gt;left = p ;<br/>
     }else{<br/>
          q-&gt;right = p ;<br/>
     }<br/>
     return p ;<br/>
}<br/><br/>
PBNode BinarySearchTree::_find_subs(PBNode pos){<br/>
     PBNode su ;<br/>
     if ( pos-&gt;left == NULL || pos-&gt;right == NULL ) {<br/>
          //有一个子树为空<br/>
          if ( pos-&gt;left == NULL ){<br/>
               su = pos-&gt;right ;<br/>
          }else{<br/>
               su = pos-&gt;left ;<br/>
          }          <br/>
     }else{<br/>
          //两个均不为空，寻找前驱，即左子树的最右枝<br/>
          su = pos-&gt;left ;<br/>
          while ( su-&gt;right ) su = su-&gt;right ;<br/>
     }<br/>
     return su ;<br/>
}<br/><br/>
void BinarySearchTree::Erase(PBNode pos){<br/>
     if ( pos == NULL ) return ;<br/>
     PBNode su = _find_subs(pos) ;//替换节点<br/>
     //根节点<br/>
     if ( pos-&gt;parent == NULL ) {<br/>
          if ( su ){<br/>
               PBNode sup = su-&gt;parent ;<br/>
               if ( su == sup-&gt;left ) {<br/>
                    sup-&gt;left = NULL ;<br/>
               }else{<br/>
                    sup-&gt;right = NULL ;<br/>
               }<br/>
               su-&gt;parent = NULL ;<br/>
          }<br/>
          root = su ;<br/>
          _BST_deallocate(pos) ;<br/>
          return ;<br/>
     }<br/><br/>
     PBNode pa = pos-&gt;parent ;//父节点<br/>
     //替换<br/>
     if ( pos == pa-&gt;left ) {<br/>
          pa-&gt;left = su ;<br/>
     }else{<br/>
          pa-&gt;right = su ;<br/>
     }<br/>
     if ( su ) {<br/>
          PBNode sup = su-&gt;parent ;<br/>
          if ( su == sup-&gt;left ) {<br/>
               sup-&gt;left = NULL ;<br/>
          }else{<br/>
               sup-&gt;right = NULL ;<br/>
          }<br/>
          su-&gt;parent = pa ;<br/>
     }<br/>
     _BST_deallocate(pos) ;<br/>
}<br/><br/>
void BinarySearchTree::Delete(ElemType d){<br/>
     Erase(Find(d)) ;<br/>
}<br/><br/>
void BinarySearchTree::_delete_node(PBNode p){<br/>
     if ( p != NULL ){<br/>
          _delete_node(p-&gt;left) ;<br/>
          _delete_node(p-&gt;right) ;<br/>
          _BST_deallocate(p) ;<br/>
     }<br/>
}<br/><br/>
void BinarySearchTree::Clear(){<br/>
     _delete_node(root) ;<br/>
     root = NULL ;<br/>
}<br/><br/><br/>
//测试代码<br/>
using namespace std;<br/><br/>
int main(){<br/>
     int a[] = {3,2,9,7,5,8,6} ;<br/>
     int b[10] ;<br/>
     int sz = sizeof(a) / sizeof(int)  ;<br/>
     int i;<br/>
     <br/>
     for ( i = 0 ; i &lt; sz ; i ++ ) b[i] = a[i] ;<br/><br/>
      _BST_initspace ;<br/><br/>
     //排序测试<br/>
     BinarySearchTree::Sort(a , sz , 1) ;<br/>
     for ( i = 0 ; i &lt; sz ; i ++ )cout&lt;&lt;a[i]&lt;&lt;' ' &lt;&lt;endl;<br/>
     <br/>
     BinarySearchTree tree ;<br/>
     for ( i = 0 ; i &lt; sz ; i ++ ){<br/>
          tree.Insert(a[i]) ;<br/>
     }<br/><br/>
     cout&lt;&lt;endl;<br/>
     cout&lt;&lt;tree.Find(4)&lt;&lt;endl;<br/><br/>
     cout&lt;&lt;endl;<br/>
     cout&lt;&lt;tree.Find(9)&lt;&lt;endl;<br/>
     cout&lt;&lt;tree.Find(9)-&gt;data&lt;&lt;endl;<br/>
     tree.Delete(9) ;<br/>
     cout&lt;&lt;tree.Find(9)&lt;&lt;endl;<br/><br/>
     cout&lt;&lt;endl;<br/>
     cout&lt;&lt;tree.Find(3)&lt;&lt;endl;<br/>
     cout&lt;&lt;tree.Retrieve(tree.Find(3))&lt;&lt;endl;<br/>
     tree.Clear() ;<br/>
     cout&lt;&lt;tree.Find(3)&lt;&lt;endl;     <br/><br/>
     return 0 ;<br/>
}
