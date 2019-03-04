---
layout: post
title: content-disposition使用
tags: 问题总结
date: 2018-03-12 00:00:00
categories: 其他
---

content-disposition 是RFC中定义的文件下载标识字段,详情查看rfc2616章节19.5 [Additional Features](http://www.rfc-editor.org/rfc/rfc2616.pdf),其中有两种形式供给我们选择，一个是inline，一个是attachment

### 在页面内打开代码：

```java
File file = new File("rfc1806.txt");  
String filename = file.getName();  
response.setHeader("Content-Type","text/plain");  
response.addHeader("Content-Disposition","inline;filename=" + new String(filename.getBytes(),"utf-8"));  
response.addHeader("Content-Length","" + file.length());  
```

### 弹出保存框代码：

```java
File file = new File("rfc1806.txt");  
String filename = file.getName();  
response.setHeader("Content-Type","text/plain");  
response.addHeader("Content-Disposition","attachment;filename=" + new String(filename.getBytes(),"utf-8"));  
response.addHeader("Content-Length","" + file.length());  
```

### 场景应用，导出word文档：

控制层使用的springmvc

```java
/**
 * 导出word功能
 * @param workflowId 流程的id
 * @throws IOException 
 */
@ApiOperation(value="导出word功能",notes="导出word功能")
@ApiResponses(value= {@ApiResponse(code=200,message="导出成功",response=BimWorkflowDetailController.class)})
@RequestMapping(value="/exportCollision")
public String exportCollision(String workflowId,HttpServletResponse response) throws IOException {
	//response.setContentType("application/octet-stream; charset=UTF-8");
	response.setHeader("content-disposition", "attachment;filename=" + new SimpleDateFormat("yyyyMMddHH:mm:ss").format(new Date(System.currentTimeMillis())) + ".doc");
	// opera和firefox可以正常使用，而ie不能正常使用 添加下列头
	response.setHeader("Pragma","No-cache"); 
	response.setHeader("Cache-Control","No-cache"); 
	response.setDateHeader("Expires",0);
	
	ApiResultEntity apiResultEntity = new ApiResultEntity();
	apiResultEntity.setDataEncode(true);
	// 1.根据workflowid从数据库查询相关信息
	Parameter parameter = new Parameter(BizServiceDefine.bimWorkflowDetailService, "getBimWorkflowInfoById").setId(NumberUtil.tryParseLong(workflowId));
	parameter = bizProvider.execute(parameter);
	apiResultEntity = (ApiResultEntity) parameter.getResult();
	Map<String,Object> param = (Map<String,Object>) apiResultEntity.getData();
	BimWorkflowDetail workflowBase = (BimWorkflowDetail) param.get("bimWorkflowDetail");
	List<BimWorkflowCollision> collisionLists = (List<BimWorkflowCollision>) param.get("collisionLists");
	OutputStream out = null;
	try {
		out = response.getOutputStream();
		// 存word
		saveDoc(workflowBase, collisionLists, out);
	} catch (Exception e) {
		logger.error("导出word异常!!!!");
		e.printStackTrace();
	}
	out.flush();  
    out.close();  
    return null;  
}
```
