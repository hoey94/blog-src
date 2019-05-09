---
title: RDD DataSet和DataFrame的区别和应用场景
date: 2019-04-24 11:47:37
tags: Spark
categories: 大数据
---

在spark中，RDD、DataFrame、Dataset是最常用的数据类型，本博文给出笔者在使用的过程中体会到的区别和各自的优势。

## 共性

1、 RDD、DataFrame和Dataset全都是spark平台下的分布式弹性数据集，为处理超大型数据提供便利；

2、 三者都有惰性机制，在进行创建、转换，如map方法时，不会立即执行，只有在遇到Action如foreach时，三者才会开始遍历运算，极端情况下，如果代码里面有创建、转换，但是后面没有在Action中使用对应的结果，在执行时会被直接跳过，如

```scala
val sparkconf = new SparkConf().setMaster("local").setAppName("test").set("spark.port.maxRetries","1000")
val spark = SparkSession.builder().config(sparkconf).getOrCreate()
val rdd=spark.sparkContext.parallelize(Seq(("a", 1), ("b", 1), ("a", 1)))
rdd.map{line=>
    println("运行")
    line._1
}
```

map中的println("运行")并不会运行。

3、三者都会根据spark的内存情况自动缓存运算，这样即使数据量很大，也不用担心会内存溢出。

4、三者都有partition的概念

```scala
var predata=data.repartition(24).mapPartitions{
    PartLine => {
        PartLine.map{
            line =>
            println(“转换操作”)
        }
    }
}
```

这样对每一个分区进行操作时，就跟在操作数组一样，不但数据量比较小，而且可以方便的将map中的运算结果拿出来，如果直接用map，map中对外面的操作是无效的

```scala
val rdd=spark.sparkContext.parallelize(Seq(("a", 1), ("b", 1), ("a", 1)))
var flag=0
val test=rdd.map{line=>
    println("运行")
    flag+=1
    println(flag)
    line._1
}
println(test.count)
println(flag)
```

结果如下:
```
运行
1
运行
2
运行
3
3
0
```

不使用partition时，对map之外的操作无法对map之外的变量造成影响。

5、三者有许多共同的函数，如filter，排序等。

6、在对DataFrame和Dataset进行操作许多操作都需要这个包进行支持。

```scala
//这里的spark是SparkSession的变量名
import spark.implicits._
```

7、DataFrame和Dataset均可使用模式匹配获取各个字段的值和类型。

DataFrame:

```scala
testDF.map{
    case Row(col1:String,col2:Int)=>
    println(col1);println(col2)
    col1
    case _=>
    ""
}
```

为了提高稳健性，最好后面有一个_通配操作，这里提供了DataFrame一个解析字段的方法。

Dataset:

```scala
case class Coltest(col1:String,col2:Int)extends Serializable //定义字段名和类型
testDS.map{
    case Coltest(col1:String,col2:Int)=>
    println(col1);println(col2)
    col1
    case _=>
    ""
}
```

## 区别

#### RDD

1、RDD一般和spark mlib同时使用。

2、RDD不支持sparkSQL操作。

DataFrame:

1、与RDD和Dataset不同，DataFrame每一行的类型固定为Row，只有通过解析才能获取各个字段的值，如

```scala
testDF.foreach{
    line =>
    val col1=line.getAs[String]("col1")
    val col2=line.getAs[String]("col2")
}
```

每一列的值没法直接访问。

2、DataFrame与Dataset一般与spark ml同时使用。

3、DataFrame与Dataset均支持sparksql的操作，比如select，groupby之类，还能注册临时表/视窗，进行sql语句操作，如

```scala
dataDF.createOrReplaceTempView("tmp")
spark.sql("select ROW,DATE from tmp where DATE is not null order by DATE").show(100,false)
```

4、DataFrame与Dataset支持一些特别方便的保存方式，比如保存成csv，可以带上表头，这样每一列的字段名一目了然。

```scala
//保存
val saveoptions = Map("header" -> "true", "delimiter" -> "t", "path" -> "hdfs://172.xx.xx.xx:9000/test")
datawDF.write.format("com.databricks.spark.csv").mode(SaveMode.Overwrite).options(saveoptions).save()
//读取
val options = Map("header" -> "true", "delimiter" -> "t", "path" -> "hdfs://172.xx.xx.xx:9000/test")
val datarDF= spark.read.options(options).format("com.databricks.spark.csv").load()
```

利用这样的保存方式，可以方便的获得字段名和列的对应，而且分隔符（delimiter）可以自由指定。

Dataset:

这里主要对比Dataset和DataFrame，因为Dataset和DataFrame拥有完全相同的成员函数，区别只是每一行的数据类型不同。

DataFrame也可以叫Dataset[Row],每一行的类型是Row，不解析，每一行究竟有哪些字段，各个字段又是什么类型都无从得知，只能用上面提到的getAS方法或者共性中的第七条提到的模式匹配拿出特定字段。

而Dataset中，每一行是什么类型是不一定的，在自定义了case class之后可以很自由的获得每一行的信息。

```scala
case class Coltest(col1:String,col2:Int)extends Serializable //定义字段名和类型
//rdd
//("a", 1)
//("b", 1)
//("a", 1)
val test: Dataset[Coltest]=rdd.map{line=>
    Coltest(line._1,line._2)
}.toDS
test.map{
    line=>
    println(line.col1)
    println(line.col2)
}
```

可以看出，Dataset在需要访问列中的某个字段时是非常方便的，然而，如果要写一些适配性很强的函数时，如果使用Dataset，行的类型又不确定，可能是各种case class，无法实现适配，这时候用DataFrame即Dataset[Row]就能比较好的解决问题。

转化：

RDD、DataFrame、Dataset三者有许多共性，有各自适用的场景常常需要在三者之间转换。

DataFrame/Dataset转RDD：

这个转换很简单

```scala
val rdd1=testDF.rdd
val rdd2=testDS.rdd
```

RDD转DataFrame：

```scala
import spark.implicits._
val testDF = rdd.map {line=>
    (line._1,line._2)
}.toDF("col1","col2")
```

一般用元组把一行的数据写在一起，然后在toDF中指定字段名。

RDD转Dataset：

```scala
import spark.implicits._
case class Coltest(col1:String,col2:Int)extends Serializable //定义字段名和类型
val testDS = rdd.map {line=>
    Coltest(line._1,line._2)
}.toDS
```

可以注意到，定义每一行的类型（case class）时，已经给出了字段名和类型，后面只要往case class里面添加值即可。

Dataset转DataFrame：

这个也很简单，因为只是把case class封装成Row。

```scala
import spark.implicits._
val testDF = testDS.toDF
```

DataFrame转Dataset：

```scala
import spark.implicits._
case class Coltest(col1:String,col2:Int)extends Serializable //定义字段名和类型
val testDS = testDF.as[Coltest]
```

这种方法就是在给出每一列的类型后，使用as方法，转成Dataset，这在数据类型是DataFrame又需要针对各个字段处理时极为方便。

特别注意：

在使用一些特殊的操作时，一定要加上 import spark.implicits._ 不然toDF、toDS无法使用。