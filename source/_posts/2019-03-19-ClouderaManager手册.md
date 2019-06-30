---
title: ClouderaManager操作指南
date: 2019-03-19 13:58:42
author: 张帅
categories: 大数据
photos: http://ww1.sinaimg.cn/large/0066vfZIgy1g182hg7z60j30cv068gln.jpg
---

作者 ： 张帅

## 1 前言 ##

构建企业级别的大数据平台不是一件简单的事情，要从多个方面进行考虑，如硬件环境、软件环境。Hadoop生态圈的产品众多，部署、安装、运维、监控等工作异常琐碎，尤其当某个组件出现问题，由于机器的数量、组件的分布情况，往往会使得运维人员无从下手。

目前市面上Hadoop的发型版本主要有三种：

	1. Apache Hadoop
	2. CDH(Cloudera Distribution Hadoop)
	3. HDP(Hortonworks Data Platform)

首先，Apache Hadoop是最正统的发行版本，版本更新快，新特性增加的多，但相对而言Bug较多，组件之间的兼容性也较差。

其次，CDH版本会将Hadoop的各个组件进行打包，形成一个发布版本，针对该版本下的各个组件进行一系列测试，补丁修复，优化策略等，保证了CDH大版本下各个Hadoop组件之间的良好协作性。大部分公司均使用该系列。

最后，HDP版本是Hortonworks公司针对Hadoop的发行版本，暂时没有过多的了解。

----------

CDH的公司Cloudera推出了Cloudera Manager用于CDH版本集群的管理。Cloudera Manager是一款管理CDH集群的端到端的应用产品，可以通过管理界面可视化的对集群中的一系列组件进行统一的管理：部署、安装、配置、监控等。

简单来说，Cloudera Manager有四大功能：

	1. 管理：对集群进行管理，如添加、删除节点等操作。
	2. 监控：监控集群的健康情况，对设置的各种指标和系统运行情况进行全面监控。
	3. 诊断：对集群出现的问题进行诊断，对出现的问题给出建议解决方案。
	4. 集成：对hadoop的多组件进行整合。

Cloudera Manager的核心是Cloudera Manager Server，简称CMS。CMS提供了管理端Web界面，统一针对其他节点进行控制，如图所示

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182jpew5tj30jc0fuq3r.jpg)

**组件介绍**

	1. Agent，Agent安装在集群中的各个节点上，用于启动、结束进程，安装、配置组件，监控节点等
	2. Management Service，由一系列的角色构成，角色有监控、预警、报告等
	3. Database，存储了配置和监控信息
	4. Cloudera Repository，Cloudera Manager用于分发的软件仓库


## 2 前置准备工作 ##

**操作系统尽量和要使用Cloudera Manager版本匹配，可以参考官方给出的Cloudera Manager与操作系统的兼容性参照表。**

