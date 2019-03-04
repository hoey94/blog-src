---
layout: post
title: firefox下利用微博图床优化markdown粘贴图片链接体验
分享
date: 2018-02-26 00:00:00
categories: 其他
---

网上有很多利用图床优化markdown粘贴图片链接的优化方式,我的这种并不是最好的,也不是最简便的.但是这个方法很容易配置,适合不懂代码的新手,具体配置步骤如下：

- 在ubuntu中配置自定义快捷键,执行xxx.sh脚本命令,该脚本命令由我们自己编写,其中会调用`gnome-screenshot`进行截图(如果不想使用gnome-screenshot截图工具,可以自行寻找其他截图方式代替).调用`xclip`将剪切板中的截图保存到某磁盘下
- 下载firefox图床拓展[`围脖就是好图床`](https://addons.mozilla.org/zh-CN/firefox/addon/acwb/)
- 手动将磁盘中的图片托到firefox图床拓展中上传。(如果有能力自己可以研究一下如何自动上传)

## 本机环境:

本机使用的是ubuntu16.04 TLS 64版,内核版本为4.10.0-28-generic,qq在本机上安装过程无任何问题(仅限本机)

> $ cat /proc/version  
> Linux version 4.10.0-28-generic (buildd@lgw01-12) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #32~16.04.2-Ubuntu SMP Thu Jul 20 10:19:48 UTC 2017

## 开始安装

首先我们需要安装`xclip`工具,这个命令其实是`命令建立了终端和剪切板之间通道，可以用命令的方式将终端输出或文件的内容保存到剪切板中，也可以将剪切板的内容输出到终端或文件中`,具体命令的细节有兴趣的小伙伴可以去研究一下。

其次我们需要用到ubuntu自带的`gnome-screenshot`截图工具,我们可以打开终端 输入`gnome-screenshot -a -c`

### 1. 安装xclip

> $ sudo apt-get install xclip

### 2. 编写snapshot.sh

打开`/home/zyh/Documents/screenshot/snapshot.sh`,具体内容如下

```shell
#!/bin/bash

gnome-screenshot -a -c
xclip -selection clipboard -t image/png -o > $HOME/Desktop/snapshot.png
```

第二行的意思是将剪切板中的图片以snapshot.png为名保存到桌面上

编写完snapshot.sh,在终端输入`chmod +x snapshot.sh`,修改snapshot.sh为`可执行`状态

### 3. 自定义截图快捷键运行snapshot.sh

我们可以在系统设置的键盘选项中自定义快捷键来运行我们想要运行的脚本文件

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fozvguy6vmj30nn0ge3z2.jpg)

点击`+`号添加自定义快捷键,`名称`随意填写即可,`命令填写我们刚刚编写的snapshot.sh,记得要写全路径`,本机填写的是/home/zyh/Documents/screenshot/snapshot.sh

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fozvjjbxy3j30nl0dujsm.jpg)

我这里设置的快捷键是`Ctrl+Alt+W`,自己根据喜好调整即可。

## 测试

我们使用Ctrl+Alt+W截图,然后会发现桌面上多出一个snapshot.png的文件,随后我们打开firefox将文件托到拓展中上传就可以拿到想要的链接了！

## 其他

如果你喜欢chrome浏览器,你可以在chrome下载新浪图床拓展程序,因为最近GWF很严,本人惨造封杀,无法科学上网,chrome拓展不太好下载,所以选择了firefox :(

