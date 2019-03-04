---
layout: post
title: Ubuntu 16.04TLS 安装最新版VMware14.1.1
tags: 问题记录
date: 2018-03-18 00:00:00
categories: ubuntu
---

由于最近搭建集群需要虚拟机,来安装VMware

效果图:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgu6bbqa4j30xc0mbgrs.jpg)

## 本机环境

本机使用的是ubuntu16.04 TLS 64版,在本机上安装过程无任何问题(仅限本机)

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgvn41tp7j30q30tq4qp.jpg)

### 1.下载

注册过帐号以后进入这个链接https://my.vmware.com/cn/group/vmware/details?downloadGroup=WKST-1411-LX&productId=686&download=true&fileId=cd30e7c2359a3dc1a5e1b1d1b17727b9&secureParam=d7a9ad9d3128741ea1642469b8d12b95&uuId=1c8d56a7-02ad-4d06-9964-a4ab7419388c&downloadType=

下载的版本VMware-Workstation-Full-14.1.1-7528167.x86_64.bundle

### 2.破解码

版本VMware-Workstation-Full-14.1.1-7528167.x86_64.bundle的破解码：VF19H-8YY5L-48DQY-JEWNG-YPKF6

获得破解码的地址：http://beikeit.com/post-513.html

### 3.安装

*.bundle 文件比较特殊，只有在给它了执行权限后才能执行安装操作。所以安装的第一步就是给 *.bundle 文件添加执行权限。介绍两种方法：

1.在 *.bundle 文件上右击鼠标，选择最后一项“属性” 选项，在弹出的“属性”窗口中选择“权限”选项卡，在该选项卡中，可以看到有“允许以程序执行文件”的选项，把它选上，如图：

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgubt3m2oj30ps0q376x.jpg)

2.另一种方法就是在终端用命令给 bundle 文件添加执行权限。打开终端(快捷键为 Ctrl+Alt+T )，打开终端后，进入 bundle 文件所在目录(便于操作)，然后用以下命令给 bundle 文件添加执行权限：

> $ sudo chmod +x *.bundle

回车，输入用户密码，这样就给 bundle 文件添加了执行权限了。

在命令行运行*.bundle进行安装

> $ sudo ./*.bundle

### 4.配置VMware vmnet0、vmnet1和vmnet8

开始因为没有配置这个,导致ip不能分配,主机不能ping通虚拟机中的节点。（**注意：假如你在安装CenOS时选用的是桥接而非NAT类型，可以忽略,你可以直接跳转到第6直接配置文件后重启网卡,看看能否成功。**）

三者的区别参考博文:http://blog.csdn.net/guizaijianchic/article/details/72190394

进入编辑->虚拟网络编辑器 配置VMware vmnet0、vmnet1和vmnet8

下图是主机配置，注意我主机的ip是`192.168.100.110`

> $ ifconfig

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgus2pw0cj30ia0nnk33.jpg)

1.vmnet0使用桥接链接方式,基本上不用动,下图是我本机的配置:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgunedheoj30tq0kl0vb.jpg)

2.vmnet1使用宿主链接方式,需要修改的是**子网**和**子网掩码**，并使用DHCP分配模式,下图是我本机的配置:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgupqev7aj30h80go0u3.jpg)

3.vmnet8使用NAT链接方式,需要修改的是**子网**和**子网掩码**,并使用DHCP分配模式，下图是我本机的配置:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgutoyr3uj30h70goabe.jpg)

打开网络设置.可以查看里面的网关

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpguub5921j30h70hswg2.jpg)

参考blog:http://blog.csdn.net/w20228396/article/details/77507908和http://blog.csdn.net/didi8206050/article/details/51872682

### 5.安装CentOS minimal

镜像自己去网上下载好了

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgugjttt8j30pu0he0uf.jpg)

安装过程除了在**选择网络**那里选择**桥接类型**以外其他全部可以默认。

参考blog:http://blog.csdn.net/capricorn90/article/details/52476228

### 6.配置网络(手动)

如果安装过后发现不能上网，这个时候我们就要手动配置网络了，在这里我碰到的是虚拟网卡没有设置ip,解决办法：

补充：如果你发现你连的ifconfig都不能用,可以使用**ip addr**查看相应信息:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgv8b9tbuj30py0e4wfp.jpg)

打开/etc/systemconfig/network-scripts/ifcfg-eth0，然后在里面加上如下的内容：

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgv9zyjn4j30q10gxwfv.jpg)

注意打开的是ifcfg-eth0 你打开什么要根据你自己的网卡名称

> /$ /etc/systemconfig/network-scripts/ifcfg-eth0

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgvbrh01mj30px0e03zh.jpg)

DEVICE=ens33#设备名称，可根据ifcofnig命令查看到。

BOOTPROTO=dhcp  #连接方式，dhcp会自动分配地址，此时不需要在下面设置ip和网关

HWADDR=00:0C:29:AD:66:9F  #硬件地址，可根据ifcofnig命令查看到。

ONBOOT=yes  #yes表示启动就执行该配置，需要改为yes 我本地开始是no,所以在开机后没有给我自动分配ip,将它改为yes,在终端重启网卡

两个命令选一个:

> $ service network restart  
> $ /etc/init.d/network restart

参考blog:http://blog.csdn.net/w20228396/article/details/77507908和http://blog.csdn.net/didi8206050/article/details/51872682

### 7.克隆

克隆和快照的区别:http://blog.csdn.net/whatday/article/details/52538031

右键已安装的centos 管理->克隆，一路下一步,由于磁盘空间比较充足所以直接选择全克隆

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fph4om2cbaj30qr0lc78x.jpg)

mini3是我刚从mini1克隆的一个新版本,启动以后发现无法正常分配ip

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fph4rnjex9j30q50kkdhd.jpg)

因为mini1的网卡名称叫eth0,而克隆的叫eth1

我们到**/etc/systemconfig/network-scripts/**发现根本没有ifcfg-eth1文件,因为我们是克隆的..所以在这里我们吧ifcfg-eth0改成ifcfg-eth1

> $ cd /etc/systemconfig/network-scripts/  
> $ mv ifcfg-eth0 ifcfg-eth1
> $ vim ifcfg-eth1

重新修改里面的物理地址和网卡名称,其他可以不用动,然后重启网卡

> /etc/init.d/network restart

重新查看一下

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fph4yry5ztj30q30kk405.jpg)

### 8.ping主机名访问

一直老使用`ssh root@192.168.0.128`,`ssh root@192.168.0.130`访问好麻烦,而且在以后编写脚本时容易弄错哪个ip对应是哪一台,我们希望通过这样`ssh root@mini1`,`ssh root@mini2`就可以访问到每台机器

> $ vim /etc/hosts

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fph540ybxbj30qo0fv78k.jpg)

像上图一样设置就可以了





