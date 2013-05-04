---
layout: post
title: "RFC925笔记,multi-lan下的地址解析(俗称的代理ARP)"
date: 2009-10-19  22:38
comments: true
categories: tech
tags: ["Network"]
_baiduhi_id: 967eaec2215eb7110ff47750.html
_baiduhi_category: Network
---

<p>(hplonline)2009.10.19</p>
<p>》多网地址解析</p>
<p>》》主题<br/>
Explicit subnets<br/>
Transparent subnets（Extended ARP）</p>
<p>明确的（不隐藏的）子网，<br/>
透明的子网（扩展arp）</p>
<p>》》INTRODUCTION</p>
<p>    The problem of treating a set of local area networks (LANs) as one<br/>
    Internet network has generated some interest and concern.  It is<br/>
    inappropriate to give each LAN within an site a distinct Internet<br/>
    network number.  It is desirable to hide the details of the<br/>
    interconnections between the LANs within an site from people,<br/>
    gateways, and hosts outside the site.  The question arises on how to<br/>
    best do this, and even how to do it at all.  One proposal is to use<br/>
    "explicit subnets" [1].  The explicit subnet scheme is a call to<br/>
    recursively apply the mechanisms the Internet uses to manage networks<br/>
    to the problem of managing LANs within one network.  In this note I<br/>
    urge another approach: the use of "transparent subnets" supported by<br/>
    a multi-LAN extension of the Address Resolution Protocol [2].</p>
<p>将一组LAN当作一个Internet网络具有实用价值：<br/>
1.给予一个站点内的所有LAN一个唯一的网络地址是不合适的<br/>
2.需要将网络的连接细节隐藏起来（对人 ，对网关，对站外主机）</p>
<p>》》OVERVIEW</p>
<p>概要性地叙述了一下ARP协议的工作方式。</p>
<p>》》代理的方式</p>
<p>文档将用BOX来指代这种设备，<br/>
现在一般的router中都有实现。</p>
<p>       Case 1: If the mapping for the host is found in the cache for the<br/>
       LAN that the query came from, the BOX does not respond (letting<br/>
       the sought host respond for itself).</p>
<p>如果报文中的&lt;IA,HA&gt;在与之同子网的chache中，不处理</p>
<p>       Case 2: If the mapping for the host is found in the cache for a<br/>
       different LAN than the query came from, the BOX sends a reply<br/>
       giving its own HA on the LAN the query came from.  The BOX acts as<br/>
       an agent for the destination host.</p>
<p>如果报文中的&lt;IA,HA&gt;在与之不同子网的chache中，以自己的HA响应。</p>
<p>       Case 3: If the mapping is not found in any of the caches then, the<br/>
       BOX must try to find out the the address, and then respond as in<br/>
       case 1 or 2.</p>
<p>如果没有该地址对，则必须试法找到。</p>
<p>       In case 3, the BOX has to do some magic.</p>
<p>          The BOX keeps a search list of sought hosts.  Each entry<br/>
          includes the IA of the host sought, the interface the ARP was<br/>
          received on, and the source addresses of the original request.<br/>
          When case 3 occurs, the search list is checked.  If the sought<br/>
          host is already listed the search is terminated, if not the<br/>
          search is propagated.</p>
<p>维护一个SH表（sought hosts，被寻找过的主机）。<br/>
每个条目包含该主机的IA，ARP报文来自的接口，请求的源地址。<br/>
如果SH在表内了，查找过程终止，否则进一步搜索。</p>
<p>          To propagate the search, an entry is first made on the search<br/>
          list, then the BOX composes and sends an ARP packet on each of<br/>
          its interfaces except the interface the instigating ARP packet<br/>
          was received on.  If a reply is received, the information is<br/>
          entered into the appropriate cache, the entry is deleted from<br/>
          the search list and a response to the search instigating ARP is<br/>
          made as in case 1 or 2.  If no reply is received, give up and<br/>
          do nothing -- no response is sent to the instigating host (the<br/>
          entry stays on the search list).</p>
<p>在除了收到 发起ARP REQUEST报文 之外的接口上，发送ARP REQUEST。<br/>
如果收到回复，将信息放进对应的chache，<br/>
从搜索表中删除该条目，按照case1或2的方法对收到的ARP REQUEST 响应。<br/>
如果没有收到回复，则什么也不做（搜索表中依然保持此条目）</p>
<p>（如果网络中有一台带这样功能的router，<br/>
则我们不断ARP REQUEST并不存在的地址，<br/>
可想而知，该router的搜索表会不断增长，直到爆掉）</p>
<p>    The entries in the caches and the search list must time out.</p>
<p>由于存在上面那个邪恶的想法，<br/>
需要使用超时来解决。</p>
<p>    For every ARP request that is received, the BOX must also put the<br/>
    sending host's IA:HA address mapping into the cache for the LAN it<br/>
    was received on.</p>
<p>对于收到的所有ARP请求，router都应该进行记录<br/>
（这与host的处理不同，<br/>
host仅记录目的地址是自身的ARP报文中的源IA:HA对）</p>
<p>（可想而知，如果网络上主机很多的话，<br/>
router的负担会很大）</p>
<p>》》关于超时的细节</p>
<p>          First, the hosts try to get the address resolved using ARP.<br/>
          They may actually make several attempts before giving up if a<br/>
          host is not responding.  One must have an good estimate of the<br/>
          length of time that a host may keep trying.  Call this time T1.</p>
<p>主机可能会不断重试请求一个不存在的地址，<br/>
需要估计其保持尝试的时间T1.</p>
<p>          Second, there is the time that an entry stays on the search<br/>
          list, or the time between BOX generated ARPs to resolve these<br/>
          addresses.  Call this time T2.</p>
