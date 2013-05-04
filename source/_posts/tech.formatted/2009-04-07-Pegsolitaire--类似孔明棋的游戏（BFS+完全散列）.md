---
layout: post
title: "Peg solitaire--类似孔明棋的游戏（BFS+完全散列）"
date: 2009-04-07  22:21
comments: true
categories: tech
tags: ["算法"]
_baiduhi_id: 691afd36243125390b55a981.html
_baiduhi_category: 算法
---

(hplonline) 2009.3.23<br/><br/>
看到有同学在做，当时正好顺便练手，就搞了一个出来。<br/><br/>
下面的字符宽度上看起来有点别扭，不过将就了吧。<br/><br/><h3 style="margin: 6pt 0cm;"><span style="font-size: 14pt;">Background</span></h3>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="color: rgb(51, 51, 0); display: none;"> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="color: rgb(51, 51, 0);">Peg solitaire is a traditional game, played with marbles (O) sat on wooden board. The game begins in some known state e.g.:</span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0);">. <span>       </span>. <span>       </span>O<span>        </span>. <span>       </span>.</span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0);">. <span>       </span>.<span>         </span>O<span>        </span>.<span>         </span>.</span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0);">O <span>      </span>O <span>      </span>. <span>       </span>O <span>      </span>O</span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0);">. <span>       </span>. <span>       </span>O <span>      </span>. <span>       </span>.</span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0);">. <span>       </span>. <span>       </span>O <span>      </span>. <span>       </span>.</span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0);">The pegs can take another peg by jumping it (as in draughts) going up, down, left or right. For the above board, the next board would look like:</span></p>
<table cellspacing="0" cellpadding="0" border="1" style="border: medium none ; border-collapse: collapse;" class="MsoNormalTable"><tbody><tr><td width="152" valign="top" style="border: 1pt solid windowtext; padding: 0cm 5.4pt; width: 114.15pt;">
            <p align="left" style="text-align: left;" class="MsoNormal"><span>. . .   . .</span></p>
            <p class="MsoNormal"><span>. . . . .</span></p>
            <p class="MsoNormal"><span>O O O O O</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>. . O . . </span></p>
            <p class="MsoNormal"><span> </span></p>
            </td>
            <td width="140" valign="top" style="border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; border-width: 1pt 1pt 1pt medium; padding: 0cm 5.4pt; width: 104.65pt;">
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>. . O O O</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span> </span></p>
            </td>
            <td width="152" valign="top" style="border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; border-width: 1pt 1pt 1pt medium; padding: 0cm 5.4pt; width: 114.1pt;">
            <p align="left" style="text-align: left;" class="MsoNormal"><span>. . O   . .</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>O O O O O</span></p>
            <p class="MsoNormal"><span>. . . . .</span></p>
            <p class="MsoNormal"><span>. . . . .</span></p>
            <p class="MsoNormal"><span> </span></p>
            </td>
            <td width="124" valign="top" style="border-style: solid solid solid none; border-color: windowtext windowtext windowtext -moz-use-text-color; border-width: 1pt 1pt 1pt medium; padding: 0cm 5.4pt; width: 93.2pt;">
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>O O O . .</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p class="MsoNormal"><span>. . O . .</span></p>
            <p align="left" style="text-align: left;" class="MsoNormal"><span> </span></p>
            </td>
        </tr></tbody></table><p class="MsoNormal"><span style="color: rgb(51, 51, 0); display: none;"> </span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0); display: none;"> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="color: rgb(51, 51, 0);">You are going to read in a 5<em>x</em>5 board and find the correct moves to return it to the completed state:</span></p>
