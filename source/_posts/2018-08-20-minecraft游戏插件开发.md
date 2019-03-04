---
layout: post
title: minecraft游戏插件开发
date: 2018-08-20 00:00:00
categories: 游戏开发
tags: Minecraft
---

本机环境：linux下的java开发minecraft游戏插件，用maven编译打jar包。

#### 概述

正式开发之前需要准备上面提到的以外，还需要准备服务端[下载链接](https://bukkit.gamepedia.com/Main_Page)和客户端

游戏插件开发好以后，会使用maven打成jar包，放在 服务端的 ``plugins`` 目录下即可生效。

### 环境搭建

大致步骤:
- 1.创建maven项目
- 2.修改pom.xml文件
- 3.下载mincecraft服务器
- 4.配置mincecraft服务器
- 5.启动mincraft客户端
- 6.编写第一个命令插件
- 7.maven打包


#### 1.创建maven项目
![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumf9w4cc6j30lr0p8ta6.jpg)

#### 2.修改pom.xml文件

这里用的是Bukkit的服务器，所以需要引入第三方仓库

```xml
<repositories>
	<repository>
		<id>spigot-repo</id>
		<url>https://hub.spigotmc.org/nexus/content/repositories/snapshots/</url>
	</repository>
</repositories>
```

接着引入开发库

```xml

<dependency>
	<groupId>org.bukkit</groupId>
	<artifactId>bukkit</artifactId>
	<version>1.12.2-R0.1-SNAPSHOT</version><!--change this value depending on the version or use LATEST-->
	<type>jar</type>
	<scope>runtime</scope>
</dependency>

<dependency>
	<groupId>org.spigotmc</groupId>
	<artifactId>spigot-api</artifactId>
	<version>1.12.2-R0.1-SNAPSHOT</version><!--change this value depending on the version-->
	<type>jar</type>
	<scope>provided</scope>
</dependency>

```

使用``maven-assembly-plugin``插件打jar包
```pom
<plugin>
	<artifactId>maven-assembly-plugin</artifactId>
	<configuration>
	<descriptorRefs>
		<descriptorRef>jar-with-dependencies</descriptorRef>
	</descriptorRefs>
	<!--<archive>
		<manifest>
		<mainClass>org.bukkit.Server</mainClass>
		</manifest>
	</archive>-->
	</configuration>
	<executions>
	<execution>
		<id>make-assembly</id>
		<phase>package</phase>
		<goals>
		<goal>single</goal>
		</goals>
	</execution>
	</executions>
</plugin>
```

#### 3.下载mincecraft服务器craftbukkit-1.7.2-R0.4-20140316.221310-4.jar

https://getbukkit.org/

#### 4.配置服务器

1.编写run.sh脚本，启动服务器

> $ touch run.sh

```shell
#!/bin/bash
echo "start bukkit server"
java -Xms1024M -Xmx1024M -jar craftbukkit-1.7.2-R0.4-20140316.221310-4.jar
```

修改run.sh为可执行文件
> $ chmod 777 run.sh  

运行run.sh脚本
> $ ./run.sh

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumh9hquh7j30kf0nntef.jpg)

启动以后会发现当前目录会生成很多文件

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumi17culcj30rc0oyjt5.jpg)

2.修改服务器参数server.properties

```properties
#Minecraft server properties
#Thu Aug 16 00:01:18 CST 2018
generator-settings=
op-permission-level=4
allow-nether=true
online-model=false
level-name=world
enable-query=false
allow-flight=false
announce-player-achievements=true
server-port=25565
level-type=DEFAULT
enable-rcon=false
force-gamemode=false
level-seed=
server-ip=
max-build-height=256
spawn-npcs=true
white-list=false
spawn-animals=true
hardcore=false
snooper-enabled=true
online-mode=false
resource-pack=
pvp=true
difficulty=1
enable-command-block=true
gamemode=0
player-idle-timeout=0
max-players=20
spawn-monsters=true
generate-structures=true
view-distance=10
spawn-protection=16
motd=A Minecraft Server
```

