---
layout: post
title: "C中的Trigraphs"
date: 2010-06-18  21:12
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: c5d58d942f014813d31b70de.html
_baiduhi_category: c&c++
---

(hplonline)2010.6.18<br/><br/>
今天又在论坛火星地发现一个东西了。。<br/>
先来个加强版的demo：<br/><font color="#ff00ff"><br/>
#include &lt;stdio.h&gt;<br/><br/>
int main()??&lt;<br/>
printf("??!") ;<br/>
printf("%d" ,  1 ??' 0) ;<br/>
return 0 ;<br/>
??&gt;</font><br/><br/><font color="#0000ff">》》转：关于Trigraphs</font><br/><br/>
Trigraphs<br/>
The source character set of C source programs is contained within the 7-bit ASCII character set but is a superset of the ISO 646-1983 Invariant Code Set. Trigraph sequences allow C programs to be written using only the ISO (International Standards Organization) Invariant Code Set. Trigraphs are sequences of three characters (introduced by two consecutive question marks) that the compiler replaces with their corresponding punctuation characters. You can use trigraphs in C source files with a character set that does not contain convenient graphic representations for some punctuation characters.<br/><br/>
Table 1.1 shows the nine trigraph sequences. All occurrences in a source file of the punctuation characters in the first column are replaced with the corresponding character in the second column.<br/><br/>
Table 1.1   Trigraph Sequences<br/><br/>
Trigraph Punctuation Character<br/>
??= #<br/>
??( [<br/>
??/ \<br/>
??) ]<br/>
??’ ^<br/>
??&lt; {<br/>
??!  |<br/>
??&gt; }<br/>
??-  ~<br/><br/><br/>
A trigraph is always treated as a single source character. <font color="#ff0000">The translation of trigraphs takes place in the firsttranslation phase</font>, before the recognition of escape characters in string literals and character constants. Only the nine trigraphs shown in Table 1.1 are recognized. All other character sequences are left untranslated.<br/><br/>
The character escape sequence, \?, prevents the misinterpretation of trigraph-like character sequences. (For information about escape sequences, see Escape Sequences.) For example, if you attempt to print the string What??! with this printf statement<br/><br/>
printf( "What??!\n" );<br/><br/>
the string printed is What| because ??! is a trigraph sequence that is replaced with the | character. Write the statement as follows to correctly print the string:<br/><br/>
printf( "What?\?!\n" );<br/><br/>
In this printf statement, a backslash escape character in front of the second question mark prevents the misinterpretation of ??! as a trigraph.<br/><br/><br/>
上面标红的这个first translation phase很关键！<br/>
编译器对trigraphs的解析是在所有动作之前的，<br/>
甚至在对转义字符“\“的前面。<br/>
所以转文附带了一个在问号前加转义的例子。<br/>
又正由于这个特性，<br/>
连前后大小括号也可以这么替代。。。<br/>
于是就出现了上面这个长的很别扭的程序。<br/><br/>
据说是因为以前有些键盘没有这些符号才这样搞的，<br/>
但这应该是很早很早以前的事了吧。。
