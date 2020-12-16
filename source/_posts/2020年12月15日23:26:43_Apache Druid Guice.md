---
title: Apache Druid Guice
date: 2020-12-15 23:26:43
categories: 大数据
tags: Apache Druid
---

大数据组件中OLAP引擎应用广泛，比较火的有presto、Kylin、Druid。

Presto基于内存处理，HQL用Presto瞬间搞定，猛成一把刀，但你再看看内存使用情况也是把人给惊呆了，真是没有个上百G内存玩不转。

再说Kylin和Druid，前者偏离线，后者偏实时。Kylin作为Hadoop领域的老大哥，已经几乎成为离线标准，指标分析领域应用广泛。而Apache Druid则在实时OLAP领域独领风骚，优异的性能、高可用、易拓展。

平安2019年底引进Druid，离线迎合数仓、实时迎合埋点+Kafka构建OLAP多维分析报表。关于Druid的资料在网上很少，接触时，只有英文文档。想要了解一下源码，资料更是少的可怜，Druid源码要看懂，得先知道Google Guice这个东西，本文来讨论一下。

### 一、 Google Guice介绍

[Guice](https://github.com/google/guice)是一个小巧的依赖注入工具，玩Java的话，关于Spring依赖注入大家肯定不陌生。早期，Spring依赖注入靠的是写XML，这种方式太过隐蔽。目前Spring依赖注入玩注解，这种方式很灵活。而Guice依赖注入是靠写代码，下面具一些小栗子方便快速入门。

### 二、 Guice实例

**1. 普通注入**

```java
package ml.yihao;

import com.google.inject.*;
import com.google.inject.name.Named;
import com.google.inject.name.Names;

/**
 * @author zyh
 * @Description:
 * @date 2020/12/158:34 下午
 */
public class Example1 {

    public static void main(String[] args) {
        Injector injector = Guice.createInjector(new Module() {
            public void configure(Binder binder) {
                binder.bind(DataBaseMeta.class).to(MysqlDataBaseMeta.class);
                // 注入用户名
                binder.bind(String.class).annotatedWith(Names.named("username")).toInstance("root");
                // 注入密码
                binder.bind(String.class).annotatedWith(Names.named("password")).toInstance("^5g%@!hKH");
            }
        });

        DataBaseMeta dataBaseMeta = injector.getInstance(DataBaseMeta.class);
        dataBaseMeta.print();
    }

}

interface DataBaseMeta{

    void print();
}

@Singleton
class MysqlDataBaseMeta implements DataBaseMeta {


    private String username;
    private String password;

    @Inject
    MysqlDataBaseMeta(@Named("username") String username, @Named("password") String password){
        this.username = username;
        this.password = password;
    }

    public void print() {
        System.out.println(username + ":" + password);
    }
}

```

使用Guice动态注入**username**和**password**属性

**2. 默认值**

```java
package ml.yihao;

import com.google.inject.*;
import com.google.inject.multibindings.OptionalBinder;

/**
 * @author zyh
 * @Description:
 * @date 2020/12/159:12 下午
 */
public class Example3 {

    public static void main(String[] args) {
        Injector injector = Guice.createInjector(new FrameWorkModule()/*, new Module() {
            @Override
            public void configure(Binder binder) {
                OptionalBinder.newOptionalBinder(binder, Emit.class).setBinding().to(KafkaEmit.class);
            }
        }*/);
        TestService instance = injector.getInstance(TestService.class);
        instance.print();
    }
}

class TestService{

    private Emit emit;

    @Inject
    TestService(Emit emit){
        this.emit = emit;
    }

    public void print(){
        this.emit.emit();
    }



}

interface Emit{
    void emit();
}

class KafkaEmit implements Emit{

    @Override
    public void emit() {
        System.out.println("kafka");
    }
}

class HttpEmit implements Emit{

    @Override
    public void emit() {
        System.out.println("http");
    }
}

class FrameWorkModule implements Module {

    @Override
    public void configure(Binder binder) {
        OptionalBinder.newOptionalBinder(binder, Emit.class).setDefault().to(HttpEmit.class);
    }
}

```

**3. 覆盖已绑定关系**


```java
package ml.yihao;

import com.google.common.collect.ImmutableList;
import com.google.inject.Guice;
import com.google.inject.Inject;
import com.google.inject.Injector;
import com.google.inject.Module;
import com.google.inject.util.Modules;

/**
 * @author zyh
 * @Description: 默认注入Mysql，后续覆盖成oracle
 * @date 2020/12/158:48 下午
 */
public class Example2 {

    public static void main(String[] args) {
        ImmutableList<Module> defaultModule = ImmutableList.of(binder -> {
            binder.bind(Database.class).to(MysqlDatabase.class);
        });

        ImmutableList<Module> customModule = ImmutableList.of(binder -> {
            binder.bind(Database.class).to(OracleDatabase.class);
        });

        // 默认
        //Injector injector = Guice.createInjector(defaultModule);

        // 覆盖
        Injector injector = Guice.createInjector(Modules.override(defaultModule).with(customModule));

        FrameWork instance = injector.getInstance(FrameWork.class);
        instance.start();
        
    }
    
}

class FrameWork{

    private Database database;

    @Inject
    FrameWork(Database database){
        this.database = database;
    }

    public void start(){
        database.print();
    }

}

interface Database{
    void print();
}

class MysqlDatabase implements Database {
    private String type = "mysql";

    public void print() {
        System.out.println(type);
    }
}


class OracleDatabase implements Database {
    private String type = "oracle";

    public void print() {
        System.out.println(type);
    }
}

```

### 三、 Druid中拓展组件

Druid在Guice基础上拓展了三个插件，这三个插件贯穿整个Druid源码，不懂会影响看代码。它们分别是``guice-lifecycle``、``guice-jsonconfig``和``guice-jersey-jetty``

* guice-lifecycle：提供生命周期管理
* guice-jsonconfig：提供配置文件Bean注入
* guice-jersey-jetty：提供jetty轻量级servlet容器

下面分别上代码演示一下三个模块的使用，在使用之前我们需要先将其加入到依赖

这里提供[源码](https://github.com/Demo233/guice-module)，你只需要**clone**下来执行``mvn package install``，然后将下面内容加入到自己项目的``pom.xml``中即可

```xml
<dependency>
    <groupId>com.google.code</groupId>
    <artifactId>guice-lifecycle</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
<dependency>
    <groupId>com.google.code</groupId>
    <artifactId>guice-jsonconfig</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>

<dependency>
    <groupId>com.google.code</groupId>
    <artifactId>guice-jersey-jetty</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
```


**1. lifecycle生命周期管理**

```java
package ml.yihao;

import com.google.code.guice.lifecycle.*;
import com.google.inject.Guice;
import com.google.inject.Inject;
import com.google.inject.Injector;

/**
 * @author zyh
 * @Description:
 * @date 2020/12/1510:04 下午
 */
public class Example4 {

    public static void main(String[] args) throws Exception{
        Injector injector = Guice.createInjector(new LifecycleModule());
        Bootstrap bootstrap = injector.getInstance(Bootstrap.class);
        bootstrap.start();

    }

    @ManageLifecycle
    public static class PrintLifecycle{

        @LifecycleStart
        void start(){
            System.out.println("start");
        }

        @LifecycleStop
        void stop(){
            System.out.println("stop");
        }

    }

    // 定义好类
    public static class Bootstrap{

        private PrintLifecycle printLifecycle;
        private Lifecycle lifecycle;

        @Inject
        Bootstrap(PrintLifecycle printLifecycle, Lifecycle lifecycle){
            this.printLifecycle = printLifecycle;
            this.lifecycle = lifecycle;
        }

        void start() throws Exception {
            System.out.println("bootstrap start");
            lifecycle.start();
            // 等待子线程运行完成以后主线程终止
            lifecycle.join();
        }
    }

}
```

**2. 配置类Bean注入**

```java
package ml.yihao;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.code.guice.jsonconfig.JsonConfigModule;
import com.google.code.guice.jsonconfig.JsonConfigProvider;
import com.google.inject.*;
import lombok.Data;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;
import java.util.Properties;

/**
 * @author zyh
 * @Description:
 * @date 2020/12/1510:31 下午
 */
public class Example5 {

    public static void main(String[] args) {
        Injector injector = Guice.createInjector(new JsonConfigModule(), new Module() {
            @Override
            public void configure(Binder binder) {
                JsonConfigProvider.bind(binder, "druid.server", DruidServerConfig.class);
            }

            @Provides
            @Singleton
            Properties init() {
                Properties prop = new Properties();
                prop.put("druid.server.host", "127.0.0.1");
                prop.put("druid.server.port", 9999);
                return prop;
            }

        });
        DruidServerConfig config = injector.getInstance(DruidServerConfig.class);
        System.out.println(config.getHost() + ":" + config.getPort());
    }

}

@Data
class DruidServerConfig{

    @JsonProperty @NotNull private String host;

    @JsonProperty @Min(6060) private int port = 8080;

}
```

**3. jetty容器管理**

```java
package ml.yihao;

import com.google.code.guice.jsonconfig.JsonConfigModule;
import com.google.code.jersey.Jerseys;
import com.google.code.jersey.ServerConfig;
import com.google.code.jersey.jetty.JerseyJettyServer;
import com.google.code.jersey.jetty.JettyServerModule;
import com.google.inject.*;

import javax.servlet.http.HttpServletRequest;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import java.util.Properties;

/**
 * @author zyh
 * @Description:
 * @date 2020/12/1510:46 下午
 */
public class Example6 {

    public static void main(String[] args) throws Exception{
        Injector injector = Guice.createInjector(new JettyServerModule(), new JsonConfigModule(), new Module() {
            @Override
            public void configure(Binder binder) {

                Jerseys.addResource(binder, IndexResource.class);
            }

            Properties init() {
                Properties prop = new Properties();
                prop.put("server.http.host", "0.0.0.0");
                prop.put("server.http.port", 8080);
                return prop;
            }

        });
        JerseyJettyServer jerseyJettyServer = injector.getInstance(JerseyJettyServer.class);
        jerseyJettyServer.start();
        Thread.currentThread().join();
    }



    @Singleton
    @Path("/index")
    public static class IndexResource {
        private ServerConfig serverConfig;
        @Inject
        public IndexResource(ServerConfig serverConfig) {
            this.serverConfig = serverConfig;
        }

        @GET
        @Produces(MediaType.APPLICATION_JSON)
        public ServerConfig doGet(@Context final HttpServletRequest req) {
            return serverConfig;
        }
    }

}

```

[源码](https://github.com/Demo233/guice-example)