<p>             Note that this time (T2) must be greater than the sum of the<br/>
             T1s for the longest loop of LANs.</p>
<p>搜索表中的条目具有存在时间T2。<br/>
T2要比最长网络环情况下，所有T1的和要大。</p>
<p>          Third, there is the time that entries stay in the cache for<br/>
          each LAN.  Call this time T3.</p>
<p>          The relationship must be  T1 &lt; T2 &lt; T3.</p>
<p>映射条目在chache中存在的时间T3。<br/>
这三个时间的关系是T1 &lt; T2 &lt; T3。</p>
<p>             One suggestion is that T1 be less than one minute, T2 be ten<br/>
             minutes, and T3 be one hour.</p>
<p>建议T1短于1分钟，T2约10分钟，T3一个小时</p>
<p>          If the environment is very stable, making T3 longer will result<br/>
          in fewer searches (less overhead in ARP traffic).  If the<br/>
          environment is very dynamic making T3 shorter will result in<br/>
          more rapid adaptation to the changes.</p>
<p>如果网络环境稳定，让T3更长可以减小开销。<br/>
如果环境不稳定，减短T3可以更好地适应。</p>
<p>          Another possibility is to restart the timer on the cache<br/>
          entries each time they are referenced, and have a small value<br/>
          for T3.  This would result in entries that are frequently used<br/>
          staying in the cache, but infrequently used information being<br/>
          discarded quickly.  Unfortunately there is no necessary<br/>
          relationship between frequency of use and correctness.  This<br/>
          method could result in an out-of-date entry persisting in a<br/>
          cache for a very long time if ARP requests for that address<br/>
          mapping were received at just less than the time out period.</p>
<p>另外的一个可能性是在每次条目被引用（referenced）的时候，<br/>
刷新定时器，并且设置一个很小的T3值。<br/>
这样可能导致频繁应用的信息一直在表中，<br/>
而非频繁引用的信息很快超时。<br/>
如果一个条目被频繁引用但已经过期(out of date)，<br/>
则该方法导致该条目长期存在于ARP表中。</p>
<p>》》多response的取舍</p>
<p>       ARP, as currently defined, will take the most recent information<br/>
       as the best and most up-to-date.  In a complicated multi-LAN<br/>
       environment where there are loops in the connectivity it is likely<br/>
       that one will get two (or more) responses to an ARP request for a<br/>
       host on some other LAN.  It is probable that the first response<br/>
       will be from the BOX that is the most efficient path.</p>
<p>       The one change to the host implementation of ARP that is suggested<br/>
       here is to prevent later responses from replacing the mapping<br/>
       recorded from the first response.</p>
<p>认为收到的第一个arp包是来自最有效的路径上的router。</p>
<p>当一个host运行的是扩展arp时（即假设存在代理arp的情况），<br/>
会选择收到的第一个ARP RESPONSE 添加到自己的ARP表中。<br/>
这样就给攻击留下了可能性，<br/>
一旦先收到了错误的arp包，则会丢弃正确的响应。</p>
<p>》》潜在问题(potential problems)</p>
<p>1.错误的chache条目<br/>
2.不用arp的主机<br/>
3.不能广播的LAN<br/>
4.表的尺寸<br/>
5.无限传输环<br/>
6.广播</p>
<p>》》关于广播</p>
<p>1.This IP Network<br/>
即网络地址+全1的主机地址。<br/>
router要转发</p>
<p>2.This LAN Only<br/>
即 255.255.255.255 ，<br/>
router不转发</p>
<p>3.Another LAN Only<br/>
有人建议给每个网络一个特殊地址</p>
<p>》》DISCUSSION</p>
<p>扩展ARP的机制在于让普通的host不用知道自己身处一个multi-LAN的环境。</p>
<p>       If a host took the trouble to analyze its local cache of IA:AH<br/>
       address mappings it might discover that several of the IAs mapped<br/>
       to the same HA.  And if it took timing measurements it might<br/>
       discover that some hosts responded with less delay that others.<br/>
       And further, it might be able to find a correlation between these<br/>
       discoveries.  But few hosts would take the trouble.</p>
<p>一个host可能通过发现若干IA映射到了同一个HA，<br/>
或者发现不同host响应ARP REQUEST的速度不一致，<br/>
来发现自己在一个multi-LAN的环境。</p>
<p>       1. How does the host discover if the destination is in this LAN or<br/>
       some other LAN?<br/>
       2. How do the BOXes that connect LANs know which BOXes are the<br/>
       routes to which LANs?</p>
<p>对这两个问的回答都是，host和router不应该知道网络的拓扑。</p>
<p>》》关于协议的选用：<br/>
       For example: use ARP within the LAN and have the BOX send ARP<br/>
       replies and act as a agent (as in the extended ARP scheme), but<br/>
       use a BOX-to-BOX protocol to get the "which hosts are where"<br/>
       information into the BOXes (as in the explicit subnet scheme).</p>
<p>可以使用普通ARP，作为代理，<br/>
也可以使用BOX-to-BOX protocol，用来在router之间传递信息。</p>
<p>》》SUMMARY</p>
<p>    Please note that neither this note nor [1] proposes a specific<br/>
    routing procedure or BOX-to-BOX protocol.  This is because such a<br/>
    routing procedure is a very hard problem.  The plan proposed here<br/>
    will let us get started on using multi-LAN environments in a<br/>
    reasonable way.  If we later decide on a routing procedure to be used<br/>
    between the BOXes we can redo the BOXes without having to redo the<br/>
    hosts.</p>
<p>如果将来要在BOX之间运行路由过程，<br/>
则不用更改主机，仅用更改BOX即可。</p>
