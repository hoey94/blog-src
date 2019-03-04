---
layout: post
title: Ngnix Websocket 400 错误
date: 2018-11-15 00:00:00
categories: 后端
tags: WebSocket
---

Spring WebSocket 结合ngnix 之后``400``报错！

今天消息推送功能上测试服以后发现不能使用，到测试服上发现发送的请求一直返回400。后来定位到是ngnix配置问题。联系运维哥们将下面代码添加上以后成功解决:

```python
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection $connection_upgrade;

```

添加好之后的样子

```python
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''  close;
}
server {
        ...
        location /chat/ {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
        }
}

```

