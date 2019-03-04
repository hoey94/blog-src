---
layout: post
title: maven exclusion
date: 2018-08-17 00:00:00
categories: 后端
tags: Maven
---

## 怎么使用dependency exclusions

我们可以在pom.xml中的``<dependency>`` 下添加``<exclusions>``,像这样

```xml
<project>
  ...
  <dependencies>
    <dependency>
      <groupId>sample.ProjectA</groupId>
      <artifactId>Project-A</artifactId>
      <version>1.0</version>
      <scope>compile</scope>
      <exclusions>
        <exclusion>  <!-- declare the exclusion here -->
          <groupId>sample.ProjectB</groupId>
          <artifactId>Project-B</artifactId>
        </exclusion>
      </exclusions> 
    </dependency>
  </dependencies>
</project>
```

## dependency exclusion 工作原理以及什么时候使用

```xml
Project-A
   -> Project-B
        -> Project-D <! -- This dependency should be excluded -->
              -> Project-E
              -> Project-F
   -> Project C
```
这个图展示了A依赖B,C B依赖D  D依赖EF,默认的项目A的 classPath 将包含

> B,C,D,E,F

场景：我们不希望项目D被依赖到项目A的classPath中，因为我们在开发时知道项目A中的功能根本不需要项目D，这个时候项目B的开发人员可以在自己的pom.xml中提供项目的依赖性``<optional>true</optional>``,像这样:

```xml
<dependency>
  <groupId>sample.ProjectD</groupId>
  <artifactId>ProjectD</artifactId>
  <version>1.0-SNAPSHOT</version>
  <optional>true</optional>
</dependency>
```

如果项目B没有这样做，作为最后手段，你可以在自己的项目中使用exclude，像这样

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>sample.ProjectA</groupId>
  <artifactId>Project-A</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>
  ...
  <dependencies>
    <dependency>
      <groupId>sample.ProjectB</groupId>
      <artifactId>Project-B</artifactId>
      <version>1.0-SNAPSHOT</version>
      <exclusions>
        <exclusion>
          <groupId>sample.ProjectD</groupId> <!-- Exclude Project-D from Project-B -->
          <artifactId>Project-D</artifactId>
        </exclusion>
      </exclusions>
    </dependency>
  </dependencies>
</project>
```

这个时候假如我们将项目A安装到本地仓库，project-x依赖了project-A,那么project-D仍然可以在项目X中被排出在外

