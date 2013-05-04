---
layout: post
title: "贴一个海明码(HammingCode)"
date: 2009-05-12  18:58
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 2a2d953dfa177e08bba167d9.html
_baiduhi_category: 算法
---

(hplonline)2009.5.12<br/><br/>
海明码在通信网中的应用还是挺有价值的。<br/><br/>
总地说，这码就是在m长度的数据中，参杂r位的码，<br/>
这样，接收方收到后，可以在只有一位错误的情况下进行纠正。<br/><br/>
数据和码的排列是。二的整数次幂位置上放码，其他位置放数据，比如：<br/><br/>
123456789<br/><font color="#ff0000">rr</font>m<font color="#ff0000">r</font>mmm<font color="#ff0000">r</font>m<br/><br/>
注意下标是从1开始的，这点在后面编码的时候要特别注意，<br/>
因为我们常用的存储结构都是从开始编下标的。<br/><br/>
上面的整串按照下面的形式来写：<br/>
r1 , r2 , m3 , r4 , m5 , m6 , m7 , r8 , m9<br/><br/><font color="#0000ff">encode：</font><br/>
mi的值就是数据串依次排下来的结果。<br/>
定义与rj相关的mi是 i &amp; rj == 1 的所有mi。<br/>
于是rj就等于所有与他相关的mi的异或（模2加）。<br/><br/><font color="#0000ff">decode：</font><br/>
对每个rj，把他与跟他相关的mi异或。<br/>
k = sum{j : rj == 1}<br/>
那么k即为出错的位。<br/>
把该位上的数取反即可纠错。<br/><br/>
为0，表示没有出错。<br/>
如果a的值超过了整个串长，说明可能有多个位出错，此时的结果不可信。<br/>
（即使没有超过，也只在一位出错时可信，<br/>
当有一位以上出错的概率小到忽略是即可）<br/><br/><font color="#0000ff">原理比较明了：</font><br/>
考虑encode和decode其实是两个相反的过程。<br/>
encode的时候把相关的mi异或到了rj上面。<br/>
decode的时候又异或了一遍。<br/>
如果所有数据都没有改动，显然rj为0。<br/>
如果rj为1，并且我们假设了只有1位出错，则该位（或是r或是m）一定与rj相关。<br/>
而与rj1,rj2,rj3...都相关的位（或是r或是m）是唯一的。<br/>
因为j1,j2,j3...都是2的幂。<br/><font color="#0000ff"><br/><br/>
代码：</font><br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;string&gt;<br/>
#include &lt;iostream&gt;<br/><br/>
//using namespace std;<br/><br/>
//海明码由数据m和码r组成<br/>
//下标从1开始计算<br/>
//r占据的是2的整数次幂的下标<br/>
//m依次占据其他空位<br/><br/>
class HammingCode{<br/>
private:<br/>
      std::string data ;<br/>
      std::string code ;<br/>
      int hamminglength ;<br/>
      int calhamminglength(int l) ;//计算长度为l的串要多少位的码<br/>
      int calhamminglength2(int l) ;//计算长度为l的总串中有多少位是码<br/>
      int lowbit(int x) ;//得到的最低比特<br/>
      int nextn2power(int x) ;//下一个非2的幂的下标<br/>
public:<br/>
      HammingCode() ;<br/>
      ~HammingCode() ;<br/>
      void SetData(std::string s) ;<br/>
      void SetCode(std::string s) ;<br/>
      void Encode() ;<br/>
      bool Decode() ;<br/>
      std::string&amp; GetData() ;<br/>
      std::string&amp; GetCode() ;<br/>
      int GetHammingLength() ;<br/>
};<br/><br/>
//下一个非2的幂的下标<br/>
//2的幂的下标将存放海明码<br/>
int HammingCode::nextn2power(int x){<br/>
      do{<br/>
            x ++ ;<br/>
      }while ( lowbit(x) == x )  ;<br/>
      return x ;<br/>
}<br/><br/>
//得到的最低比特<br/>
int HammingCode::lowbit(int x){<br/>
      return x&amp;(-x) ;<br/>
}<br/><br/>
//1byte = 8bit ，使用4个位做海明码<br/>
int HammingCode::calhamminglength(int l){<br/>
      //纠错码纠错一位所需位数r满足：<br/>
      //l + r + 1 &lt;= 2 ^ r<br/>
      int r = 1 ;<br/>
      int pr = 2 ;<br/>
      while ( l + r + 1 &gt; pr ) {<br/>
            r = r + 1 ;<br/>
            pr &lt;&lt;= 1 ;<br/>
      }<br/>
      return r ;<br/>
}<br/><br/>
//计算长度为l的总串中有多少位是码<br/>
int HammingCode::calhamminglength2(int l){<br/>
      int r = 1 ;<br/>
      int pr = 2 ;<br/>
      while ( l &gt;= pr ) {<br/>
            r = r + 1 ;<br/>
            pr &lt;&lt;= 1 ;<br/>
      }<br/>
      return r ;<br/>
}<br/><br/>
HammingCode::HammingCode(){<br/><br/>
}<br/><br/>
HammingCode::~HammingCode(){<br/><br/>
}<br/><br/>
void HammingCode::SetData(std::string s){<br/>
      data = s ;<br/>
      hamminglength = calhamminglength(s.size()) ;<br/>
}<br/><br/>
void HammingCode::SetCode(std::string s){<br/>
      code = s ;<br/>
      hamminglength = calhamminglength2(s.size()) ;<br/>
}<br/><br/>
void HammingCode::Encode(){<br/>
      int i; <br/>
      int curpos = 1 ;//初始的数据放置点<br/>
      code.reserve(hamminglength + data.length()) ;<br/>
      code = "" ;<br/>
//      cout&lt;&lt;code.length()&lt;&lt;' '&lt;&lt;code.capacity()&lt;&lt;endl;<br/>
      //置0，因为0是异或操作的证同元素<br/>
      for ( i = 0 ; i &lt; hamminglength + data.length() ; i ++ ) {<br/>
            code += '\0' ;<br/>
      }<br/>
      //字符变化为数字<br/>
      for ( i = 0 ; i &lt; data.length() ; i ++ ) {<br/>
            data[i] -= '0' ;<br/>
      }<br/>
      //下面注意对code[x]引用的时候，string是从0开始的，所以要减1<br/>
      for ( i = 0 ; i &lt; data.length() ; i ++ ) {<br/>
            curpos = nextn2power(curpos) ;<br/>
            code[curpos - 1] = data[i] ;<br/>
            int tmp = curpos ;<br/>
            int lb ;<br/>
            //加到相关位上，即下标中2进制位为1的位上<br/>
            while ( tmp ) {<br/>
                  lb = lowbit(tmp) ;<br/>
                  code[lb - 1] ^= data[i] ;<br/>
                  tmp -= lb ;<br/>
            }<br/>
      }<br/>
      for ( i = 0 ; i &lt; data.length() ; i ++ ){<br/>
            data[i] += '0' ;<br/>
      }<br/>
      for ( i = 0 ; i &lt; code.length() ; i ++ ){<br/>
            code[i] += '0' ;<br/>
      }<br/>
}<br/><br/>
bool HammingCode::Decode(){<br/>
      int i ;<br/>
      int curpos = 1 ;<br/>
      int wpos = 0 ;//计算出错位<br/>
      data.reserve(code.length() - hamminglength) ;<br/>
      data = "" ;<br/>
      for ( i = 0 ; i &lt; code.length() ; i ++ ) {<br/>
            code[i] -= '0' ;<br/>
      }<br/>
      <br/>
      for ( curpos = 3 ; curpos &lt;= code.length() ; curpos = nextn2power(curpos) ){<br/>
      //      code[curpos - 1] = data[i] ;<br/>
            int tmp = curpos ;<br/>
            int lb ;<br/>
            //加到相关位上，即下标中2进制位为1的位上<br/>
            while ( tmp ) {<br/>
                  lb = lowbit(tmp) ;<br/>
                  code[lb - 1] ^= code[curpos - 1] ;<br/>
                  tmp -= lb ;<br/>
            }<br/>
      }<br/>
      <br/>
      for ( i = 1 ; i &lt;= code.length() ; i &lt;&lt;= 1 ){<br/>
            if ( code[i - 1] ) wpos += i ;<br/>
      }<br/><br/>
      //可能不止一位出错，解码失败<br/>
      if ( wpos &gt; code.length() ) return false ;<br/>
      if ( wpos ) code[wpos - 1] = !code[wpos - 1] ;<br/>
      <br/>
      data = "" ;<br/>
      for ( curpos = 3 ; curpos &lt;= code.length() ; curpos = nextn2power(curpos) ){<br/>
            data += code[curpos - 1] ;<br/>
      }<br/><br/>
      for ( i = 0 ; i &lt; code.length() ; i ++ ){<br/>
            code[i] += '0' ;<br/>
      }<br/>
      for ( i = 0 ; i &lt; data.length() ; i ++ ){<br/>
            data[i] += '0' ;<br/>
      }<br/>
      return true ;<br/>
}<br/><br/>
std::string&amp; HammingCode::GetData(){<br/>
      return data ;<br/>
}<br/><br/>
std::string&amp; HammingCode::GetCode(){<br/>
      return code ;<br/>
}<br/><br/>
int HammingCode::GetHammingLength(){<br/>
      return hamminglength ;<br/>
}<br/><br/>
//测试部分开始<br/>
using namespace std;<br/><br/>
int main(){<br/>
      string src = "11100010" ;<br/>
      string dst ;<br/>
      HammingCode hc ;<br/><br/>
      cout&lt;&lt;"original:"&lt;&lt;endl;<br/>
      cout&lt;&lt;src&lt;&lt;endl;<br/><br/>
      cout&lt;&lt;"hamming encoding:"&lt;&lt;endl;<br/>
      hc.SetData(src) ;<br/>
      hc.Encode() ;<br/>
      dst = hc.GetCode() ;<br/>
      cout&lt;&lt;dst&lt;&lt;endl;<br/>
      <br/>
      if ( dst[3] == '1' ) dst[3] = '0' ;<br/>
      else dst[3] = '1' ;<br/><br/>
      cout&lt;&lt;"modified by 1 bit:"&lt;&lt;endl;<br/>
      cout&lt;&lt;dst&lt;&lt;endl;<br/><br/>
      hc.SetCode(dst) ;<br/>
      hc.Decode() ;<br/>
      cout&lt;&lt;"hamming decoding:"&lt;&lt;endl;<br/>
      cout&lt;&lt;hc.GetData()&lt;&lt;endl;<br/>
      return 0 ;<br/>
}
