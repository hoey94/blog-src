---
layout: post
title: Azkaban任务调度系统部署

date: 2018-05-05 00:00:00
categories: 大数据
tags: Azkaban
---

## 概述

### 为什么需要工作流调度系统

一个完整的数据分析系统通常都是由大量任务单元组成：

shell脚本程序，java程序，mapreduce程序、hive脚本等

各任务单元之间存在时间先后及前后依赖关系

为了很好地组织起这样的复杂执行计划，需要一个工作流调度系统来调度执行；

 

例如，我们可能有这样一个需求，某个业务系统每天产生20G原始数据，我们每天都要对其进行处理，处理步骤如下所示：

1、  通过Hadoop先将原始数据同步到HDFS上；

2、  借助MapReduce计算框架对原始数据进行转换，生成的数据以分区表的形式存储到多张Hive表中；

3、  需要对Hive中多个表的数据进行JOIN处理，得到一个明细数据Hive大表；

4、  将明细数据进行复杂的统计分析，得到结果报表信息；

5、  需要将统计分析得到的结果数据同步到业务系统中，供业务调用使用。

### 工作流调度实现方式

简单的任务调度：直接使用linux的crontab来定义；

复杂的任务调度：开发调度平台

或使用现成的开源调度系统，比如ooize、azkaban等

###  常见工作流调度系统

市面上目前有许多工作流调度器

在hadoop领域，常见的工作流调度器有Oozie, Azkaban,Cascading,Hamake等

### 各种调度工具特性对比

下面的表格对上述四种hadoop工作流调度器的关键特性进行了比较，尽管这些工作流调度器能够解决的需求场景基本一致，但在设计理念，目标用户，应用场景等方面还是存在显著的区别，在做技术选型的时候，可以提供参考

<table>
<tr>
    <td>特性</td>
    <td>Hamake</td>
    <td>Oozie</td>
    <td>Azkaban</td>
    <td>Cascading</td>
</tr>
<tr>
    <td>工作流描述语言</td>
    <td>XML</td>
    <td>XML (xPDL based)</td>
    <td>text file with key/value pairs</td>
    <td>Java API</td>
</tr>
<tr>
    <td>依赖机制</td>
    <td>data-driven</td>
    <td>explicit</td>
    <td>explicit</td>
    <td>explicit</td>
</tr>
<tr>
    <td>是否要web容器</td>
    <td>No</td>
    <td>Yes</td>
    <td>yes</td>
    <td>yes</td>
</tr>
<tr>
    <td>进度跟踪</td>
    <td>console/log messages</td>
    <td>web page</td>
    <td>web page</td>
    <td>Java API</td>
</tr>
<tr>
    <td>Hadoop job调度支持</td>
    <td>No</td>
    <td>Yes</td>
    <td>yes</td>
    <td>yes</td>
</tr>
<tr>
    <td>运行模式</td>
    <td>command line utility</td>
    <td>daemon</td>
    <td>daemon</td>
    <td>API</td>
</tr>
<tr>
    <td>Pig支持</td>
    <td>YES</td>
    <td>Yes</td>
    <td>yes</td>
    <td>yes</td>
</tr>
<tr>
    <td>事件通知</td>
    <td>no</td>
    <td>no</td>
    <td>no</td>
    <td>yes</td>
</tr>
<tr>
    <td>需要安装</td>
    <td>No</td>
    <td>Yes</td>
    <td>yes</td>
    <td>no</td>
</tr>
<tr>
    <td>支持的hadoop版本</td>
    <td>0.18+</td>
    <td>0.20+</td>
    <td>currently unknown</td>
    <td>0.18+</td>
</tr>
<tr>
    <td>重试支持</td>
    <td>no</td>
    <td>workflownode evel</td>
    <td>yes</td>
    <td>yes</td>
</tr>
<tr>
    <td>运行任意命令</td>
    <td>yes</td>
    <td>yes</td>
    <td>yes</td>
    <td>yes</td>
</tr>
<tr>
    <td>Amazon EMR支持</td>
    <td>yes</td>
    <td>no</td>
    <td>currently unknown</td>
    <td>yes</td>
</tr>
</table>

### Azkaban与Oozie对比

对市面上最流行的两种调度器，给出以下详细对比，以供技术选型参考。总体来说，ooize相比azkaban是一个重量级的任务调度系统，功能全面，但配置使用也更复杂。如果可以不在意某些功能的缺失，轻量级调度器azkaban是很不错的候选对象。

