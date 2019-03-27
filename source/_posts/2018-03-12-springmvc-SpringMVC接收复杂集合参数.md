---
layout: post
title: SpringMVC接收复杂集合参数
tags: 问题总结
date: 2018-03-12 00:00:00
categories: 后端
tags: spring
---

记两个方式

## 1.使用form的ajax方式提交

### 后台代码

后台使用的是springmvc框架

实体类：

```java
public class BimWorkflowDetailBase {

	@TableField("model_id")
	private String modelId;
   
	@TableField("cc_name")
	private String ccName;

	@TableField("cc_names")
	private String ccNames;

	@TableField("status_")
	private String status;
	....
}
```

实体类包装起来

```java
public class WorkFlowCollisionWrapper {

	private List<BimWorkflowCollision> collisions;

	public List<BimWorkflowCollision> getCollisions() {
		return collisions;
	}

	public void setCollisions(List<BimWorkflowCollision> collisions) {
		this.collisions = collisions;
	}
}
```

在控制器的参数中直接写上包装类

```java
@RequestMapping(value="/check",method=RequestMethod.POST,produces="application/json")
public @ResponseBody String check(WorkFlowCollisionWrapper collisions) {
	System.out.println(collisions.getCollisions().size());
	return null;
}
```

### 前台代码

这里我使用了ES6动态生成html 里面的${index} 是ES6的写法,我们在这边的写法是`name="collisions[0].id"  name="collisions[1].id`以此类推就可以正常传入到后台

```html
<table class="m-initating-table hei30" name="initating-table-${index}">
	<tr>
		<td class="center">专业编号</td>
		<td>
			<input readonly="readonly" name="collisions[${index}].zybh" value="${typeof(node.zybh)=='undefined'?'':node.zybh}" class="tableinput first firstStageInput fourthStageInput" type="text" maxlength="20">
		</td>
		<td class="center">类别编号</td>
		<td>
			<select disabled="disabled" name="collisions[${index}].lbbh" class="tableSelect first firstStageSelect fourthStageSelect" style="width: 80%;margin: 0 auto;display: block;">
				<option value="A" ${typeof(node.lbbh)=='undefined' || node.lbbh == 'A'?'selected':''}>A</option>
				<option value="B" ${node.lbbh == 'B'?'selected':''}>B</option>
				<option value="C" ${node.lbbh == 'C'?'selected':''}>C</option>
				<option value="D" ${node.lbbh == 'D'?'selected':''}>D</option>
			</select>
		</td>
	</tr>
</table>
```

这里使用form表单序列化所有的值,发送ajax请求后台

```javascript
var url = publicJS.tomcat_url + '/workflow/check';
var data = $('#collisionForm').serialize();
$.ajax({
	url : url,
	type : 'POST',
	data : data,
	dataType : 'json',
	success : function(data){

	},
	error : function(error){
		
	}
})
```

## 2.使用纯ajax方式提交

### 后台

实体类

```java
public class User {  
        private String name;   
    private String pwd;  
    //省略getter/setter  
}    
```

控制器

```java
@Controller  
@RequestMapping("/catalog.do")  
public class CatalogController {  
  
    @RequestMapping(params = "fn=saveUsers")  
    @ResponseBody  
    public AjaxJson saveUsers(@RequestBody List<User> userList) {  
        …  
    }  
}
```

### 前台

```javascript
var userList = new Array();  
userList.push({name: "李四",pwd: "123"});   
userList.push({name: "张三",pwd: "332"});   
$.ajax({  
    type: "POST",  
    url: "<%=path%>/catalog.do?fn=saveUsers",  
    data: JSON.stringify(userList),//将对象序列化成JSON字符串  
    dataType:"json",  
    contentType : 'application/json;charset=utf-8', //设置请求头信息  
    success: function(data){  
        …  
    },  
    error: function(res){  
        …  
    }  
});
```