---
layout: post
title: git -- 忽略某个文件
date: 2018-08-08 00:00:00
categories: 后端
tags: git
---

## 修改 .gitignore 文件

在git中如果想忽略掉某个文件，不让这个文件提交到版本库中，可以使用修改 .gitignore 文件的方法。

举例：.gitignore文件内容如下：

```javascript
# Android generated
bin/
gen/
classes/
gen-external-apklibs/

# Ant
local.properties

# Maven
target/
release.properties

# Eclipse
.classpath
.project
.externalToolBuilders/
.metadata
.settings

# IntelliJ
*.iml
*.ipr
*.iws
.idea/
out/

# Mac
.DS_Store

# gitignore
.gitignore
```


## 使用命令

.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。

正确的做法是在每个clone下来的仓库中手动设置不要检查特定文件的更改情况。

> git update-index --assume-unchanged FILE 

在FILE处输入要忽略的文件。

如果要还原的话，使用命令：

> git update-index --no-assume-unchanged FILE

#### 使用.git/info/exclude

git 还提供了另一种 exclude 的方式来做同样的事情，不同的是 .gitignore 这个文件本身会提交到版本库中去。用来保存的是公共的需要排除的文件。而 .git/info/exclude 这里设置的则是你自己本地需要排除的文件。 他不会影响到其他人。也不会提交到版本库中去。

举例：
```javascript
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~
.gradle/
.idea/
.settings/
appcompat_v7/
bin/
build/
gen/
gradle/
out/
proguard/
ship/
target/
.classpath
.gitignore
.idea
.project
.readme
.update-config
*.iml
local.properties
```

.gitignore 还有个有意思的小功能， 一个空的 .gitignore 文件 可以当作是一个 placeholder 。当你需要为项目创建一个空的 log 目录时， 这就变的很有用。 你可以创建一个 log 目录 在里面放置一个空的 .gitignore 文件。这样当你 clone 这个 repo 的时候 git 会自动的创建好一个空的 log 目录了。