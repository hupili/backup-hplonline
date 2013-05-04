---
layout: post
title: "Apache+Asp.Net的基本配置记录"
date: 2010-05-06  22:11
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 5de264066e5c9677030881a4.html
_baiduhi_category: Network
---

(hplonline)2010.5.6<br/><br/><font color="#0000ff">一。下载</font><br/><br/>
Apache下载：<a target="_blank" href="http://httpd.apache.org/download.cgi">http://httpd.apache.org/download.cgi</a><br/>
（我下的是2.2.15）<br/><br/>
Mod_AspdotNet下载：<a target="_blank" href="http://sourceforge.net/projects/mod-aspdotnet/">http://sourceforge.net/projects/mod-aspdotnet/</a><br/>
（官方<a target="_blank" href="http://httpd.apache.org/modules/">表示</a>开发人员不够，停止对这个模块的开发，<br/>
所以到原作者SourceForge的页面下载）<br/><br/><font color="#0000ff">二。安装</font><br/><br/>
其实没啥好说的，<br/>
不过在VISTA下面折腾UAC是一件囧事，<br/>
反正害得我第一次安是失败的。<br/><br/>
按照默认的参数安了，<br/>
访问<a target="_blank" href="http://localhost/">http://localhost/</a>，<br/>
应该可以看到<font color="#ff0000"> It works</font>的字样，就OK了。<br/><br/><font color="#0000ff">三。基本配置</font><br/><br/>
我刚一装好，到处想找诸如IIS那样的界面，<br/>
比如在什么地方填下目录，在什么地方配置下别名等。<br/>
结果显然是没找到。<br/>
唯一的一个GUI就是Monitor，<br/>
其功能也就是开启/停止/重启服务器这些。。<br/><br/>
其配置全部都浓缩在httpd.conf这个文件里了，<br/>
默认的路径应该是：<br/><font color="#ff9900">C:\Program Files\Apache Software Foundation\Apache2.2\conf\httpd.conf</font><br/>
用记事本打开即可，<br/>
vista同样要注意UAC的问题，<br/>
要不修改了保存不了。。<br/><br/>
修改几个地方即可呈现基本的页面。<br/>
设网站放在 d:\web，默认页面是index.htm。<br/><font color="#ff00ff">紫色</font>是原内容，可以先ctrl+f到，然后修改。<br/>
每修改一处，可以用monitor restart一下server看效果。<br/><br/><font color="#ff00ff">DocumentRoot "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs"</font><br/>
DocumentRoot "d:/web"<br/><br/><font color="#ff00ff">&lt;Directory "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs"&gt;</font><br/>
&lt;Directory "d:/web"&gt;<br/><br/>
在第二处的上面有句话：<br/><font color="#38761d"># This should be changed to whatever you set DocumentRoot to.</font><br/>
所以很显然地把两个路径改成一样。。<br/><br/>
有了这两个之后，输入完整路径，应该可以访问d:\web下的东西了。<br/><br/>
紧接着第二处的地方：<br/><font color="#ff00ff">Options Indexes FollowSymLinks</font><br/>
Options -Indexes FollowSymLinks<br/><br/>
这样，服务器不会列出目录。<br/><br/>
再往下走：<br/><font color="#ff00ff">DirectoryIndex index.html</font><br/>
DirectoryIndex index.htm index.html <br/><br/>
当访问目录的时候，自动导向的页面填在这里。<br/><br/>
最后随便找个地方添句话：<br/><font color="#ff0000">AddDefaultCharset GB2312</font><br/><br/>
否则，直接访问localhost而定向到的index.htm可能是乱码。<br/><br/><font color="#0000ff">四。Asp.Net</font><br/><br/><a target="_blank" href="http://weblogs.asp.net/israelio/archive/2005/09/11/424852.aspx">译自文章</a>。<br/><br/>
在httpd.conf后面添加内容：<br/>
-------------<br/><p class="MsoNormal" style="color: navy;"><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;"><font color="#009f00">#asp.net</font> <br/>
LoadModule aspdotnet_module "modules/mod_aspdotnet.so" </span></font></p>
<p class="MsoNormal" style="color: navy;"><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;">AddHandler asp.net asax ascx ashx asmx aspx axd config cs csproj licx rem resources resx soap vb vbproj vsdisco webinfo <br/></span></font><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;"><br/>
&lt;IfModule mod_aspdotnet.cpp&gt; <br/></span></font><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;">  <font color="#009f00"># Mount the ASP.NET /asp application <br/></font>  AspNetMount /SampleASP "c:/SampleASP" <br/><font color="#009f00">#/SampleASP is the alias name for asp.net to execute <br/>
#"c:/SampleASP" is the actual execution of files/folders  in that location </font></span></font></p>
<p class="MsoNormal" style="color: navy;"><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;">  <font color="#009f00"># Map all requests for /asp to the application files <br/></font>  Alias /SampleASP "c:/SampleASP" <br/><font color="#009f00">#maps /SampleASP request to "c:/SampleASP" <br/>
#now to get to the /SampleASP type </font><a href="http://localhost/SampleASP"><font color="#009f00">http://localhost/SampleASP</font></a><font color="#009f00"> <br/>
#It'll redirect </font><a href="http://localhost/SampleASP"><font color="#009f00">http://localhost/SampleASP</font></a><font color="#009f00"> to "c:/SampleASP"</font></span></font></p>
<p class="MsoNormal" style="color: navy;"><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;"> <font color="#009f00"> # Allow asp.net scripts to be executed in the /SampleASP example <br/></font>  &lt;Directory "c:/SampleASP"&gt; <br/>
Options FollowSymlinks ExecCGI <br/>
Order allow,deny <br/>
Allow from all <br/>
DirectoryIndex index.htm index.aspx <br/><font color="#009f00">#default the index page to .htm and .aspx <br/></font>  &lt;/Directory&gt; </span></font></p>
<p class="MsoNormal" style="color: navy;"><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;">  <font color="#009f00"># For all virtual ASP.NET webs, we need the aspnet_client files <br/>
# to serve the client-side helper scripts. <br/></font>  AliasMatch /aspnet_client/system_web/(\d+)_(\d+)_(\d+)_(\d+)/(.*) "C:/Windows/Microsoft.NET/Framework/v$1.$2.$3/ASP.NETClientFiles/$4" <br/>
&lt;Directory "C:/Windows/Microsoft.NET/Framework/v*/ASP.NETClientFiles"&gt; <br/>
Options FollowSymlinks <br/>
Order allow,deny <br/>
Allow from all <br/>
&lt;/Directory&gt; <br/></span></font><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;">&lt;/IfModule&gt; <br/></span></font><font face="Arial" color="navy" size="2"><span style="font-size: 10pt;"><font color="#009f00">#asp.net</font> </span></font></p>
------------<br/><br/>
在C:\SampASP\ 下面创建index.aspx<br/><br/>
------------<br/><br/>
&lt;%@ Page Language="VB" %&gt; <br/>
&lt;html&gt; <br/>
&lt;head&gt; <br/>
&lt;link rel="stylesheet"href="intro.css"&gt; <br/>
&lt;/head&gt; <br/>
&lt;body&gt; <br/>
&lt;center&gt; <br/>
&lt;form action="index.aspx" method="post"&gt; <br/>
&lt;h3&gt; Name: &lt;input id="Name" type=text&gt; <br/>
Category:  &lt;select id="Category" size=1&gt; <br/>
&lt;option&gt;One&lt;/option&gt; <br/>
&lt;option&gt;Two&lt;/option&gt; <br/>
&lt;option&gt;Three&lt;/option&gt; <br/>
&lt;/select&gt; <br/>
&lt;/h3&gt; <br/>
&lt;input type=submit value="Lookup"&gt; <br/>
&lt;p&gt; <br/>
&lt;% Dim I As Integer <br/>
For I = 0 to 7 %&gt; <br/>
&lt;font size="&lt;%=I%&gt;"&gt; Sample ASP.NET TEST&lt;/font&gt; &lt;br&gt; <br/>
&lt;% Next %&gt; <br/>
&lt;/form&gt; <br/>
&lt;/center&gt; <br/>
&lt;/body&gt; <br/>
&lt;/html&gt;<br/><br/>
---------------<br/><br/>
重启服务器，访问地址：<strong><font face="Arial" color="navy" size="2"><a title="http://localhost/SmartASP/index.aspx" href="http://localhost/SampleASP/index.aspx"><strong>http://localhost/SampleASP/index.aspx</strong></a></font></strong><br/><br/><span><img border="0" src="http://hiphotos.baidu.com/hplonline/pic/item/a2f68d01f6cb2bef267fb500.jpg" small="0" class="blogimg"/></span><br/><br/><br/>
这个路径居然是区分大小写的。。<br/><br/><font color="#0000ff">五。评论：</font><br/><br/>
一开始摸不着头脑，<br/>
一旦摸着了感觉很方便。<br/>
在vista下折腾了很久的iis7，<br/>
总是遇到各种诡异的问题。<br/><br/>
纯文本的配置方式很不错，<br/>
不管是修改起来还是备份配置都是很方便。<br/><br/>
服务器主程序加ASP.NET模块总共不超过6M。<br/><br/>
