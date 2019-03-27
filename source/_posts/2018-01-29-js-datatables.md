---
layout: post
title: DataTables与requireJs冲突的解决
date: 2018-01-29 00:00:00
---

**DataTables与requireJs冲突的解决**当我在项目中同时使用requireJs和DataTablesJs的时候，提示了一个错误**$(...).DataTable is not a function**，我通过尝试修改源码并解决了这个问题。具体操作步骤如下:

先看datatables.js源码总体的一个结构:

```javascript
(function( factory ) {//......}
(function() {
      "use strict";
       //.......
       return $.fn.dataTable;
}));  
```

修改为以下两种任意一种形式都可以（一本机测试为准）:

```javascript
(function( factory ) {//......}
(function( $ ) {
      "use strict";
      //.......
      return $.fn.dataTable;
}($));  
```

```javascript
(function( factory ) {//......}
(function( ) {
      "use strict";
      //.......
      return $.fn.dataTable;
}());
```