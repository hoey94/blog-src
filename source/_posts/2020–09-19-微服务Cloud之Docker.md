---
title: 微服务Cloud之Docker
date: 2020年09月19 11:49:00
categories: 微服务
tags: Docker
---


![1586333742105](http://qgw3wcroi.hn-bkt.clouddn.com/1586333742105.png)

> Author：Eric 
> 
> Version：9.0.1
> 
> From : 转载


看到Eric哥们在b站中分享的Docker视频，觉得讲的很好，这里提供一下讲义方便大家学习。


[TOC]

### 一、引言

----

#### 1.1 环境不一致

> 我本地运行没问题啊：由于环境不一致，导致相同的程序，运行结果却不一致。



#### 1.2 隔离性

> 哪个哥们又写死循环了，怎么这么卡：在多用户的操作系统下，会因为其他用户的操作失误影响到你自己编写的程序。



#### 1.3 弹性伸缩

> 淘宝在双11，用户量暴增：需要很多很多的运维人员去增加部署的服务器，运维成本过高。



#### 1.4 学习成本

> 学习一门技术，得先安装啊：学习每一门技术都要先安装响应的软件，但是还有他所依赖的各种环境，安装软件成本快高过学习成本啦。



### 二、Docker介绍

---

#### 2.1 Docker的由来

> Docker 最初是 dotCloud 公司创始人Solomon Hykes 在法国期间发起的一个公司内部项目。
>
> 2010年的专门做PAAS平台，但是到了2013年的时候，像亚马逊，微软，Google都开始做PAAS平台。
>
> 到了2013年，公司资金链断裂，不得不倒闭，于是将公司内的核心技术对外开源，核心技术就是Docker。
>
> 由于开源了Docker，到了2014年的时候，得到了各轮融资，于是公司开始全神贯注的维护Docker。

|            Docker主要作者-Solomon            |
| :------------------------------------------: |
| ![1586340594252](http://qgw3wcroi.hn-bkt.clouddn.com/1586340594252.png) |

|    现在Solomon已经离开了维护Docker的团队     |
| :------------------------------------------: |
| ![1586340639934](http://qgw3wcroi.hn-bkt.clouddn.com/1586340639934.png) |



#### 2.2 Docker的思想

> - 封装：将需要的操作系统，环境，软件封装到一个镜像中。
>
> - 标准化：
>   - 运输的标准化：Docker提供了中央仓库，所有官方的镜像都放在了这个中央仓库中，当需要使用某一个镜像时，通过相应的方式拉取即可。
>   - 命令的标准化：Docker提供了一些列的命令，帮助我们去获取镜像，管理容器等等操作。
>   - 提供了REST的API：基于标准REST的API衍生出了很多的图形化界面，如Rancher等。
>
> - 隔离性：Docker在运行镜像时，会在Linux的内核中，单独的开辟一片空间，这片空间不会影响到其他程序。



### 三、Docker的安装

----

#### 3.1 下载Docker依赖的环境

> 安装Docker，需要先将依赖的环境全部下载，就像Maven依赖JDK一样。

```sh
yum -y install yum-utils device-mapper-persistent-data lvm2
```



#### 3.2 指定Docker镜像源

> 默认情况下，下载Docker会从国外服务器下载，速度较慢，我们可以设置为阿里云镜像源，速度更快。

```sh
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```



#### 3.3 安装Docker

> 采用yum的方式安装。

```sh
yum makecache fast
yum -y install docker-ce
```

Docker 安装不了可能是源的问题,我的机器是ubuntu，这里参考了链接完成了安装https://www.runoob.com/docker/ubuntu-docker-install.html


#### 3.4 启动Docker并测试

> 安装成功后，需要手动启动，设置为开机自启，并测试。

```sh
# 启动Docker服务
systemctl start docker
# 设置开机自动启动
systemctl enable docker
# 测试
docker run hello-world
```



### 四、Docker的中央仓库【`重点`】

----

> - Docker官方的中央仓库：这个仓库是镜像最全的，但是下载速度较慢。
>
>      https://hub.docker.com/
>
> - 国内的镜像网站：网易蜂巢，daoCloud等，下载速度快，但是镜像相对不全。
>
>      https://c.163yun.com/hub#/home
>
>      http://hub.daocloud.io/     （推荐使用）
>
> - 在公司内部会采用私服的方式拉取镜像，需要添加配置，如下……

```json
# 需要创建或修改/etc/docker/daemon.json，并添加如下内容，"ip:port"可以编写多个。
{
	"registry-mirrors": ["https://registry.docker-cn.com"],
	"insecure-registries": ["ip:port"]   
}
# 重启docker服务
systemctl restart docker
```



### 五、镜像的操作

----

#### 5.1 拉取镜像

> 从中央仓库拉取镜像到本地

```sh
docker pull 镜像名称[:tag]

# 举个栗子：docker pull daocloud.io/library/tomcat:8.5.15-jre8
```



#### 5.2 查看本地全部镜像

> 查看本地已经安装过的镜像信息，包含标识，名称，版本，更新时间，大小

```sh
docker images
```



#### 5.3 删除本地镜像

> 镜像会占用磁盘空间，可以直接手动删除，表示通过查看获取

```sh
docker rmi 镜像的标识 | 镜像名称:tag
docker rmi b8dfe9ade316
docker rmi daocloud.io/library/tomcat:8.5.15-jre8
```



#### 5.4 镜像的导入导出

> - 如果出现网络故障，可以采过硬盘的方式传输镜像，虽然不规范，但是有效。
> - 但是这种方式导出的镜像名称和版本都是null，需要手动修改

```sh
# 将本地的镜像导出
docker save -o 导出的路径 镜像id
doeker save -o /usr/local/abc.tar b8dfe9ade316
# 加载本地的镜像文件
docker load -i 镜像文件
docker load -i /usr/local/abc.tar
# 修改镜像名称
docker tag 镜像id 新镜像名称:版本
docker tag b8dfe9ade316  mytomcat:1.0
```



### 六、容器操作【`重点`】

----

#### 6.1 运行容器

> 运行容器需要指定具体镜像，如果镜像不存在，会直接下载

```sh
# 简单操作
docker run 镜像的标识 | 镜像名称[:tag]
docker run b8dfe9ade316
docker run daocloud.io/library/tomcat:8.5.15-jre8
# 常用的参数
docker run -d -p 宿主机端口:容器端口 --name 容器名称 镜像的标识|镜像名称[:tag]
docker run -d -p 8090:8080 --name my_container b8dfe9ade316
# -d：代表后台运行容器
# -p 宿主机端口:容器端口：为了映射当前Linux的端口和容器的端口
# --name 容器名称：指定容器的名称
```



#### 6.2 查看正在运行的容器

> 查看全部正在运行的容器信息

```sh
docker ps [-qa]
# -a：查看全部的容器，包括没有运行
# -q：只查看容器的标识
```



#### 6.3 查看容器日志

> 查看容器日志，以查看容器运行的信息

```sh
docker logs -f 容器id
# -f：可以滚动查看日志的最后几行
```



#### 6.4 进入容器内容部

> 可以进入容器内部进行操作

```sh
docker exec -it 容器id bash
docker exec -it 容器名称 bash
```



#### 6.5 复制内容到容器

> 将宿主机的文件复制到容器内部的指定目录

```sh
docker cp 文件名称 容器id:容器内部路径
```



#### 6.6 重启&启动&停止&删除容器

> 容器的启动，停止，删除等操作，后续经常会使用到

```sh
# 重新启动容器
docker restart 容器id

# 启动停止运行的容器
docker start 容器id

# 停止指定的容器（删除容器前，需要先停止容器）
docker stop 容器id
# 停止全部容器
docker stop $(docker ps -qa)

# 删除指定容器
docker rm 容器id
# 删除全部容器
docker rm $(docker ps -qa)
```





### 七、Docker应用

----

#### 7.1 Docker安装Tomcat

> 运行Tomcat容器，为部署SSM工程做准备

```sh
docker run -d -p 8080:8080 --name tomcat daocloud.io/library/tomcat:8.5.15-jre8
```



#### 7.2 Docker安装MySQL

> 运行MySQL容器，为部署SSM工程做准备

```sh
docker run -d -p 3366:3306 --name mysql -e MYSQL_ROOT_PASSWORD=root daocloud.io/library/mysql:5.7.4

# 宿主机中通过 3366连接 容器中的mysql
[root@localhost logs]# mysql -uroot -P 3366 -proot -h 192.168.1.135
```



#### 7.3 部署SSM工程

> - 修改SSM工程环境，设置为Linux中Docker容器的信息
> - 通过Maven的package重新打成war包
> - 将Windows下的war包复制到Linux中
> - 通过docker命令将宿主机的war包复制到容器内部
> - 测试访问SSM工程





### 八、数据卷【`重点`】

---------

> - 为部署SSM的工程，需要使用到Docker的cp命令将宿主机内的ssm.war文件复制到容器内部，操作麻烦。
>
> - [数据卷]()：
>  - 将宿主机的一个目录映射到容器的一个目录中。
>   - 可以在宿主机中操作目录中的内容，容器内部映射的文件会跟着一起改变。



#### 8.1 创建数据卷

> 创建数据卷之后，默认会存放在一个目录下 /var/lib/docker/volumes/数据卷名称/_data

```sh
docker volume create 数据卷名称
```



#### 8.2 查看数据卷详情

> 查看数据卷的详细信息，可以查询到存放路径，创建时间等等

```sh
docker volume inspect 数据卷名称
```



#### 8.3 查看全部数据卷

> 查看全部数据卷信息

```sh
docker volume ls
```



#### 8.4 删除数据卷

> 删除指定数据卷

```sh
docker volume rm 数据卷名称
```



#### 8.5 容器映射数据卷

> 映射有两种方式：
>
> - 通过数据卷名称映射，如果数据卷不存在。Docker会帮你自动创建，会将容器内部自带的文件，存储在默认的存放路径中。
> - 通过路径映射数据卷，直接指定一个路径作为数据卷的存放位置。但是这个路径下是空的。

```sh
# 通过数据卷名称映射
docker run -v 数据卷名称:容器内部的路径 镜像id
docker run -v webapps2004:/usr/local/tomcat/webappss 镜像id
# 通过路径映射数据卷
docker run -v 路径:容器内部的路径 镜像id
docker run -v /usr/local/tomcat_webapps2004:/usr/local/tomcat/webapps 镜像id
```



### 九、Dockerfile自定义镜像【`重点`】

---

> 我们可以从中央仓库下载一个镜像，也可以自己手动去制作一个镜像，需要通过Dockerfile去指定自定义镜像的信息



#### 9.1 Dockerfile

> 创建自定义镜像就需要创建一个Dockerfile，如下为Dockerfile的常用配置

```sh
from: 指定当前自定义镜像依赖的环境
copy: 将相对路径下的内容复制到自定义镜像中
workdir: 声明镜像的默认工作目录
run: 执行的命令，可以编写多个
cmd: 需要执行的命令（在workdir下执行的，cmd可以写多个，但是只以最后一个为准）

# 举个例子，制作SSM容器镜像，而且ssm.war要放在Dockerfile的同级目录下
from daocloud.io/library/tomcat:8.5.15-jre8
copy ssm.war /usr/local/tomcat/webapps
```



#### 9.2 通过Dockerfile制作镜像

> 编写完Dockerfile后需要Dockerfile所在目录通过命令将其制作为镜像，注意最后的 [.]()  代表当前目录。

```sh
docker build -t 镜像名称[:tag] .
```



### 十. Docker-Compose【`重点`】

---------

> - 运行一个容器，我们需要添加大量的参数，可以通过Docker-Compose文件配置参数。
> - 参数信息通过docker-compose.yml文件去维护。
> - Docker-Compose可以批量管理容器。



#### 10.1 下载并安装Docker-Compose

##### 10.1.1 下载Docker-Compose

> 去github官网搜索docker-compose，下载1.24.1版本的Docker-Compose
>
> 下载路径：[https://github.com/docker/compose/releases/download/1.24.1/docker-compose-Linux-x86_64]()



##### 10.1.2 设置权限

> 需要将DockerCompose文件的名称修改一下，给予DockerCompose文件一个可执行的权限

```sh
mv docker-compose-Linux-x86_64 docker-compose
chmod 777 docker-compose
```



##### 10.1.3 移动到/usr/local/bin目录下

>  方便后期操作，将docker-compose文件移动到了/usr/local/bin
>

```sh
mv docker-compose /usr/local/bin
```



##### 10.1.4 测试

> 在任意目录下输入docker-compose

|                   测试效果                   |
| :------------------------------------------: |
| ![1586420176720](http://qgw3wcroi.hn-bkt.clouddn.com/1586420176720.png) |



#### 10.2 Docker-Compose管理MySQL和Tomcat容器

> - yml文件以key: value方式来指定配置信息
>
> - 多个配置信息以换行+缩进的方式来区分
>
> - 在docker-compose.yml文件中，不要使用制表符

```yml
version: '3.1'
services:
  mysql:           # 服务的名称
    restart: always   # 代表只要docker启动，那么这个容器就跟着一起启动
    image: daocloud.io/library/mysql:5.7.4  # 指定镜像路径
    container_name: mysql  # 指定容器名称
    ports:
      - 3306:3306   #  指定端口号的映射
    environment:
      MYSQL_ROOT_PASSWORD: root   # 指定MySQL的ROOT用户登录密码
      TZ: Asia/Shanghai        # 指定时区
    volumes:
     - /opt/docker_mysql_tomcat/mysql_data:/var/lib/mysql   # 映射数据卷
  tomcat:
    restart: always
    image: daocloud.io/library/tomcat:8.5.15-jre8
    container_name: tomcat
    ports:
      - 8080:8080
    environment:
      TZ: Asia/Shanghai
    volumes:
      - /opt/docker_mysql_tomcat/tomcat_webapps:/usr/local/tomcat/webapps
      - /opt/docker_mysql_tomcat/tomcat_logs:/usr/local/tomcat/logs
```



#### 10.3 使用docker-compose命令管理容器

> 在docker-compose.yml文件目录下使用docker-compose的命令时 

```sh
# 1. 基于docker-compose.yml启动管理的容器
docker-compose up -d

# 2. 关闭并删除容器
docker-compose down

# 3. 开启|关闭|重启已经存在的由docker-compose维护的容器
docker-compose start|stop|restart

# 4. 查看由docker-compose管理的容器
docker-compose ps

# 5. 查看日志
docker-compose logs -f
```



#### 10.4 docker-compose配合Dockerfile使用

> 使用docker-compose.yml文件以及Dockerfile文件在生成自定义镜像的同时启动当前镜像，并且由docker-compose去管理容器

##### 10.4.1 docker-compose文件

> 编写docker-compose.yml文件

```yml
# yml文件
version: '3.1'
services:
  ssm:
    restart: always
    build:            # 构建自定义镜像
      context: ../      # 指定dockerfile文件的所在路径
      dockerfile: Dockerfile   # 指定Dockerfile文件名称
    image: ssm:1.0.1
    container_name: ssm
    ports:
      - 8081:8080
    environment:
      TZ: Asia/Shanghai
```



##### 10.4.2 Dockerfile文件

> 编写Dockerfile文件

```
from daocloud.io/library/tomcat:8.5.15-jre8
copy ssm.war /usr/local/tomcat/webapps
```



##### 10.4.3 运行

> 测试效果

```sh
# 可以直接启动基于docker-compose.yml以及Dockerfile文件构建的自定义镜像
docker-compose up -d
# 如果自定义镜像不存在，会帮助我们构建出自定义镜像，如果自定义镜像已经存在，会直接运行这个自定义镜像

# 重新构建自定义镜像
docker-compose build

# 运行当前内容，并重新构建
docker-compose up -d --build
```



### 十一. Docker CI、CD

----

#### 11.1 CI、CD引言

> 项目部署
>
> - 将项目通过maven进行编译打包
> - 将文件上传到指定的服务器中
> - 将war包放到tomcat的目录中
> - 通过Dockerfile将Tomcat和war包转成一个镜像，由DockerCompose去运行容器
>
> 项目更新后，需要将上述流程再次的从头到尾的执行一次，如果每次更新一次都执行一次上述操作，很费时，费力。我们就可以通过CI、CD帮助我们实现持续集成，持续交付和部署。
>



#### 11.2 CI介绍

> CI（continuous intergration）持续集成
>
> 持续集成：编写代码时，完成了一个功能后，立即提交代码到Git仓库中，将项目重新的构建并且测试。
>
> - 快速发现错误。
> - 防止代码偏离主分支。



#### 11.3 搭建Gitlab服务器

> 实现CI，需要使用到Gitlab远程仓库，先通过Docker搭建Gitlab



##### 11.3.1 准备工作

> - 创建一个全新的虚拟机，并且至少指定4G的运行内存，4G运行内存是Gitlab推荐的内存大小。
> - 并且安装Docker以及Docker-Compose



##### 11.3.2 修改ssh的22端口

> 将ssh的默认22端口，修改为60022端口，因为Gitlab需要占用22端口

```
vi /etc/ssh/sshd_config
  PORT 22 -> 60022
systemctl restart sshd
```



##### 11.3.3 编写docker-compose.yml

> docker-compose.yml文件去安装gitlab（下载和运行的时间比较长的）

```yml
version: '3.1'
services:
 gitlab:
  image: 'twang2218/gitlab-ce-zh:11.1.4'
  container_name: "gitlab"
  restart: always
  privileged: true
  hostname: 'gitlab'
  environment:
   TZ: 'Asia/Shanghai'
   GITLAB_OMNIBUS_CONFIG: |
    external_url 'http://192.168.199.110'
    gitlab_rails['time_zone'] = 'Asia/Shanghai'
    gitlab_rails['smtp_enable'] = true
    gitlab_rails['gitlab_shell_ssh_port'] = 22
  ports:
   - '80:80'
   - '443:443'
   - '22:22'
  volumes:
   - /opt/docker_gitlab/config:/etc/gitlab
   - /opt/docker_gitlab/data:/var/opt/gitlab
   - /opt/docker_gitlab/logs:/var/log/gitlab
```



#### 11.4 搭建GitlabRunner

##### 11.4.1 配置私服信息

> 创建或修改/etc/docker/daemon.json，并添加如下内容。

```json
{
  "registry-mirrors": [
    "https://registry.docker-cn.com"
  ],
  "insecure-registries": [
    "baseservice.qfjava.cn:60001" 
  ]
}
```

> 重启两个服务

```sh
systemctl daemon-reload
systemctl restart docker
```



##### 11.4.2 添加docker-compose.yml文件

> - 创建工作目录 /opt/docker_gitlab-runner
> - 在 /opt/docker_gitlab-runner添加docker-compose.yml文件

```yml
version: '3.1'
services:
  gitlab-runner:
    build: environment
    restart: always
    container_name: gitlab-runner
    privileged: true
    volumes:
      - ./config:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
```



##### 11.4.3 在yml文件目录添加环境目录

> 创建environment目录，在目录中逐个添加各个配置及软件

> Dockerfile

```
FROM baseservice.qfjava.cn:60001/gitlab-runner:bleeding
# 修改软件源
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse' > /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse' >> /etc/apt/sources.list && \
    #下面的地址需要根据实际情况变化
    wget https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2018.2_all.deb --no-check-certificate && \
    apt install -y ./kali-archive-keyring_2018.2_all.deb && \
    apt-get update -y && \
    apt install -y  gnupg  && \
    apt-get clean

# 安装 Docker
RUN curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | apt-key add - && \
    apt-get install -y python-software-properties software-properties-common && \
    echo 'deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable' >> /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce

COPY daemon.json /etc/docker/daemon.json

# 安装 Docker Compose,因为下载不下来，所以我们本地上传一份docker-compose到environment目录
WORKDIR /usr/local/bin
#RUN wget https://raw.githubusercontent.com/topsale/resources/master/docker/docker-compose
COPY docker-compose docker-compose
RUN chmod +x docker-compose

# 安装 Java
RUN mkdir -p /usr/local/java
WORKDIR /usr/local/java
COPY jdk-8u231-linux-x64.tar.gz /usr/local/java
RUN tar -zxvf jdk-8u231-linux-x64.tar.gz && \
    rm -fr jdk-8u231-linux-x64.tar.gz

# 安装 Maven
RUN mkdir -p /usr/local/maven
WORKDIR /usr/local/maven
# RUN wget https://raw.githubusercontent.com/topsale/resources/master/maven/apache-maven-3.6.3-bin.tar.gz
COPY apache-maven-3.6.3-bin.tar.gz /usr/local/maven
RUN tar -zxvf apache-maven-3.6.3-bin.tar.gz && \
    rm -fr apache-maven-3.6.3-bin.tar.gz
#需要配置maven 私服的话,不需要就加#注释掉
#COPY settings.xml /usr/local/maven/apache-maven-3.6.3/conf/settings.xml



# 配置环境变量
ENV JAVA_HOME /usr/local/java/jdk1.8.0_231
ENV MAVEN_HOME /usr/local/maven/apache-maven-3.6.3
ENV PATH $PATH:$JAVA_HOME/bin:$MAVEN_HOME/bin

WORKDIR /
```

> daemon.json

```
{
  "registry-mirrors": [
    "https://registry.docker-cn.com"
  ],
  "insecure-registries": [
    "baseservice.qfjava.cn:60001" 
  ]
}
```

> docker-compose可执行文件。

> [apache-maven-3.6.3-bin.tar.gz]()，以及[jdk-8u231-linux-x64.tar.gz]()压缩包文件。



##### 11.4.4 设置Docker权限

> - 在宿主机启动docker程序后先执行 [sudo chown root:root /var/run/docker.sock]()。
> - 在[/opt/docker_gitlab-runner]()目录中执行[docker-compose up -d --build]()启动容器。
> - 启动容器成功后，添加容器权限，保证容器可以使用宿主机的docker：[docker exec -it gitlab-runner usermod -aG root gitlab-runner]()



##### 11.4.5 注册Runner信息到gitlab

> 注册信息整个过程

```sh
docker exec -it gitlab-runner gitlab-runner register

# 输入 GitLab 地址
Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com/):
http://192.168.199.109/  # 根据gitlab地址添加

# 输入 GitLab Token
Please enter the gitlab-ci token for this runner:
1Lxq_f1NRfCfeNbE5WRh

# 输入 Runner 的说明
Please enter the gitlab-ci description for this runner:
可以为空

# 设置 Tag，可以用于指定在构建规定的 tag 时触发 ci
Please enter the gitlab-ci tags for this runner (comma separated):
deploy

# 这里选择 true ，可以用于代码上传后直接执行（根据版本，也会没有次选项）
Whether to run untagged builds [true/false]:
true

# 这里选择 false，可以直接回车，默认为 false（根据版本，也会没有次选项）
Whether to lock Runner to current project [true/false]:
false

# 选择 runner 执行器，这里我们选择的是 shell
Please enter the executor: virtualbox, docker+machine, parallels, shell, ssh, docker-ssh+machine, kubernetes, docker, docker-ssh:
shell
```



#### 11.5 整合项目入门测试

##### 11.5.1 创建项目

> 创建maven工程，添加web.xml文件，编写html页面



##### 11.5.2 编写.gitlab-ci.yml

> 编写[.gitlab-ci.yml]()文件

```
stages:
  - test

test:
  stage: test
  script:
    - echo first test ci   # 测试回声命令，测试效果
```



##### 11.5.3 将maven工程推送到gitlab中

> 执行git命令推送到Gitlab

```sh
git push origin master
```



##### 11.5.4 查看效果

> 可以在gitlab中查看到gitlab-ci.yml编写的内容

|                    效果图                    |
| :------------------------------------------: |
| ![1588671760385](http://qgw3wcroi.hn-bkt.clouddn.com/1588671760385.png) |



#### 11.6 完善项目配置

> 添加Dockerfile以及docker-compose.yml， 并修改[.gitlab-ci.yml]()文件

##### 11.6.1 创建Dockerfile

```
# Dockerfile
FROM daocloud.io/library/tomcat:8.5.15-jre8
COPY testci.war /usr/local/tomcat/webapps
```



##### 11.6.2 创建docker-compose.yml

```yml
# docker-compose.yml
version: "3.1"
services:
  testci:
    build: docker
    restart: always
    container_name: testci
    ports:
      - 8080:8080
```



##### 11.6.3 修改.gitlab-ci.yml

```
# ci.yml
stages:
  - test

test:
  stage: test
  script:
    - echo first test ci
    - /usr/local/maven/apache-maven-3.6.3/bin/mvn package
    - cp target/testci-1.0-SNAPSHOT.war docker/testci.war
    - docker-compose down
    - docker-compose up -d --build
    - docker rmi $(docker images -qf dangling=true)
```



##### 11.6.4 测试

|                   测试效果                   |
| :------------------------------------------: |
| ![1588674040060](http://qgw3wcroi.hn-bkt.clouddn.com/1588674040060.png) |





#### 11.7 CD介绍

> CD（持续交付，持续部署）
>
> 持续交付：将代码交付给专业的测试团队去测试
>
> 持续部署：可以直接将指定好tag的代码直接部署到生产环境中

|                    CICD图                    |
| :------------------------------------------: |
| ![1588677492583](http://qgw3wcroi.hn-bkt.clouddn.com/1588677492583.png) |



#### 11.8 安装Jenkins

##### 11.8.1 编写docker-compose.yml

> 官网：https://www.jenkins.io/

```yml
version: "3.1"
services:
  jenkins:
   image: jenkins/jenkins
   restart: always
   container_name: jenkins
   ports:
     - 8888:8080
     - 50000:50000
   volumes:
     - ./data:/var/jenkins_home
```



##### 11.8.2 运行并访问Jenkins

> 第一次运行时，会因为data目录没有权限，导致启动失败

```
chmod 777 data
```

> 访问http://192.168.199.109:8888

```
访问速度奇慢无比。。。。。
```

> 访问成功后，需要输入密码，可在日志中查看



| 查看日志,以及Jenkins页面                                     |
| ------------------------------------------------------------ |
| ![image-20200708232643961](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232643961.png) |
| ![image-20200708232614918](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232614918.png) |

| 选择安装插件方式 |
| :--------------: |
|  手动选择插件.   |

> 查看需要实现安装[Publish Over SSH]() 以及 [Git Parameter]()

|                           安装插件                           |
| :----------------------------------------------------------: |
| ![image-20200708232754318](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232754318.png) |
| ![image-20200708232800931](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232800931.png) |

> 安装成功后，需要指定上用户名和密码等信息

|                      指定用户名密码信息                      |
| :----------------------------------------------------------: |
| ![image-20200708232842803](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232842803.png) |
| ![image-20200708232910197](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232910197.png) |
| ![image-20200708232922638](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708232922638.png) |

> 登陆成功

|                   登录成功                   |
| :------------------------------------------: |
| ![1588681196639](http://qgw3wcroi.hn-bkt.clouddn.com/1588681196639.png) |

> 登录成功后,还需要单独安装[Persistent Parameter]()插件
>

|                     安装方式及安装成功图                     |
| :----------------------------------------------------------: |
| ![image-20200708233023116](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708233023116.png) |
| ![image-20200708233031967](http://qgw3wcroi.hn-bkt.clouddn.com/image-20200708233031967.png) |



#### 11.9 配置Jenkins的目标服务器

> 执行过程：代码提交到Gitlab，Jenkins会从Gitlab中拉取代码，并在Jenkins中打包并发布到目标服务器中。



##### 11.9.1 点击左侧的系统设置

|                   左侧导航                   |
| :------------------------------------------: |
| ![1588681954779](http://qgw3wcroi.hn-bkt.clouddn.com/1588681954779.png) |



##### 11.9.2 选中中间区域的系统设置

|                   系统设置                   |
| :------------------------------------------: |
| ![1588681970621](http://qgw3wcroi.hn-bkt.clouddn.com/1588681970621.png) |



##### 11.9.3 搜索Publish over SSH

|               Publish over SSH               |
| :------------------------------------------: |
| ![1588682011820](http://qgw3wcroi.hn-bkt.clouddn.com/1588682011820.png) |



##### 11.9.4 点击上图新增

| 新增SSH连接                                  |
| -------------------------------------------- |
| ![1588682092002](http://qgw3wcroi.hn-bkt.clouddn.com/1588682092002.png) |



#### 11.10 配置GitLab免密码登录

> 链接Gitlab需要使用密码，我们可以通过SSH的方式，免密码登陆Gitlab拉取代码，避免每次都输入密码。



##### 11.10.1登录Jenkins容器内部

```
docker exec -it jenkins bash
```



##### 11.10.2 输入生成SSH秘钥命令

```
ssh-keygen -t rsa -C "邮箱（随便写）"
```



##### 11.10.3将秘钥复制到GitLab的SSH中

|                   配置密钥                   |
| :------------------------------------------: |
| ![1588683585249](http://qgw3wcroi.hn-bkt.clouddn.com/1588683585249.png) |



#### 11.11 配置JDK和Maven

> 我们需要再Jenkins中将代码打包，需要依赖JDK和Maven的环境



##### 11.11.1 复制软件到data目录下

|                     效果                     |
| :------------------------------------------: |
| ![1588684490466](http://qgw3wcroi.hn-bkt.clouddn.com/1588684490466.png) |



##### 11.11.2 在监控界面中配置JDK和Maven

|                 配置环境变量                 |
| :------------------------------------------: |
| ![1588684458028](http://qgw3wcroi.hn-bkt.clouddn.com/1588684458028.png) |



##### 11.11.3 手动拉取gitlab项目

>  使用SSH无密码连接时，第一次连接需要手动确定

|                 手动拉取一次                 |
| :------------------------------------------: |
| ![1588685220324](http://qgw3wcroi.hn-bkt.clouddn.com/1588685220324.png) |



#### 11.12 创建maven任务

> 实现通过Jenkins的Maven任务，自动去Gitlab拉取代码，并在本地打包，发布到目标服务器上



##### 11.12.1 创建maven工程，推送到GitLab中

> 随便创建一个即可……



##### 11.12.2 Jenkins的监控页面中创建maven任务

|                指定GitLab地址                |
| :------------------------------------------: |
| ![1588686481506](http://qgw3wcroi.hn-bkt.clouddn.com/1588686481506.png) |

|              指定maven打包方式               |
| :------------------------------------------: |
| ![1588686489821](http://qgw3wcroi.hn-bkt.clouddn.com/1588686489821.png) |



##### 11.12.3 执行maven任务

|             立即构建，并查看日志             |
| :------------------------------------------: |
| ![1588686591351](http://qgw3wcroi.hn-bkt.clouddn.com/1588686591351.png) |

|              控制台查看日志信息              |
| :------------------------------------------: |
| ![1588686553880](http://qgw3wcroi.hn-bkt.clouddn.com/1588686553880.png) |



##### 11.12.4 最终效果

|                   打包成功                   |
| :------------------------------------------: |
| ![1588687382594](http://qgw3wcroi.hn-bkt.clouddn.com/1588687382594.png) |





#### 11.13 实现持续交付持续部署

> 实现根据tag标签，实现持续交付和持续部署



##### 11.13.1 安装Persistent Parameter的插件

|                   安装插件                   |
| :------------------------------------------: |
| ![1588693533099](http://qgw3wcroi.hn-bkt.clouddn.com/1588693533099.png) |



##### 11.13.2 重新指定构建项目的方式

|               根据标签构建项目               |
| :------------------------------------------: |
| ![1588696879059](http://qgw3wcroi.hn-bkt.clouddn.com/1588696879059.png) |

|                  自定义构建                  |
| :------------------------------------------: |
| ![1588697752850](http://qgw3wcroi.hn-bkt.clouddn.com/1588697752850.png) |



##### 11.13.3 构建项目成功后，需要将内容发布到目标服务器

|            发布服务器后执行的命令            |
| :------------------------------------------: |
| ![1588697770621](http://qgw3wcroi.hn-bkt.clouddn.com/1588697770621.png) |



##### 11.13.4 添加程序代码

> 指定目标服务器的Dockerfile以及docker-compose.yml文件。

```yml
# Dockerfile 文件
FROM daocloud.io/library/tomcat:8.5.15-jre8
COPY testcd-1.0-SNAPSHOT.war /usr/local/tomcat/webapps

# docker-compose.yml文件
version: "3.1"
services:
  testcd:
    build: docker
    restart: always
    container_name: testcd
    ports:
      - 8081:8080
```



##### 11.13.5 测试

> 在Jenkins中指定Tag后，Jenkins会从Gitlab拉取指定版本分支，并打包推送到目标服务器。

|             根据标签修改发布版本             |
| :------------------------------------------: |
| ![1588700462690](http://qgw3wcroi.hn-bkt.clouddn.com/1588700462690.png) |


