---
title: java.lang.NoClassDefFoundError scala/Product$class
date: 2019-04-16 13:18:58
tags: Spark
categories: 大数据
---

环境：windows 7 + idea + scala + spark

本地运行以后报下面错误

```java
Exception in thread "main" java.lang.NoClassDefFoundError: scala/Product$class
	at org.apache.spark.SparkConf$DeprecatedConfig.<init>(SparkConf.scala:682)
	at org.apache.spark.SparkConf$.<init>(SparkConf.scala:539)
	at org.apache.spark.SparkConf$.<clinit>(SparkConf.scala)
	at org.apache.spark.SparkConf.set(SparkConf.scala:72)
	at org.apache.spark.SparkConf.setAppName(SparkConf.scala:87)
	at com.bim.WordCount$.main(WordCount.scala:9)
	at com.bim.WordCount.main(WordCount.scala)
Caused by: java.lang.ClassNotFoundException: scala.Product$class
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:335)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	... 7 more
```

Spark和Scala的版本是有对应关系的，下面有个查看关系的小技巧，去[https://mvnrepository.com/](https://mvnrepository.com/)中搜索**spark**，进入**Spark Project Core**查看即可

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g24entpf59j309m04z3yc.jpg)

下面分别引入**spark-core**和**spark-sql**（不需要的话可以不引）运行即可。