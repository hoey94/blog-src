---
layout: post
title: 利用wine安装迅雷和QQ
tags: 问题总结
date: 2018-03-13 00:00:00
categories: ubuntu
---

## 本机环境:

这个方法在本机试了。不行。小伙伴们还是散了吧！！

前一篇安装QQ2012国际版由于版本太老，部分功能不能使用，下面我们安装新版QQ。本机环境

> $ cat /proc/version  
> Linux version 4.10.0-28-generic (buildd@lgw01-12) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #32~16.04.2-Ubuntu SMP Thu Jul 20 10:19:48 UTC 2017

## 核心内容

* 1.迅雷运行几乎完美，能够用手机号登录，能够正常下载和加速。已知部分图片无法正常显示，无伤大雅。
* 2.QQ运行效率比起其他版本的wineqq来说要高，能够记住密码和自动登录，无法视频通话、远程演示。

### 所需文件一览

```
+-- deepin.com.qq.im_8.9.19983deepin16_i386.deb
+-- deepin.com.thunderspeed_7.10.35.366deepin15_i386.deb
+-- deepin-wine-d
|   +-- deepin-fonts-wine_1.9-26_all.deb
|   +-- deepin-libwine_1.9-26_i386.deb
|   +-- deepin-wine32_1.9-26_i386.deb
|   +-- udis86_1.72-2_i386.deb
+-- deepin-wine-helper-d
|   +-- libgif4_4.1.6-11_i386.deb
|   +-- libgnutls26_2.12.23-18_i386.deb
|   +-- libgnutls-deb0-28_3.3.20-1_i386.deb
|   +-- libgstreamer0.10-0_0.10.36-1.5_i386.deb
|   +-- libgstreamer-plugins-base0.10-0_0.10.36-2_i386.deb
|   +-- libpng16-16_1.6.26-1_i386.deb
|   +-- libreadline7_7.0-1_i386.deb
+-- dependences
+-- install.sh
+-- qq-d
|   +-- deepin-wine_1.9-26_all.deb
|   +-- deepin-wine32-preloader_1.9-26_i386.deb
|   +-- deepin-wine-helper_1.0deepin17_i386.deb
|   +-- deepin-wine-uninstaller_0.1deepin2_i386.deb
+-- README
+-- remove.sh
```

![附图](http://ww1.sinaimg.cn/large/0066vfZIgy1fpai4outlqj318t0jddhj.jpg)

- qq-d文件夹中为搭建deepin-wine环境所需的第一级依赖软件，包括deepin-wine，deepin-wine-helper等。
- deepin-wine-d中为软件包deepin-wine所需的依赖软件，包括deepin-libwine等。
- deepin-wine-helper-d中为软件包deepin-wine-helper所需的部分依赖软件，包括32位的libreadline7等。

网盘链接（链接: https://pan.baidu.com/s/1S69P6tK9St6ZDGBX2E1f2w 密码: 06i9）

### 安装方法

64位操作系统安装前需检查dpkg是否包含了i386架构的软件包。终端输入
> $ dpkg --print-foreign-architectures

如果输出i386则继续下面步骤，如果没有的话，需要先执行：

> $ sudo dpkg --add-architecture i386  
> $ sudo apt-get update

接下来安装deepin-qq和deepin-thunder，方法为打开终端，执行:

> $ sudo bash install.sh

如果是 32位操作系统请查看原博客 https://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=30614

转自https://www.ubuntukylin.com/ukylin/forum.php?mod=viewthread&tid=30614
