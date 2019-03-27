---
layout: post
title: Struts2和Spring集成后关于struts.xml中的class如何写的问题
date: 2017-08-22 00:00:00
categories: 后端
tags: struts
---

Sturts整合Spring后，想让Spring管理Struts的Action，在struts.xml中配置Action的class属性时使用bean的id来指定Action的类路径

## 配置

* 在applicationContext.xml中注册TeamAction,id我们写成TeamAction在这里写成大写的 'T'

```xml
 <bean id="TeamAction" class="com.Action.TeamAction">
    <property name="tm" ref="TeamMapper"></property>
    <property name="bts" ref="BDIPUtils"></property>
</bean>
```

* 在struts.xml中配置,配置的时候class写TeamAction即可从spring容器中获取TeamAction对象

```xml
<action name="TeamInfo" class="TeamAction">
    ...
</action>
```

## 错误

由于Action根据class="TeamAction"去spring容器中寻找对应的bean这一特性是由**struts2-spring-plugin-2.3.1.2.jar**提供的,没有引入它就会报这样的错误！

```properties
Unable to load configuration. - action - file:/E:/apache-tomcat-7.0.81/webapps/4DAnalog/WEB-INF/classes/struts.xml:6:46
	at org.apache.struts2.dispatcher.Dispatcher.init(Dispatcher.java:428)
	at org.apache.struts2.dispatcher.ng.InitOperations.initDispatcher(InitOperations.java:69)
	at org.apache.struts2.dispatcher.ng.filter.StrutsPrepareAndExecuteFilter.init(StrutsPrepareAndExecuteFilter.java:51)
	at org.apache.catalina.core.ApplicationFilterConfig.initFilter(ApplicationFilterConfig.java:279)
	at org.apache.catalina.core.ApplicationFilterConfig.getFilter(ApplicationFilterConfig.java:260)
	at org.apache.catalina.core.ApplicationFilterConfig.<init>(ApplicationFilterConfig.java:105)
	at org.apache.catalina.core.StandardContext.filterStart(StandardContext.java:4950)
	at org.apache.catalina.core.StandardContext.startInternal(StandardContext.java:5652)
	at org.apache.catalina.util.LifecycleBase.start(LifecycleBase.java:145)
	at org.apache.catalina.core.ContainerBase.addChildInternal(ContainerBase.java:1009)
	at org.apache.catalina.core.ContainerBase.addChild(ContainerBase.java:985)
	at org.apache.catalina.core.StandardHost.addChild(StandardHost.java:652)
	at org.apache.catalina.startup.HostConfig.deployDirectory(HostConfig.java:1296)
	at org.apache.catalina.startup.HostConfig$DeployDirectory.run(HostConfig.java:2038)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:471)
	at java.util.concurrent.FutureTask$Sync.innerRun(FutureTask.java:334)
	at java.util.concurrent.FutureTask.run(FutureTask.java:166)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1110)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:603)
	at java.lang.Thread.run(Thread.java:722)
Caused by: Unable to load configuration. - action - file:/E:/apache-tomcat-7.0.81/webapps/4DAnalog/WEB-INF/classes/struts.xml:6:46
	at com.opensymphony.xwork2.config.ConfigurationManager.getConfiguration(ConfigurationManager.java:69)
	at org.apache.struts2.dispatcher.Dispatcher.init_PreloadConfiguration(Dispatcher.java:371)
	at org.apache.struts2.dispatcher.Dispatcher.init(Dispatcher.java:415)
	... 19 more
Caused by: Action class [TeamAction] not found - action - file:/E:/apache-tomcat-7.0.81/webapps/4DAnalog/WEB-INF/classes/struts.xml:6:46
	at com.opensymphony.xwork2.config.providers.XmlConfigurationProvider.verifyAction(XmlConfigurationProvider.java:420)
	at com.opensymphony.xwork2.config.providers.XmlConfigurationProvider.addAction(XmlConfigurationProvider.java:365)
	at com.opensymphony.xwork2.config.providers.XmlConfigurationProvider.addPackage(XmlConfigurationProvider.java:479)
	at com.opensymphony.xwork2.config.providers.XmlConfigurationProvider.loadPackages(XmlConfigurationProvider.java:275)
	at org.apache.struts2.config.StrutsXmlConfigurationProvider.loadPackages(StrutsXmlConfigurationProvider.java:111)
	at com.opensymphony.xwork2.config.impl.DefaultConfiguration.reloadContainer(DefaultConfiguration.java:204)
	at com.opensymphony.xwork2.config.ConfigurationManager.getConfiguration(ConfigurationManager.java:66)
	... 21 more
```
