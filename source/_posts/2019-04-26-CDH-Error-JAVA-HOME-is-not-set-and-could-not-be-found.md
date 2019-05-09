---
layout: posts
title: 'CDH Error: JAVA_HOME is not set and could not be found.'
date: 2019-04-26 13:23:25
tags: CDH
categories: 大数据
---

### 错误一

```shell
hdfs dfs -mkdir -p /flume/mysql
Permission denied: user=root, access=WRITE, inode="/":hdfs:supergroup:drwxr-xr-x
```

执行命令的用户没有执行权限。直接给当前用户授权。（这种想法是不正确的，不要为了简化输入命令，就试图修改这些东西）正确的做法应该是。切换指定用户执行命令

```shell
[root@cdh1 data]#sudo -u hdfs  hadoop fs -mkdir /newFile
```

或者

```shell
[root@cdh1 data]#sudo -u hdfs  dfhs dfs  -mkdir /newFile
```

更简单的是，先进入这个用户，su hdfs

###  错误二

```shell
sudo -u hdfs hdfs dfs -mkdir -p /flume/mysql  
Error: JAVA_HOME is not set and could not be found.
java -version
java version "1.8.0_91"
```

确实已经设置了JAVA_HOME ，而且在linux shell 执行 echo $JAVA_HOME  也是有输出。

```shell
find / -name cloudera-config.sh
/*/*/*/cloudera-manager/cm-5.10.0/lib64/cmf/service/common/cloudera-config.sh
local JAVA8_HOME_CANDIDATES=(
    '/usr/java/jdk1.8'
    '/usr/java/jre1.8'
    '/usr/lib/jvm/j2sdk1.8-oracle'
    '/usr/lib/jvm/j2sdk1.8-oracle/jre'
    '/usr/lib/jvm/java-8-oracle'
)
```

解决办法:

建立一个已经有的JAVA_HOME  链接到 /usr/java/jdk1.8 就好了！
目标位置：/usr/java/jdk1.8
原文件：/*/*/jdk1.8.0_91

```shell
ln -s 源文件 目标文件
ln -s /*/*/jdk1.8.0_91 /usr/java/jdk1.8
sudo -u hdfs hdfs dfs -mkdir -p /flume/mysql
```

