---
layout: post
title: "generating RFC content with the help of VIM&#39;s plugins(taglist.vim+txt.vim)"
date: 2010-01-10  14:05
comments: true
categories: tech
tags: ["Linux"]
_baiduhi_id: 6d3387101823680a203f2edb.html
_baiduhi_category: Linux
---

(hplonline)2010.1.10<br/><br/>
(..I found my installed ubuntu an English version without Chinese IMEs ...<br/>
I'll try to solve it later . Now , it's OK to just work without Chinese words ,<br/>
for most of the  materials we get from internet are in English ..<br/>
this is the FIRST blog under Linux .)<br/><br/>
A few months ago , when I started to read RFCs , I found it's disturbing <br/>
switching from chapter to chapter . But we can do nothing , since all the <br/>
documents are in plain text ... One thing I tried hard to do is CTRL+F from <br/>
here to there . Another is writting a toy program ( <a href="http://hi.baidu.com/hplonline/blog/item/b7f4a2d39e567e3e960a1659.html" target="_blank">see here</a> ..) to generate <br/>
contents for these documents .<br/><br/>
Yesterday , I came across the idea PLUGINs . So I surfed pages of www.vim.org<br/>
to hunt for some interesting ones . The one named txt.vim flashed in front <br/>
of my eyes . It look like this when installed properly . take <a href="http://www.ietf.org/rfc/rfc3000.txt" target="_blank">RFC3000</a> for example :<br/><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/1d1e3bad1dd9fa384a36d636.jpg" small="0" class="blogimg"/></span><br/><br/>
you can now jump to a topic by just moving the cursor to the headlines and <br/>
pressing RETURN . What's more , I defined some function keys F5-F8 to <br/>
operate the taglist's bar easily (see notes below) . <br/><br/>
It seems one can define syntax rules for further use of this plugin <br/>
with a variety of txt formats .<br/><br/><font color="#0000ff">my NOTES today :</font><br/><br/>
&gt;&gt;help analyze plain text <br/><br/>
download:<br/><br/><a href="http://www.vim.org/scripts/script.php?script_id=2899" target="_blank">http://www.vim.org/scripts/script.php?script_id=2899</a><br/><br/>
the 'txt.txt' in the zip archive shows <br/>
exactly how to install the plugin in chapter 3.<br/><br/>
it needs to install taglis first ..<br/>
so I turned to taglist<br/><br/>
download:<br/><br/><a href="http://www.vim.org/scripts/script.php?script_id=273" target="_blank">http://www.vim.org/scripts/script.php?script_id=273</a><br/><br/>
however , when vim is launched , I get this message ..<br/><br/><font color="#ff0000">Taglist: Exuberant ctags (http://ctags.sf.net) not found in PATH. Plugin is not loaded.</font><br/><br/>
so I install the ctags :<br/><br/><font color="#ff9900">sudo apt-get install exuberant-ctags</font><br/><br/>
&gt;&gt;about plugins<br/><br/>
vim plugins are all in ~/.vim/plugin . <br/>
the subdirectory is not that important .<br/>
vim will search the whole plugin directory for that . <br/><br/>
but to FILETYPE plugins , vim should associate the <br/>
filetype with the plugin's name . so , the three <br/>
available ways look like this:<br/><font color="#ff9900">    ftplugin/&lt;filetype&gt;.vim<br/>
ftplugin/&lt;filetype&gt;_&lt;name&gt;.vim<br/>
ftplugin/&lt;filetype&gt;/&lt;name&gt;.vim</font><br/><br/>
&gt;&gt;about removing plugins<br/><br/>
simply to remove the related files from doc/ or plugin/ , <br/>
like *.vim in plugin/ , *.txt in doc/<br/><br/>
&gt;&gt;taglis operation:(from mannual , listed here for quick reference)<br/><br/>
&lt;CR&gt;          Jump to the location where the tag under cursor is<br/>
defined.<br/>
o             Jump to the location where the tag under cursor is<br/>
defined in a new window.<br/>
P             Jump to the tag in the previous (Ctrl-W_p) window.<br/>
p             Display the tag definition in the file window and<br/>
keep the cursor in the taglist window itself.<br/>
t             Jump to the tag in a new tab. If the file is already<br/>
opened in a tab, move to that tab.<br/>
Ctrl-t        Jump to the tag in a new tab.<br/>
&lt;Space&gt;       Display the prototype of the tag under the cursor.<br/>
For file names, display the full path to the file,<br/>
file type and the number of tags. For tag types, display the<br/>
tag type and the number of tags.<br/>
u             Update the tags listed in the taglist window<br/>
s             Change the sort order of the tags (by name or by order)<br/>
d             Remove the tags for the file under the cursor<br/>
x             Zoom-in or Zoom-out the taglist window<br/>
+             Open a fold<br/>
-             Close a fold<br/>
*             Open all folds<br/>
=             Close all folds<br/>
[[            Jump to the beginning of the previous file<br/>
&lt;Backspace&gt;   Jump to the beginning of the previous file<br/>
]]            Jump to the beginning of the next file<br/>
&lt;Tab&gt;         Jump to the beginning of the next file<br/>
q             Close the taglist window<br/>
&lt;F1&gt;          Display help<br/><br/>
&gt;&gt;setup accelerated keys <br/>
add these lines in the file $HOME/.vimrc<br/><br/><font color="#ff9900">nmap &lt;F8&gt; &lt;ESC&gt;:TlistOpen&lt;RETURN&gt;<br/>
nmap &lt;F7&gt; &lt;ESC&gt;:TlistClose&lt;RETURN&gt;<br/>
nmap &lt;F6&gt; &lt;ESC&gt;:Tlist&lt;RETURN&gt;<br/>
nmap &lt;F5&gt; &lt;ESC&gt;:TlistUpdate&lt;RETURN&gt;</font><br/><br/>
I even add another function key :<br/><font color="#ff9900">nmap &lt;F2&gt; &lt;ESC&gt;:w&lt;RETURN&gt;</font><br/>
in my memory of high school  times..<br/>
it's the key I used most frequently . ( free PASCAL's convetion)<br/>
like CTRL+S in word ,  F2 is very important for saving our works . <br/>
And as coder , when I get stuck in thoughts , it's the only 'safe' key<br/>
to press as I wish . This may be a bad habit like children biting their <br/>
pencils when thinking  . However , it's hard to get rid of it .<br/>
