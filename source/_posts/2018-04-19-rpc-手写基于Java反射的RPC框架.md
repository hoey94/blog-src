---
layout: post
title: 手写基于Java反射的RPC框架

date: 2018-04-19 00:00:00
categories: 后端
tags: RPC
---
### 目录说明
项目已经传至github仓库。

* rpc-client : 框架中客户端框架核心代码
* rpc-server : 框架中服务端框架核心代码
* rpc-common : 框架工具
* rpc-registry : 框架中两个核心业务类功能
	* 注册服务 - ServiceDiscovery
	* 发现服务 - ServiceRegistry
* rpc-sample-app : 客户端程序 (调用被发布的服务,执行对应业务代码)
* rpc-sample-server : 服务区程序 (用来发布RPC服务)

### 框架结构

预备知识梳理。采用Java语言编写，需要掌握线程、动态代理、反射、Netty、注解、Spring等知识。RPC远程过程调用，是一种常见的底层通信框架，有效的理解它对于后续学习其他开源框架有很大帮助。下面梳理设计思路与具体代码逻辑。见整体框架图：

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fqgkibcspdj31460kcq42.jpg)

`注:实线以上部分是用户需要完成的操作，一下部分则是需要封装后打包成jar包，供用户导入的框架内部核心代码。`

### 用户部分
用户部分也分为客户端和服务端，服务端用来发布想要发布的服务，客户端通过本框架来调用被发布的服务。

参考新浪的motan以及阿里的dubbo，想要启动RPC框架，首先需要在spring的配置文件application.xml中配置框架类才行，我们这边也同样是这个思路。

##### 1.服务端
服务端只需要完成以下两步操作就可以完成业务的发布了。

* application.xml配置框架ServiceRegistry以及RpcServer
* 在想要发布成服务的具体实现业务类上添加@RpcService(interface.class)

`注:两个类的细节问题见框架核心代码业务梳理。`


##### 2.客户端
客户端只需要完成以下两步操作就可以完成远程服务调用。

* application.xml配置框架ServiceDiscovery以及RpcProxy
* 在调用时使用@autowried构造RpcProxy对象。通过RpcProxy来获取具体调用的业务类接口代理对象，通过该对象调用具体方法即可。

`注:两个类的细节问题见框架核心代码业务梳理。`

对于RPC框架的使用者来说,不管是客户端还是服务端，底层细节都是透明的。

### 框架核心代码业务梳理

服务端框架的核心业务包含两个类，ServiceRegistry和RpcServer

**a. RpcServer.java**

- 在Spring容器启动后会构造RpcServer，扫描@RpcService(interface.class)注解,拿到具体业务类的接口以及接口实现类，将信息已k,v形式封装到指定的HashMap中。
- 在服务端启动一个netty主程序，在netty中指定具体的Handler业务线
	- 字节流的反序列化 
	- 对象的序列化
- 调用ServiceRegistry的registry()

**b. ServiceRegistry.java**

- 为RpcServer提供registry方法,启动zookeeper主程序，将启动好的netty的ip:port存到zookeeper节点中(后续可以拓展zookeeper节点，应对不同的业务场景)

客户端框架的核心业务包含两个类，ServiceDiscovery和RpcProxy

**a. RpcProxy.java**

- 在Spring容器启动后会构造RpcProxy
- 用户拿到该对象调用interfaceProxy = create(interface.class)就可以拿到对应的接口代理对象
- 用户使用interfaceProxy调用具体业务时，会触发JDK动态代理中的invoke方法,将方法及方法参数进行封装
- 调用ServiceDiscovery的discoveryy()
- 启动netty客户端程序，执行netty中指定具体的Handler业务线
	- 对象的序列化 outputStream
	- 字节流的反序列化 inputStream
	- 返回数据结果 inputStream

**b. ServiceDiscovery.java**

- ServiceDiscovery会从启动的zookeeper中找到服务器的地址(netty server ip:port)

这边对象的序列化和反序列化使用的是google的protobuf框架,它最大的特点就是可以跨平台。想要深入这边有链接:https://developers.google.com/protocol-buffers/

框架还有很多地方可以优化，比如可以增加zookeeper的存放根节点，来进行拓展业务，适应不同的业务场景；比如客户端中netty并没进行封装，应该是spring web容器启动时自动装载netty客户端。再有这个框架不能满足同一接口存在多个实现的case，那么想要满足，只需要为@RpcServer注解添加额外属性即可。
