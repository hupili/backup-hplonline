---
layout: post
title: "MATRIX LIB (pure C)"
date: 2009-11-23  13:06
comments: true
categories: tech
tags: ["c","c++"]
_baiduhi_id: 6d338710a500ff0b203f2eba.html
_baiduhi_category: c&c++
---

<p>(hplonline)2009.11.23</p>
<p><font color="#0000ff">BACKGROUND:</font></p>
<p><a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/ede99845db316435869473c9.html">CLAPACK</a> is efficient but <a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/0832b63e5cd883f0838b1386.html">hard to use</a>.<br/>
We often care about a few of its returning values.<br/>
So I wrapped functions for eigenvectors , eigenvalues and solving linear equation here.<br/>
BTW , some basic operation must be realised first ,<br/>
like CREATE , COPY , DESTROY ...<br/>
This results in about 650 lines pure C code , <br/>
appearing like a simple MATRIX LIB .</p>
<p>Any bug report is welcome .</p>
<p><font color="#0000ff">CODE :</font></p>
<p><font color="#ff9900">/*matrix_lib.h*/</font></p>
<p>#ifndef __H_MATRIX_LIB_<br/>
#define __H_MATRIX_LIB_</p>
<p>typedef struct mat_type{<br/>
 int height ;<br/>
 int width ;<br/>
 double **space ;<br/>
}MAT ;</p>
<p>int _toint(double d) ;</p>
<p>MAT m_create(int iHeight , int iWidth);<br/>
void m_destroy(MAT *pM);<br/>
void m_copy(MAT *pMdst , MAT *pMsrc);<br/>
MAT m_get(MAT *pM , MAT *pRow , MAT *pCol);<br/>
void m_set(MAT *pMdst , MAT *pRow , MAT *pCol , MAT *pMsrc);<br/>
void m_add(MAT *pMdst , MAT *pMsrc);<br/>
MAT m_multiply(MAT *pM1 , MAT *pM2);<br/>
void m_scale(MAT *pM , double k);<br/>
MAT m_repmat(MAT *pM , int iHeight , int iWidth);<br/>
MAT m_sort(MAT *pM);<br/>
MAT m_zeros(int iHeight , int iWidth);<br/>
MAT m_ones(int iHeight , int iWidth);<br/>
MAT m_eye(int iHeight , int iWidth);<br/>
void m_print(MAT *pM);<br/>
int m_solve(MAT *pA , MAT *pb , MAT *px) ;<br/>
void m_inv(MAT *pM);<br/>
int m_eig(MAT *pM , MAT *pD , MAT *pV);<br/>
MAT m_series(int begin , int end);<br/>
MAT m_transpose(MAT *pM) ;</p>
<p>#endif</p>
<p><br/>
==============================================</p>
<p><font color="#ff9900">/*matrix_lib.c*/</font></p>
<p>/*<br/>
MATRIX LIB , for quick programming in C .<br/>
Efficiency is not in consideration .</p>
<p>initiated when I have to translate a MATLAB file into C .</p>
<p>functions:<br/>
create<br/>
destroy<br/>
copy<br/>
get<br/>
set<br/>
transpose<br/>
series<br/>
add<br/>
multiply<br/>
scale<br/>
repmat<br/>
sort<br/>
zeros<br/>
ones<br/>
eye<br/>
solve ( built on CLAPACK )<br/>
inv ( a wrapping of 'solve' for A*X=I)<br/>
eig ( built on CLAPACK )</p>
<p>MAT is the structure for my MATRIX.<br/>
remember to destroy it after the work is completed.</p>
<p>all parameter of MAT is in pointer style , <br/>
while returning MAT is not .</p>
<p>I simply use double as the element type .</p>
<p>indices start from 0 .</p>
<p>it's disturbing that the CLIENT should keep in mind that <br/>
MAT must be DESTROYED after using .<br/>
space allocation of returning MAT and OUTPUT MAT structure is done by the functions themself , <br/>
while INPUT MAT should be properly created by the CLIENT .</p>
<p>------------code by hplonline</p>
<p>*/</p>
<p>#include &lt;stdio.h&gt;<br/>
#include &lt;assert.h&gt;</p>
<p>#include "matrix_lib.h"</p>
<p>/*<br/>
these lines are for VC6 .<br/>
please add these lib files for your own compiler<br/>
*/<br/>
#pragma comment(lib , "blas.lib") <br/>
#pragma comment(lib , "clapack.lib")</p>
<p>/*<br/>
since some functions in stdlib.h collide with ones in clapack.h" , <br/>
I make these declarations mannually<br/>
*/<br/>
void *malloc(size_t n) ;<br/>
void free(void* p) ;</p>
<p>#include "f2c.h"<br/>
#include "clapack.h"</p>
<p>/*<br/>
memory is managed through an Iliffle vector.<br/>
so reference to the elements is rather simple :</p>
<p>  m.space[0][1] = 3 ;<br/>
*/</p>
<p>int _toint(double d){<br/>
 return (int)(d + 0.5) ;<br/>
}</p>
<p>MAT m_create(int iHeight , int iWidth){<br/>
 int i ;<br/>
 MAT tmp ;<br/>
 tmp.width = iWidth ;<br/>
 tmp.height = iHeight ;<br/>
 tmp.space = (double **)malloc(iHeight * sizeof(double*)) ;<br/>
 for ( i = 0 ; i &lt; iHeight ; i ++ ){<br/>
   tmp.space[i] = (double *)malloc(iWidth * sizeof(double)) ;<br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>/*<br/>
return a row vector from begin to end<br/>
ie.<br/>
begin = 1 , end = 4 ;<br/>
return :<br/>
1 2 3 4 <br/>
*/<br/>
MAT m_series(int begin , int end){<br/>
 MAT tmp ;<br/>
 int i ;</p>
<p> assert(end &gt; begin) ;</p>
<p> tmp = m_create(1 , end - begin + 1) ;<br/>
 for ( i = 0 ; i &lt; tmp.width ; i ++ ){<br/>
   tmp.space[0][i] = (double)(begin + i) ; <br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>MAT m_transpose(MAT *pM){<br/>
 MAT tmp ;<br/>
 int i , j ;</p>
<p> assert(pM-&gt;space != NULL) ;</p>
<p> tmp = m_create(pM-&gt;width , pM-&gt;height) ;<br/>
 for ( i = 0 ; i &lt; pM-&gt;height ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pM-&gt;width ; j ++ ){<br/>
    tmp.space[j][i] = pM-&gt;space[i][j] ;<br/>
   }<br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>void m_destroy(MAT *pM){<br/>
 int i ;</p>
<p> assert(pM-&gt;space != NULL) ;</p>
<p> for ( i = 0 ; i &lt; pM-&gt;height ; i ++ ){<br/>
   free(pM-&gt;space[i]) ;<br/>
 }<br/>
 free(pM-&gt;space) ;<br/>
 pM-&gt;space = NULL ;<br/>
 pM-&gt;height = 0 ;<br/>
 pM-&gt;width = 0 ;<br/>
}</p>
<p>void m_copy(MAT *pMdst , MAT *pMsrc){<br/>
 int i , j ;</p>
<p> assert(pMsrc-&gt;space != NULL) ;</p>
<p> m_destroy(pMdst) ;<br/>
 *pMdst = m_create(pMsrc-&gt;height , pMsrc-&gt;width) ;<br/>
 for ( i = 0 ; i &lt; pMsrc-&gt;height ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pMsrc-&gt;width ; j ++ ){<br/>
    pMdst-&gt;space[i][j] = pMsrc-&gt;space[i][j] ;<br/>
   }<br/>
 }<br/>
}</p>
<p>/*<br/>
pRow and pCol must be row vectors <br/>
pM-&gt;:<br/>
1 2 3 <br/>
4 5 6<br/>
7 8 9<br/>
pRow-&gt;:<br/>
0 2 <br/>
pCol-&gt;:<br/>
0 1<br/>
return:<br/>
1 2 <br/>
7 8<br/>
*/<br/>
MAT m_get(MAT *pM , MAT *pRow , MAT *pCol){<br/>
 MAT tmp ;<br/>
 int i , j ;<br/>
 tmp = m_create(pRow-&gt;width , pCol-&gt;width) ;<br/>
 for ( i = 0 ; i &lt; pRow-&gt;width ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pCol-&gt;width ; j ++ ){<br/>
    tmp.space[i][j] = <br/>
     pM-&gt;space[_toint(pRow-&gt;space[0][i])][_toint(pCol-&gt;space[0][j])] ;<br/>
   }<br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>void m_set(MAT *pMdst , MAT *pRow , MAT *pCol , MAT *pMsrc){<br/>
 int i , j ;</p>
<p> assert(pRow-&gt;width == pMsrc-&gt;height &amp;&amp; pCol-&gt;width == pMsrc-&gt;width) ;</p>
<p> for ( i = 0 ; i &lt; pRow-&gt;width ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pCol-&gt;width ; j ++ ){<br/>
    pMdst-&gt;space[_toint(pRow-&gt;space[0][i])][_toint(pCol-&gt;space[0][j])]<br/>
     = pMsrc-&gt;space[i][j] ;<br/>
   }<br/>
 }</p>
<p>}</p>
<p>/* add *pMsrc to *pMdst */<br/>
void m_add(MAT *pMdst , MAT *pMsrc){<br/>
 int i , j ;</p>
<p> assert(pMdst-&gt;height == pMsrc-&gt;height <br/>
   &amp;&amp; pMdst-&gt;width == pMsrc-&gt;width) ;</p>
<p> for ( i = 0 ; i &lt; pMsrc-&gt;height ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pMsrc-&gt;width ; j ++ ){<br/>
    pMdst-&gt;space[i][j] += pMsrc-&gt;space[i][j] ;<br/>
   }<br/>
 }<br/>
}</p>
<p>/*<br/>
return *m1 multiply *m2<br/>
*/<br/>
MAT m_multiply(MAT *pM1 , MAT *pM2){ <br/>
 MAT tmp ;<br/>
 int i , j , k ;</p>
<p> assert(pM1-&gt;width == pM2-&gt;height) ;</p>
<p> tmp = m_create(pM1-&gt;height , pM2-&gt;width) ;<br/>
 for ( i = 0 ; i &lt; tmp.height ; i ++ ){<br/>
   for ( j = 0 ; j &lt; tmp.width ; j ++ ){<br/>
    tmp.space[i][j] = (double)0.0 ;<br/>
    for ( k = 0 ; k &lt; pM1-&gt;width ; k ++ ){<br/>
     tmp.space[i][j] += <br/>
      pM1-&gt;space[i][k] * pM2-&gt;space[k][j] ;<br/>
    }<br/>
   }<br/>
 }</p>
<p> return tmp ;<br/>
}</p>
<p>/*<br/>
return k*A<br/>
*/<br/>
void m_scale(MAT *pM , double k){<br/>
 int i , j ;<br/>
 for ( i = 0 ; i &lt; pM-&gt;height ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pM-&gt;width ; j ++ ){<br/>
    pM-&gt;space[i][j] *= k ;<br/>
   }<br/>
 }<br/>
}</p>
<p>/*<br/>
pm-&gt;:<br/>
1 2<br/>
3 4<br/>
repmat(pm , 1 , 2)-&gt;:<br/>
1 2 <br/>
3 4<br/>
1 2<br/>
3 4<br/>
*/</p>
<p>MAT m_repmat(MAT *pM , int iHeight , int iWidth){<br/>
 int i , j , ii , jj;<br/>
 MAT tmp ;<br/><br/>
 assert(pM-&gt;space != NULL) ;</p>
<p> tmp = m_create(pM-&gt;height * iHeight , pM-&gt;width * iWidth) ;<br/>
 for ( i = 0 ; i &lt; iHeight ; i ++ ){<br/>
   for ( j = 0 ; j &lt; iWidth ; j ++ ){<br/>
    for ( ii = 0 ; ii &lt; pM-&gt;height ; ii ++ ){<br/>
     for ( jj = 0 ; jj &lt; pM-&gt;width ; jj ++ ){<br/>
      tmp.space[i * pM-&gt;height + ii][j * pM-&gt;width + jj]<br/>
       = pM-&gt;space[ii][jj] ;<br/>
     }<br/>
    }<br/>
   }<br/>
 }</p>
<p> return tmp ;<br/>
}</p>
<p>/*<br/>
sort each column<br/>
return indice</p>
<p>using select sorting <br/>
*/</p>
<p>MAT m_sort(MAT *pM){<br/>
 int i , j , k ;<br/>
 MAT  index ;<br/>
 double tmp ;<br/><br/>
 index = m_create(pM-&gt;height , pM-&gt;width) ;<br/>
 for ( j = 0 ; j &lt; pM-&gt;width ; j ++ ){<br/>
   for ( i = 0 ; i &lt; pM-&gt;height ; i ++ ){<br/>
    index.space[i][j] = i ;<br/>
   }<br/>
   for ( i = 0 ; i &lt; pM-&gt;height - 1 ; i ++ ){<br/>
    for ( k = i + 1 ; k &lt; pM-&gt;height ; k ++ ){<br/>
     if ( pM-&gt;space[k][j] &lt; pM-&gt;space[i][j] ) {<br/>
      tmp = pM-&gt;space[k][j] ;<br/>
      pM-&gt;space[k][j] = pM-&gt;space[i][j] ;<br/>
      pM-&gt;space[i][j] = tmp ;<br/>
    <br/>
      tmp = index.space[k][j] ;<br/>
      index.space[k][j] = index.space[i][j] ;<br/>
      index.space[i][j] = tmp ;     <br/>
     }<br/>
    }<br/>
   }<br/>
 }</p>
<p> return index ;<br/>
}</p>
<p>MAT m_zeros(int iHeight , int iWidth){<br/>
 MAT tmp ;<br/>
 int i , j ;<br/>
 tmp = m_create(iHeight , iWidth) ;<br/>
 for ( i = 0 ; i &lt; iHeight ; i ++ ){<br/>
   for ( j = 0 ; j &lt; iWidth ; j ++ ){<br/>
    tmp.space[i][j] = 0 ;<br/>
   }<br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>MAT m_ones(int iHeight , int iWidth){<br/>
 MAT tmp ;<br/>
 int i , j ;<br/>
 tmp = m_create(iHeight , iWidth) ;<br/>
 for ( i = 0 ; i &lt; iHeight ; i ++ ){<br/>
   for ( j = 0 ; j &lt; iWidth ; j ++ ){<br/>
    tmp.space[i][j] = 1 ;<br/>
   }<br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>MAT m_eye(int iHeight , int iWidth){<br/>
 MAT tmp ;<br/>
 int i , j ;<br/>
 tmp = m_create(iHeight , iWidth) ;<br/>
 for ( i = 0 ; i &lt; iHeight ; i ++ ){<br/>
   for ( j = 0 ; j &lt; iWidth ; j ++ ){<br/>
    if ( i ==j ) {<br/>
     tmp.space[i][j] = 1 ;<br/>
    }else{<br/>
     tmp.space[i][j] = 0 ;<br/>
    }<br/>
   }<br/>
 }<br/>
 return tmp ;<br/>
}</p>
<p>void m_print(MAT *pM){<br/>
 int i , j ;<br/>
 printf("%d * %d :\n" , pM-&gt;height , pM-&gt;width) ;<br/>
 for ( i = 0 ; i &lt; pM-&gt;height ; i ++ ){<br/>
   for ( j = 0 ; j &lt; pM-&gt;width ; j ++ ){<br/>
    printf("%8.2f" , pM-&gt;space[i][j]) ;<br/>
   }<br/>
   printf("\n") ;<br/>
 }<br/>
}</p>
<p>/*<br/>
Ax=b<br/>
return x<br/>
*/<br/>
int m_solve(MAT *pA , MAT *pb , MAT *px){<br/>
 integer n , nrhs , lda , *ipiv , ldb , info ;<br/>
 doublereal *a , *b;<br/>
 int i , j ;<br/>
     <br/>
 n = pA-&gt;width ;<br/>
 nrhs = pb-&gt;width ;<br/>
 lda = pA-&gt;height ;<br/>
 ldb = pb-&gt;height ;<br/>
 ipiv = (integer*) malloc(sizeof(integer) * n) ;</p>
<p> a = (doublereal*) malloc(sizeof(doublereal) * n * lda) ;<br/>
 for ( j = 0 ; j &lt; n ; j ++ ){<br/>
   for ( i = 0 ; i &lt; lda ; i ++ ){<br/>
    a[lda * j + i] = pA-&gt;space[i][j] ;<br/>
   }<br/>
 }</p>
<p> b = (doublereal*) malloc(sizeof(doublereal) * nrhs * ldb) ;<br/>
 for ( j = 0 ; j &lt; nrhs ; j ++ ){<br/>
   for ( i = 0 ; i &lt; ldb ; i ++ ){<br/>
    b[ldb * j + i] = pb-&gt;space[i][j] ;<br/>
   }<br/>
 }</p>
<p> dgesv_(&amp;n, &amp;nrhs, a, &amp;lda, ipiv, b, &amp;ldb, &amp;info) ;</p>
<p> if ( info != 0 ) return info ;</p>
<p> printf("\ntesting ipiv:\n") ;<br/>
 for ( i = 0 ; i &lt; n ; i ++ ){<br/>
   printf("%d " , ipiv[i]) ;<br/>
 }<br/>
 printf("\ntesting ipiv end\n\n") ;</p>
<p> printf("\ntesting A\n") ;<br/>
 for ( i = 0 ; i &lt; lda ; i ++ ){<br/>
   for ( j = 0 ; j &lt; n ; j ++ ){<br/>
    printf("%8.2f" , a[j * lda + i]) ;<br/>
   }<br/>
   printf("\n") ;<br/>
 }<br/>
 printf("\ntesting matrix A end..\n\n") ;</p>
<p> *px = m_create(n , nrhs) ;<br/>
 for ( j = 0 ; j &lt; nrhs ; j ++ ){<br/>
   for ( i = 0 ; i &lt; n ; i ++ ){<br/>
    px-&gt;space[i][j] = b[j * n + i] ;<br/>
   }<br/>
 }</p>
<p> free(ipiv) ;<br/>
 free(a) ;<br/>
 free(b) ;<br/>
 return info ;<br/>
}</p>
<p>/*<br/>
inverse *pM<br/>
*/</p>
<p>void m_inv(MAT *pM){<br/>
 MAT I , x ;<br/>
 I = m_eye(pM-&gt;height , pM-&gt;height) ;<br/>
 m_solve(pM , &amp;I , &amp;x) ;<br/>
 m_copy(pM , &amp;x) ;<br/>
 m_destroy(&amp;I) ;<br/>
 m_destroy(&amp;x) ;<br/>
}</p>
<p>/* <br/>
return eigenvectors in *pV and eigenvalues in *pD<br/>
only tested for *pM is square<br/>
*/</p>
<p>int m_eig(MAT *pM , MAT *pD , MAT *pV){<br/>
 int i , j ;<br/>
 char jobvl , jobvr;<br/>
 integer n , lda , info , ldvr , ldvl , lwork ;<br/>
 doublereal *a , *wr , *wi , *vl , *vr , *work;</p>
<p> jobvl = 'N' ;<br/>
 jobvr = 'V' ;<br/>
 n = pM-&gt;width ;<br/>
 lda = pM-&gt;height ;</p>
<p> wr = (doublereal*)malloc( sizeof(doublereal) * n) ;<br/>
 wi = (doublereal*)malloc( sizeof(doublereal) * n) ; </p>
<p> ldvr = pM-&gt;height ;<br/>
 vr = (doublereal*)malloc( sizeof(doublereal) * n * ldvr) ;<br/>
 ldvl = ldvr ;<br/>
 vl = vr ;</p>
<p> a = (doublereal*) malloc(sizeof(doublereal) * n * lda) ;<br/>
 for ( j = 0 ; j &lt; n ; j ++ ){<br/>
   for ( i = 0 ; i &lt; lda ; i ++ ){<br/>
    a[lda * j + i] = pM-&gt;space[i][j] ;<br/>
   }<br/>
 }</p>
<p>/* ldvl = 3 ;<br/>
 vl = (doublereal*)malloc( sizeof(doublereal) * n * ldvl) ;*/</p>
<p> lwork = n * 4 ;<br/>
 work = (doublereal*)malloc( sizeof(doublereal) * lwork) ;</p>
<p> dgeev_(&amp;jobvl, &amp;jobvr, &amp;n, a,  &amp;lda, wr, wi, vl , &amp;ldvl , vr, &amp;ldvr, work, &amp;lwork, &amp;info) ;</p>
<p> if ( info != 0 ) return info ;</p>
<p> *pD = m_create(n , n) ;<br/>
 for ( j = 0 ; j &lt; n ; j ++ ){<br/>
   for ( i = 0 ; i &lt; n ; i ++ ){<br/>
    if ( i == j ){<br/>
     pD-&gt;space[i][j] = wr[i] ;<br/>
    }else{<br/>
     pD-&gt;space[i][j] = 0.0 ;<br/>
    }<br/>
   }<br/>
 }</p>
<p> *pV = m_create(n , n) ;<br/>
 for ( j = 0 ; j &lt; n ; j ++ ){<br/>
   for ( i = 0 ; i &lt; n ; i ++ ){<br/>
    pV-&gt;space[i][j] = vr[j * n + i] ;<br/>
   }<br/>
 }</p>
<p> free(a) ;<br/>
 free(wr) ;<br/>
 free(wi) ;<br/>
 free(work) ;<br/>
 free(vr) ;</p>
<p> return info ;</p>
<p>/* printf("info:%d\n" , info) ;<br/>
 printf("D = \n") ;<br/>
 for ( i = 0 ; i &lt; n ; i ++ ){<br/>
   for ( j = 0 ; j &lt; n ; j ++ ){<br/>
    if ( i == j ) printf("%10.5f" , wr[i]) ;<br/>
    else printf("%10.5f" , 0.0) ;<br/>
   }<br/>
   printf("\n") ;<br/>
 }<br/>
 printf("Vl = \n") ;<br/>
 for ( i = 0 ; i &lt; n ; i ++ ){<br/>
   for ( j = 0 ; j &lt; n ; j ++ ){<br/>
    printf("%10.5f" , vl[n * j + i]) ;<br/>
   }<br/>
   printf("\n") ;<br/>
 }<br/>
 printf("Vr = \n") ;<br/>
 for ( i = 0 ; i &lt; n ; i ++ ){<br/>
   for ( j = 0 ; j &lt; n ; j ++ ){<br/>
    printf("%10.5f" , vr[n * j + i]) ;<br/>
   }<br/>
   printf("\n") ;<br/>
 }<br/>
*/</p>
<p>}</p>
<p>/*<br/>
tests of :<br/>
eigs , solve , inv , sort<br/>
*/</p>
<p>int main(){<br/>
 int i , j ;<br/>
 double data_a[3][3] = {<br/>
   {1 , 3 , 5} ,<br/>
   {2 , 7 , 1} , <br/>
   {9 , 2 , 4}<br/>
 } ;<br/>
 double data_b[3] = {5 , 1 , 2} ;<br/>
 MAT A , b , x , D , V , index;</p>
<p> A = m_create(3 , 3) ;<br/>
 for ( i = 0 ; i &lt; 3 ; i ++ ){<br/>
   for ( j = 0 ; j &lt; 3 ; j ++ ){<br/>
    A.space[i][j] = data_a[i][j] ;<br/>
   }<br/>
 }<br/>
 b = m_create(3 , 1) ;<br/>
 for ( i = 0 ; i &lt; 3 ; i ++ ){<br/>
   b.space[i][0] = data_b[i] ;<br/>
 }</p>
<p> printf("A=\n") ;<br/>
 m_print(&amp;A) ;<br/>
 printf("b=\n") ;<br/>
 m_print(&amp;b) ;</p>
<p> m_eig(&amp;A , &amp;D , &amp;V) ;<br/>
 printf("D=\n") ;<br/>
 m_print(&amp;D) ;<br/>
 printf("V=\n") ;<br/>
 m_print(&amp;V) ;</p>
<p> m_solve(&amp;A , &amp;b ,&amp;x) ;<br/>
 printf("solving A*x = b\n") ;<br/>
 printf("x=\n") ;<br/>
 m_print(&amp;x) ;</p>
<p> m_inv(&amp;A) ;<br/>
 printf("inversing A\n") ;<br/>
 printf("A=") ;<br/>
 m_print(&amp;A) ;</p>
<p> index = m_sort(&amp;A) ;<br/>
 printf("sorting A:\n") ;<br/>
 m_print(&amp;A) ;<br/>
 printf("index is:\n") ;<br/>
 m_print(&amp;index) ;</p>
<p> m_destroy(&amp;index) ;<br/>
 m_destroy(&amp;A) ;<br/>
 m_destroy(&amp;b) ;<br/>
 m_destroy(&amp;x) ;<br/>
 m_destroy(&amp;D) ;<br/>
 m_destroy(&amp;V) ;</p>
<p> return 0 ;<br/>
}</p>
<p> </p>
<p>/*<br/>
tests of :<br/>
get , set , series<br/>
*/</p>
<p>/*<br/>
int main(){<br/>
 int i , j ;<br/>
 MAT m1 , m2 , col , row ;</p>
<p> m1 = m_create(3 , 3) ;<br/>
 for ( i = 0 ; i &lt; 3 ; i ++ ){<br/>
   for ( j = 0 ; j &lt; 3 ; j ++ ){<br/>
    m1.space[i][j] = i * 3 + j + 1 ;<br/>
   }<br/>
 }<br/>
 m_print(&amp;m1) ;</p>
<p> col = m_create(1 , 2) ;<br/>
 col.space[0][0] = 0 ;<br/>
 col.space[0][1] = 1 ;</p>
<p> row = m_create(1 , 2) ;<br/>
 row.space[0][0] = 0 ;<br/>
 row.space[0][1] = 2 ;</p>
<p> m2 = m_get(&amp;m1 , &amp;row ,  &amp;col) ;<br/>
 m_print(&amp;m2) ;</p>
<p> m_destroy(&amp;m2) ;<br/>
 m2 = m_zeros(2,2) ;<br/>
 col.space[0][1] = 2 ;<br/>
 m_set(&amp;m1 , &amp;row , &amp;col , &amp;m2) ;<br/>
 m_print(&amp;m1) ;</p>
<p> m_destroy(&amp;col) ;<br/>
 m_destroy(&amp;m2) ;<br/>
 col = m_series(0 , 2) ;<br/>
 m2 = m_get(&amp;m1 , &amp;row  , &amp;col) ;<br/>
 m_print(&amp;m2) ;</p>
<p> m_destroy(&amp;m1) ;<br/>
 m_destroy(&amp;m2) ;<br/>
 m_destroy(&amp;col) ;<br/>
 m_destroy(&amp;row) ;</p>
<p> return 0 ;<br/>
}<br/>
*/</p>
<p>/*<br/>
basic tests :<br/>
create ,destroy , copy , print ,eye ,ones ,zeros ,repmat ,add ,multiply , scale , transpose<br/>
*/</p>
<p>/*<br/>
int main(){<br/>
 MAT m , mm , a , b , c;<br/>
 int i , j ;</p>
<p> m = m_zeros(2 , 3) ;<br/>
 m.space[1][2] = 1 ;<br/>
 m_print(&amp;m) ;<br/>
 mm = m_repmat(&amp;m , 3 , 2) ;<br/>
 m_print(&amp;mm) ;<br/>
 m_destroy(&amp;mm) ;<br/>
 m_destroy(&amp;m) ;</p>
<p> m = m_ones(6 , 5) ;<br/>
 m_print(&amp;m) ;<br/>
 m_destroy(&amp;m) ;</p>
<p> m = m_eye(3 , 4) ;<br/>
 m_print(&amp;m) ;<br/>
 m_destroy(&amp;m) ;</p>
<p> m = m_eye(4 , 3) ;<br/>
 m_print(&amp;m) ;<br/>
 m_destroy(&amp;m) ;</p>
<p> a = m_ones(2 , 3) ;<br/>
 b = m_ones(3 , 2) ;<br/>
 m_print(&amp;a) ;<br/>
 m_print(&amp;b) ;<br/>
 c = m_multiply(&amp;a , &amp;b) ;<br/>
 m_print(&amp;c) ;<br/>
 m_destroy(&amp;a) ;<br/>
 m_destroy(&amp;b) ;<br/>
 m_destroy(&amp;c) ;</p>
<p> a = m_ones(2 , 3) ;<br/>
 b = m_ones(2 , 3) ;<br/>
 m_scale(&amp;b , 1.7) ;<br/>
 m_print(&amp;b) ;<br/>
 m_add(&amp;a , &amp;b) ;<br/>
 m_print(&amp;a) ;</p>
<p> m_destroy(&amp;b) ;<br/>
 b = m_transpose(&amp;a) ;<br/>
 m_print(&amp;b) ;<br/>
 m_destroy(&amp;a) ;<br/>
 m_destroy(&amp;b) ;</p>
<p> return 0 ;<br/>
}<br/>
*/</p>
<p><font color="#0000ff">TO BE CONTINUED:</font></p>
<p>It's well-known that the memory management in C is hard to done ,<br/>
for you should always keep in mind where you put a MALLOC <br/>
and whether you put a corresponding FREE .</p>
<p>My next step is to convert it to C++ class .<br/>
This can free the client from memory management , <br/>
which must be done in the CTOR and DTOR of a class .</p>
<p> </p>
