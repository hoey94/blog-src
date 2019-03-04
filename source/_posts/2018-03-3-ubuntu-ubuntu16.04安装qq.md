---
layout: post
title: ubuntu16.04安装QQ国际版
date: 2018-03-03 00:00:00
categories: ubuntu
---

经过不断折腾,终于找到了一个可安装的QQ,下面的方法不出意外应该是适用与所有的ubuntu16版本,本人已经使用这个方法正常安装了QQ2012国际版,如图:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fozs6ft0q2j30ue0k7wh5.jpg)

QQ2012国际版:

* 支持密码键盘输入并记住密码。
* 可以发送QQ表情无问题。
* 传送文件无问题。
* IBus输入法正常。
* QQ设置常用功能，比较精简，且占用CPU少。

## 本机环境:

本机使用的是ubuntu16.04 TLS 64版,内核版本为4.10.0-28-generic,qq在本机上安装过程无任何问题(仅限本机)

> $ cat /proc/version  
> Linux version 4.10.0-28-generic (buildd@lgw01-12) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #32~16.04.2-Ubuntu SMP Thu Jul 20 10:19:48 UTC 2017

## 开始安装

首先我们需要安装依赖库 `libgtk2.0-0:i386` 因为我们是64位系统,所以我们还需要安装 `ia32-libs` , 但是ubuntu16.04中该软件包已经被其他版本代替了,所以我们选择安装`lib32ncurses5`

### 1. 安装libgtk2.0-0:i386

在终端输入`sudo apt-get install libgtk2.0-0:i386`

> $ sudo apt-get install libgtk2.0-0:i386

### 2. 安装 lib32ncurses5

在终端输入`sudo apt-get install lib32ncurses5`

> $ sudo apt-get install lib32ncurses5

### 3. 下载QQ2012国际版

下载链接[`https://pan.baidu.com/s/1bpF3p7L`](https://pan.baidu.com/s/1bpF3p7L),我们只需要下载`wine-qqintl-www.linuxidc.com.tar.xz`到本地,随后我们解压出里面的三个deb文件:

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1foztpxcpjej30kw0armzb.jpg)

我们使用dpkg分别安装三个deb文件

### 4. 安装 wine-qqintl_0.1.3-2_i386.deb

> $ sudo dpkg -i wine-qqintl_0.1.3-2_i386.deb

初次安装这个文件的时候,如果有部分lib没有配置,就会安装失败.我们的解决办法 执行一遍`sudo apt-get install -f`,这个命令的意思是`假如用户的系统上有某个package不满足依赖条件，这个命令就会自动修复,安装程序包所依赖的包`.完成以后我们再运行一遍`sudo dpkg -i wine-qqintl_0.1.3-2_i386.deb`就会发现成功安装了

### 5. 安装ttf-wqy-microhei_0.2.0-beta-2_all.deb和fonts-wqy-microhei_0.2.0-beta-2_all.deb

安装完后面两个deb文件

> $ sudo dpkg -i ttf-wqy-microhei_0.2.0-beta-2_all.deb  
> $ sudo dpkg -i fonts-wqy-microhei_0.2.0-beta-2_all.deb

## 运行QQ2012国际版

在开始菜单中我们可以找到QQ2012国际版

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fozty0w145j30x20n1dpc.jpg)

我们可以在终端使用命令`sudo dpkg -l|grep qq` 和 `sudo find / -name qq*` 查看QQ的安装情况

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fozu2b7ed6j30ku065t9p.jpg)

如果在登录时提示版本过低,我们只需要将 手机QQ-->设置-->帐号、设备安全-->设备锁 设置为`未启用`状态即可

## 卸载QQ2012国际版

### 1.查看有关qq的详情信息 

> $ sudo dpkg -l | grep qq

我们可以发现存在两个package,使用`dpkg -P`命令分别卸载两个package

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpbgro2a88j30jj0argns.jpg)

### 2.卸载 wine-qqintl:i386

> $ sudo dpkg -P wine-qqintl:i386

### 3.卸载 libqqwing2v5:amd64

> $ sudo dpkg -P libqqwing2v5:amd64

在卸载的时候提示存在依赖,所以卸载失败了,我们使用`-l`查看gnome-sudoku详情,并将其卸载后一切就正常了

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fpbguk17nuj30ji0aq0v1.jpg)

> $ sudo dpkg -l | grep gnome-sudoku  
> $ sudo dpkg -P gnome-sudoku


