---
layout: post
title: SpringMVC乱码
date: 2017-08-22 00:00:00
categories: 后端
tags: Spring
---

解决SpringMvc的POST和GET乱码问题

### POST乱码

在web.xml配置SpringMVC提供的Filter就可以解决POST乱码了

```xml

<filter>
    <filter-name>CharacterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <async-supported>true</async-supported>
    <init-param>
        <param-name>encoding</param-name>
        <param-value>UTF-8</param-value>
    </init-param>
    <init-param>
        <param-name>forceEncoding</param-name>
        <param-value>true</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>CharacterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>

```

### GET乱码

Filter只针对POST请求的，tomacat对GET和POST请求处理方式是不同的，要处理针对GET请求的编码问题，则需要改tomcat的server.xml配置文件，如下：

```xml

<Connector connectionTimeout="20000" port="8080" protocol="HTTP/1.1" redirectPort="8443"/>

```

注意:如果你用的是MyEclipse,到tomcat的根目录下修改server.xml,运行即可生效,如果你是eclipse需要在eclipse中修改server.xml才能生效

![server](http://images.cnitblog.com/blog/205051/201412/222012348121043.png)