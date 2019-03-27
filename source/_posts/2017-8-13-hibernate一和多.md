---

layout: post
title: hibernateone to many 和many to one 有什么区别？
date: 2017-08-13 00:00:00
categories: 后端
tags: hibernate
---

室友问了我个奇怪的问题

* 问：我们在配Hibernate的时候有<one-to-many>也有<many-to-one>,为什么会有两个？
* 问：我的意思one to many 要是反过来不就是many to one了吗？
* 问：我要是把相关的配置 调换一下，那么one to many和many to one不就是可以互换了吗？

从字面意思上看，one to many 是一对多,many to one是多对一。很明显就是区别（说实话，问这样的问题，一开始我也有点诧异，后来想了想还是不对劲）。从实际开发角度来说，一对多反过来就是多对一。我们以学生和班级为例。学生对班级是many to one，班级对学生就是one to many。那么问题来了，到底我们配置班级方的one to many？还是配置学生方的many to one呢？这个问题就要看实际开发需求了。在这个需求中，从经验上可以想象，我们查看班级的时候，并不一定要看到每个学生的信息。因为学生很多。但我们查看学生的时候，可能想看班级的信息，因为一个学生对应一个班级。在这种情况下，我们当然是配置学生方的many to one，然后做级联操作。以便取出学生时取出对应班级。而事实上，大多数情况下，many to one比one to many的应用也更为防范，这主要是基于一个效率考虑