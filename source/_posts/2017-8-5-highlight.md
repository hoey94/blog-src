---
layout: post
title: highlight网页代码高亮显示
date: 2017-08-05 00:00:00
categories: 博客
---

#### 使用

1. 引入highlight.min.js和monokai_sublime.min.css，使用initHighlightingOnLoad()初始化.

```
<link href="http://cdn.bootcss.com/highlight.js/8.0/styles/monokai_sublime.min.css" rel="stylesheet">
<script src="http://cdn.bootcss.com/highlight.js/8.0/highlight.min.js"></script>
<script >hljs.initHighlightingOnLoad();</script>    
```

2. 使用`<pre>`和`<code class="html">` 指定文本的内容信息例如

`<pre><code class="js">code.....</code></pre>`

#### 展示

* js代码:

<pre>
<code class="js">
    var arr = new Array();
    var input_element =  document.getElementById("input");
    alert(input_element.value);
</code>
</pre>

* java代码:

<pre>
<code class="java">
   class Demo{
    public static void main(String[] args){
        Systemm.out.println("java");
    }
   }
</code>
</pre>

* C代码:

<pre>
<code class="c">
   int main(){
    printf("c");
    return 1;
   }
</code>
</pre>

* linux

<pre>
<code class="linux">
   $ echo $(xdpyinfo|grep 'dimensions:' | awk '{print $2}')
</code>
</pre>

官网 https://highlightjs.org/download/