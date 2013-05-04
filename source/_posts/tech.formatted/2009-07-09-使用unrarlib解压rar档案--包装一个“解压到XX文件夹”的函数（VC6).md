---
layout: post
title: "使用unrarlib解压rar档案--包装一个“解压到XX文件夹”的函数（VC6)"
date: 2009-07-09  14:21
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: 4411b8fb9c6d2a2b4e4aea0b.html
_baiduhi_category: Vc
---

(hplonline)2009.7.9<br/><br/>
今天早上看到的个贴子提到解压rar的问题。<br/>
说了三种方法：<br/><font color="#ff6600"><br/>
1.调用rar的命令行<br/>
2.使用rar相关的dll，unrar.dll</font><br/><font color="#ff6600">3.unrarlib</font><br/><br/>
法1，要求用户装有rar，虽然现在不装rar的电脑几乎没有，<br/>
但是总的说来显得不是很好。<br/><br/>
法2，据说自己的程序走到哪里都要拖着dll，不好看。<br/><br/>
法3，有相应的源码，可以直接放在自己的工程中使用，很方便。<br/><br/>
工程网站：<br/><a href="http://www.unrarlib.org/" target="_blank">http://www.unrarlib.org/</a><br/><br/>
去上面把源码下下来，把<br/>
unrarlib.h<br/>
unrarlib.c<br/>
包含在自己的工程里面就可以用了。<br/><br/>
\samples\很不错，里面有三个例子，基本上一看就明白的。<br/><br/><font color="#0000ff">完整程序：</font><br/><br/>
实现一个把指定档案解压到指定文件夹的函数UnComp<br/><br/>
#include &lt;windows.h&gt;<br/>
#include "unrarlib.h"<br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;stdlib.h&gt;<br/>
#include &lt;string.h&gt;<br/>
#include &lt;set&gt;<br/>
#include &lt;string&gt;<br/><br/>
#pragma warning(disable:4786)<br/><br/>
std::set&lt;std::string&gt; PathSet ;<br/><br/>
BOOL OutputFile(char *buffer , DWORD size , char *path) ;<br/>
BOOL CreateDir(char *path) ;<br/>
BOOL UnComp(char *rarfile , char *dir , char *password) ;<br/><br/>
int main(){<br/><br/>
     if ( UnComp("1.rar" , "1" , "password") == TRUE ){<br/>
          printf("\nsuccessfully done.\n") ;<br/>
     }else{<br/>
          printf("\nfail to uncompress it . \n") ;<br/>
          printf("be sure your archive is created by rar2.0\n") ;<br/>
          printf("and expected directory does not exist\n") ;<br/>
     }<br/><br/>
     return 0 ;<br/>
}<br/><br/>
BOOL OutputFile(char *buffer , DWORD size , char *path){<br/>
     FILE *fp = fopen(path , "wb") ;<br/>
     if ( !fp ){<br/>
          printf("error opening file") ;<br/>
          return FALSE ;<br/>
     }<br/>
     fwrite(buffer , size , 1 , fp) ;<br/>
     fclose(fp) ;<br/>
     return TRUE ;<br/>
}<br/><br/>
BOOL CreateDir(char *path){<br/>
     char temppath[MAX_PATH] ;<br/>
     int l = strlen(path) ;<br/>
     int i ;<br/>
     for ( i = l - 1 ; i &gt;= 0 ; i -- ) if (path[i] == '\\') break ;<br/>
     <br/>
     //base directory reached<br/>
     if (i &lt; 0) return TRUE ;<br/><br/>
     //create parent directory<br/>
     memcpy(temppath , path , i) ;<br/>
     temppath[i] = '\0' ;<br/><br/>
     //already created<br/>
     if (PathSet.count(temppath)){<br/>
          return TRUE ;<br/>
     }     <br/><br/>
     if ( CreateDir(temppath) == FALSE ){<br/>
          return FALSE ;<br/>
     }else{<br/>
          if ( CreateDirectory(temppath , NULL) == FALSE){<br/>
               return FALSE ;<br/>
          }else{<br/>
               PathSet.insert(temppath) ;<br/>
               return TRUE ;<br/>
          }<br/>
     }<br/>
}<br/><br/>
BOOL UnComp(char *rarfile , char *dir , char *password){<br/>
     PathSet.clear() ;<br/>
     ArchiveList_struct *list ;<br/>
     urarlib_list(rarfile , (ArchiveList_struct*) &amp;list) ;<br/>
     ArchiveList_struct *p = list ;<br/>
     while ( p ){<br/>
          //extract only when not directory<br/>
          if (p-&gt;item.FileAttr != 16){<br/>
               printf("now extracting %s ...",p-&gt;item.Name) ;<br/><br/>
               char *buffer ;<br/>
               DWORD size ;<br/>
               char path[MAX_PATH] ;<br/><br/>
               int ret = urarlib_get(&amp;buffer , &amp;size , p-&gt;item.Name , rarfile , password) ;<br/>
               if ( ret == FALSE ) {<br/>
                    printf("error getting file\n") ;<br/>
                    return FALSE ;<br/>
               }<br/>
               sprintf(path , "%s\\%s" , dir , p-&gt;item.Name) ;<br/>
               if ( CreateDir(path) == FALSE ){<br/>
                    printf("error creating path") ;<br/>
                    return FALSE ;<br/>
               }<br/>
               OutputFile(buffer , size , path) ;<br/>
               free(buffer) ;<br/><br/>
               printf("done!.\n") ;<br/>
          }<br/>
          p = p-&gt;next ;<br/>
     }<br/><br/>
     urarlib_freelist(list) ;<br/><br/>
     return TRUE ;<br/>
}<br/><br/><font color="#0000ff">提要：</font><br/><br/>
关于这套lib，就三个函数<img src="http://img.baidu.com/hi/jx/j_0011.gif"/>，所以说很容易使用嘛。<br/><br/>
urarlib_list<br/>
用来得到一个链表，存放了rar档案的所有文件的信息。<br/><br/>
urarlib_freelist<br/>
用来释放上面得到的链表。<br/><br/>
urarlib_get<br/>
用来得到档案中的某个文件。<br/><br/>
大体上的流程就是，得到文件链表，然后一个一个地提取出来，fwrite到该放他的地方。<br/><br/><font color="#0000ff">建立目录：</font><br/><br/>
整个提取流程很直观，唯一要考虑的就是建立目录的问题。<br/>
win32api的CreateDirectory只能在已经存在的目录下创建新的目录，<br/>
当目录存在的时候，就自动忽略。<br/><br/>
而观察过urarlib返回的list就知道，里面的文件并不一定是按照目录从浅到深排序的。<br/>
所以可能第一个文件的路径就是1\2\3\4.txt。<br/>
那么为了他，要先创建1，再创建1\2，然后是1\2\3，最后才能写入文件4.txt。<br/><br/>
这个任务就放在自己的<br/>
CreateDir<br/>
函数里面完成了。<br/><br/>
这个函数递归处理传进去的路径字符串，于是可以从浅到深地创建目录。<br/><br/>
其中用到了个stl里的PathSet，用来判断是否已经创建过该目录了，<br/>
是的话，就直接返回，避免重复创建。<br/>
(虽然重复调用CreateDirectory可以自动忽略存在的目录，<br/>
毕竟效率上会吃亏）<br/><br/><font color="#0000ff">用处：</font><br/><br/>
有的时候，想给自己的程序一起带上一些数据，<br/>
直接放在资源里面，消耗空间确实不少，<br/>
这下有了这套装备，就可以先压缩起来，<br/>
然后随时解压出来，由于是unrarlib是源码形式发布，<br/>
不用带上其他的东西，很清爽。<br/><br/><font color="#0000ff">缺点：</font><br/><br/><font color="#ff0000">由于这套库实在是比较老了，只支持到rar2.0</font>。。。<br/>
这就是个问题了，先不说压缩质量肯定不如后面的版本。<br/>
关键在于要找到rar2.0都是一个麻烦的事情。。<br/><br/>
还好，在<a href="http://hi.baidu.com/hplonline/blog/item/28f8b91b0207bf108718bf2e.html" target="_blank">上一篇</a>介绍的网站中，搜集到了。。<br/><br/>
另外一个就是函数的参数设计上，有点令人费解的地方：<br/><br/>
先看下声明：<br/>
extern int urarlib_list(void *rarfile, ArchiveList_struct *list);<br/><br/>
再看下调用：<br/>
     ArchiveList_struct *list ;<br/>
     urarlib_list(rarfile , (ArchiveList_struct*) &amp;list) ;<br/><br/>
是个人都会觉得很奇怪。。<br/>
首先，ArchiveList_struct是链表的节点。<br/>
在没有头节点的时候，要用一个头指针来维护，就是这里的list。<br/><br/>
这个list定义出来时，显然是随机值，<br/>
要依赖urarlib_list把他的值改成生成的链表的头指针。<br/><br/>
出于这个目的，于是应该传的不是指向ArchiveList_struct的指针，<br/>
而是一个指向指针的指针，从后面的&amp;list的位置也看得出来。<br/><br/>
而根据函数的参数列表，却还要先强制转换成ArchiveList_struct的指针。。。<br/><br/>
从这个函数的源码可以看到，里面有：<br/>
(*(DWORD*)list) = (DWORD)NULL;     <br/><br/>
也就是在里面，list还是先被转化成指向指针（DWORD）的指针，再赋值。。。<br/><br/>
嗯，很绕口。。这个设计确实不好看，不过由于这套库的配套sample很不错，能够看懂怎么用。<br/>
