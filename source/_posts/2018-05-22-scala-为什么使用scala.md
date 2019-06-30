---
layout: post
title: 为什么使用scala
date: 2018-05-22 00:00:00
categories: 编程语言
tags: Scala
---

近期Scala十分火，很大一部分是spark的原因;当然另一个很重要的原因，Scala本身确实也是一个十分不错的语言,Scala是一门多范式编程语言，以JVM为目标环境，将面向对象和函数式编程有机地结合在一起，带来独特的编程体验。虽然JDK 8以后也推出了lambda,但是Scala与其相比还是略胜一筹。

Scala的作者[Martin Odersky](https://baike.baidu.com/item/Martin%20Odersky/8898309?fr=aladdin)早期曾是JVM的核心代码提供者，所以他在编写Scala时也尽量弥补Java中存在的不足。Martin Odersky曾说“没有一门预言能像Scala这样,让我产生持续的兴趣和热情，让我重新感受到学习、思考和解决问题的乐趣”。

正如你所看到的 Scala底层也是跑在JVM上的，所以它与Java集成度非常高，我们可以直接拿Scala调用已经写好的Java接口实现无缝对接。目前已经有很多公司和个人采用Scala来构建他们的平台和应用，作为JVM上第一个获得广泛成功的非Java语言，Scala正以它独特的魅力吸引着越来越多人的热情投入。

![image](http://ww1.sinaimg.cn/large/006qboNIgy1frjeo39r5nj30go0go0wl.jpg)

Scala语言表达能力十分强，一行代码抵得上Java多行，开发速度快；Scala是静态编译的，所以和JRuby,Groovy比起来速度会快很多。可以看到上图中Sacala程序员工作状态略显轻松。

## 安装

到Scala官网https://www.scala-lang.org/download/下载对应操作系统安装程序并安装,后续配置好环境变量

## Helloword

创建HelloScala.scala文件

```

object HelloScala{

    def main(args:Array[String]) {
        println("hello scala!");
    }

}

```

编译

> $ scalac HelloScala.scala

运行

> $ scala HelloScala