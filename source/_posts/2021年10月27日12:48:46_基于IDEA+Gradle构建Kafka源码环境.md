
---
title: Kafka2.1.0源码环境构建IDEA+Gradle
date: 2021-10-27 12:39:13
categories: 大数据
tags: Kafka
---

### 一. 环境

* MacOS
* Kafka:[Kafka-2.1.0-src](https://archive.apache.org/dist/kafka/2.1.0/kafka-2.1.0-src.tgz)
* Gradle:[Gradle-5.2-all](https://services.gradle.org/distributions/gradle-5.2-all.zip)
* Scala:Scala-2.11.8
* Java:1.8

### 二. Gradle安装

Gradle解压到``/Users/zyh/Library``
在``~/.zshrc``中配置下面环境变量，如果你用的不是zsh需要根据实际情况来配置环境变量

```shell
export GRADLE_HOME=/Users/zyh/Library/gradle-5.2
export GRADLE_USER_HOME=$GRADLE_HOME/gradle-reposity
export PATH=$GRADLE_HOME/bin:$PATH
```

### 三.Scala安装

![title](https://raw.githubusercontent.com/zyh194/images/main/gitnote/2021/10/27/1635314194466-1635314194468.png)


### 四.Kafka源码编译

下载kafka源码,解压到文件夹替换build.gradle中所有的mavenCentral()，改成阿里的源
```gradle
buildscript {
  repositories {
    //mavenCentral()
    maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }
    maven {
      url "https://plugins.gradle.org/m2/"
    }
  }
....
allprojects {
  repositories {
    //mavenCentral()
    maven { url 'http://maven.aliyun.com/nexus/content/groups/public/' }
    maven {
      url "https://plugins.gradle.org/m2/"
    }
  }
....
```

### 五.IDEA配置

![title](https://raw.githubusercontent.com/zyh194/images/main/gitnote/2021/10/27/1635312590215-1635312590217.png)

![title](https://raw.githubusercontent.com/zyh194/images/main/gitnote/2021/10/27/1635312602619-1635312602620.png)

检查配置Gradle环境，File -> Settings -> Build, Execution, Deployment -> Build Tools -> Gradle

![title](https://raw.githubusercontent.com/zyh194/images/main/gitnote/2021/10/27/1635314286995-1635314286997.png)


### 六.最终结果

![title](https://raw.githubusercontent.com/zyh194/images/main/gitnote/2021/10/27/1635314611366-1635314611373.png)