---
layout: post
title: NoClassDefFoundError和ClassNotFoundExceptio的区别

date: 2018-06-29 00:00:00
categories: 后端
---

## 问题描述

小伙伴突然说新部署的企业级某功能不能用了，到线上查看，发现访问界面报 NoClassDefFoundError com.xxxx.xxxx.xxx.java 异常。

## 问题排查

乍一看NoClassDefFoundError貌似是类没找到，你会发现tomcat中并没有缺少任何class。那么这个异常到底是什么意思。看下面java代码:

```java
public class Constants {
	static String ABC = "abc";
	static {
		if (1 == 1)
			throw new RuntimeException();
	}
}

public class Test {
	public static void main(String[] args) {
		new Thread() {
			public void run() {
				String s2 = Constants.ABC;
			}
		}.start();
		try {
			Thread.sleep(1000);
		} catch (Exception e) {
		}
		String s = Constants.ABC;
	}
}

```

在运行上面程序后，会报NoClassDefFoundError异常，原因是：在初始化Constants类时调用了static静态代码块抛了异常。所以再次使用Constants类时就报了这个错误了。

## 解决

那么问题定位到了以后，到线上对com.xxxx.xxxx.xxx.class 进行反编译 发现有这样一段代码

```java
static{
    // ...
    String sql = "select cversion from license";
    st = rs.executeSql(sql);
    while(st.next()){
        if( StringUtil.isNullOrEmpty(st.getString(1))){
            throw new Exception();
        }
        // ...
    }
    // ....
}
```

到数据库查了一下license表,发现cversion 字段的值为null