详情如下:

**功能**

两者均可以调度mapreduce,pig,java,脚本工作流任务

两者均可以定时执行工作流任务

**工作流定义**

Azkaban使用Properties文件定义工作流

Oozie使用XML文件定义工作流

**工作流传参**

Azkaban支持直接传参，例如${input}

Oozie支持参数和EL表达式，例如${fs:dirSize(myInputDir)}

**定时执行**

Azkaban的定时执行任务是基于时间的

Oozie的定时执行任务基于时间和输入数据

**资源管理**

Azkaban有较严格的权限控制，如用户对工作流进行读/写/执行等操作

Oozie暂无严格的权限控制

**工作流执行**

Azkaban有两种运行模式，分别是soloserver mode(executor server和web server部署在同一台节点)和multi server mode(executor server和web server可以部署在不同节点)

Oozie作为工作流服务器运行，支持多用户和多工作流

**工作流管理**

Azkaban支持浏览器以及ajax方式操作工作流

Oozie支持命令行、HTTP REST、Java API、浏览器操作工作流

## Azkaban介绍

Azkaban是由Linkedin开源的一个批量工作流任务调度器。用于在一个工作流内以一个特定的顺序运行一组工作和流程。Azkaban定义了一种KV文件格式来建立任务之间的依赖关系，并提供一个易于使用的web用户界面维护和跟踪你的工作流。

它有如下功能特点：

* Web用户界面
* 方便上传工作流
* 方便设置任务之间的关系
* 调度工作流
* 认证/授权(权限的工作)
* 能够杀死并重新启动工作流
* 模块化和可插拔的插件机制
* 项目工作区
* 工作流和任务的日志记录和审计

## Azkaban安装部署

### 准备工作

Azkaban Web服务器

azkaban-web-server-2.5.0.tar.gz

Azkaban执行服务器 

azkaban-executor-server-2.5.0.tar.gz

MySQL

目前azkaban只支持 mysql,需安装mysql服务器,本文档中默认已安装好mysql服务器,并建立了 root用户,密码 root.下载地址:http://azkaban.github.io/downloads.html
 
### 安装

将安装文件上传到集群,最好上传到安装 hive、sqoop的机器上,方便命令的执行

在当前用户目录下新建 azkabantools目录,用于存放源安装文件.新建azkaban目录,用于存放azkaban运行程序

#### 1.azkaban web服务器安装

解压azkaban-web-server-2.5.0.tar.gz

命令: tar –zxvf azkaban-web-server-2.5.0.tar.gz

将解压后的azkaban-web-server-2.5.0 移动到 azkaban目录中,并重新命名 webserver
```shell
mv azkaban-web-server-2.5.0 ../azkaban
cd ../azkaban
mv azkaban-web-server-2.5.0  server
```

#### 2.azkaban 执行服器安装
解压azkaban-executor-server-2.5.0.tar.gz

命令:tar –zxvf azkaban-executor-server-2.5.0.tar.gz

将解压后的azkaban-executor-server-2.5.0 移动到 azkaban目录中,并重新命名 executor

```shell
mv azkaban-executor-server-2.5.0  ../azkaban
cd ../azkaban
mv azkaban-executor-server-2.5.0  executor
```

azkaban脚本导入

解压: azkaban-sql-script-2.5.0.tar.gz

命令:tar –zxvf azkaban-sql-script-2.5.0.tar.gz

将解压后的mysql 脚本,导入到mysql中:

进入mysql

```shell
mysql> create database azkaban;
mysql> use azkaban;
Database changed
mysql> source/home/hadoop/azkaban-2.5.0/create-all-sql-2.5.0.sql;
```

### 创建SSL配置

参考地址: http://docs.codehaus.org/display/JETTY/How+to+configure+SSL

命令: keytool -keystore keystore -alias jetty -genkey -keyalg RSA

运行此命令后,会提示输入当前生成 keystor的密码及相应信息,输入的密码请劳记,信息如下:

输入keystore密码： 

再次输入新密码:

您的名字与姓氏是什么？

  [Unknown]： 

您的组织单位名称是什么？

  [Unknown]： 

您的组织名称是什么？

  [Unknown]： 

您所在的城市或区域名称是什么？

  [Unknown]： 

您所在的州或省份名称是什么？

  [Unknown]： 

