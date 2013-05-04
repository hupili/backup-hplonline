---
layout: post
title: "SplayTree(伸展树，自顶向下的实现）"
date: 2009-06-01  15:59
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: a3fb9913c36f28886438db60.html
_baiduhi_category: 算法
---

(hplonline)2009.6.1<br/><br/>
代码基本上是照着别人的写出来的。<br/><br/>
主要还是自顶向下的伸展过程，在实现上真有点纠结。<br/>
现在假设已经有了splay(d , p)的过程。<br/>
表示把值为d的元素伸展到以p为根的树根处。<br/>
那么基于这个操作，可以很方便完成以下内容：<br/><br/><font color="#0000ff">insert:</font><br/>
先把对待插元素d做一个splay。<br/>
这时如果根的值和d相等，那么说明d在树里了。<br/>
否则的话，建立新根，令其值为d。<br/>
如果d小于旧根的值，<br/>
把旧根的左枝给新根做左枝，旧根的左枝为空，<br/>
把旧根作为新根的右枝。<br/>
另一种情况同理。<br/><br/><font color="#0000ff">delete:</font><br/>
先对待删元素d做一个splay。<br/>
如果根的值不为d，那么啥都不做。<br/>
如果根的两端均为空，那么直接删除，令新根为空。<br/>
如果只有一端为空，那么把根移向不为空的子树，删除原来的。<br/>
如果两端都有内容，那么在根的左边对值d做一次splay，<br/>
做完后，得到的p是原来左枝上最大的值，他的右端肯定为空。<br/>
于是把旧根的右枝挂到p的右枝上，删除旧根，p为新根。<br/><font color="#0000ff"><br/>
nextnode:</font><br/>
------<br/>
这个函数要完成的是找根节点的下一节点。<br/>
找任意节点的下一节点的话，只需要先对“任意节点”进行一次查找，<br/>
则“任意节点”会位于根的位置，那么调用该函数即可。<br/>
----------<br/>
对根的右枝，按照根的值做一次splay。<br/>
这样得到的p为右枝上最小的，他没有左枝，<br/>
把旧根挂到p的左枝上，旧根的右枝令为空。<br/>
把新根令为p，即完成。<br/><br/>
剩下的就看代码吧，顺便找找bug<img src="http://img.baidu.com/hi/jx/j_0019.gif"/>。<br/>
随便跑了下，感觉不是很快的样子喃。。<img src="http://img.baidu.com/hi/jx/j_0016.gif"/>有待进一步测试。<br/><br/><font color="#0000ff">代码：</font><br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;stdlib.h&gt;<br/><br/>
//元素类型<br/>
typedef int ElemType ;<br/><br/>
//树的节点<br/>
struct SNode{<br/>
      ElemType data ;<br/>
      SNode *left , *right ;<br/>
};<br/>
typedef SNode *PSNode ;<br/><br/>
//空间分配宏，便于实现其他配置方式<br/>
#define _S_initspace <br/>
#define _S_allocate() (SNode *)malloc(sizeof(SNode))<br/>
#define _S_deallocate(p) free(p) <br/>
//SNode space[200000] , *spacehead ;<br/>
//#define _S_initspace spacehead = space <br/>
//#define _S_allocate() spacehead++ ;<br/>
//#define _S_deallocate(p) <br/><br/>
//S<br/>
class SplayTree{<br/>
private:<br/>
      ElemType INFINITE , NEG_INFINITE ;<br/>
      PSNode root ;<br/>
      SNode nil_node ; //空节点<br/>
      PSNode nil ;<br/>
      void _delete_node(PSNode p) ;<br/>
      PSNode _rotate_left(PSNode p) ;//左旋<br/>
      PSNode _rotate_right(PSNode p) ;//右旋<br/>
      PSNode _splay(ElemType d , PSNode p) ;//伸展<br/>
      void _in_order(PSNode p) ;//p节点的中序遍历<br/>
      void _pre_order(PSNode p) ;//p节点的前序遍历<br/>
public:      <br/>
      SplayTree() ;//构造空树<br/>
      ~SplayTree() ;//销毁树<br/>
      PSNode Find(ElemType d) ;//查找元素，<br/>
      PSNode FindMax() ;//查找最大元素，<br/>
      PSNode FindMin() ;//查找最小元素，<br/>
      ElemType&amp; Retrieve(PSNode p) ;//获取元素<br/>
      PSNode Insert(ElemType d) ;//插入元素<br/>
      void Delete(ElemType d) ;//按元素删除<br/>
      void Erase(PSNode p) ;//按节点位置删除<br/>
      void Clear() ;//清除整棵树<br/>
      void InOrder() ; //中序遍历<br/>
      void PreOrder() ; //前序遍历<br/>
      PSNode Nil() ;//返回空节点，便于调用端判断边界条件<br/>
      static void Sort(ElemType a[] , int n , int d = 1) ;//利用S进行排序，静态函数<br/>
      void SetInfinite(ElemType inf , ElemType ninf) ;//设置极值<br/>
      bool NextNode() ;//根的后继节点，返回是否存在后继<br/>
      bool PrevNode() ;//根的前驱节点<br/>
      PSNode Root() ;//返回根<br/>
} ;<br/><br/>
PSNode SplayTree::Nil(){<br/>
      return nil ;<br/>
}<br/><br/>
PSNode SplayTree::Root(){<br/>
      return root ;<br/>
}<br/><br/>
//d：1，从小到大，0，从大到小<br/>
void SplayTree::Sort(ElemType a[] , int n , int d){<br/>
      SplayTree tree ;<br/>
      int i ;<br/>
      for ( i = 0 ; i &lt; n ; i ++ ){<br/>
            tree.Insert(a[i]) ;<br/>
      //      tree.InOrder() ;<br/>
      //      tree.PreOrder() ;<br/>
      }<br/>
//      tree.InOrder() ;<br/>
//      tree.PreOrder() ;<br/>
      for ( i = 0 ; i &lt; n ; i ++ ){<br/>
            PSNode p ;<br/>
            if ( d ) {<br/>
                  p = tree.FindMin() ;<br/>
            }else{<br/>
                  p = tree.FindMax() ;      <br/>
            }<br/>
            a[i] = tree.Retrieve(p) ;<br/>
            tree.Erase(p) ;<br/>
      }<br/>
}<br/><br/>
SplayTree::SplayTree(){<br/>
      nil = &amp;nil_node ;<br/>
      root = nil ;<br/>
      nil_node.left = nil ;<br/>
      nil_node.right = nil ;<br/>
      //利用ElemType的默认构造函数创建极值<br/>
      ElemType *p = new ElemType ;<br/>
      INFINITE = *p ;<br/>
      NEG_INFINITE = *p ;<br/>
      delete p ;<br/>
}<br/><br/>
void SplayTree::SetInfinite(ElemType inf , ElemType ninf){<br/>
      INFINITE = inf ;<br/>
      NEG_INFINITE = ninf ;<br/>
}<br/><br/>
SplayTree::~SplayTree(){<br/>
      Clear() ;<br/>
}<br/><br/>
void SplayTree::_in_order(PSNode p){<br/>
      if ( p != nil ) {<br/>
            _in_order(p-&gt;left) ;<br/>
            std::cout&lt;&lt;p-&gt;data&lt;&lt;' ' ;<br/>
            _in_order(p-&gt;right) ;<br/>
      }<br/>
}<br/><br/>
void SplayTree::_pre_order(PSNode p){<br/>
      if ( p != nil ) {<br/>
            std::cout&lt;&lt;p-&gt;data&lt;&lt;' ' ;<br/>
            _pre_order(p-&gt;left) ;<br/>
            _pre_order(p-&gt;right) ;<br/>
      }      <br/>
}<br/><br/>
void SplayTree::InOrder(){<br/>
      _in_order(root) ;<br/>
      std::cout&lt;&lt;std::endl;<br/>
}<br/><br/>
void SplayTree::PreOrder(){<br/>
      _pre_order(root) ;<br/>
      std::cout&lt;&lt;std::endl;<br/>
}<br/><br/>
bool SplayTree::NextNode(){<br/>
      PSNode newroot = root-&gt;right ;<br/>
      if ( newroot != nil ){<br/>
            newroot = _splay(root-&gt;data , newroot) ;<br/>
            newroot-&gt;left = root ;<br/>
            root-&gt;right = nil ;<br/>
            root = newroot ;<br/>
            return true ;<br/>
      }<br/>
      return false ;<br/>
}<br/><br/>
bool SplayTree::PrevNode(){<br/>
      PSNode newroot = root-&gt;left ;<br/>
      if ( newroot != nil ){<br/>
            newroot = _splay(root-&gt;data , newroot) ;<br/>
            newroot-&gt;right = root ;<br/>
            root-&gt;left = nil ;<br/>
            root = newroot ;<br/>
            return true ;<br/>
      }<br/>
      return false ;      <br/>
}<br/><br/>
PSNode SplayTree::Find(ElemType d){      <br/>
      return root = _splay(d , root) ;<br/>
}<br/><br/>
PSNode SplayTree::FindMax(){<br/>
      return root = _splay(INFINITE , root) ;<br/>
}<br/><br/>
PSNode SplayTree::FindMin(){<br/>
      return root = _splay(NEG_INFINITE , root) ;<br/>
}<br/><br/>
ElemType&amp; SplayTree::Retrieve(PSNode p){<br/>
      if ( p != nil ) <br/>
            return p-&gt;data ;<br/>
      else return nil-&gt;data ;<br/>
}<br/><br/>
//左旋<br/>
PSNode SplayTree::_rotate_left(PSNode p){<br/>
      PSNode child = p-&gt;right ;<br/>
      p-&gt;right = child-&gt;left ;<br/>
      child-&gt;left = p ;<br/>
      return child ;<br/>
}<br/><br/>
//右旋<br/>
PSNode SplayTree::_rotate_right(PSNode p){<br/>
      PSNode child = p-&gt;left ;<br/>
      p-&gt;left = child-&gt;right ;<br/>
      child-&gt;right = p ;<br/>
      return child ;<br/>
}<br/><br/>
PSNode SplayTree::_splay(ElemType d , PSNode p){<br/>
      //(1)left:待完成的树左子树，他的右子树为空<br/>
      //(2)通过移动，可以把left视为右子树为空的树串成的链表<br/>
      //left为左子树中的最大值（因为右子树为空）<br/>
      PSNode left , right ;<br/>
      //为了满足(1)，设置一个header，他初始的时候左右均空<br/>
      SNode header ;<br/>
      header.left = nil ;<br/>
      header.right = nil ;<br/>
      //而left和right均从header开始出发<br/>
      //(3)当left离开header的时候，left的右端挂上的肯定是当前树的左端<br/>
      left = &amp;header ;<br/>
      right = &amp;header ;<br/><br/>
      nil-&gt;data = d ;//(4)避免在空节点处发生双旋<br/><br/>
      while ( p-&gt;data != d ){<br/>
            if ( d &lt; p-&gt;data ){<br/>
                  if ( d &lt; p-&gt;left-&gt;data ) { // 当p-&gt;left为nil时，条件自动不成立，见(4)<br/>
                        p = _rotate_right(p) ; //同个方向前进，应该双旋<br/>
                  }<br/>
                  if ( p-&gt;left == nil ) break ;//节点查找失败，但p已经为新节点应当的插入点了。<br/>
                  right-&gt;left = p ;<br/>
                  right = p ;<br/>
                  p = p-&gt;left ;<br/>
            }else{<br/>
                  if ( p-&gt;right-&gt;data &lt; d ) {<br/>
                        p = _rotate_left(p) ;<br/>
                  }<br/>
                  if ( p-&gt;right == nil ) break ;<br/>
                  left-&gt;right = p ;<br/>
                  left = p ;<br/>
                  p = p-&gt;right ;<br/>
            }<br/>
      }<br/><br/>
      //p已经是我们要的节点了。他为新的根<br/>
      left-&gt;right = p-&gt;left ;//left的右端是空的,见(1)<br/>
      right-&gt;left = p-&gt;right ;<br/>
      //将header左右子树链接到p上面<br/>
      p-&gt;left = header.right ;//head的右端是新根的左端，见(3)<br/>
      p-&gt;right = header.left ;<br/>
      return p ;<br/>
}<br/><br/>
PSNode SplayTree::Insert(ElemType d){      <br/>
      //根为空<br/>
      if ( root == nil ) {<br/>
            root = _S_allocate() ;<br/>
            root-&gt;left = nil ;<br/>
            root-&gt;right = nil ;<br/>
            root-&gt;data = d ;<br/>
            return root ;<br/>
      }<br/>
      root = _splay(d , root) ;<br/>
      //已经存在<br/>
      if ( d == root-&gt;data ) return root ;<br/>
      PSNode p = _S_allocate() ;<br/>
      p-&gt;data = d ;<br/>
      if ( d &lt; root-&gt;data ){<br/>
            p-&gt;right = root ;<br/>
            p-&gt;left = root-&gt;left ;<br/>
            root-&gt;left =nil ;<br/>
      }else{<br/>
            p-&gt;left = root ;<br/>
            p-&gt;right = root-&gt;right ;<br/>
            root-&gt;right = nil ;<br/>
      }<br/>
      return root = p ;<br/>
}<br/><br/>
void SplayTree::Erase(PSNode pos){<br/>
      Delete(pos-&gt;data) ;<br/>
}<br/><br/>
void SplayTree::Delete(ElemType d){<br/>
      root = _splay(d , root) ;<br/>
      if ( root-&gt;data == d ){<br/>
            PSNode tmp = root ;<br/>
            if ( root-&gt;left == nil ){//有可能无左子树<br/>
                  root = root-&gt;right ;<br/>
            }else{<br/>
                  //伸展得到的是左树的最大节点，他无右子树<br/>
                  PSNode newroot = root-&gt;left ;<br/>
                  newroot = _splay(d , newroot) ;<br/>
                  newroot-&gt;right = root-&gt;right ;<br/>
                  root =newroot ;<br/>
            }<br/>
            _S_deallocate(tmp) ;<br/>
      }<br/>
}<br/><br/>
//容易栈溢<br/>
void SplayTree::_delete_node(PSNode p){<br/>
      if ( p != nil ){<br/>
            _delete_node(p-&gt;left) ;<br/>
            _delete_node(p-&gt;right) ;<br/>
            _S_deallocate(p) ;<br/>
      }<br/>
}<br/><br/>
void SplayTree::Clear(){<br/>
//      _delete_node(root) ;<br/>
      if ( root == nil ) return ;<br/>
      FindMin() ;<br/>
      while ( root-&gt;right != nil ){<br/>
            PSNode tmp = root ;<br/>
            root = root-&gt;right ;<br/>
            _S_deallocate(tmp) ;<br/>
      }<br/>
      _S_deallocate(root) ;<br/>
      root = nil ;<br/>
}<br/><br/><br/>
//测试代码<br/>
using namespace std;<br/>
#include &lt;algorithm&gt;<br/>
#include &lt;time.h&gt;<br/><br/>
const TOTAL = 200000 ;<br/>
int c[TOTAL] ;<br/><br/>
int main(){<br/><br/>
      int a[] = {3,2,9,7,5,8,6} ;<br/>
//      int a[] = {5 , 2 , 3} ;<br/>
      int b[10] ;<br/>
      int sz = sizeof(a) / sizeof(int)  ;<br/>
      int i;<br/><br/>
      //初始化空间<br/>
       _S_initspace ;<br/><br/>
      for ( i = 0 ; i &lt; sz ; i ++ ) b[i] = a[i] ;<br/><br/>
      //排序测试<br/>
      SplayTree::Sort(a , sz , 1) ;<br/>
      for ( i = 0 ; i &lt; sz ; i ++ )cout&lt;&lt;a[i]&lt;&lt;' ';<br/>
      cout&lt;&lt;endl;<br/>
      <br/>
      SplayTree tree ;<br/>
      tree.SetInfinite(1000000000 , -1000000000) ;//重要，在查找最值时用到<br/><br/>
      //插入，删除，中序遍历，空树测试<br/>
/*      tree.Insert(1) ;<br/>
      tree.InOrder() ;<br/>
      tree.Insert(1) ;<br/>
      tree.InOrder() ;<br/>
      tree.Delete(1) ;<br/>
      tree.InOrder() ;<br/>
*/<br/>
      //插入测试，根据中序和前序，可以构造出整树，来检验插入是否正确<br/>
      for ( i = 0 ; i &lt; sz ; i ++ ){<br/>
            tree.Insert(a[i]) ;<br/>
            tree.InOrder() ;<br/>
            tree.PreOrder() ;<br/>
      }<br/>
      cout&lt;&lt;endl;<br/><br/>
//      return 0 ;<br/><br/>
      //查找测试<br/>
      //不存在元素<br/>
      cout&lt;&lt;tree.Find(4)&lt;&lt;endl;<br/>
      cout&lt;&lt;endl;<br/>
      //存在的元素<br/>
      cout&lt;&lt;tree.Find(9)&lt;&lt;endl;<br/>
      cout&lt;&lt;tree.Find(9)-&gt;data&lt;&lt;endl;<br/>
      //删除元素<br/>
      tree.Delete(9) ;<br/>
      cout&lt;&lt;tree.Find(9)&lt;&lt;endl;<br/><br/>
      tree.InOrder() ;<br/>
      tree.PreOrder() ;<br/><br/>
      //清除测试<br/>
      cout&lt;&lt;endl;<br/>
      cout&lt;&lt;tree.Find(3)&lt;&lt;endl;<br/>
      cout&lt;&lt;tree.Retrieve(tree.Find(3))&lt;&lt;endl;<br/>
      tree.Clear() ;<br/>
      cout&lt;&lt;tree.Find(3)&lt;&lt;endl;      <br/>
      tree.PreOrder() ;<br/><br/>
//大数据测试<br/>
      for ( i = 0 ; i &lt; TOTAL ; i ++ ) c[i] = i ; <br/>
      random_shuffle(c , c + TOTAL) ;<br/>
//      可选择输出数据检验      <br/>
//      for ( i = 0 ; i &lt; TOTAL ; i ++ ) cout&lt;&lt;c[i]&lt;&lt;' ' ;<br/>
//      cout&lt;&lt;endl;<br/>
//      return 0 ;<br/>
      clock_t tt = clock() ;<br/>
//      _S_initspace ;<br/>
//      SplayTree::Sort(c , TOTAL , 1) ;<br/>
      tree.Clear() ;<br/>
      for ( i = 0 ; i &lt; TOTAL ; i ++ ){<br/>
            tree.Insert(c[i]) ;<br/>
      }<br/>
      tree.FindMin() ;<br/>
      for ( i = 0 ; i &lt; TOTAL ; i ++ ){<br/>
            c[i] = tree.Root()-&gt;data ;<br/>
            tree.NextNode() ;<br/>
      }<br/>
      printf("time: %d\n" , clock() - tt) ;<br/>
      for ( i = 0 ; i &lt; TOTAL ; i ++ ) if ( c[i] != i ) break; <br/>
      if ( i == TOTAL ) cout&lt;&lt;"ok"&lt;&lt;endl;<br/>
      else cout&lt;&lt;"bad alg!"&lt;&lt;endl;<br/><br/>
      return 0 ;<br/>
}
