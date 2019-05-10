---
layout: posts
title: Hbase ThriftServer访问内网HBase
date: 2019-05-10 17:59:00
tags: Hbase
categories: 大数据
---


本地集群环境架构结构如下图所示:

![架构图.png](https://i.loli.net/2019/05/10/5cd54df270f9f.png)

实现thriftClient与thriftServer通信，实现访问内网HBase集群

118.166.152.33和101.118.124.111 分别为公网IP,192.168.5.2/3/4分别为内网IP

### 域名映射

首先我们要做的是将ThriftServer服务的通信端口9000 映射到内网中，这边映射成了公网的9000端口

### thrift

下面是Thrift的百度百科

> Thrift是一种接口描述语言和二进制通讯协议，它被用来定义和创建跨语言的服务。它被当作一个远程过程调用（RPC）框架来使用，是由Facebook为“大规模跨语言服务开发”而开发的。

Thrift支持众多通讯协议：

* TBinaryProtocol – 一种简单的二进制格式，简单，但没有为空间效率而优化。比文本协议处理起来更快，但更难于调试。
* TCompactProtocol – 更紧凑的二进制格式，处理起来通常同样高效。

想了解更多[百度百科](https://baike.baidu.com/item/thrift/3879058?fr=aladdin)

支持的传输协议有：

* TFramedTransport – 当使用一个非阻塞服务器时，要求使用这个传输协议。它按帧来发送数据，其中每一帧的开头是长度信息。
* TSocket – 使用阻塞的套接字I/O来传输。

想了解更多[百度百科](https://baike.baidu.com/item/thrift/3879058?fr=aladdin)

HBase ThriftServer有下面两个参数用来指定是否使用TFramedTransport协议,默认是false这边CDH中不用开启

hbase.regionserver.thrift.framed

> Use Thrift TFramedTransport on the server side. This is the recommended transport for thrift servers and requires a similar setting on the client side. Changing this to false will select the default transport, vulnerable to DoS when malformed requests are issued due to THRIFT-601.

hbase.regionserver.thrift.compact

> Use Thrift TCompactProtocol binary serialization protocol.

下面参数用来配置Thrift Gateway的认证，如果你配了这个东西就必须用doAs完成认证才能完成通信

```xml
<property>
  <name>hbase.regionserver.thrift.http</name>
  <value>true</value>
</property>
<property>
  <name>hbase.thrift.support.proxyuser</name>
  <value>true/value>
</property>
```

想了解更多[Configure the Thrift Gateway to Use the doAs Feature](http://hbase.apache.org/1.2/book.html)，看59.6章节

我这边都没有开启如下图

![thrift.png](https://i.loli.net/2019/05/10/5cd552448d4f2.png)

### Client

客户端可以用python或者是Java与ThriftServer进行通信。值得一提的是python3 在访问时会抛异常，这边初步查了一下也有解决方案，这边就先用python2.7进行测试，下面是代码示例:

**python**

```python
#!/usr/bin/python

from common import *
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase

# Connect to HBase Thrift server
transport = TTransport.TBufferedTransport(TSocket.TSocket("101.118.124.111", "9090"))
protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)

# Create and open the client connection
client = Hbase.Client(protocol)
transport.open()

rows = client.getRow("cars", "row1")

for row in rows:
        rowKey = row.row
        print("Got row:" + rowKey);

# Close the client connection
transport.close()
```
**java**

```java
package com.bim.hbase;


import org.apache.hadoop.hbase.thrift.generated.AlreadyExists;
import org.apache.hadoop.hbase.thrift.generated.Hbase;
import org.apache.hadoop.hbase.thrift.generated.ColumnDescriptor;
import org.apache.thrift.transport.*;
import org.apache.thrift.protocol.*;
import org.apache.thrift.protocol.TCompactProtocol;
import org.apache.thrift.transport.TFramedTransport;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.util.Properties;

public class HbaseThriftTest {

    private static String host;
    private static Integer port;

    public static void init(){
        Properties properties = new Properties();
        InputStream in = null;
        try {
            in = HbaseThriftTest.class.getClassLoader().getResourceAsStream("system.properties");
            properties.load(in);
            host = properties.getProperty("hbase.thrift.host");
            port = Integer.parseInt(properties.getProperty("hbase.thrift.port"));
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            if(in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {

        init();
        String Proto = "binary";
        String TableName = "t1";
        String ColFamily = "rowkey002";

        // setup the hbase thrift connection
        TTransport Transport;
        Transport = new TSocket(host, port);
        TCompactProtocol FProtocol = new TCompactProtocol(Transport);
        Hbase.Client Client = new Hbase.Client(FProtocol);
        if (Proto.equals("binary")) {
            TProtocol Protocol = new TBinaryProtocol(Transport, true, true);
            Client = new Hbase.Client(Protocol);
        } else if ( Proto.equals("framed")) {
            Transport = new TFramedTransport(new TSocket(host, port));
            TProtocol Protocol = new TBinaryProtocol(Transport, true, true);
            Client = new Hbase.Client(Protocol);
        } else if ( ! Proto.equals("compact")) {
            System.out.println("Protocol must be compact or framed or binary");
        }
        Transport.open();

        // prepare the column family
        List<ColumnDescriptor> Columns = new ArrayList<ColumnDescriptor>();
        ColumnDescriptor col = new ColumnDescriptor();
        col.name = ByteBuffer.wrap(ColFamily.getBytes());
        Columns.add(col);

        // dump existing tables
        System.out.println("#~ Dumping Existing tables");
        for (ByteBuffer tn : Client.getTableNames()) {
            System.out.println("-- found: " + new String(tn.array(), Charset.forName("UTF-8")));
        }

        // create the new table
        System.out.println("#~ Creating table: " + TableName);
        try {
            Client.createTable(ByteBuffer.wrap(TableName.getBytes()), Columns);
        } catch (AlreadyExists ae) {
            System.out.println("WARN: " + ae.message);
        }

        Transport.close();
    }

}
```

下面是system.properties

```xml
hbase.thrift.host=101.118.124.111
hbase.thrift.port=9090
```