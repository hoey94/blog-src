---
title: java.lang.ArrayIndexOutOfBoundsException 10582
date: 2019-04-16 13:11:07
tags: Spark
categories: 大数据
---

环境：windows 7 + idea + scala 1.12.6 + spark 2.4.0

在IDEA中运行报下面错误

```java
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: 10582
	at com.thoughtworks.paranamer.BytecodeReadingParanamer$ClassReader.accept(BytecodeReadingParanamer.java:563)
	at com.thoughtworks.paranamer.BytecodeReadingParanamer$ClassReader.access$200(BytecodeReadingParanamer.java:338)
	at com.thoughtworks.paranamer.BytecodeReadingParanamer.lookupParameterNames(BytecodeReadingParanamer.java:103)
	at com.thoughtworks.paranamer.CachingParanamer.lookupParameterNames(CachingParanamer.java:90)
	at com.fasterxml.jackson.module.scala.introspect.BeanIntrospector$.getCtorParams(BeanIntrospector.scala:44)
	at com.fasterxml.jackson.module.scala.introspect.BeanIntrospector$.$anonfun$apply$1(BeanIntrospector.scala:58)
	at com.fasterxml.jackson.module.scala.introspect.BeanIntrospector$.$anonfun$apply$1$adapted(BeanIntrospector.scala:58)
	at scala.collection.TraversableLike.$anonfun$flatMap$1(TraversableLike.scala:241)
	at scala.collection.Iterator.foreach(Iterator.scala:944)
	at scala.collection.Iterator.foreach$(Iterator.scala:944)
	at scala.collection.AbstractIterator.foreach(Iterator.scala:1432)
	at scala.collection.IterableLike.foreach(IterableLike.scala:71)
    ...

```

下面是pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>ml.yihao</groupId>
  <artifactId>spark</artifactId>
  <version>1.0-SNAPSHOT</version>

  <properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
    <encoding>UTF-8</encoding>
    <scala.version>2.12.6</scala.version>
    <spark.version>2.4.0</spark.version>
    <hadoop.version>2.6.4</hadoop.version>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.scala-lang</groupId>
      <artifactId>scala-library</artifactId>
      <version>${scala.version}</version>
    </dependency>

    <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-core_2.12</artifactId>
      <version>${spark.version}</version>
    </dependency>

    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-client</artifactId>
      <version>${hadoop.version}</version>
    </dependency>

    <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-sql_2.12</artifactId>
      <version>${spark.version}</version>
    </dependency>

    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>5.1.38</version>
    </dependency>

    <!--<dependency>-->
      <!--<groupId>com.thoughtworks.paranamer</groupId>-->
      <!--<artifactId>paranamer</artifactId>-->
      <!--<version>2.8</version>-->
    <!--</dependency>-->
  </dependencies>

  <build>
    <sourceDirectory>src/main/scala</sourceDirectory>
    <testSourceDirectory>src/test/scala</testSourceDirectory>
    <plugins>
      <plugin>
        <groupId>net.alchim31.maven</groupId>
        <artifactId>scala-maven-plugin</artifactId>
        <version>3.2.2</version>
        <executions>
          <execution>
            <goals>
              <goal>compile</goal>
              <goal>testCompile</goal>
            </goals>
          </execution>
        </executions>
      </plugin>

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
              <filters>
                <filter>
                  <artifact>*:*</artifact>
                  <excludes>
                    <exclude>META-INF/*.SF</exclude>
                    <exclude>META-INF/*.DSA</exclude>
                    <exclude>META-INF/*.RSA</exclude>
                  </excludes>
                </filter>
              </filters>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
```

<font color="red">解决</font>：在pom.xml中添加paranamer即可

```xml
<dependency>
    <groupId>com.thoughtworks.paranamer</groupId>
    <artifactId>paranamer</artifactId>
    <version>2.8</version>
</dependency>
```