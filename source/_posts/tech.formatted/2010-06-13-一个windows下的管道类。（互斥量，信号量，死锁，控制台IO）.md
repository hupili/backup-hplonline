---
layout: post
title: "一个windows下的管道类。（互斥量，信号量，死锁，控制台IO）"
date: 2010-06-13  14:31
comments: true
categories: tech
tags: ["Vc"]
_baiduhi_id: f8ba3f2aeaf233355243c1c1.html
_baiduhi_category: Vc
---

(hplonline)2010.6.13<br/><br/><font color="#0000ff">一。起因</font><br/><br/>
之前做了个字符串协议的<a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/a23496824285c8b26d8119b0.html">引擎</a>，<br/>
后来基于这个引擎做点协议设计的实验。<br/><br/>
考虑了一下，引擎和上层协议之间用什么东西交互呢？<br/>
发送windows消息？<br/>
但是控制台程序，还要去获得句柄，并且改写窗口过程，<br/>
感觉比较麻烦，虽然也有办法得到控制台窗口句柄。（见<a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/e9f38c18ddd9cbbd4bedbcf3.html">这里</a>）<br/><br/>
想到以前也接触过进线程同步的理论，<br/>
但没有实践过，于是顺便写个管道类备用。<br/><br/><font color="#0000ff">二。信号量(semaphore)</font><br/><br/>
以前粗略了解过<a target="_blank" href="http://hi.baidu.com/hplonline/blog/item/7a8a06336903a0f11b4cff5f.html">互斥量，信号量，事件，临界区</a>等几种同步机制。<br/>
对于信号量的认识比较浅，只认识到其用来做互斥之用。<br/><font color="#ff0000">其实信号量的关键在于，其含有一个当前计数，和最大计数。</font><br/>
利用这个特点，就可以实现有限数量资源的访问控制了。<br/><br/>
从MSDN上摘抄一下对semaphore的介绍，每段只记录大意。<br/><br/>
Semaphore Objects<br/>
A semaphore object is a synchronization object that maintains a count between zero and a specified maximum value. The count is decremented each time a thread completes a wait for the semaphore object and incremented each time a thread releases the semaphore. When the count reaches zero, no more threads can successfully wait for the semaphore object state to become signaled. The state of a semaphore is set to signaled when its count is greater than zero, and nonsignaled when its count is zero.<br/><br/><font color="#ff00ff">信号量的值可以在0和max之间。<br/>
当信号量的值为0的时候，为无信号状态。</font><br/><br/>
The semaphore object is useful in controlling a shared resource that can support a limited number of users. It acts as a gate that limits the number of threads sharing the resource to a specified maximum number. For example, an application might place a limit on the number of windows that it creates. It uses a semaphore with a maximum count equal to the window limit, decrementing the count whenever a window is created and incrementing it whenever a window is closed. The application specifies the semaphore object in call to one of the wait functions before each window is created. When the count is zero — indicating that the window limit has been reached — the wait function blocks execution of the window-creation code.<br/><br/>
A thread uses the CreateSemaphore or CreateSemaphoreEx function to create a semaphore object. The creating thread specifies the initial count and the maximum value of the count for the object. The initial count must be neither less than zero nor greater than the maximum value. The creating thread can also specify a name for the semaphore object. Threads in other processes can open a handle to an existing semaphore object by specifying its name in a call to the OpenSemaphore function. For additional information about names for mutex, event, semaphore, and timer objects, see Interprocess Synchronization.<br/><br/><font color="#ff00ff">使用CreateSemaphore创建信号量，可以指定一个名称，用于进程间同步。</font><br/><br/>
If more than one thread is waiting on a semaphore, a waiting thread is selected. Do not assume a first-in, first-out (FIFO) order. External events such as kernel-mode APCs can change the wait order.<br/><br/><font color="#ff00ff">等待同一信号量的多个线程不一定按照FIFO顺序得到信号量。</font><br/><br/>
Each time one of the wait functions returns because the state of a semaphore was set to signaled, the count of the semaphore is decreased by one. The ReleaseSemaphore function increases a semaphore's count by a specified amount. The count can never be less than zero or greater than the maximum value.<br/><br/><font color="#ff00ff">当wait函数返回的时候，信号量的值会减少1。<br/>
ReleaseSemaphore调用会使得信号量的值增加1。<br/>
计数值不会小于0，也不会比max更大。</font><br/><br/>
The initial count of a semaphore is typically set to the maximum value. The count is then decremented from that level as the protected resource is consumed. Alternatively, you can create a semaphore with an initial count of zero to block access to the protected resource while the application is being initialized. After initialization, you can use ReleaseSemaphore to increment the count to the maximum value.<br/><br/><font color="#ff00ff">初始值一般都被设置为max。<br/>
也可以先设置为0，然后程序进行初始化。<br/>
之后多次使用ReleaseSemaphore使计数值达到max。</font><br/><br/>
A thread that owns a mutex object can wait repeatedly for the same mutex object to become signaled without its execution becoming blocked. A thread that waits repeatedly for the same semaphore object, however, decrements the semaphore's count each time a wait operation is completed; the thread is blocked when the count gets to zero. Similarly, only the thread that owns a mutex can successfully call the ReleaseMutex function, though any thread can use ReleaseSemaphore to increase the count of a semaphore object.<br/><br/><font color="#ff00ff">线程可以重复地wait一个信号量，而且每次都减少其值。<br/>
对于互斥量（Mutex），只有拥有它的线程能够调用ReleaseMutex。<br/>
对于信号量（Semaphore），每个线程都可以使用ReleaseSemaphore。</font><br/><br/>
A thread can decrement a semaphore's count more than once by repeatedly specifying the same semaphore object in calls to any of the wait functions. However, calling one of the multiple-object wait functions with an array that contains multiple handles of the same semaphore does not result in multiple decrements.<br/><br/><font color="#ff00ff">线程重复wait，可以重复减少信号量的值。<br/>
但使用multi-wait函数，数组中重复放置该信号量，<br/>
不会产生多次减少的动作。</font><br/><br/>
可见，即使是把max和init计数都置为1的信号量，<br/>
与互斥量之间还是有着细微的区别的。<br/><br/><font color="#0000ff">三。管道的总体结构</font><br/><br/>
首先考虑的是存储问题。<br/>
由于管道中不断有东西进出，<br/>
并且同时存在管道中的内容有上限，<br/>
那么可以使用一个循环队列来实现。<br/><br/>
在管道的ctor中开启相关的空间，<br/>
在管道的dtor中销毁相关的空间即可。<br/><br/>
然后是同步机制的设计。<br/><br/>
对循环队列的访问是必须互斥的，<br/>
否则可能会出现操作结果不一致的情况。<br/>
比如两个线程同时对管道进行输入，<br/>
那么可能有这么一句话：<br/>
rear = rear + 1 ;<br/>
两个线程如果“一起”执行到这里，<br/>
最后可能出现rear只加了1，而非2的情况。<br/>
这样，就需要设置一个互斥量mutexLock，<br/>
用来控制对循环队列这种临界资源的访问。<br/><br/>
由于队列是有容量上限的，<br/>
所以需要有手段来记录已经消耗的存储空间。<br/>
开设一个semaphoreIn，初始的时候为容量上限，<br/>
每当要向管道输入的时候，需要等待这个信号量，<br/>
如果信号量为0，那么线程就阻塞。<br/>
这样就保证了不会超过队列的容量。<br/>
而从队列输出数据也是类似的，<br/>
当队列里面没有东西的时候，也不能操作。<br/>
开设一个semaphoreOut，初始的时候为0。<br/>
当放入一个数据，semaphoreOut增加，<br/>
取走一个数据，semaphoreOut减少。<br/>
如果semaphoreOut为0，那么线程阻塞，直到有数据输入。<br/><br/>
最后是两个关键操作：Input和Output。<br/>
两个操作的大体过程都是：<br/><font color="#ff0000">等待信号量、互斥量<br/>
操作<br/>
释放信号量、互斥量</font><br/><br/><font color="#0000ff">四。I/O流程和死锁</font><br/><br/>
先来看我最初流程：<br/><font color="#ff00ff"><br/>
输入：</font><br/>
wait for mutexLock<br/>
wait for semaphoreIn<br/>
input some data<br/>
release semaphoreOut<br/>
release mutexLock<br/><font color="#ff00ff">输出：</font><br/>
wait for mutexLock<br/>
wait for semaphoreOut<br/>
ouput some data<br/>
release semaphoreIn<br/>
release mutexLock<br/><br/>
乍看起来还像那么回事，<br/>
结果第一次跑就卡起来了。<br/><br/>
想了很久，才意识到同步顺序上存在问题，<br/>
所以搞出了可耻的死锁。。<br/><br/>
以上面的流程为例。<br/>
假设管道位于初始状态，则里面没有任何内容。<br/>
现在一个线程开始要求输出，<br/>
首先，该线程对mutexLock的等待会立即返回。<br/>
然后，该线程开始等待semaphoreOut。<br/>
由于semaphoreOut还是0，于是阻塞起了。<br/>
这个时候，有另外一个线程准备对管道进行输入。<br/>
本来的设想是，一旦有了输入，之前的线程就可以继续工作。<br/>
但实际情况是，这个输入线程对mutexLock的等待会阻塞。<br/>
这样，两边都卡起了，既不能输入，也不能输出。<br/><br/>
所以需要对流程顺序作出调整，<br/>
先对信号量进行等待，<br/>
得到信号量表示输入或者输出操作是可行的，<br/>
然后才对循环队列的锁进行等待。<br/><br/>
改正过后的流程为：<br/><br/><font color="#ff00ff">输入：</font><br/><br/>
wait for semaphoreIn<br/><font color="#ff0000">wait for mutexLock</font><br/>
input some data<br/><font color="#ff0000">release mutexLock</font><br/>
release semaphoreOut<br/><br/><font color="#ff00ff">输出：</font><br/><br/>
wait for semaphoreOut<br/><font color="#ff0000">wait for mutexLock</font><br/>
ouput some data<br/><font color="#ff0000">release mutexLock</font><br/>
release semaphoreIn<br/><br/>
对这个教训进行一点归纳，可以提升到方法论的层面：<br/><font color="#ff0000">对互斥量的等待和释放操作应该紧包对互斥资源访问的代码段。</font><br/>
（如同改正后流程中标红所示的内容）<br/><br/>
最后，就像WaitForSingleObject的参数所示，<br/>
对于等待操作，我们可以指定一个时间。<br/>
由于上层的阻塞与否，是取决于信号量的，<br/>
所以对信号量的等待，应该交由上层来指定超时时间。<br/>
而对互斥量的等待，是用于同步对循环队列的访问，<br/>
其中包含的代码段是我们已知和可控的。<br/>
一般来说，如果不出现正在访问队列的线程时间片用完，<br/>
那么这个操作都是可以瞬间完成的。<br/>
所以对于mutexLock的等待就使用INFINITE（-1）的超时值。<br/><br/><font color="#0000ff">五。delete和delete[]</font><br/><br/>
可以说，这又是一个极其惨痛的教训。<br/>
由于写C++的时间变少了，<br/>
没有注意到这两者还有区别，<br/>
导致开始运行的时候出现了奇怪的现象。<br/><br/>
基本原则倒是很简单：<br/><font color="#ff0000">使用new的用delete销毁，<br/>
使用new xx[]的用delete[]销毁。</font><br/><br/>
不过我这里还是对现象的调试过程记录下，<br/>
其中有不少可以沿用到其他地方的经验。<br/><br/>
由于创建的时候，要存储一堆数据，肯定用的是new xx[]的形式。<br/>
在销毁的时候，没有注意到，直接写了个delete。<br/><br/>
第一个现象就是，程序运行完后，发现没有自动结束。<br/>
（由输出可以判断，自己写的流程已经走完）<br/>
在vs2008下试的时候，就一直卡在那里，感觉很奇怪。<br/><br/>
开始怀疑是不是main函数没有结束，<br/>
于是在自身逻辑完的时候，手动调用exit。<br/>
当然，现象还是一样的。<br/><br/>
遂注释掉原来的main函数，<br/>
自己手写了一个空的main函数，<br/>
结果是程序依然会卡住。<br/><br/>
之后换回VC6进行调试，发现在卡了几秒后会有ASSERTION错误。<br/>
看下信息，应该是debug模式对堆进行检查时所报的错。<br/><br/>
没有想明白，开始散弹枪调试了。。<br/>
依次把各个部分注释掉，<br/>
发现一旦没有用我的管道类就不会出这个问题。。。<br/><br/>
检查管道类，没有看出问题，再次散弹枪调试。<br/>
管道类中，原来使用的是<br/>
CPipe&lt;string , 3&gt; pipe;<br/>
内含的是一组string对象，改成其他类型试试。<br/>
发现一旦改成int这些基本类型，就不会出错。<br/><br/>
而这些基本类型和string和区别就在于其构造和析构。<br/>
基本类型是有trivial constructor的，而string不行。<br/>
故又检查了对象的创建与销毁，但还是没有发现delete[]的问题。<br/><br/>
最后又是一次散弹枪调试，<br/>
把管道类中的各个部分依次注释了看，<br/>
发现不析构居然就不会有任何问题，<br/>
看来bug一定就在析构函数里面。<br/>
这个时候，再仔细看，终于发现了可耻的delete。。。<br/><br/><font color="#ff0000">散弹枪调试是很暴力、很终极的调试手段，<br/>
但使用它的时候，往往意味着我们已经失去分析问题的理智。。</font><br/><br/>
在这个问题上花了近一个小时之后，<br/>
好生想了一下，其实合格的debug过程应该是这样的：<br/><font color="#ff0000">1。发现自身逻辑完了，程序还没结束。<br/>
2。肯定是有代码还在运行，不管是自己写的还是系统的。<br/>
3。断到main的结束，发现确实运行过了return。<br/>
4。能够在main之后运行的代码一般只有onexit指定的函数或者全局对象的dtor。<br/>
5。我没有onexit过，所以肯定是的dtor中出的问题。<br/>
6。detor中的一般操作是对资源的释放。<br/>
7。内存管理的时候，delete和new存在配对问题，着重检查。<br/>
8。debug结束。</font><br/><br/>
只有清晰的思路才能指导清晰的行动。<br/>
乱枪打鸟就是典型的土鳖表现。<br/>
为了避免经常土鳖，<br/>
多睡一小时觉其实比多debug两个小时还有效。<br/><br/><font color="#0000ff">六。控制台IO</font><br/><br/>
管道类到这里算是折腾完了，<br/>
结果写测试程序的时候又被囧了一下。<br/>
弄了个生产者和消费者的模型，<br/>
最先写出来的运行效果犹如这样：<br/><br/>
get stuff 81<br/><font color="#ff0000">Produce 'product 81'<br/>
Produce 'product 81'</font><br/>
Consume 'product 81'<br/>
get stuff 82<br/><br/>
可以看到，有两个Procude xxxx。<br/>
在有的地方又可以观察到两个Consume xxx。<br/>
但通过对代码的跟踪，和打印一些中间结果，<br/>
可以确定，对管道的输入输出一个产品只对应了一个操作。<br/><br/>
这就让人觉得很诡异，无法弄清楚究竟是哪里出的毛病。<br/>
对控制台IO函数进行检查，<br/>
也会发现其实只调用了一次。。<br/><br/>
今天中午再来看这个问题，<br/>
突然意识到：<br/><font color="#ff0000">控制台在这里也是个临界资源，需要进行互斥访问。。</font><br/><br/>
于是速度写个控制台的类：<br/>
class CConsole{<br/>
private:<br/>
HANDLE mutexLock ;<br/>
public:<br/>
CConsole(){<br/>
mutexLock = CreateMutex(NULL , FALSE , NULL) ;<br/>
}<br/><font color="#ff0000">void Write(char *p){<br/>
WaitForSingleObject(mutexLock , INFINITE) ;<br/>
printf("%s" , p) ;<br/>
ReleaseMutex(mutexLock) ;<br/>
}</font><br/>
} ;<br/><br/>
对控制台的输出就通过Write成员函数进行。<br/><br/>
没想到一加上这个，输出就变正常了。<br/><font color="#ff0000">但之前为什么不是输出内容交错，<br/>
而是输出内容重复呢？</font><br/>
这个问题暂时还没解决。。<br/><br/><font color="#0000ff">七。相关代码下载</font><br/><br/>
pipe.h，管道类，包含可用。<br/>
pipetest.cpp，正常的测试样例。<br/>
pipetest2.cpp，没有考虑控制台问题的测试代码。<br/><br/><a target="_blank" href="http://www.box.net/shared/cv73fe113q">下载地址</a><br/>
