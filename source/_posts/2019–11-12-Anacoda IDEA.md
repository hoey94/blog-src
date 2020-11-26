---
title: Anaconda IDEA
date: 2019-11-11 22:56:00
categories: 机器学习
tags: Anaconda
---

好的优秀的IDEA可以提高生产效率，下面介绍一下Python的常用IDEA。

PyCharm：复杂大型的企业级应用。
IDLE、Sublime ： 300+行的代码程序。
Anaconda：适合科学计算和数据分析。


### 概述

Anacoda免费开源、支持8000个第三方库、包含多个主流工具，适合数据计算领域开发。下面了解一下里面的基本组件。

我们可以上www.continuum.io上安装最新的Anacoda IDEA。

它可以装在linux、win、mac上。实际上，Anacoda只是帮我们集成各类python工具，比如下面三个组件：

* Conda： 与pip和maven类似，是一个包管理工具用于管理第三方包。
* Spyder： 它可以编写python代码，并且支持调试运行。
* IPython： 是一个功能强大的交互式shell，编写代码变得更方便，适合进行交互式数据可视化和GUI相关应用开发，便于做数据分析。

### conda

安装Anacoda ，打开Anacoda Navigator。在Environments一栏中可以看到默认的root环境空间，空间中已经包含了很多默认的第三方包。如果需要可以继续创建别的环境空间。

### Spyder

Spyder有三个工作区，分别为编辑区、文本导航和帮助区、IPython区

文本导航和帮助区我们不经常使用，建议删除掉简化开发页面。

在tools -> perference -> syntax coloring中可以设置主题

### IPython

In [num] : In指的是输入的命令，num是IPython的行号
Out [num] : Out指的是输出值或结果

下面介绍一下IPython中常用的两个指令：？和%

？跟在变量的后面，可以打印更多的详细信息。
%run file.py 可以运行任意目录下的file.py文件。

除上面命令以外，IPython还有很多其他指令，如下图所示：

 