---
layout: post
title: mybatis like相关问题

date: 2018-04-10 00:00:00
categories: 后端
tags: Mybatis
---

Mybatis 中关于like的使用

1. 使用字符串传值
我们要使用#{0}#{1}#{2去匹配传入的每个参数},因为带like,所以在传入值的时候要在名字左右拼上`%`号，像这样'%tom%',而不是'tom'，还有一点就是一定注意传入的顺序

Mapper.java

```java
public List<BdipChatPoint> selectListByPage(String modelUrl,String username);
```

Mapper.xml
```xml
<select id="selectListByPage" parameterType="java.lang.String" resultMap="pointMap">
		select * from bdip_chat_point 
			where tree_id = #{0} 
			and user_name like #{1}
</select>

```

main.java
```java

mapper.selectListByPage("1","%tom%");

```

有的人在Mapper.xml可能会这样写,是取不到值的,下面是错误演示
```xml 
<select id="selectListByPage" parameterType="java.lang.String" resultMap="pointMap">
		select * from bdip_chat_point 
			where tree_id = #{modelUrl} 
			and user_name like #{username}
	</select>
```
如果我们就想使用这种方法查,要怎么办呢？可以用Map封装参数，看一下使用Map传值

2.使用Map传值

Mapper.java

```java
public List<BdipChatPoint> selectListByPage(Map map);

```

Mapper.xml

```xml

<select id="selectListByPage" parameterType="Map" resultMap="pointMap">
		select * from bdip_chat_point 
			where tree_id = #{modelUrl} 
			and user_name like #{username}
	</select>

```

调用的时候初始化map对象

```java

Map map = new HashMap();
map.put("modelUrl", "624");
map.put("username", "%tom%");

```

需要注意的是`like #{username}`和`map.put("username", "%tom%");`如果你不想去拼`%`号,怎么办？我们可以这样子写。

Mapper.xml

```xml

<select id="selectListByPage" parameterType="Map" resultMap="pointMap">
		select * from bdip_chat_point 
			where tree_id = #{modelUrl} 
			and user_name like '%${username}%'
	</select>

```

```java

Map map = new HashMap();
map.put("modelUrl", "624");
map.put("username", "tom");

```

good luck!~




