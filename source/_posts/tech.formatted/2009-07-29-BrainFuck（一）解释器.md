---
layout: post
title: "BrainFuck（一）解释器"
date: 2009-07-29  12:05
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: bd4524dd46d4fed08c102968.html
_baiduhi_category: c&c++
---

(hplonline)2009.7.29<br/><br/>
前天听说了brainfuck这种强大的语言，<br/>
在fuck自己brain的同时也fuck别人的brain。<br/><font color="#0000ff"><br/>
从网上摘抄一段描述：</font><br/><em><br/>
这种语言基于一个简单的机器模型，除了指令，这个机器还包括：一个以字节为单位、被初始化为零的数组、一个指向该数组的指针(初始时指向数组的第一个字节)、以及用于输入输出的两个字节流。<br/>
下面是这八种状态的描述，其中每个状态由一个字符标识：<br/>
字符 含义 <br/>
＞ 指针加一 <br/>
＜; 指针减一 <br/>
+ 指针指向的字节的值加一 <br/>
- 指针指向的字节的值减一 <br/>
. 输出指针指向的单元内容(ASCII码) <br/>
, 输入内容到指针指向的单元(ASCII码) <br/>
[ 如果指针指向的单元值为零，向前跳转到对应的]指令的次一指令处 <br/>
] 如果指针指向的单元值不为零，向后跳转到对应的[指令的次一指令处 </em>          <br/><br/>
规则简单，则变化更为灵活多样，就像围棋一样。<br/><br/>
前面若干条都很好理解，<br/>
最后两条的话，用C的循环去对应，就能想通了：<br/><br/><font color="#ff6600">[</font> while (*ptr) {<br/><font color="#ff6600">] </font>} <br/><br/>
在以上指令的基础上，为了能够进行调试，<br/>
我自己加一个'@'，用来输出当前整个数组的情况。<br/><font color="#0000ff"><br/>
我的解释器：</font><br/><br/>
网上有不少地方提到编译器，总觉得听上去有点别扭，<br/>
看他们所干的事情实际上就是解释的功能，<br/>
甚至连函数名都是interpret之类的。<br/><br/>
我这个解释器的一个特点是用STL实现，<br/>
所以那个数组可以是任意伸缩的。<br/>
但是由于在语言的定义里面没有规范数组下标为负的情况，<br/>
所以遇到的时候，仅仅是简单报告错误。<br/><br/>
第二个特点就是没有用递归实现[]。<br/>
由于[]在逻辑行为上很像while循环，<br/>
我在网上看到过的一份代码就是采用每次找到一对括号，<br/>
把这段截取成一个新的字符串，然后递归调用执行。<br/>
我是直接从上面的定义出发，让程序按照那样的规定跳转。<br/>
在实际操作上，先用map&lt;string::iterator , string::iterator&gt;<br/>
的结构把匹配的括号保存下来，即可实现高速查找配对括号的位置。<br/>
而这个预处理只占用一次线性的时间。<br/><br/>
第三个也将就算个特点，就是忽略空格、tab、换行这些字符。<br/>
于是可以把程序写得更有结构一点。。<br/><br/><font color="#0000ff">代码：</font><br/><br/>
#pragma warning(disable:4786)<br/><br/>
#include &lt;iostream&gt;<br/>
#include &lt;fstream&gt;<br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;stack&gt;<br/>
#include &lt;list&gt;<br/>
#include &lt;string&gt;<br/>
#include &lt;map&gt;<br/><br/>
using namespace std ;<br/><br/>
bool work_brackets(string &amp;code , map&lt;string::iterator , string::iterator&gt; &amp;brackets){<br/>
       stack&lt;string::iterator&gt; st ;<br/>
       string::iterator it ;<br/><br/>
       brackets.clear() ;<br/>
       while ( !st.empty() ) st.pop() ;<br/>
       for ( it = code.begin() ; it != code.end() ; it ++ ){<br/>
              if ( *it == '[' ){<br/>
                     st.push(it) ;       <br/>
              }<br/>
              if ( *it == ']' ){<br/>
                     if ( st.empty() ) return false ;//brackets unbalanced<br/>
                     brackets[it] = st.top() ;<br/>
                     brackets[st.top()] = it ;<br/>
                     st.pop() ;<br/>
              }<br/>
       }<br/><br/>
       if ( st.empty() ) return true ;<br/>
       else return false ;<br/>
}<br/><br/>
void interpret(string &amp;code){<br/>
       list&lt;char&gt;::iterator pointer ;<br/>
       list&lt;char&gt;::iterator tmpit ;<br/>
       list&lt;char&gt; array ;<br/>
       map&lt;string::iterator , string::iterator&gt; brackets ;<br/><br/>
       if ( !work_brackets(code , brackets) ){<br/>
              cerr&lt;&lt;"brackets is unbalanced"&lt;&lt;endl ;<br/>
              return ;<br/>
       }<br/><br/>
       array.clear() ;<br/>
       array.push_back(char(0)) ;<br/>
       pointer = array.begin() ;<br/>
       string::iterator it = code.begin();<br/><br/>
       while ( it != code.end() ){<br/>
              switch(*it){<br/>
              case '+': <br/>
                     ++ *pointer ;<br/>
                     break ;<br/>
              case '-':<br/>
                     -- *pointer ;<br/>
                     break ;<br/>
              case '&lt;': <br/>
                     if ( pointer != array.begin() ) {<br/>
                            -- pointer ;<br/>
                     }else{<br/>
                            cerr&lt;&lt;"pointer down overflow"&lt;&lt;endl ;<br/>
                     }<br/>
                     break ;<br/>
              case '&gt;': <br/>
                     tmpit = pointer ;<br/>
                     ++ tmpit ;<br/>
                     if ( tmpit == array.end() ){<br/>
                            array.push_back(char(0)) ;<br/>
                     }<br/>
                     ++pointer ;<br/>
                     break ;<br/>
              case '[': <br/>
                     if ( *pointer == 0 ) {<br/>
                            it = brackets[it] ;<br/>
                     }<br/>
                     break ;<br/>
              case ']': <br/>
                     if ( *pointer != 0 ) {<br/>
                            it = brackets[it] ;<br/>
                     }<br/>
                     break ;<br/>
              case '.': <br/>
                     cout.put(*pointer) ;<br/>
                     break ;<br/>
              case ',': <br/>
                     *pointer = cin.get() ;<br/>
                     break ;<br/>
              case '@':<br/>
                     cout&lt;&lt;endl&lt;&lt;"-----------memory:"&lt;&lt;endl ;<br/>
                     for ( tmpit = array.begin() ; tmpit != array.end() ; tmpit ++ ){<br/>
                            if ( tmpit == pointer ){<br/>
                                   cout&lt;&lt;'('&lt;&lt;int(*tmpit)&lt;&lt;") " ;<br/>
                            }else{<br/>
                                   cout&lt;&lt;int(*tmpit)&lt;&lt;' ' ;<br/>
                            }<br/>
                     }<br/>
                     cout&lt;&lt;endl&lt;&lt;"-----------end of memory"&lt;&lt;endl ;<br/>
                     break ;<br/>
              default:<br/>
                     if ( strchr("        \r\n" , *it) ){<br/>
                            //ignore blanks<br/>
                     }else{<br/>
                            cerr&lt;&lt;endl&lt;&lt;"bad charactor ("&lt;&lt;*it&lt;&lt;") in file"&lt;&lt;endl; <br/>
                     }<br/>
                     break ;<br/>
              }<br/>
              it ++ ;<br/>
       }<br/>
       cout&lt;&lt;endl&lt;&lt;"program end."&lt;&lt;endl;<br/>
}<br/><br/><br/>
int main(int argc , char* argv[]){<br/>
       string code ;<br/>
       string tmp ;<br/>
       ifstream fin(argv[1]) ;<br/><br/>
       if ( fin.is_open() ){<br/>
              code = "" ;<br/>
              while ( !fin.eof() ){<br/>
                     fin&gt;&gt;tmp ;<br/>
                     code += tmp ;<br/>
              }<br/>
              interpret(code) ;<br/>
       }else{<br/>
              cout&lt;&lt;"file open error"&lt;&lt;endl; <br/>
       }<br/>
       return 0 ;<br/>
}<br/><br/><font color="#0000ff">一个样例：</font><br/><br/>
&gt;+++++++<font color="#ff0000">@</font>++[&lt;++++++++&gt;-]&lt;.&gt;++++<br/>
+++[&lt;++++&gt;-]&lt;+.+++++++..+++.[-]&gt;++++++++[&lt;++++&gt;-]&lt;.<br/>
&gt;+++++++++++[&lt;+++++&gt;-]&lt;.&gt;++++++++[&lt;+++&gt;-]&lt;.+++.------.--------.[-]<br/>
&gt;++++++++[&lt;++++&gt;-]&lt;+.[-]++++++++++.<br/><br/>
保存成一个文件，把文件名用第一参数传给上面的解释器就行了。<br/>
如：bf 1.txt<br/><br/>
结果：<br/><br/>
-----------memory:<br/>
0 (7)<br/>
-----------end of memory<br/>
Hello World!<br/><br/>
program end.<br/><br/>
除了标红的@是我自己加进去的便于调试的东西外，<br/>
这段程序就是网上很流行的那个hello world。<br/>
其中每一段调试信息输出都由-------分节。<br/><br/>
数组是从左到右输出，带有括号的表示当前指针所指向的单元。<br/><br/>
这下把这个小东西做好了<img src="http://img.baidu.com/hi/jx/j_0015.gif"/>，就可以耍一耍这种哦哦那个语言了。。
