---
layout: post
title: Raspberry Pi微型计算机的使用
date: 2018-07-28 00:00:00
categories: 物联网
tags: Raspberry Pi
---

## 简述

Raspberry Pi(中文名为“树莓派”,简写为RPi，(或者RasPi / RPI)，只有信用卡大小的微型电脑，其系统基于Linux。 先今Raspberry Pi已经可以安装并运行Window操作系统。

Raspberry Pi是一款基于ARM的微型电脑主板，以SD/MicroSD卡为内存硬盘，卡片主板周围有1/2/4个USB接口和一个10/100 以太网接口（A型没有网口），可连接键盘、鼠标和网线，同时拥有视频模拟信号的电视输出接口和HDMI高清视频输出接口，以上部件全部整合在一张仅比信用卡稍大的主板上，具备所有PC的基本功能只需接通电视机和键盘，就能执行如电子表格、文字处理、玩游戏、播放高清视频等诸多功能。 Raspberry Pi B款只提供电脑板，无内存、电源、键盘、机箱或连线。

树莓派的生产是通过有生产许可的三家公司Element 14/Premier Farnell、RS Components及Egoman。这三家公司都在网上出售树莓派。现在，你可以在诸如京东、淘宝等国内网站购买到你所想要的树莓派。

树莓派基金会提供了基于ARM的Debian和Arch Linux的发行版供大众下载。还计划提供支持Python作为主要编程语言，支持Java、BBC BASIC (通过 RISC OS 映像或者Linux的"Brandy Basic"克隆)、C 和Perl等编程语言.

摘自百度百科


## 前期准备

如果想玩Raspberry Pi,来先从软硬件两方面来列一下前期的准备。

#### 硬件

1.Raspberry Pi主板 (238 RMB)

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpula4go9j31hc141ajb.jpg)

在买主板的时候，店家往往会给你推荐很多配件，比如电源、SD卡、散热片、外壳等等，不买也不影响正常使用，我购买的时候什么配件都没要，只要了一个主板

关于电源的话，我用的是小米的手机充电器，这里需要注意一点说明书上标明电源要用5V-2A的电源，如果不是5V-2A的最好还是别用。

当然如果是个不差钱的当我啥都没说。（土豪一起玩啊！！*v*）

2.SD卡 (59 RMB)

SD卡我这边是单独购买的，买的是闪迪32G的，听朋友说8G就已经够用了，如果你觉得太小可以买16G(40+ RMB)。32G 确实有点太大了。

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpvvcew2nj30db09uad0.jpg)

3.读卡器(6 RMB)

读卡器是在SD卡write OS时用的。我这边从便利店买了一个便宜货6块钱。

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpuuz6zqcj31kw16ox2w.jpg)

#### 软件

软件需要准备三个，三个软件都是为了制作SD而准备的

1.SDFormatter

用这个更是化SD卡

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpuyqhns6j302z027743.jpg)

2.Win32DiskImager

这个是往SD卡中写操作系统用的

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpuzom9ljj303y030mx0.jpg)

3.RASPBIAN OS

RASPBIAN OS它是树梅派基金会专门依据debain操作系统改出来的一个新的定制化的操作系统。也是官方推荐安装的一款操作系统。这边油两个不同版本

RASPBIAN STRETCH WITH DESKTOP : 会带着桌面一起安装

RASPBIAN STRETCH LITE ： 只安装命令行，不安装桌面

关于选择哪个，全在个人，想要桌面就安第一个。我使用的第第二个不带桌面的。

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpv1bb8e0j31hb0tz0zs.jpg)

## 制作SD卡

具体流程也很简单，这边大概说一下，用读卡器将SD卡与电脑连接起来，用SDFormatter格式化SD卡，启动Win32DiskImager，选择下好的镜像，点击write写入SD等待成功即可。

## SSH

这边没有网线，也没有显示器，那么要怎么ssh？具体操作步骤如下。需要注意的是，

###### 1.方案一

前提你需要准备一个linux操作系统。

插上SD卡，如果你是linux操作系统，除了第一个boot盘符意外，你就能看到第二个盘符，叫"rootfs"

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpvels5v7j30dh02x0sm.jpg)

> $ sudo vim rootfs/etc/wap_supplicant/wpa_supplicant.conf

在其中添加下段代码

```json
network={
ssid="your wifi name"
psk="your wifi password"
}
```

进入到与rootfs并列的boot目录,在其中添加一个空的名字为ssh的文件

> $ touch boot/ssh

拔出SD卡，将SD卡插入Raspberry Pi主板卡槽中，插上小米手机充电器，在事先登录好的路由器管理界面查看IP变化。新增的那个IP就是Raspberry Pi的ip了

然后就可以愉快的链接ssh了。默认帐号:**pi**密码:**raspberry**

> $ ssh pi@192.168.100.109

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftpvtg4hz8j30i80cbjud.jpg)

假如没有linux操作系统，我们就不能修改/etc/wpa_supplicant 目录下的 wpa_supplicant.conf文件，那么你可以尝试方案二

###### 2.方案二

插上SD卡,因为是window所以只能看到boot分区，在boot分区下新建 空的ssh文件

再创建一个wpa_supplicant.conf

将下段代码替换进去

```json
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
ssid="your wifi name"
psk="your wifi password"
}
```

将内存卡拔出重新插入接上电源,操作系统会将boot下的wpa_supplicant.conf,替换到/etc/wpa_supplicant/目录下。最后同上找到ip，进行ssh就好了

下面说一下我在探索这块时踩过的坑

关于wpa_supplicant.conf里面的写法，网上有很多版本，开始参考了两篇文章，里面的配置我试了试都不行，折腾了一下午，其中的心酸一言难尽，尽管如此这边还是附上链接地址[链接一](https://segmentfault.com/a/1190000010976507)，[链接二](http://shumeipai.nxez.com/2017/09/13/raspberry-pi-network-configuration-before-boot.html)

经过踩坑以后，这边对配置文件进行了调整最后才成功。

就是把里面的第一行country=xx 删掉.猜测的原因是，因为xx填写的并不正确导致无法正常链接wifi。这边干脆就把它删掉，因为删掉就是默认的了，事实证明删掉它以后wifi就可以连了，猜测是正确的。




