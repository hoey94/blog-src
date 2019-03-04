---
layout: post
title: Ubuntu 16.04TLS 安装SecureCRT破解版
tags: 问题记录
date: 2018-03-18 00:00:00
categories: ubuntu
---

由于最近使用vm搭建集群使用ubuntu的终端连接节点太繁琐,来安装SecureCRT

## 本机环境

本机使用的是ubuntu16.04 TLS 64版,在本机上安装过程无任何问题(仅限本机)

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgvn41tp7j30q30tq4qp.jpg)

### 1.下载

- securecrt_linux_crack.pl 破解程序
- scrt-8.3.1-1537.ubuntu16-64.x86_64.deb 程序包

[百度网盘](https://pan.baidu.com/s/1oMJypFZQTGiuNe7VVqJo3w) 密码: 7j9k


### 2.安装

安装secureCRT 

> sudo dpkg -i scrt-8.3.1-1537.ubuntu16-64.x86_64.deb

### 3.破解

运行破解脚本程序

> sudo perl securecrt_linux_crack.pl /usr/bin/SecureCRT

认证信息:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpgts6s34sj30i90bfgru.jpg)

到dash中搜索securecrt启动,securecrt会提示你产品没有license，需要购买不然只能使用30天,
我们输入上图中的认证信息就可以完成注册。

### 4.解决读取串口设备的权限问题

当在启动器中启动SecureCRT 时，我们是以当前用户的权限启动的软件，因此没有操作串口的权限。

使用命令：**$ls -l /dev/ttyS0**查看当前串口信息，会显示如下信息

> $ ls -l /dev/ttyS0

可以看到，串口设备文件是  dialout这个组的，我们我们只要将当前用户添加到这个组就行了。加入当前登录的用户名为：fox，则执行如下命令
    
> $sudo usermod -a -G dialout zyh

重启系统，之后就可以直接打开SecureCRT来操作串口了

转自:http://blog.csdn.net/a499957739/article/details/79582999

参考1:http://www.cnblogs.com/wangkongming/p/3533240.html

参考2:http://www.vandyke.com/products/securecrt/