该单位的两字母国家代码是什么

  [Unknown]：  CN

CN=Unknown, OU=Unknown, O=Unknown,L=Unknown, ST=Unknown, C=CN 正确吗？

  [否]：  y

 

输入<jetty>的主密码

        （如果和 keystore 密码相同，按回车）： 

再次输入新密码:

完成上述工作后,将在当前目录生成 keystore 证书文件,将keystore 考贝到 azkaban web服务器根目录中.如:cp keystore azkaban/server

### 配置文件

注：先配置好服务器节点上的时区

1、先生成时区配置文件Asia/Shanghai，用交互式命令 tzselect 即可

2、拷贝该时区文件，覆盖系统本地时区配置

cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 

 

 

azkaban web服务器配置

进入azkaban web服务器安装目录 conf目录

 

v  修改azkaban.properties文件

命令vi azkaban.properties

内容说明如下:
---
`#`Azkaban Personalization Settings

azkaban.name=Test                           #服务器UI名称,用于服务器上方显示的名字

azkaban.label=My Local Azkaban                               #描述

azkaban.color=#FF3601                                                 #UI颜色

azkaban.default.servlet.path=/index                         #

web.resource.dir=web/                                                 #默认根web目录

`default.timezone.id=Asia/Shanghai`                           #默认时区,已改为亚洲/上海 默认为美国

 

`#`Azkaban UserManager class

user.manager.class=azkaban.user.XmlUserManager   #用户权限管理默认类

user.manager.xml.file=conf/azkaban-users.xml              #用户配置,具体配置参加下文

 

`#`Loader for projects

executor.global.properties=conf/global.properties    # global配置文件所在位置

azkaban.project.dir=projects                                                #

 

`database.type=mysql`                                                              #数据库类型

`mysql.port=3306`                                                                       #端口号

`mysql.host=localhost`                                                      #数据库连接IP

`mysql.database=azkaban`                                                       #数据库实例名

`mysql.user=root`                                                                 #数据库用户名

`mysql.password=root`                                                          #数据库密码

`mysql.numconnections=100`                                                  #最大连接数

 

`#` Velocity dev mode

velocity.dev.mode=false

`#` Jetty服务器属性.

jetty.maxThreads=25                                                               #最大线程数

jetty.ssl.port=8443                                                                   #Jetty SSL端口

jetty.port=8081                                                                         #Jetty端口

`jetty.keystore=keystore`                                                          #SSL文件名

`jetty.password=123456`                                                             #SSL文件密码

`jetty.keypassword=123456`                                                      #Jetty主密码 与 keystore文件相同

`jetty.truststore=keystore`                                                                #SSL文件名

`jetty.trustpassword=123456`                                                   # SSL文件密码

 

`#` 执行服务器属性

executor.port=12321                                                               #执行服务器端口

 

`#` 邮件设置

mail.sender=xxxxxxxx@163.com                                       #发送邮箱

mail.host=smtp.163.com                                                       #发送邮箱smtp地址

mail.user=xxxxxxxx                                       #发送邮件时显示的名称

mail.password=**********                                                 #邮箱密码

job.failure.email=xxxxxxxx@163.com                              #任务失败时发送邮件的地址

job.success.email=xxxxxxxx@163.com                            #任务成功时发送邮件的地址

lockdown.create.projects=false                                           #

cache.directory=cache                                                            #缓存目录

---

v  azkaban 执行服务器executor配置

进入执行服务器安装目录conf,修改azkaban.properties

vi azkaban.properties

---
`#`Azkaban

`default.timezone.id=Asia/Shanghai`                                              #时区

`#` Azkaban JobTypes 插件配置

azkaban.jobtype.plugin.dir=plugins/jobtypes                   #jobtype 插件所在位置

 

`#`Loader for projects

executor.global.properties=conf/global.properties

azkaban.project.dir=projects
 

`#`数据库设置

database.type=mysql                                                 #数据库类型(目前只支持mysql)

mysql.port=3306                                                                                #数据库端口号

`mysql.host=192.168.20.200`                                                           #数据库IP地址

`mysql.database=azkaban`                                                                #数据库实例名

`mysql.user=root`                                                                       #数据库用户名

`mysql.password=root`                                  #数据库密码

mysql.numconnections=100                                                           #最大连接数

 

`#` 执行服务器配置

executor.maxThreads=50                                                                #最大线程数

executor.port=12321                                                               #端口号(如修改,请与web服务中一致)

