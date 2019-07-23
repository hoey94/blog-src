---
title: Google Colab
date: 2019-07-23 23:34:00
categories: 机器学习
---

机器学习训练模型的时间往往很长，这个时间可能是1小时2小时，甚至1天？而且训练后的模型，如果不满足要求，还得再反复调整这简直是个噩梦有么有？那么考虑一下性能优秀的计算机如何呢？去某宝、JD上一搜，你在逗我一台上万哪买的起。对于我们这些穷得揭不开锅而且很想搞机器学习的苦比学生党来说，Google Colab来拯救你！

Colaboratory 是一款研究工具，用于进行机器学习和研究。它是一个 Jupyter 笔记本环境，重点是它不需要进行任何设置就可以跑代码，而且性能方面Google提供了Tesla K80 GPU,对，是免费的GPU无期限的使用权！是不是仿佛发现了新大陆ヾ(≧O≦)〃嗷~，虽然不知道性能到底怎么样，但是根我这用了5年的烂本子比，已经不知道好到哪去了。

### 官网

首先这是Google的东西，想用肯定得FQ，这没啥说的，访问下面链接[Google Colab](https://colab.research.google.com)。Google Colab 支持Python2和Python3语言;想用R和Scala的小伙伴得忍忍了，Google方面正在研发对他们的支持，后续会开方相关功能。

### 记事本

写代码我们需要先建个“记事本”，可以通过下面两种方法建立:

1.第一次进入会弹出一个框，点框下面的 <font color="red">"NEW PYTHON 3 NOTBOOK"新建“记事本”
[![snapshot.png](https://i.loli.net/2019/07/23/5d3722e1577ab71988.png)](https://i.loli.net/2019/07/23/5d3722e1577ab71988.png)

2.这个框关掉以后，左上角找到 File->New Python 3 Notbook
[![file.png](https://i.loli.net/2019/07/23/5d372313881d457467.png)](https://i.loli.net/2019/07/23/5d372313881d457467.png)

### 用例

点击“CODE”创建一个代码片段，你可以创建多个代码片段。

[![2.png](https://i.loli.net/2019/07/23/5d3728ac90b5852441.png)](https://i.loli.net/2019/07/23/5d3728ac90b5852441.png)

下面用Python3 测试一下环境是否正常,试着打印tensorflow版本号：

```python
import tensorflow as tf
print(tf.__version__)
```

点击画的红色框框运行代码
[![snapshot.png](https://i.loli.net/2019/07/23/5d372439cf26465483.png)](https://i.loli.net/2019/07/23/5d372439cf26465483.png)

有兴趣的可以看一下下面的链接

[^脚注]: https://research.google.com/colaboratory/faq.html#browsers