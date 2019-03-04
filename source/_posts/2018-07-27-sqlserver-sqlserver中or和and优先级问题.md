---
layout: post
title: sqlserver中or和and优先级问题
date: 2018-07-27 00:00:00
categories: 后端
---

今天发现写的接口有问题,排查到最后发现因为自己忽略了sqlserver中or和and的优先级，导致查询的数据不正确。

关于他们的使用见下面的例子

比如想要查询高三2班2000年出生或者是2002年出生的所有男生，那么sql应该这么写

```sql
select * from tb_class where sex = 'male' and (birth = '2000' or birth = '2002')
```

还有另一种写法，可以用in代替or
```sql
select * from tb_class where sex = 'male' and birth in ( '2000' , '2002')
```