executor.flow.threads=30                                                                #线程数
---

v  用户配置

进入azkaban web服务器conf目录,修改azkaban-users.xml

vi azkaban-users.xml 增加 管理员用户

---
<azkaban-users>

        <user username="azkaban" password="azkaban" roles="admin" groups="azkaban" />

        <user username="metrics" password="metrics" roles="metrics"/>

        `<user username="admin" password="admin" roles="admin,metrics" />`

        <role name="admin" permissions="ADMIN" />

        <role name="metrics" permissions="METRICS"/>

</azkaban-users>
---

### 启动

#### web服务器

在azkaban web服务器目录下执行启动命令

bin/azkaban-web-start.sh

注:在web服务器根目录运行

或者启动到后台

nohup bin/azkaban-web-start.sh 1>/tmp/azstd.out 2>/tmp/azerr.out &

#### 执行服务器

在执行服务器目录下执行启动命令

bin/azkaban-executor-start.sh

注:只能要执行服务器根目录运行

 

启动完成后,在浏览器(建议使用谷歌浏览器)中输入https://服务器IP地址:8443 ,即可访问azkaban服务了.在登录中输入刚才新的户用名及密码,点击 login.

## Azkaban实战

Azkaba内置的任务类型支持command、java

## Command类型单一job示例

1、创建job描述文件

vi command.job
```shell
#command.job
type=command
command=echo 'hello'
```

2、将job资源文件打包成zip文件
zip -r command.zip command.job

3、通过azkaban的web管理平台创建project并上传job压缩包

首先创建project

![image](http://ww1.sinaimg.cn/large/006qboNIgy1fqzshkulcwj30pq0ij3zv.jpg)

上传zip包

![image](http://ww1.sinaimg.cn/large/006qboNIgy1fqzsie27azj30oi0bvwfi.jpg)

4、启动执行该job

## Command类型多job工作流flow

1、创建有依赖关系的多个job描述

第一个job：foo.job
```shell
# foo.job
type=command
command=echo foo
```

第二个job：bar.job依赖foo.job
```shell
# bar.job
type=command
dependencies=foo
command=echo bar
```
2、将所有job资源文件打到一个zip包中

3、在azkaban的web管理界面创建工程并上传zip包

4、启动工作流flow

## HDFS操作任务

1、创建job描述文件
```shell
#fs.job
type=command
command=/home/hadoop/apps/hadoop-2.6.1/bin/hadoop fs -mkdir /azaz
```
2、将job资源文件打包成zip文件

3、通过azkaban的web管理平台创建project并上传job压缩包

4、启动执行该job

## MAPREDUCE任务
Mr任务依然可以使用command的job类型来执行

1、创建job描述文件，及mr程序jar包（示例中直接使用hadoop自带的examplejar）
```shell
# mrwc.job
type=command
command=/home/hadoop/apps/hadoop-2.6.1/bin/hadoop  jar hadoop-mapreduce-examples-2.6.1.jar wordcount /wordcount/input /wordcount/azout
```
2、将所有job资源文件打到一个zip包中

3、在azkaban的web管理界面创建工程并上传zip包

4、启动job

## HIVE脚本任务

l  创建job描述文件和hive脚本

Hive脚本： test.sql
```shell
use default;
load data local inpath '/home/hadoop/demo.json' into table statis;
insert into table statis_new
select get_json_object(line,'$.username') as username,get_json_object(line,'$.visitdate') as visitdate,get_json_object(line,'$.visit') as visitdate,get_json_object(line,'$.visit') as sumvisit from statis;
insert overwrite table statis_new
select A.username,A.visitdate,max(A.visit) as visit,sum(B.visit) as sumvisit
from 
(select username,visitdate,sum(visit) as visit
from statis_new
group by username,visitdate)A
inner join
(select username,visitdate,sum(visit) as visit
from statis_new
group by username,visitdate)B
on A.username = B.username
where B.visitdate <= A.visitdate
group by A.username,A.visitdate;
```

Job描述文件：hivef.job

```shell
# hivef.job
type=command
command=/home/hadoop/apps/hive/bin/hive -f 'test.sql'
```
2、将所有job资源文件打到一个zip包中

3、在azkaban的web管理界面创建工程并上传zip包

4、启动job


感谢博主分享，很不错的资料很全面，转载一波https://blog.csdn.net/hblfyla/article/details/74384915


