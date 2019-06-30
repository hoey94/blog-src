---
layout: post
title: HDFS and YARN
tags: Hadoop
date: 2017-08-21 00:00:00
categories: 大数据
---

本文主要说明HDFS和MapReduce两门技术的入门使用.因为MapReduce太长,后面就简称MR,我们到[官网](http://hadoop.apache.org/releases.html)下载hadoop-2.4.1.tar.gz,并解压,进入到hadoop-2.4.1/etc/hadoop,分别配置以下几个文件

* hadoop-env.sh
* core-site.xml
* hdfs-site.xml
* mapred-site.xml.template(重命名为mapred-site.xml)
* yarn-site.xml

### 配置 hadoop-env.sh

需要到hadoop-env.sh中配置Java环境,值得注意的是在hadoop-env.sh文件中使用的变量名不会生效,我们在这里写死它,查询Java存放路径

> ehco $JAVA_HOME

![java](https://i.loli.net/2019/06/30/5d18567363a5f26626.jpg)

![](https://i.loli.net/2019/06/30/5d185674e1eac90408.jpg)

### 配置 core-site.xml

1. fs.defaultFS: 指定HADOOP所使用的文件系统访问的URI
2. hadoop.tmp.dir: 指定hadoop运行时产生文件的存储目录


```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://zyh:9000/</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/media/zyh/software/hadoop-2.4.1/data/</value>
    </property>
</configuration>
```

这里hdfs://zyh:9000/中的zyh相当于localhost,因为我在/etc/hosts文件中修改了

![](https://i.loli.net/2019/06/30/5d1856759d07a87559.jpg)

### 配置 hdfs-site.xml

1. dfs.replication: 指定HDFS切块(blk)的副本数量

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

### 配置 mapred-site.xml

1. mapreduce.framework.name:指定MR的运行的资源由yarn分配

```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
```

### 配置 yarn-site.xml

1. yarn.resourcemanager.hostname: 指定YARN的ResourceManager的地址,其实就是我本机zyh(127.0.0.1)
2. yarn.nodemanager.aux-services: reducer获取数据的方式

```xml
<configuration>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>zyh</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

### 将hadoop添加到环境变量

```
    $ vim /etc/proflie
    $ export JAVA_HOME=/usr/java/jdk1.6.0_45
    $ export HADOOP_HOME=/media/zyh/software/software for linux/hadoop-2.4.1
    $ export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
    $ source /etc/profile
```
这个是我本地的profile作参考

![hadoop添加到环境变量](https://i.loli.net/2019/06/30/5d18567686ce084291.jpg)

### 初始化namenode（又叫格式化namenode）

> $ hdfs namenode -format (hadoop namenode -format)

![初始化namenode](https://i.loli.net/2019/06/30/5d18567a2fe3a45964.jpg)

弹出一大片log,英语很nice可以稍微看看,不好的可以键入命令``echo $?``来校验上一个操作是否正确,如果是0就是正确的

## 启动hadoop

如果你格式化namenode已成功,就可以运行hadoop了！在**hadoop-2.4.1/sbin**目录下面,hadoop为我们提供了很多命令

1. start-all.sh : 启动dfs和yarn
2. start-dfs.sh : 启动dfs
3. start-yarn.sh : 启动yarn

![](https://i.loli.net/2019/06/30/5d18567b17a6e33029.jpg)

作为入门的新手,我们当然是一步一步启动,先启动HDFS,再启动YARN.并观察启动后的运行状态

### 启动HDFS

> $ sbin/start-dfs.sh

启动报错,如果说本地ssh拒绝访问,那么我们需要安装openssh-server,如果没有报错请无视！

![报错](https://i.loli.net/2019/06/30/5d18567e4b37e92668.jpg)

安装后再次键入命令.HDFS会提示会让我们输入很多次密码并确认,因为部署的是分布式系统,尽管我们只使用了一台电脑,但是HDSF不知道,他会使用SSH去访问我们远程的服务器(本例中远程服务器就是本机啦！)之后它会启动一系列进程,这些进程分别是:

1. NameNode
2. DataNode
3. SecondaryNameNode

![启动HDFS](https://i.loli.net/2019/06/30/5d18567fd7f1683994.jpg)


### 启动YARN

> $ sbin/start-yarn.sh

yarn也是一样的一路yes并输入密码即可,yarn会先后开启两个进程,他们分别是

1. ResourceManager
2. NodeManager

![启动YARN](https://i.loli.net/2019/06/30/5d185682ac28195281.jpg)

### 查看启动进程的状态

> $ jps

![查看启动状态](https://i.loli.net/2019/06/30/5d184751aabf122988.jpg)

## 使用HDFS

打开网址http://zyh:50070 （HDFS管理界面）,在该界面我们可以查看HDFS的运行状态信息,在Browse the file system一栏中可以查看HDFS目录结构

![Browse the file system](https://i.loli.net/2019/06/30/5d1847531472850379.jpg)

因为我们什么都没有做,所以在Browse Directory下面什么都没有,HDFS的目录结构和linux的目录结构差不多,都是以``/``为根目录.

![什么都没有](https://i.loli.net/2019/06/30/5d1847540b49622501.jpg)

编写test.txt并上传到HDFS中(被上传的文件会被分为若干个切块，分别放于不同的datanode中)

![test.txt](https://i.loli.net/2019/06/30/5d184755225a588947.jpg)

键入命令,将test.txt上传到hdfs上

> $ hadoop fs -put test.txt hdfs://zyh:9000/

![put](https://i.loli.net/2019/06/30/5d1856883ee1b39713.jpg)

再次打开http://zyh:50070,查看HDFS就会发现多出了一个test.txt文件

![查看结果](https://i.loli.net/2019/06/30/5d1856891db3037047.jpg)

## 使用MR

到**hadoop-2.4.1/share/hadoop/mapreduce**目录下可以找到**hadoop-mapreduce-examples-2.4.1.jar**,这个jar是Hadoop为我们编写的mapreduce小例子,我们可以使用它来做一些测试

![examples](https://i.loli.net/2019/06/30/5d18568a5a14a37356.jpg)

我们使用MR做一些小测试！

* 打印pi的值

到**hadoop-mapreduce-examples-2.4.1.jar**根目录

1. pi : 方法名
2. 5 : 参数1
3. 100 : 参数2

> $ hadoop jar hadoop-mapreduce-examples-2.4.1.jar pi 5 100

![pi](https://i.loli.net/2019/06/30/5d18568c4251f40910.jpg)

* 统计我们之前test.txt中字符串出现的次数

> $ cat test.txt

![test file](https://i.loli.net/2019/06/30/5d18568e7a5b870045.jpg)

这一次我们在HDFS文件系统中创建一些目录,将test.txt上传到指定目录中去

创建/**wordcount**/**input**用来放被统计的文件,值得注意的是我们必须先创建/**wordcount**,才能再创建/**input**

> $ hadoop fs -mkdir /wordcount

> $ hadoop fs -mkdir /wordcount/input

![](https://i.loli.net/2019/06/30/5d18568fba13758809.jpg)

![](https://i.loli.net/2019/06/30/5d1856912037076903.jpg)

同理创建创建/**wordcount**/**output**用来放被统计后的输出文件

> $ hadoop fs -mkdir /wordcount

> $ hadoop fs -mkdir /wordcount/out 

将test.txt文件上传到HDFS文件系统中的input目录

> $ hadoop fs -put text.txt /wordcount/input 

使用命令对test.txt进行统计,**wordcount**:指定本次运行的是统计方法,/**wordcount**/**input**:指定被统计的文件,/**wordcount**/**out**: 指定统计后的输出目录

1. wordcount : 方法名
2. /wordcount/input : 参数1
3. /wordcount/out : 参数2

> $ hadoop jar hadoop-mapreduce-examples-2.4.1.jar wordcount /wordcount/input /wordcount/out 

![](https://i.loli.net/2019/06/30/5d185692e5a9d43661.jpg)

到/**wordcount**/**out**查看MR分析结果,并使用命令下载文件

> $ hadoop fs -ls /wordcount/out/

![](https://i.loli.net/2019/06/30/5d185699bc9f428703.jpg)

> $ hadoop fs -get /wordcount/out part-r-00000

![](https://i.loli.net/2019/06/30/5d18569c354df29231.jpg)

查看MR分析结果

![](https://i.loli.net/2019/06/30/5d18569d7134b87906.jpg)