---
layout: post
title: An invalid character [32] was present in the Cookie value
tags: 问题总结
date: 2018-03-12 00:00:00
categories: 其他
---

这是因为Cookies中存储特殊字符串引起的，当我们在里面存储分号空格等一些特殊符号时，就会抛异常。

解决办法我们只需要存入和取出的时候用`URLEncoder.encode(xxx，"UTF-8")`和`URLDcoder.decoder(xxx,"UTF-8")`就可以得到解决。