---
layout: post
title: ubuntu16.04TLS tar系统整机备份及恢复
tags: 问题记录
date: 2018-03-20 00:00:00
categories: ubuntu
---

老实说，备份是系统损毁时的救星。事实上，没有人希望自己的系统损坏，往往由于不预期的伤害导致系统发生错误，比如之前我想在电脑上卸载一个依赖包，结果卸载以后，系统导致不能正常启动。不用慌，插上硬盘，执行一条命令电脑就恢复正常了！正是因为计算机是个相当不可靠的机器，所以我们要时常对它进行备份，进而来预防不测。

## 预言

linux是一个文件系统，因此可以利用tar来备份。备份之前首先要了解哪些是我们需要备份的数据，哪些是我们不需要备份的数据。

### 排除的文件

下面这些文件是我们不需要考虑备份的文件

```shell
/proc
/tmp
/mnt
/dev
/sys
/run 
/media 
/var/log  #日志文件
/var/cache/apt/archives  #apt下载的任何.deb文件
/usr/src/linux-headers*
/home/*/.gvfs
/home/*/.cache
/home/*/.local/share/Trash
```

### 需要备份的文件

下面这些文件是我们需要考虑备份的文件

```shell
/etc
/home
/var/spool/mail
/boot/
/root
#自己安装过的套件会存放在/user/local和/opt所以他俩也备份
/user/local
/opt
```

## 完整备份

使用管理员身份，进入到根目录下运行tar命令

这里有一点需要注意的是，第三条命令不是死的，你要灵去修改，`假如你把备份的文件放在了根目录下，那么我们在tar的命令里面要再加上一句 --exclude=/备份的文件名`

上面这一点很重要，因为我们**备份过的文件**也是要排除的。如果忘了这一点可能会备份失败，我为什么没有加，是因为把备份文件放在/media目录下了.

可能是因为界面样式问题 `--` 有点像 `-` Orz

> $ sudo su  
> $ cd /  

```shell
tar --exclude=/home/zyh/Pictures/* --exclude=/proc --exclude=/tmp --exclude=/mnt --exclude=/dev --exclude=/sys --exclude=/run --exclude=/media --exclude=/var/log --exclude=/var/cache/apt/archives --exclude=/usr/src/linux-headers* --exclude=/home/*/.gvfs --exclude=/home/*/.cache --exclude=/home/*/.local/share/Trash -jcvp -f /media/zyh/software/ubuntubackup/system.tar.bz2 /
```

* --exclude 将会排除掉我们不希望备份的内容
* -j 压缩为bz2 能有一个更好的压缩比
* 最后-f /media/zyh/software/ubuntubackup/system.tar.bz2 是我们要备份**到哪个目录**以及**文件名字**，后面的`/`表示压缩目录从根目录开始

### 恢复

`注意：恢复操作很危险，如果你不知道自己在做什么，将可能会导致系统数据丢失！`我们将备份好的system.tar.bz2文件解压到根目录

> $ cd /media/zyh/software/ubuntubackup/  
> $ tar -jxvf system.tar.bz2 -C /

* -j 类型为bz2
* -x 解压
* -v 显示解压过程
* -f 使用档名，请留意，在 f 之后要立即接档名通常我们把f放在最后

参考blog:https://help.ubuntu.com/community/BackupYourSystem/TAR#Alternate_backup

参考blog:http://linux.vbird.org/linux_basic/0580backup.php