<p class="MsoNormal"><span>. . . . .</span></p>
<p class="MsoNormal"><span>. . . . .</span></p>
<p class="MsoNormal"><span>. . O . .</span></p>
<p class="MsoNormal"><span>. . . . .</span></p>
<p class="MsoNormal"><span>. . . . .</span></p>
<br/><h3 style="margin: 6pt 0cm;"><span style="font-size: 14pt;">Requirements</span></h3>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0); display: none;"> </span></p>
<p align="left" style="text-align: left;" class="MsoNormal"><span style="color: rgb(51, 51, 0);">Write a program that:</span></p>
<p style="background: white none repeat scroll 0% 0%; margin-left: 18pt; text-indent: -18pt; line-height: 12pt; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;" class="MsoNormal"><span style="color: black;"><span>1.<span>          </span></span></span><span style="color: black;">Reads in a 5x5 board from a file, and checks that it is valid. Boards are specified in a file that has 5 lines of 5 characters each. Each character is either a full-stop or an uppercase ‘O’ (oh) or a lowercase ‘o’.</span></p>
<p style="background: white none repeat scroll 0% 0%; margin-left: 18pt; text-indent: -18pt; line-height: 12pt; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;" class="MsoNormal"><span style="color: black;"><span>2.<span>          </span></span></span><span style="color: black;">Prints out the correct solution (reverse order is fine) and running times. </span></p>
<p class="MsoNormal"><span style="color: rgb(51, 51, 0); display: none;"> </span></p>
<p style="margin: 0cm 0cm 0.0001pt; line-height: 12pt;"><span style="font-size: 10.5pt;">You must write your program in VC ++6.0 and create an executable code which will run on the University computer. </span></p>
<br/><font color="#0000ff">SOLUTION:</font><br/><br/>
这个数据量可谓很小很小，直接BFS。<br/><br/>
2^(5*5)的量的完全散列。<br/><br/>
跟一般做的OJ题目有点不同，就是需要验证输入，看看是否规范。<br/><br/><font color="#0000ff">CODE:</font><br/><br/>
#include &lt;stdio.h&gt;<br/>
#include &lt;string.h&gt;<br/>
#include &lt;time.h&gt;<br/><br/>
const int MAX_FILENAME_LEN = 50 ;<br/>
//add test files' name here<br/>
//all files in ".\testfiles" directory<br/>
const char *filenames[] = {<br/>
"a.txt",<br/>
"b.txt",<br/>
"c.txt",<br/>
"d.txt",<br/>
"e.txt",<br/>
"f.txt",<br/>
"g.txt",<br/>
"h.txt"<br/>
};<br/>
const int TEST_FILE_NUM = sizeof(filenames) / 4 ;<br/><br/>
const int MAX_HASH = 33554432 ;<br/>
const int MAX_LINE_LEN = 100 ;<br/>
const int MAX_QUEUE = MAX_HASH ;<br/><br/>
const int dx[4] = { 0 , 0 , 1 , -1 } ;<br/>
const int dy[4] = { 1 , -1 , 0 , 0 } ;<br/><br/>
typedef int STATE ;<br/><br/>
bool init(FILE *fp);<br/>
int hash(char c[5][5]);<br/>
bool process() ; <br/>
void output(STATE s);<br/>
void outsteps(int index) ;<br/><br/>
bool appeared[MAX_HASH] ;<br/>
STATE start , end ;//states <br/>
STATE q[MAX_QUEUE] ;<br/>
int from[MAX_QUEUE] ;<br/>
int front , rear ;//pointer for the queue <br/>
int stp ;<br/><br/><br/>
int main(){<br/>
       int i ;<br/>
       FILE *fp ; <br/>
       time_t tt ;<br/>
       bool ok ;<br/>
       char fullname[MAX_FILENAME_LEN] ;<br/>
       freopen( "output.txt" , "w" , stdout ) ;<br/>
       for ( i = 0 ; i &lt; TEST_FILE_NUM ; i ++ ){<br/>
              printf("\n=====now begin test case : %d\nfile name:%s\n" , i , filenames[i] ) ;<br/>
              strcpy( fullname , "testfiles\\" ) ;<br/>
              strcat(fullname , filenames[i]) ;<br/>
              fp = fopen( fullname , "r" ) ;<br/>
              if ( !fp ){<br/>
                     printf("can't read from file:%s\n" , filenames[i] ) ;<br/>
              }<br/>
              if ( !init(fp) ){<br/>
                     puts("file format error!!") ;<br/>
              }else{<br/>
                     puts("file validation passed!!") ;<br/>
                     puts("initial state:");<br/>
                     output(start);<br/>
                     puts("final state:");<br/>
                     output(end);<br/>
                     tt = clock() ;<br/>
                     ok = process() ;<br/>
                     printf("processing time %.2fs\n" , double( clock() - tt ) / CLOCKS_PER_SEC);<br/>
                     if ( ok ){;<br/>
                            puts("succeed !! steps are:");<br/>
                            stp = 1 ;<br/>
                            outsteps(front) ;<br/>
                     }else{<br/>
                            puts("no solution was found!") ;<br/>
                     }       <br/>
              }<br/>
              printf("========end of case %d\n\n" , i ) ;<br/>
       }<br/>
       return 0 ;<br/>
}<br/><br/>
//check if the file is valid <br/>
//and make initial and terminal state<br/>
//also , initialize some variants <br/>
//return :<br/>
//true : valid<br/>
//false: invalid<br/>
bool init(FILE *fp){<br/>
       char m[6][MAX_LINE_LEN] ; // raw data from files<br/>
       char c[5][5] ; // standardized data 0 for vacancies and 1 for pegs<br/>
       int i , j ;<br/>
       for ( i = 0 ; i &lt; 5 &amp;&amp; !feof(fp) ; i ++ ){<br/>
              fscanf( fp , "%s" , m[i] ) ;<br/>
       }<br/>
       if ( i != 5 ) return false ; // not enough lines<br/>
       for ( i = 0 ; i &lt; 5 ; i ++ ){<br/>
              for ( j = 0 ; j &lt; 5 ; j ++ ){<br/>
                     if ( m[i][j] == '.' ){<br/>
                            c[i][j] = 0 ;<br/>
                            continue ;<br/>
                     }<br/>
                     if ( m[i][j] == 'o' || m[i][j] == 'O' ){<br/>
                            c[i][j] = 1 ;<br/>
                            continue ;<br/>
                     }<br/>
                     return false ; //other symbols in the file<br/>
              }<br/>
              if ( m[i][j] != '\0' ) return false ; //more than 5 columns <br/>
       }<br/>
       if ( EOF !=       fscanf( fp , "%s" , m[5] ) ){<br/>
              if ( m[5][0] != '\0' ) return false ; //more than 5 rows<br/>
       }<br/>
       <br/>
       start = hash(c) ;<br/>
       end = 4096 ; // 2 ^ 12 <br/><br/>
       return true ;<br/>
}<br/><br/>
//caculate the hash key for a state<br/>
STATE hash(char c[5][5]){<br/>
       int i , j , t = 0 , b = 1 ;<br/>
       for ( i = 0 ; i &lt; 5 ; i ++ ){<br/>
              for ( j = 0 ; j &lt; 5 ; j ++ ){<br/>
                     if ( c[i][j] )<br/>
                            t |= b ;<br/>
                     b &lt;&lt;= 1 ;<br/>
              }<br/>
       }<br/>
       return t ;<br/>
}<br/><br/>
void rhash(char c[5][5] , STATE s ){<br/>
       int i , j ; <br/>
       for ( i = 0 ; i &lt; 5 ; i ++ ){<br/>
              for ( j = 0 ; j &lt; 5 ; j ++ ) {<br/>
                     c[i][j] = s &amp; 1 ;<br/>
                     s &gt;&gt;= 1 ;<br/>
              }<br/>
       }<br/>
}<br/><br/>
bool valid( int x , int y ){<br/>
       return x &gt;= 0 &amp;&amp; x &lt; 5 &amp;&amp; y &gt;= 0 &amp;&amp; y &lt; 5 ;<br/>
}<br/><br/>
bool process(){<br/>
       STATE curs , news ;<br/>
       char c[5][5] ;<br/>
       int x1 , y1 , x2 , y2 , x3 , y3 , k ;<br/>
       int fr ;<br/>
       front = 0 ;<br/>
       rear = 1 ;<br/>
       memset(appeared , false , sizeof(appeared) ) ;<br/>
       q[0] = start ;<br/>
       appeared[start] = true ;<br/>
       from[0] = -1 ;<br/>
       while ( front &lt; rear ) {<br/>
              fr = front ;<br/>
              curs = q[front ++ ] ;<br/>
       //       output(curs);<br/>
              if ( curs == end ) break ; <br/>
              rhash( c , curs ) ;<br/>
              for ( x1 = 0 ; x1 &lt; 5 ; x1 ++ ){<br/>
                     for ( y1 = 0 ; y1 &lt; 5 ; y1 ++ )if ( c[x1][y1] ){<br/>
                            c[x1][y1] = 0 ;<br/>
                            for ( k = 0 ; k &lt; 4 ; k ++ ){<br/>
                                   x2 = x1 + dx[k] ;<br/>
                                   y2 = y1 + dy[k] ;<br/>
                                   if ( valid(x2 , y2) &amp;&amp; c[x2][y2]){<br/>
                                          c[x2][y2] = 0 ;<br/>
                                          x3 = x2 + dx[k] ;<br/>
                                          y3 = y2 + dy[k] ;<br/>
                                          if (valid( x3 , y3 ) &amp;&amp; !c[x3][y3] ) {<br/>
                                                 c[x3][y3] = 1 ;<br/>
                                                 news = hash(c) ;<br/>
                                          //       output(news);<br/>
                                                 if ( !appeared[news] ){<br/>
                                                        appeared[news] = true ;<br/>
                                                        from[rear] = fr ;<br/>
                                                        q[rear ++ ] = news ;<br/>
                                                 }<br/>
                                                 c[x3][y3] = 0 ;<br/>
                                          }<br/>
                                          c[x2][y2] = 1 ;<br/>
                                   }<br/>
                            }              <br/>
                            c[x1][y1] = 1 ;<br/>
                     }<br/>
              }<br/>
       }<br/>
       if ( curs == end ){<br/>
              front -- ;<br/>
              return true ;<br/>
       }<br/>
       else return false ;<br/>
}<br/><br/>
//output single state<br/>
void output(STATE s){<br/>
       char c[5][5] ;<br/>
       int i , j ; <br/>
       rhash( c , s ) ;<br/>
       for ( i = 0 ; i &lt; 5 ; i ++ ){<br/>
              for ( j = 0 ; j &lt; 5 ; j ++ ){<br/>
                     printf("%d ",c[i][j] ) ;<br/>
              }<br/>
              printf("\n");<br/>
       }<br/>
       printf("\n");<br/>
}<br/><br/>
//output the moving steps<br/>
void outsteps(int index){<br/>
       if ( index != -1 ){<br/>
              outsteps(from[index]) ;<br/>
              printf("step %d:\n",stp) ;<br/>
              stp ++ ;<br/>
              output(q[index]);<br/>
       }<br/>
}<br/><br/><br/>
在<a href="http://www.box.net/shared/bivh8xgvgv" target="_blank">这里</a>取得完整的工程文件和，测试文件。<br/><p style="background: white none repeat scroll 0% 0%; margin-left: 18pt; text-indent: -18pt; line-height: 12pt; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;" class="MsoNormal"> </p>
<br/><p style="background: white none repeat scroll 0% 0%; margin-left: 18pt; text-indent: -18pt; line-height: 12pt; -moz-background-clip: -moz-initial; -moz-background-origin: -moz-initial; -moz-background-inline-policy: -moz-initial;" class="MsoNormal"> </p>
