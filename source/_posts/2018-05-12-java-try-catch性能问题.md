---
layout: post
title: try-catch影响性能？
date: 2018-05-12 00:00:00
categories: 后端
---

今天在审查代码时，发现自己的查询接口并没有try-catch。开始这样写是因为觉得写try-catch没必要，查询不可能会发生异常，但后来想了想又不太对，假如以后拓展接口，在查询后又用了查询后信息呢？就会抛空指针异常了！为了保证接口的健壮性，最好还是要加上try-catch。那么到底try-catch影不影响程序执行的速度？

网上也有好多类似的博客，去解释这个问题。结果是：try-catch不影响性能，严格意义上说，如果不是百万级别的数据并发，try-catch对程序的影响是微乎其微的。

有人做过例子，可以参考一下[参考blog](https://blog.csdn.net/axuanqq/article/details/51328964)

在stackoverflow上老外也帮着讲了一下try-catch的运行机制[参考链接1](https://stackoverflow.com/questions/141560/should-try-catch-go-inside-or-outside-a-loop)[参考链接2](https://www.javaworld.com/article/2076868/learn-java/how-the-java-virtual-machine-handles-exceptions.html)

总结:

如果在运行时，程序抛了异常就会去查异常表,这是影响性能的主要原因。

至于在哪里写try-catch，其实只是影响了异常表里的两个变量而已（起始地址、结束地址），写在哪里跟應不影响性能是没有关系的。