具体配置可以查看[wiki](https://minecraft.gamepedia.com/Server.properties)

重新启动服务器使其生效。

#### 5.启动mincraft客户端

想要启动``minecraft客户端``，需要提前准备一个启动器。

``minecraft启动器``和``minecraft客户端``这篇博客https://www.linuxidc.com/Linux/2016-04/129764.htm有下载链接，不过里面的``minecraft客户端``启动会抛异常，可能是因为是linux的原因，在下载1.7.2的时候某些jar包损坏导致无法正常启动,后续通过排查找到损坏的jar，从新到网上下载完好的jar才得以解决。如果你用的也是linux，可以联系我，为你提供一个完好版本，当然也可以从网上搜一下，很好解决的。

下载好启动器和客户端以后，我们先运行启动器，同服务端一样，编写``run.sh`` 脚本运行``minecraft启动器``,run.sh内容如下:
```shell
#!/bin/bash

echo "run minecraft client on linux os..."
java -jar HMCL-2.1.7.jar
```
使用下面命令运行启动器

> $ ./run.sh

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumhfd428qj30px0sp4qp.jpg)

进入游戏，选择Multiplayer开启多人游戏即可

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumhi365o1j31f00rvkjm.jpg)

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumhoujxj7j30qb0fjtc8.jpg)


#### 6.编写第一个命令插件

这个命令暂时叫做example，当用户在游戏内输入example时，作出相应提示

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumhq9i2x3j30mt0degtp.jpg)

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumhr0d9cuj30p30erwl4.jpg)

---

当服务器启动以后，会加载放在plugin目录下实现JavaPlugin的类，触发它的onEnable方法

在src/main/java下创建FirstPlugin.java

```java
package com.zonegood;

import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;


/**
 * @author zyh
 */
public final class FirstPlugin extends JavaPlugin {


    @Override
    public void onEnable() {
        this.getLogger().info("FirstPlugin running...");
        // 加载CommandExample指令
        this.getCommand("example").setExecutor(new CommondExample());
    }

    @Override
    public void onDisable() {
        for (Player player : getServer().getOnlinePlayers()){
            this.getLogger().info("disable method" + player.getName());
        }
    }
}
```

这边对指令类进行封装，指令需要实现``CommandExecutor``类，实现``onCommand``方法，当系统检测到有人发送example指令时，``onCommand``方法就会被触发，当然前提是，它必须已被注册。

在src/main/java/目录下创建CommondExample.java

```java

package com.zonegood;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

/**
 * @author zyh
 */
public class CommondExample implements CommandExecutor{

    private static final String commandName = "example";

    @Override
    public boolean onCommand(CommandSender commandSender, Command command, String s, String[] strings) {

        if(commandName.equalsIgnoreCase(command.getName())){
            ((Player)commandSender).sendMessage(((Player)commandSender).getName() + "execute example command");
            return true;
        }

        return false;
    }
}
```

在src/resources/目录下创建``plugin.yml``,在里面我们需要对``example``指令进行描述

``aliases`` 可以理解为``example``指令的昵称，在游戏内输入``a1``,``a2`` 等价于输入``example``

除此之外里面还有其他参数，详情参考[wiki](https://bukkit.gamepedia.com/Plugin_YAML)

```yml
name: firstplugin
version: 1.0
description: This plugin is so 31337. You can set yourself on fire.
# We could place every author in the authors list, but chose not to for illustrative purposes
# Also, having an author distinguishes that person as the project lead, and ensures their
# name is displayed first
author: Zyh
authors: [zyh]
website: http://www.zonegood.com

main: com.zonegood.FirstPlugin

commands:
 example:
   description: Set yourself on fire.
   aliases: [a1,a2]
   usage: Syntax error! Simply type /&lt;command&gt; to ignite yourself.

```

项目的整体目录结构

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumi8p3g8dj30fw0n2n08.jpg)


#### 7.maven打包

下面的指令会将编写好的代码编译打包成jar，放在target目录下

> $ mvn clean package

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumhsv1usaj31260o9q57.jpg)

可以看到

``Building jar: /media/zyh/workspace/workspace/IDEA/bukiitplugin/target/bukiitplugin-1.0-SNAPSHOT.jar``

将bukiitplugin-1.0-SNAPSHOT.jar拷贝到server/plugins/目录下重新启动服务器即可


## 资料

官方开发文档：https://bukkit.gamepedia.com/Main_Page

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1fumicly8sjj31hb0tzair.jpg)

Developers一栏就是了


