---
layout: posts
title: 'TProtocolException: Bad version in readMessageBegin'
date: 2019-04-26 13:23:25
tags: Hbase
categories: 大数据
---

链接thrift异常 

```java
org.apache.thrift.protocol.TProtocolException: Bad version in readMessageBegin
        at org.apache.thrift.protocol.TBinaryProtocol.readMessageBegin(TBinaryProtocol.java:223)
        at org.apache.thrift.TBaseProcessor.process(TBaseProcessor.java:27)
        at org.apache.hadoop.hbase.thrift.TBoundedThreadPoolServer$ClientConnnection.run(TBoundedThreadPoolServer.java:289)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
        at java.lang.Thread.run(Thread.java:748)
2019-04-26 11:04:02,472 ERROR org.apache.hadoop.hbase.thrift.TBoundedThreadPoolServer: Thrift error occurred during processing of message.
org.apache.thrift.protocol.TProtocolException: Bad version in readMessageBegin
        at org.apache.thrift.protocol.TBinaryProtocol.readMessageBegin(TBinaryProtocol.java:223)
        at org.apache.thrift.TBaseProcessor.process(TBaseProcessor.java:27)
        at org.apache.hadoop.hbase.thrift.TBoundedThreadPoolServer$ClientConnnection.run(TBoundedThreadPoolServer.java:289)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
        at java.lang.Thread.run(Thread.java:748)
```


去CDH中的Hbase面板中检查*hbase.regionserver.thrift.compact*和*hbase.regionserver.thrift.framed*是否启用

hbase.regionserver.thrift.framed

Description:
>Use Thrift TFramedTransport on the server side. This is the recommended transport for thrift servers and requires a similar setting on the client side. Changing this to false will select the default transport, vulnerable to DoS when malformed requests are issued due to THRIFT-601.

hbase.regionserver.thrift.compact

Description
>Use Thrift TCompactProtocol binary serialization protocol.

增加ThriftServer堆栈大小到2G并保存

重启ThriftServer服务即可