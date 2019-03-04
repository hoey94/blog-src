---
layout: post
title: github-jekyll搭建个人博客网站
date: 2017-07-20 00:00:00
categories: 博客
---

使用**github**和**jekyll**搭建的[博客](http://www.zonegood.com),运行环境是**ubuntu 1.6.04**使用的域名是[阿里云](https://cn.aliyun.com/),听说.tk的也不错，但是我注册的域名在.tk很贵

推荐: [github Pages和Jekyll入门](http://www.ruanyifeng.com/blog/2012/08/blogging_with_jekyll.html),[Git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

## 附录

- [jekyll](#jekyll)
    - [ruby安装](#ruby安装)
    - [rubyGems安装](#rubyGems安装)
    - [jekyll安装](#jekyll安装)
- [创建并发布博客](#创建并发布博客)
    - [无样式的博客](#无样式的博客)
    - [有样式的博客](#有样式的博客)
- [注册域名](#注册域名)


## jekyll

Jekyll是一个简单的博客形态的静态站点生产机器。它有一个模版目录，其中包含原始文本格式的文档，通过 [Markdown](https://daringfireball.net/projects/markdown/) （或者 [Textile](http://textile.sitemonks.com/)） 以及 [Liquid](http://docs.shopify.com/themes/liquid-basics) 转化成一个完整的可发布的静态网站，你可以发布在任何你喜爱的服务器上。Jekyll 也可以运行在 [GitHub Page](https://pages.github.com/) 上，也就是说，你可以使用 GitHub 的服务来搭建你的项目页面、博客或者网站，而且是完全免费的。

安装jekyll之前呢，需要准备下面三样东西。

* [Ruby](https://www.ruby-lang.org/en/downloads/)
* [RubyGems](https://rubygems.org/pages/download)
* Ubuntu 1.6.04

### ruby安装

具体怎么可以到[Ruby官网](https://www.ruby-lang.org/en/downloads/)下载tar.gz安装包安装，这里只提供思路，不要直接粘贴下面代码，我们是有智慧的程序员。（注意有时候make install 报错的话，可能是权限问题，我就碰到咯，只要在代码前面加上sudo 就行了）

```
$ wget https://cache.ruby-lang.org/pub/ruby/2.4/ruby-2.4.1.tar.gz
$ tar -zxvf ruby-2.4.1.tar.gz
$ cd ruby-2.4.1/
$ ./configure
$ make
$ make install
$ make clean
$ sudo make distclean
$ ruby -v

```


### rubyGems安装

具体怎么可以到[RubyGems官网](https://rubygems.org/pages/download),和Ruby安装是一样的，不做详细说明

```
$ wget https://rubygems.org/rubygems/rubygems-2.6.12.tgz
$ tar -zxvf rubygems-2.6.12.tgz
$ cd rubygems-2.6.12
$ ./configure
$ make
$ make install
$ make clean
$ sudo make distclean
```


### jekyll安装

[jekyll官网](http://jekyll.com.cn/docs/installation/),jekyll的doc一栏中也提供了安装的参考

``` 
$ sudo gem install jekyll

```
可能会出现一些错误，这是因为少安装了一些插件，这里我也卡了很久，搜索了很多资料，试了很多次

```
ERROR: Loading command: update (LoadError)
cannot load such file -- zlib
ERROR: While executing gem ... (NoMethodError)
undefined method `invoke_with_build_args' for nil:NilClass
```

解决办法，如果我的方法不行，这个就要摆脱google了,这里面$?是上一个执行命令的执行结果，如果返回0就代表没问题

```
$  sudo apt-get update
$  sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev libcurl4-openssl-dev python-software-properties
$  sudo apt-get install libgdbm-dev libncurses5-dev automake libtool bison libffi-dev
$  sudo apt-get install zlib1g-dev
$  cd ruby-2.4.1/ext/zlib/
$  ruby extconf.rb 
$  make
$  echo $?
$  cd /usr/ruby-2.4.1/
$  ./configure
$  echo $?
$  make
$  echo $?
$  make install
$  sudo make install
$  echo $?
$  make clean
$  make distclean
```
## 创建并发布博客

### 无样式的博客

* 创建一个无样式的博客
    ```
    $ jekyll new blog
    $ cd blog
    $ git init 
    $ git add .
    $ git commit -m "fist jekyll program"
    $ git status
    ```
* 将博客关联到github远程仓库
    * 登录[github](http://github.com)
    * 选择New repository
    
    * 填写Repository name为username.github.io （注意这里的格式，这里的username就是github.com/username中的username）
    * Create repository创建玩之后会给你一个https的链接，比如我的username是Demo233，给我的链接就是https://github.com/Demo233/Demo233.github.io.git
    
* 将无样式的blog项目远程推送到github仓库中,这里以我的为例，我的username为Demo233,注意修改成自己的

    ```
    $ cd blog/
    $ git remote add origin https://github.com/Demo233/Demo233.github.io.git
    $ git push origin master
    ```

* 配置github pages,并运行
    * 进入到github.com/Demo233/Demo233.github.io项目中，在Settings选项卡中找到GitHub Pages面板，在Source中选择master branch，并save
    * 通过demo233.github.io就可以成功访问我们的界面了！


### 有样式的博客

本次lz用到的样式是[hyde](https://github.com/poole/hyde)，以这个为例子进行推送部署。在github上网有学多jekyll的样式，你也可以下载并部署,[样式链接](https://github.com/jekyll/jekyll/wiki/Themes)

```
$ git clone https://github.com/poole/hyde.git
$ cd hyde/
```

我们需要修改一些东西，不然会报错，之前lz同样卡在这里半天，网上搜索了半天资料才解决。

* 修改_config.yml文件中的relative_permalinks: false,如果不改，会报XXX过期的错误，记不得了
* 删除CNAME中的内容，如果不改会提示域名已经存在，因为这个是别人的项目，人家已经在github上注册了，后面会介绍怎么配置自己的域名

```
$ rm -rm .git/ # 删除原本的.git 文件使用自己的.git
$ git init
$ git add .
$ git commit -m "beautiful jekyll theme"
$ git remote add https://github.com/Demo233/Demo233.github.io.git # 记得退回历史版本之后再进行这里的操作不然会报错的
$ git push origin master
```

后面的和无样式博客发布是一样的，只要注意修改_config.yml文件，其他应该没什么大碍了。

> Tip : 项目里面已经有一个.gitignore我们可以使用它来忽略上传内容


## 注册域名

登录[阿里云](https://www.aliyun.com/)注册一个帐号，然后选择一个自己喜欢的域名并购买即可。

我们买好域名以后，我们就可以去绑定github pages了。lz的域名是zonegood.com，在CNAME中写入zonegood.com并保存

```
$ cd hyde/
$ vim ./CNAME
```

推送更改信息，更新项目

```
$ git add .
$ git commit -m "modify CNAME file ,add zonegood.com"
$ git push origin master
```

登录[阿里云域名控制台](https://home.console.aliyun.com/new#/)

在云解析DNS选项卡中找到自己购买的域名选项，并点击“解析”

在“解析设置”一栏中选择“添加解析”，记录类型填写为CNAME，主机记录填写www，记录值在这里以我的为例填写demo233.github.io之后保存。推荐一片博文[解析域名的时候不同的项目代表什么含义？主机记录、记录类型、线路类型、记录值、MX优先级、TTL](http://blog.csdn.net/pzasdq/article/details/51171424)

推荐 : http://jmcglone.com/guides/github-pages/