---
layout: post
title: 常用的maven插件
date: 2018-08-15 00:00:00
categories: 后端
tags: Maven
---

## maven-compiler-plugin

编译Java源码，一般只需设置编译的jdk版本

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.6.0</version>
    <configuration>
        <source>1.8</source>
        <target>1.8</target>
    </configuration>
</plugin>
```

或者在properties设置jdk版本

```xml
<properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
 </properties>
```

## maven-dependency-plugin

用于复制依赖的jar包到指定的文件夹里

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-dependency-plugin</artifactId>
    <version>2.10</version>
    <executions>
        <execution>
            <id>copy-dependencies</id>
            <phase>package</phase>
            <goals>
                <goal>copy-dependencies</goal>
            </goals>
            <configuration>
                <outputDirectory>${project.build.directory}/lib</outputDirectory>
            </configuration>
        </execution>
    </executions>
</plugin>
```

## maven-jar-plugin

打成jar时，设定manifest的参数，比如指定运行的Main class，还有依赖的jar包，加入classpath中

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <version>2.4</version>
    <configuration>
        <archive>
            <manifest>
                <addClasspath>true</addClasspath>
                <classpathPrefix>/data/lib</classpathPrefix>
                <mainClass>com.zhang.spring.App</mainClass>
            </manifest>
        </archive>
    </configuration>
</plugin>
```


##  wagon-maven-plugin

用于一键部署，把本地打包的jar文件，上传到远程服务器上，并执行服务器上的shell命令

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>wagon-maven-plugin</artifactId>
    <version>1.0</version>
    <configuration>
        <serverId>crawler</serverId>
        <fromDir>target</fromDir>
        <includes>*.jar,*.properties,*.sh</includes>
        <url>sftp://59.110.162.178/home/zhangxianhe</url>
        <commands>
            <command>chmod 755 /home/zhangxianhe/update.sh</command>
            <command>/home/zhangxianhe/update.sh</command>
        </commands>
        <displayCommandOutputs>true</displayCommandOutputs>
    </configuration>
</plugin>
```

##  tomcat7-maven-plugin

用于远程部署Java Web项目

```xml
<plugin>
    <groupId>org.apache.tomcat.maven</groupId>
    <artifactId>tomcat7-maven-plugin</artifactId>
    <version>2.2</version>
    <configuration>
        <url>http://59.110.162.178:8080/manager/text</url>
        <username>linjinbin</username>
        <password>linjinbin</password>
    </configuration>
</plugin>
```

##  maven-shade-plugin

用于把多个jar包，打成1个jar包

一般Java项目都会依赖其他第三方jar包，最终打包时，希望把其他jar包包含在一个jar包里

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>2.4.3</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals>
                <goal>shade</goal>
            </goals>
            <configuration>
                <transformers>
                    <transformer
                        implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <manifestEntries>
                            <Main-Class>com.meiyou.topword.App</Main-Class>
                            <X-Compile-Source-JDK>${maven.compile.source}</X-Compile-Source-JDK>
                            <X-Compile-Target-JDK>${maven.compile.target}</X-Compile-Target-JDK>
                        </manifestEntries>
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```