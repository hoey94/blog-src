---
title: Export requires a --table or a --call argument
date: 2019-07-16 11:03:59
categories: 其他
tags: 问题总结
---

参考官方文档[10. sqoop-export](http://sqoop.apache.org/docs/1.4.6/SqoopUserGuide.html#_failed_exports)使用Sqoop导入数据到RDSMS数据库，结果报错；错误也是让人摸不着头脑，说需要一个**--table**或**--call**参数，但是命令中是有这些参数的。

[![1.png](https://i.loli.net/2019/07/16/5d2d3f654bffa92187.png)](https://i.loli.net/2019/07/16/5d2d3f654bffa92187.png)

### 解决办法

做下面修改，在值的左右加上<font color="red">双引号</font>即可。

```xml
--connect "jdbc:sqlserver://47.92.105.228:1433;database=ecologydata" \
```
