---
layout: post
title: MapReduce小例子

date: 2018-05-04 00:00:00
categories: 大数据
tags: MapReduce
---
案例一 : 统计单词出现个数

a  b  a  b a  
a  b  a  b a  
b a b a b  a  b a  
b a b  

a,1 a,1 a,1 a,1 a,1 a,1 a,1 a,1 a,1 ```|``` b,1 b,1 b,1 b,1 b,1 b,1 b,1 b,1 b,1

k -> a  values -> 1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1  
sum = 0  
for (int i=0; values.length ; i++){  
	sum ++;  
}  

案例二 : 统计手机上下行流量

17654565484    80000000   6000  
17654565484    80000000   6000  
17654565484    80000000   6000  
17654565484    80000000   6000  
17654565484    80000000   6000  
17654565484    80000000   6000  
15565658787    54455455   5464654  
15565658787    54455455   5464654  
15565658787    54455455   5464654  
15565658787    54455455   5464654  
15565658787    54455455   5464654  

17654565484,bean 17654565484,bean 17654565484,bean 17654565484,bean ```|``` 15565658787,bean 15565658787,bean 15565658787,bean 15565658787,bean

k -> 17654565484  values -> bean ,bean ,bean ,bean

sumUpStream = 0  
sumDownStream = 0  
for (int i=0; values.length ; i++){  
	sumUpStream += bean.upStream();  
	sumDownStream += bean.DOwnStream();  
}  

案例三 : 统计两个人的共同好友

A : B,C,D  
B : E,F,D   
C : E,D  

B,A C,A D,A E,B F,B D,B E,C D,C ->  B,A ```|``` C,A ```|``` D,A D,B D,C ```|``` E,B E,C ```|``` F,B

B : A  
C : A  
D : A ,B ,C  
E : B ,C  
F : B  

A ,B的好友是D  
A ,C的好友是D  

