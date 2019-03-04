---
layout: post
title: forge开发环境Setup
date: 2018-05-12 00:00:00
categories: Autodesk
tags: forge
---

windows下搭建forge官网提供的案例[链接](https://github.com/Autodesk-Forge/forge-rcdb.nodejs),编译器使用vscode。

## 目录

- 安装 node
- 安装 git
- 安装 MongoDB
- 注册Autodesk Developer帐号
- 配置项目
- 启动项目

## 安装 node

推荐使用nvm安装,[github](https://github.com/coreybutler/nvm-windows/releases) 下载并安装最新版的nvm。

使用管理员权限打开命令提示符输入如下命令：

```shell
nvm install 8.11.1
npm install -g --production windows-build-tools
npm install -g cross-env
```

配置npm以及yarn

打开powershell或命令行输入如下命令，将npm使用淘宝的镜像进行加速并安装yarn：

```shell
npm config set registry=https://registry.npm.taobao.org
npm install -g yarn
yarn config set registry https://registry.npm.taobao.org
```
## 安装 git

安装git命令行客户端或SourceTree等GUI客户端。

命令行下输入

> $ git clone https://github.com/Autodesk-Forge/forge-rcdb.nodejs.git

GUI客户端用界面操作将https://github.com/Autodesk-Forge/forge-rcdb.nodejs.git clone到本地。

## 安装 MongoDB
下载Robo 3t客户端 （ https://robomongo.org/download ）。

连接本地mongo（默认不用认证直接连接）

创建database: forge-rcdb

给该database创建用户，并授予readWrite权限。

将forge-rcdb项目中 resources\db\dev 目录下的数据导入mongodb。

mongodb相关一些指令:

```shell
sudo service mongod start
mongo -uroot -p
mongoimport -h localhost:27017 -d forge-rcdb  /home/zyh/workspace/nodejs/forge-rcdb.nodejs/resources/db/dev
less /etc/mongod.conf
```

## 注册Autodesk Developer帐号

访问 https://developer.autodesk.com/myapps/create 创建 App。
Callback URL设为 http://localhost:3000/api/forge/callback/oauth 。
记录下Client ID以及Client Secret

## 配置项目

编辑forge-rcdb项目中的config\development.config.js 将database部分的设置为刚安装的mongodb的信息。

可选：将Client Id以及Client Secret替换掉Client Id以及Client Secret部分。

在forge-rcdb项目目录下执行

> yarn install

## 启动项目

执行如下命令可以启动项目：

> cross-env NODE_ENV=development HOT_RELOADING=true FORGE_DEV_CLIENT_SECRET=<Client Secret> FORGE_DEV_CLIENT_ID=<Client Id> npm start

若上一步中将Client Id以及Secret写入到配置文件，运行如下命令启动项目

> cross-env NODE_ENV=development HOT_RELOADING=true npm start

