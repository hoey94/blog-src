---
layout: post
title: hbase集群搭建
date: 2018-06-21 00:00:00
categories: 大数据
tags: Hbase
---

#### 本机环境

* Ubuntu 16.0.4 TLS
* Vmware Workstation 14.1.1
* hadoop 2.7.3 （集群）
* zookeeper 3.4.10 (集群)

前提已经在VM中部署好Hadoop 和Zookeeper集群。本次使用3台主机分别为cor1、cor2、cor3，在部署Hbase之前首先确保zookeeper和hadoop完好且可用。

#### 下载

[apache官方下载](http://apache.org/dist/),选取的版本是hbase-2.0.1-bin.tar.gz。

关于hbase和hadoop版本的对应关系，这边给一个blog做参考https://blog.csdn.net/vtopqx/article/details/77882491，小伙伴也可以去看官方文档，会更详细一些。

#### 安装

解压到当前目录

> $ tar -zxvf hbase-2.0.1-bin.tar.gz  -C ./

进去conf目录编辑hbase-env.sh文件

> $ vim hbase-env.sh

```shell
# the java implementation to use. 1.7+ required

export JAVA_HOME=/opt/jdk//jdk1.8.0_66

# export JAVA_HOME=/usr/java/jdk1.8.0_66
# 设置日志目录和PID目录

export HBASE_LOG_DIR=/data/bigdata/logs/hbase
export HBASE_PID_DIR=/data/bigdata/data/hbase

# 使用外部zookeeper

export HBASE_MANAGES_ZK=false
```

编辑hbase-site.xml,关于每个参数的详细描述可以在官方文档的第7章节`7. Default Configuration`中查到这边就不做详述,附上链接http://hbase.apache.org/book.html#config.files

> $ vi hbase-site.xml

```shell
<configuration>
    <property>
        <name>hbase.tmp.dir</name>
        <value>/home/hadoop/hbase-2.0.1/data</value>
    </property>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://cor1:9000/hbase</value>
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.zookeeper.quorum</name>
        <value>cor1:2181,cor2:2181,cor3:2181</value>
    </property><property>
        <name>hbase.zookeeper.property.clientPort</name>
        <value>2181</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/home/hadoop/zookeeper/data</value>
    </property>
</configuration>
```

配置``conf/regionservers``，写在该文件中的将被认为是从节点，在主节点上运行``bin/start-hbase.sh``以后，会自动启动从节点。

#### 分发

使用scp命令，将配置好的hbase分发给其他cor2和cor3节点

> $ scp -r hbase-2.0.1 hadoop@cor2:/home/hadoop

> $ scp -r hbase-2.0.1 hadoop@cor2:/home/hadoop

#### 启动

进入到hbase根目录执行下面命令就可以运行hbase,`需要提前确保zookeeper和hadoop集群正常运行`。

> $ bin/start-hbase.sh

#### 测试

与Hadoop一样，hbase同样为我们提供了好看的WEB UI界面

master   | regionServer
-------- | -----------
http://cor1:16010 | http://cor1:16030

我们也可以在本地CLI中使用命令进入hbase shell

> $ bin/hbase shell

#### 案例

1.查看有哪些表

```shell
hbase(main)> list
```

2.创建表

```shell

# 语法：create <table>, {NAME => <family>, VERSIONS => <VERSIONS>}
# 例如：创建表t1，有两个family name：f1，f2，且版本数均为2

hbase(main)> create 't1',{NAME => 'f1', VERSIONS => 2},{NAME => 'f2', VERSIONS => 2}
```

3.删除表

```shell
hbase(main)> disable 't1'
hbase(main)> drop 't1'
```

4.查看表的结构

```shell
# 语法：describe <table>
# 例如：查看表t1的结构

hbase(main)> describe 't1'
```

5.修改表结构

修改表结构必须先disable

```shell
# 语法：alter 't1', {NAME => 'f1'}, {NAME => 'f2', METHOD => 'delete'}
# 例如：修改表test1的cf的TTL为180天

hbase(main)> disable 'test1'
hbase(main)> alter 'test1',{NAME=>'body',TTL=>'15552000'},{NAME=>'meta', TTL=>'15552000'}
hbase(main)> enable 'test1'
```

6.添加数据

```shell
# 语法：put <table>,<rowkey>,<family:column>,<value>,<timestamp>
# 例如：给表t1的添加一行记录：rowkey是rowkey001，family name：f1，column name：col1，value：value01，timestamp：系统默认

hbase(main)> put 't1','rowkey001','f1:col1','value01'
```

7.查询数据

```shell
# 语法：get <table>,<rowkey>,[<family:column>,....]
# 例如：查询表t1，rowkey001中的f1下的col1的值

hbase(main)> get 't1','rowkey001', 'f1:col1'

# 或者：

hbase(main)> get 't1','rowkey001', {COLUMN=>'f1:col1'}

# 查询表t1，rowke002中的f1下的所有列值

hbase(main)> get 't1','rowkey001'


# 语法：scan <table>, {COLUMNS => [ <family:column>,.... ], LIMIT => num}
# 另外，还可以添加STARTROW、TIMERANGE和FITLER等高级功能
# 例如：扫描表t1的前5条数据

hbase(main)> scan 't1',{LIMIT=>5}

# 语法：count <table>, {INTERVAL => intervalNum, CACHE => cacheNum}
# INTERVAL设置多少行显示一次及对应的rowkey，默认1000；CACHE每次去取的缓存区大小，默认是10，调整该参数可提高查询速度
# 例如，查询表t1中的行数，每100条显示一次，缓存区为500

hbase(main)> count 't1', {INTERVAL => 100, CACHE => 500}
```

8.删除数据

```shell
# 语法：delete <table>, <rowkey>,  <family:column> , <timestamp>,必须指定列名
# 例如：删除表t1，rowkey001中的f1:col1的数据

hbase(main)> delete 't1','rowkey001','f1:col1'
# 注：将删除改行f1:col1列所有版本的数据

# 语法：deleteall <table>, <rowkey>,  <family:column> , <timestamp>，可以不指定列名，删除整行数据
# 例如：删除表t1，rowk001的数据

hbase(main)> deleteall 't1','rowkey001'

# 语法： truncate <table>
# 其具体过程是：disable table -> drop table -> create table
# 例如：删除表t1的所有数据

hbase(main)> truncate 't1'
```

前些日子去日本旅游，blog停更几天。后面需要继续加油了！！
