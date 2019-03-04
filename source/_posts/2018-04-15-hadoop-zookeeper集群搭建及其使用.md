---
layout: post
title: 部署zookeeper集群

date: 2018-04-15 00:00:00
categories: 大数据
tags: Zookeeper
---

zookeeper是一个分布式协调服务框架，本次手写RPC框架需要使用zookeeper做中间件，进行通信的业务的协调。下面开始部署分布式zookeeper。这边我使用的是虚拟机，在虚拟机中部署多台zookeeper。

## 1.下载

我们需要到apache官网上下载Zookeeper,官网地址https://archive.apache.org/dist/zookeeper/,我这边是ubuntu操作系统,下载尾缀是tar.gz,如果是windows下载zip，我下载的是3.4.10版本

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fqdbob01lyj30pu0t9tc4.jpg)

## 2.启动虚拟机集群
我在虚拟机中安装了cor1、cor2、cor3、cor4四台机器，用的是centOS操作系统。 关于数量配置的是偶数台集群，其实不太好，最好集群数量是基数，这是因为zookeeper的运行机制，只要有半数的集群数存活的话，zookeeper就能正常工作，我们分别启动每台机器。

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fqdbq6y6cyj30z10sgjsm.jpg)

小技巧：SecureCRT链接集群使用`Send commands to all sessions`可以一次性控制多台机器,我们只需要打一条命令就可以了，这个很重要，假如集群数太多上千台，我们不可能一台一台去陪，这个时候使用这个功能就可以同时操作了。

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fqdbxzh3zqj30mx0ju41o.jpg)

## 3.zookeeper配置

配置的话分两步
* 配置zoo.cfg
* 配置配台机器对应的myid

配置zookeeper/conf/zoo.cfg:

```xml
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial 
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between 
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just 
# example sakes.
dataDir=/root/zookeeper/data
dataLogDir=/root/zookeeper/log
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the 
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
server.1=cor1:2888:3888
server.2=cor2:2888:3888
server.3=cor3:2888:3888
server.4=cor4:2888:3888
```
配置里面大部分都不需要我们动，我们只需要配好我们的集群就可以了
> server.1=cor1:2888:3888   
> server.2=cor2:2888:3888    
> server.3=cor3:2888:3888    
> server.4=cor4:2888:3888    

2888是内部每个zookeeper的通信接口
3888是zookeeper的投票选举leader的接口

后续我们需要在zookeeper/data/目录下创建每台zookeeper的id
创建`myid`文件 在里面写上每台机器对应的编号,如果是`cor1` 就在`myid`文件中写上**1**,`cor2`就写**2**

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fqdc9n7du3j30ni0iqq42.jpg)

## 4.配置集群服务器

在一台机器上部署好zookeeper后，我们使用`scp`命令将配好的zookeeper分发到其他机器上就可以了。但是运行zookeeper还需要Java环境，我们不可能手动为每台电脑一一做配置，这边就用脚本。其中牵扯两个脚本auto_install_jdk.sh和install_jdk.sh

思路：ssh免密登录`-->`发送jdk安装包`-->`发送jdk安装脚本（自动解压jdk,自动配置环境变量,自动运行zookeeper）`-->`发送已配好的zookeeper包`-->`运行已发送的jdk安装脚本

**auto_install_jdk.sh**

```shell
#!/bin/bash
SERVERS="192.168.0.102"
PASSWORD="1"
INDEX=1

auto_ssh(){
	expect -c "set timeout -1;
        spawn ssh-copy-id root@$1;
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            *password:* {send -- $2\r;exp_continue;}
            eof {exit 0;}
        }";
}
each_server(){
    for SERVER in $SERVERS
    do
        auto_ssh $SERVER $PASSWORD
    done
}

each_server

#发送jdk安装包
scp $HOME/Documents/jdk-8u161-linux-x64.tar.gz root@$SERVER:/root
#发送jdk安装命令并自动配置环境变量的脚本1
scp $HOME/workspace/shell/install_jdk.sh root@$SERVER:/root
#发送zookeeper包
scp -r /home/zyh/zookeeper root@$SERVER:/root

#脚本1 $INDEX 指的就是每台机器对应的myid
ssh root@$SERVER /root/install_jdk.sh $INDEX
```

**install_jdk.sh**
```shell
#/bin/bash
tar -zxvf /root/jdk-8u161-linux-x64.tar.gz -C ./
cat >> /etc/profile << EOF
export JAVA_HOME=/root/jdk1.8.0_161
export PATH=\$PATH:\$JAVA_HOME/bin
EOF
source /etc/profile

#关闭防火墙
service iptables stop
chkconfig iptables off

echo "" > /root/zookeeper/data/myid
echo $1 > /root/zookeeper/data/myid

cd /root/zookeeper/bin
./zkServer.sh start
```

## 5.运行脚本

这边想要运行修改一下下面的参数
> SERVERS="192.168.0.102"  
> PASSWORD="1"  
> INDEX=1  

执行./auto_install_jdk.sh，脚本还有很多优化的地方，可以结合自己的业务场景适当修改。







