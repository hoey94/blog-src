﻿---
layout: post
title: ubuntu16.04 Teamviewer不能远程控制
date: 2018-05-08 00:00:00
categories: Linux
tags: Ubuntu
---

## 问题描述

通过windows 7旗舰版 可以连接ubuntu的TeamViewer，但是鼠标不能控制电脑。ubuntu的版本是16.04TLS,TeamViewer 的版本是 13

![image](https://i.loli.net/2019/07/02/5d1aafa4411b163095.jpg)

## 解决

开始以为是Ubuntu中TeamViewer的权限没有开，但是后来看了看权限是开着的

![image](https://i.loli.net/2019/07/02/5d1aafaa8e45b20675.jpg)

在网上搜索了好久，各种说法都有，试了好多都没用。最后通过在askubuntu搜索TeamViewer关键字，一页一页看看了10几页把问题解决了，还是国外网站靠谱啊。

不能访问的原因是因为ubuntu本机某些依赖包没有装导致的。尝试运行下面指令:

> $ sudo apt-get install libjpeg62:i386 libxinerama1:i386 libxrandr2:i386 libxtst6:i386 ca-certificates

可以看到本机运行以后又安装了两个包 **libjpeg62:i386** 和 **libxtst6:i386**，应该就是它俩的原因了。

![image](https://i.loli.net/2019/07/02/5d1aafb6c8ba651486.jpg)

另外附上解决问题的帖子https://askubuntu.com/questions/764228/teamviewer-11-wont-run-on-ubuntu-16-04-64-bit