---
layout: post
title: "一套win下的perl工作环境（cygwin，e-texteditor，参数解决方案）"
date: 2010-10-17  23:37
comments: true
categories: tech
tags: ["Linux"]
_baiduhi_id: 3695942fbb0c63371f30899a.html
_baiduhi_category: Linux
---

(hplonline)2010.10.17<br/><br/><font color="#0000ff">》》背景</font><br/><br/>
自从在公司被逼着用了perl之后，就有点习惯了。<br/>
有时候想处理点小东西，第一反映居然是用perl。<br/>
处理点字符串和简单的统计确实比较方便，<br/>
以前做mcm的时候如果会这东西，<br/>
在数据的搜集和预处理上，应该要提高不少效率。<br/><br/>
今天在xq和auxten的帮助下，搞了套perl的工作环境。<br/>
以后要用ruby、python什么的，也比较类似。<br/><br/><font color="#0000ff">》》下载</font><br/><br/>
e:<br/><br/><a target="_blank" href="http://www.cehx.com/portal.php?mod=view&amp;aid=12205">E-TextEditor v1.0.39(crack)</a><br/><br/>
cygwin:<br/><br/><a target="_blank" href="http://cygwin.com/win-9x.html">CygWin-legacy</a> 里面的setup-legacy.exe下下来配置。<br/>
（e需要旧的cygwin支持）<br/><br/><font color="#0000ff">》》cygwin</font><br/><br/>
一路默认下去，直到选择要安装的组件。<br/>
中间镜像可以添个，<br/>
http://mirrors.sohu.com/cygwin<br/><br/>
可以安装的组件比较多，除了默认的，<br/>
把gcc，perl，还有其他一些小工具安上。<br/>
反正后面用到缺少哪个命令的时候，<br/>
随时回头来安装就行了。<br/><br/><font color="#0000ff">》》e-texteditor</font><br/><br/>
这编辑器做得不错，就是名字太短，“e”。<br/>
名字短本身也不是什么大的缺陷，<br/>
但是在各个地方搜索的时候，经常无法召回。<br/>
毕竟TFIDF还是IR这方面的基础，<br/>
e貌似又是英文中出现频率最高的字母，囧。<br/><br/>
界面就下面这样子：<br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/c0f979f095919de7a50f52a1.jpg"/></span><br/><span><br/>
一般编辑器该有的功能都有，像tab，普通快捷键这些。<br/>
最大的这块是编辑区域，下面是脚本执行后的输出。<br/>
e的撤销确实比较nb，保存文件重启e之后，还可以进行撤销操作。<br/><br/>
左边是Bundle的编辑。<br/>
Bundle就是一些模版(snippet)或者命令(command)的集合，<br/>
可以对应上相应的触发词或者快捷键。<br/>
通过编辑bundle可以扩充这个编辑器的功能。<br/>
扩充snippet是编辑器本身支持的，但要用comman的需要cygwin的支持。<br/>
测试cygwin是否有效：edit-&gt;settings-&gt;UNIX-&gt;show version information<br/><br/>
下面看下bundle的样子，<br/>
左边是bundle浏览器，展开了perl的if..elsif..else模版。<br/>
右边就是这个模版的内容。<br/><br/>
里面的$1-9是几个编辑位置。<br/>
snippet展开后，首先到$1，<br/>
编辑完第一个位置，直接tab就可以到$2。<br/>
这样可以大大缩短打括号再方向键切回来的时间。<br/><br/><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/4f3587b10c818e1c082302a1.jpg"/></span><br/><br/>
在代码中输入触发词，“ifee”，按下tab，<br/>
展开上面所示的那个模版如下：<br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/dff197164a686819f2de32a1.jpg"/></span><br/><br/>
其中#号后面的只是提示词，输入任意字符后就消失。<br/>
you needn't bother to delete them manually..<br/><br/>
再看下command的样子，<br/>
下面这个就是perl下面的run script命令。<br/>
不过不是原版的，是我修改过后的样子。<br/><br/><span><img border="0" class="blogimg" small="0" src="http://hiphotos.baidu.com/hplonline/pic/item/63614d1049800fb4c2ce79a1.jpg"/></span><br/><br/>
scope selector是指定作用域，比如目前这个就是在perl源码里面都有效。<br/>
command本质是一个shell脚本，里面可以引用很多环境变量，和linux命令。<br/>
TM_SCOPE 常量中记载了光标目前所处的作用域，<br/>
可以识别出函数名、行首tab等等语法上的关键位置。<br/>
编辑高级功能的时候，自己把这个常量打出来就知道可以用的有哪些了。<br/><br/>
另外一个可以关注的output这里，指定命令执行后输出的方式。<br/>
可以把输出直接插入到到文本中，或者替换一段文本。<br/>
这样就给了很大的发挥空间，用command做出更复杂的编辑。<br/>
但像run script这样的功能，我们就是想看下标准输出。<br/>
可惜的是，e没有提供output as plaintext的方式，<br/>
所以在输出成html之前要做处理，后面详述。<br/><br/>
关于bundle更多的信息，可以参考<a target="_blank" href="http://www.e-texteditor.com/wiki/index.php/Bundles">官方帮助页</a>。<br/>
很短，读完差不多就可以个性化自己的编辑器了。<br/><br/><font color="#0000ff">》》perl解释设置</font><br/><br/>
安装好后，perl默认的run script是这样的：<br/><br/><font color="#ff9900">export TM_RUBY=$(type -p "${TM_RUBY:-ruby}")<br/>
"${TM_RUBY}" -- "$TM_BUNDLE_SUPPORT/PerlMate/perlmate.rb"</font><br/><br/>
如果cygwin也ok，把ruby安装好，可以直接运行。<br/><br/>
不过这样一个中转之后，实在是太慢，<br/>
并且ruby中转过的输出页面很丑陋。<br/><br/>
其实在command的Evironment中选择Cygwin(generic)之后，直接下面就行了：<br/><font color="#ff9900">/usr/bin/perl ${TM_FILEPATH}</font><br/>
后面这个环境变量是被调用文件的绝对路径。<br/>
这个用法与在实际linux中无异。<br/><br/>
其实我倾向更简洁一点的写法：<br/><font color="#ff9900">${TM_FILEPATH}</font><br/>
在perl脚本的首行，加上解释器路径即可：<br/><font color="#ff9900">#!/usr/bin/perl -w</font><br/><br/>
这样弄好后，运行没问题了，不过输出会没有换行。<br/>
因为这个版本的e只提供了输出为html的方式，<br/>
所以必须手动使用&lt;br /&gt;标签去换行；<br/>
或者也可以试试&lt;pre&gt;&lt;/pre&gt;标签。<br/><br/>
我这里直接把\r\n或者\n替换为&lt;br /&gt;，<br/>
那么run script命令就是这样了：<br/><font color="#ff9900">${TM_FILEPATH} | perl -npe's/\r?\n/&lt;br \/&gt;/g' </font><br/><br/>
把输出解决之后，基本上就可以用了。<br/>
剩下一个问题，就是要传入参数怎么办。<br/>
实际用的时候可以手动输入，<br/>
但在编辑+调试阶段，每次都去命令行也不方便。<br/><br/>
想了个变相的方法。<br/>
如果决定给自己的脚本带参数，<br/>
就在同目录下写个&lt;filename&gt;.args的文件，<br/>
把要带的参数写在这个文件里面即可。<br/>
这样，run script脚本就先判断一下，是否有args这个文件。<br/>
最终的代码如下：<br/><br/><font color="#ff9900">if [[ -e ${TM_FILEPATH}.args ]] ; then<br/>
perl_arg_line=`head -n1 ${TM_FILEPATH}.args`<br/>
${TM_FILEPATH} ${perl_arg_line} | perl -npe's/\r?\n/&lt;br \/&gt;/g' <br/>
else <br/>
${TM_FILEPATH} | perl -npe's/\r?\n/&lt;br \/&gt;/g' <br/>
fi </font><br/><br/><font color="#ff0000">(2010.10.22,update)</font><br/><br/>
前面的虽然对于换行没有问题了，但是中文支持上不好。<br/>
即使用run script默认的ruby脚本，output出来的中文还是有问题。<br/>
经过测试，应该是e的那个输出显示窗口的毛病，<br/>
直接输出到文件的结果是对的。<br/>
所以改一下，重定向脚本输出到*.stdout,*.stderr，<br/>
最后调用e自己打开这两个文件就是了。<br/><br/>
先在cygwin下面ln -s给e的可执行文件建一个软连接，<br/>
我这里是/bin/e-texteditor，<br/><br/>
echo "begin running script&lt;/br&gt;"<br/>
if [[ -e ${TM_FILENAME}.args ]] ; then<br/>
perl_arg_line=`head -n1 ${TM_FILENAME}.args`<br/>
./${TM_FILENAME} ${perl_arg_line} 1&gt;${TM_FILENAME}.stdout 2&gt;${TM_FILENAME}.stderr<br/>
else <br/>
./${TM_FILENAME} 1&gt;${TM_FILENAME}.stdout 2&gt;${TM_FILENAME}.stderr<br/>
fi <br/>
e-texteditor ${TM_FILENAME}.stderr<br/>
e-texteditor ${TM_FILENAME}.stdout<br/>
echo "running script complete&lt;/br&gt;"<br/><br/><br/><font color="#0000ff">》》cygwin shell</font><br/><br/>
用cygwin.bat打开的shell比较丑，<br/>
疼哥给了个很暴力的方法：<br/>
在cygwin中安上sshd，然后securecrt去连自己机器。<br/><br/>
先还是用setup-legacy.exe装上sshd这个组件。<br/>
配置方法，就按照<a target="_blank" href="http://www.baidu.com/baidu?wd=cygwin+sshd&amp;tn=monline_dg">网上讲的</a>即可。<br/>
sshd会开启成为windows的系统服务，<br/>
还会添加上一个特殊的用户。<br/><br/>
登陆的时候用的是自己的windows账户。<br/>
