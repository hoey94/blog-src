---
layout: post
title: ubuntu sublime不能输入中文
date: 2017-09-19 00:00:00
categories: ubuntu
---

ubuntu 16.0.4使用sublime不能输入中文

### 解决

* 从github上下载下面这个玩意


```
$ git clone https://github.com/lyfeyaj/sublime-text-imfix.git

```

* 进入目录

```
$ cd sublime-text-imfix/
```

* 像这样把文件拷到对应目录下

```
$ sudo cp ./lib/libsublime-imfix.so /opt/sublime_text/
$ sudo cp ./src/subl /usr/bin/
```

* 编写一个sh脚本启动sublime

```
$ vim sublime
```

```
#!/bin/bash
LD_PRELOAD=/opt/sublime_text/libsublime-imfix.so subl
```