[Cloudera Manager官方下载](http://archive.cloudera.com/cm5)

[Cloudera CDH 各个组件官方下载](http://archive.cloudera.com/cdh5/cdh/5/)

[CDH Requirements for Cloudera Manager](https://www.cloudera.com/documentation/enterprise/release-notes/topics/rn_consolidated_pcm.html#cm_cdh_compatibility)

### 2.1 关于RAID 0的说明 ###

尽管建议采用RAID(Redundant Array of Independent Disk,即磁盘阵列)作为NameNode的存储器以保护元数据，但是若将RAID作为datanode的存储设备则不会给HDFS带来益处。HDFS所提供的节点间数据复制技术已可满足数据备份需求，无需使用RAID的冗余机制。

此外，尽管RAID条带化技术(RAID 0)被广泛用户提升性能，但是其速度仍然比用在HDFS里的JBOD(Just a Bunch Of Disks)配置慢。JBOD在所有磁盘之间循环调度HDFS块。RAID 0的读写操作受限于磁盘阵列中最慢盘片的速度，而JBOD的磁盘操作均独立，因而平均读写速度高于最慢盘片的读写速度。需要强调的是，各个磁盘的性能在实际使用中总存在相当大的差异，即使对于相同型号的磁盘。针对某一雅虎集群的评测报告[点我](http://markmail.org/message/xmzc45zi25htr7ry)表明，在一个测试(Gridmix)中，JBOD比RAID 0 快10%；在另一测试(HDFS写吞吐量)中，JBOD比RAID 0 快30%。

最后，若JBOD配置的某一磁盘出现故障，HDFS可以忽略该磁盘，继续工作。而RAID的某一盘片故障会导致整个磁盘阵列不可用，进而使相应节点失效。

[https://zh.hortonworks.com/blog/why-not-raid-0-its-about-time-and-snowflakes/](https://zh.hortonworks.com/blog/why-not-raid-0-its-about-time-and-snowflakes/)

*备注：我们实际生成环境使用的是RAID5，12块4T硬盘，可用空间为40T。虽然有可能因为RAID卡的损坏导致节点故障，但是RAID卡极大程度的提高了IO性能，并且在逻辑上将12块硬盘映射为了一块大磁盘。单块磁盘故障不会影响到节点的状态。*


### 2.2 IP地址 ###

尽可能的将集群部署在同一网段中，避免夸路由进行数据交互。

### 2.3 主机名及映射 ###

主机名映射为全限定名称和短名称的形式，例如：
​	
​	192.168.15.193 datacenter01.aisino.com datacenter01

### 2.4 启动级别 ###

启动级别尽可能设置为3，避免其他图形界面消耗机器资源。

### 2.5 防火墙和selinux ###

关闭防火墙的原因是一些动态任务（YARN、Spark Executor）在运行时动态分配端口号，如果开启防火墙的话会导致任务无法连接，导致任务执行失败。

selinux记得要关闭。

### 2.6 配置系统文件打开数量以及用户最大进程数量 ###

	vi /etc/security/limits.conf
	* soft nofile 65536
	* hard nofile 65536
	* soft nproc 16384
	* hard nproc 16384

*注意，星号表示所有用户*

### 2.7 配置NTP服务 ###

Cloudera Manager要求各个节点都启动NTP服务，保证集群内各节点之间的时间同步，由于是分布式架构，节点与节点之间时刻保持通信，如果节点之间时间差别过大，会导致通信故障，从而节点造成宕机。

### 2.8 配置SSH ###

所有节点都需要配置SSH免密登录（包括自己）。


## 3 安装Cloudera Manager ##

**本次安装环境为CDH-5.7.0版本**

### 3.1 下载安装包 ###

	1. 下载Cloudera Manager安装包
	http://archive.cloudera.com/cm5/cm/5/cloudera-manager-centos7-cm5.7.0_x86_64.tar.gz
	
	2. 下载Parcel离线包
	http://archive.cloudera.com/cdh5/parcels/5.7.0/CDH-5.7.0-1.cdh5.7.0.p0.45-el7.parcel
	http://archive.cloudera.com/cdh5/parcels/5.7.0/CDH-5.7.0-1.cdh5.7.0.p0.45-el7.parcel.sha1
	http://archive.cloudera.com/cdh5/parcels/5.7.0/manifest.json

### 3.2 安装yum依赖 ###

	yum install -y chkconfig python bind-utils psmisc libxslt zlib sqlite
	yum install -y cyrus-sasl-plain cyrus-sasl-gssapi fuse portmap fuse-libs
	yum install -y redhat-lsb bind-utils libxslt
	yum install -y protobuf snappy

### 3.3 安装MySQL数据库 ###

Cloudera Manager需要将配置信息以及监控信息存储至数据库中，这里采用MySQL数据。

### 3.4 MySQL驱动包路径 ###

必须将MySQL驱动包复制至/usr/share/java目录下，并且驱动包的名称必须为mysql-connector-java.jar。

**注意，所有节点都需要MySQL驱动包**

### 3.5 在MySQL中创建数据库 ###

	create database hive DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
	create database hue DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
	create database monitor DEFAULT CHARSET 
	utf8 COLLATE utf8_general_ci;
	create database oozie DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
	create database cloudera DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

### 3.6 解压Cloudera Manager安装包 ###

Cloudera Manager Server服务安装在Manager1服务器上，因此需要将Cloudera Manager的压缩包以及所有Parcel文件上传至服务器，并将Cloudera Manager压缩包解压至/opt/cloudera-manager目录下

### 3.7 创建用户 ###

在所有节点上创建cloudera-scm用户：
​	
​	useradd --system --home=/opt/cloudera-manager/cm-5.7.0/run/cloudera-scm-server --no-create-home --shell=/bin/false --comment "Cloudera SCM User" cloudera-scm

### 3.8 创建Cloudera Manager Server元数据目录 ###

在主节点上需要创建Cloudera Manager Server的元数据目录：

	mkdir /var/cloudera-scm-server
	chown cloudera-scm:cloudera-scm /var/cloudera-scm-server
	chown cloudera-scm:cloudera-scm /opt/cloudera-manager

### 3.9 复制cloudera-manager目录到其他节点 ###

首先将/opt/cloudera-manager/cm-5.7.0/etc/cloudera-scm-agent/config.ini文件中server_host配置项的地址更改为主节点的地址

将主节点上/opt/cloudera-manager目录复制至其他集群节点下，命令如下：

	scp -r /opt/cloudera-manager 主机:/opt/

### 3.10 创建Parcel目录 ###

在主节点上创建Parcel包的存储目录，命令如下：

	mkdir -p /opt/cloudera/parcel-repo
	chown cloudera-scm:cloudera-scm /opt/cloudera/parcel-repo

将以下文件复制到该目录下

* CDH-5.7.0-1.cdh5.7.0.p0.45-el7.parcel
* CDH-5.7.0-1.cdh5.7.0.p0.45-el7.parcel.sha1
* manifest.json


将**CDH-5.7.0-1.cdh5.7.0.p0.45-el7.parcel.sha1**文件的名称修改为**CDH-5.7.0-1.cdh5.7.0.p0.45-el7.parcel.sha**

### 3.11 创建Parcel包分发目录 ###

Cloudera Manager在安装的过程中，需要将安装包复制到集群的各个节点上，因此需要在集群各个节点上事先创建Parcel包的分发目录。

在所有节点上：

	mkdir -p /opt/cloudera/parcels
	chown cloudera-scm:cloudera-scm /opt/cloudera/parcels

### 3.12 初始化CSM数据库脚本 ###

在主节点上，执行初始化脚本：

	/opt/cloudera-manager/cm-5.7.0/share/cmf/schema/scm_prepare_database.sh mysql -hmanager1 -uroot -p123456 --scm-host manager1 scmdbn scmdbu scmdbp

说明：这个脚本就是用来创建和配置CMS需要的数据库的脚本。

各参数是指：

mysql：数据库用的是mysql，如果安装过程中用的oracle，那么该参数就应该改为oracle。

-hmanager1：数据库建立在manager1主机上面。也就是主节点上面。

-uroot：root身份运行mysql。

-123456：mysql的root密码是123456。

--scm-host manager1：CMS的主机，一般是和mysql安装的主机是在同一个主机上。

最后三个参数是：数据库名，数据库用户名，数据库密码。

**我的实际环境中采用如下命令**

	/opt/cloudera-manager/cm-5.7.0/share/cmf/schema/scm_prepare_database.sh mysql -hlocalhost -uroot -p -P13066 --scm-host localhost cloudera root BIM@123%$#qwe 

### 3.13 配置与启动Cloudera Manager Server ###

首先将Cloudera Manager Server的启动脚本复制到/etc/init.d/目录下：
​	
​	cp \
​	/opt/cloudera-manager/cm-5.7.0/etc/init.d/cloudera-scm-server \
​	/etc/init.d/cloudera-scm-server

配置/etc/init.d/cloudera-scm-server：

	vi /etc/init.d/cloudera-scm-server
	找到CMF_DEFAULTS配置项，进行修改。
	CMF_DEFAULTS=${CMF_DEFAULTS:-/opt/cloudera-manager/cm-5.7.0/etc/default}

启动Cloudera Manager Server：

	service cloudera-scm-server start
	chkconfig cloudera-scm-server on

### 3.14 配置与启动Cloudera Manager Agent ###

在所有节点上创建agent的运行时目录：

	mkdir /opt/cloudera-manager/cm-5.7.0/run/cloudera-scm-agent

将Cloudera Manager Agent的启动脚本复制到/etc/init.d/目录下：

	cp \
	/opt/cloudera-manager/cm-5.7.0/etc/init.d/cloudera-scm-agent \
	/etc/init.d/cloudera-scm-agent

配置Cloudera Manager Agent：

	vi /etc/init.d/cloudera-scm-agent 
	找到CMF_DEFAULTS配置项，进行修改。
	CMF_DEFAULTS=${CMF_DEFAULTS:-/opt/cloudera-manager/cm-5.7.0/etc/default}

启动Cloudera Manager Agent：

	service cloudera-scm-agent start
	chkconfig cloudera-scm-agent on

### 3.15 日志文件路径 ###

启动Server或Agent由于各种原因可能会导致启动失败，因此需要查看日志文件定位错误信息，进行修复。

Server的日志文件位于：

	/opt/cloudera-manager/cm-5.7.0/log/cloudera-scm-server

Agent的日志文件位于：

	/opt/cloudera-manager/cm-5.7.0/log/cloudera-scm-agent

### 3.16 进入Cloudera Manager Server管理页面 ###

当Server与Agent全部启动完成后，可以访问CMS的WEB管理页面[example link](http://localhost:7180 "例子")，如图所示。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pm79yij30lz08k0su.jpg)

*账户密码均为admin*

## 4 安装CDH ##

*在Cloudera Manager Server的WEB管理页面中，可以批量进行组件的安装、配置等，下面开始安装CDH各种组件。*

### 4.1 接受协议 ###

首次登陆时，会自动弹出“接受协议”页面，接受即可。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmcti9j30m00b2wh3.jpg)

### 4.2 选择版本 ###

选择版本时，选择免费版本即可。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmgi4bj30m409n401.jpg)

### 4.3 查看当前已管理主机 ###

如果Agent正产启动，在“当前管理的主机”页面会显示所有管理主机，否则请检查Agent是否正常启动。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmkbq7j30m30awta9.jpg)

选择所有主机，点击“继续”按钮。

### 4.4 等待系统分发Parcel包 ###

Cloudera Manager会将Parcel包分发至各个节点，等待几分钟即可。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pm7kulj30m108ojro.jpg)

**注意，在分发Parcel包的过程中，可以会出现分发失败的问题，查看相应的Agent日志，定位错误，进行修复。**

**比较常见的一个错误是Python脚本出现问题，需要进行一些修改，参见链接：**
[http://www.jianshu.com/p/0d70a67b66b2](http://www.jianshu.com/p/0d70a67b66b2)

#### 4.5 等待检查主机正确性 ####

Parcel包分发完成后，Cloudera Manager会检查主机的的正确性，包括一些优化的配置、要关闭的属性等，该步骤非常重要，一定要根据检查结果对主机进行配置修复，否则在以后的过程中会出现各种不可预料问题。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pm7fgtj30m00aqaab.jpg)

### 4.6 选择要安装的组件 ###

主机正确性检查完成后，就可以进入安装环节了，Cloudera Manager会要求你选择要安装的组件。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmiziwj30m30auwgm.jpg)

**选择“自定义服务”，选择集群中要安装的组件。**

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmmg99j30m20bhdjk.jpg)

### 4.7 设置数据库 ###

选择完成要安装的组件后，需要为Cloudera Manager配置运行时数据库环境，如图所示。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmbbqkj30m60bn75o.jpg)

配置的数据库在前面的步骤中已经提前创建完成。

### 4.8 设置组件的基本运行环境 ###

该步骤主要用于设置组件的基本运行环境，例如NameNode的节点、DataNode的节点、数据存放的目录等，该步骤根据实际的物理环境进行设置即可。

### 4.9 等待启动集群 ###

在集群的启动过程中，可能会因为权限或其他问题导致某些服务启动失败，只需要根据错误信息进行修复，即可启动完成。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pma4kyj30ly0b2dgq.jpg)

### 4.10 启动成功 ###

集群启动成功后，可在首页查看集群的总览。

![](http://ww1.sinaimg.cn/large/0066vfZIgy1g182pmklf3j30m00a70ut.jpg)

### 4.11 其他 ###

后续可以启动HDFS的HA、YARN的HA以及优化各个组件的配置等。

感谢张帅分享。