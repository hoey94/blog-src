---
layout: post
title: Spring WebSocket消息推送
date: 2018-11-14 00:00:00
categories: 后端
tags: WebSocket
---


需求:后台编辑推送消息，前台实时接收消息

下面是js实现
```javascript

$(function() {
	bdipOnline();
});

var bdipWebSocket;
var bdipReconnectTime = 5000;
function bdipOnline() {
	if (window.WebSocket) {
		var protocol = publicJS.protocol == "https"? "wss": "ws";
        try{
            bdipWebSocket = new WebSocket(encodeURI(protocol + '://' + publicJS.host +'/ws')); //cloud.bimbdip.com
        }catch (err){
            console.log("online链接websocket失败");
        }

        if(bdipWebSocket){

			bdipWebSocket.onopen = function() {
				console.log("bdipWebSocket链接成功... bdipReconnectTime :" + bdipReconnectTime)
				//连接成功
				//bdipReconnectTime = 10000;
                setTimeout(bdipOnline, bdipReconnectTime);
			};

			bdipWebSocket.onerror = function() {
				console.log("bdipWebSocket发生错误... bdipReconnectTime :" + bdipReconnectTime)
				//连接失败
				setTimeout(bdipOnline, bdipReconnectTime);
				bdipReconnectTime += 5000;
			};
			bdipWebSocket.onclose = function() {
				//连接断开
				console.log("bdipWebSocket断开链接... bdipReconnectTime :" + bdipReconnectTime)
				setTimeout(bdipOnline, bdipReconnectTime);
				bdipReconnectTime += 5000;
			};
			//消息接收
			bdipWebSocket.onmessage = function(message) {
				console.log("接收到消息，消息内容为:" + message);
				var data = JSON.parse(message.data);
				if (data.type == 'logMessage') {
					notificate(data.data);
				}
			};
        }
	}
}

// 弹出消息框
function notificate(_message) {
    var msgContent = JSON.parse(_message.content)
	var title = msgContent.title;
	if(title == null || typeof(title) == 'undefined' || title == '') {
		title = "通知中心";
	}
	var content = msgContent.content;
	if(content.length > 140) {
		content = content.substr(0, 140);
	}
	$("#notification-title").html(title);
	$("#notification-content").html(content);
	//$(".notification-panel").show();
    $(".notification-panel").slideDown(1000);
	setTimeout(function(){
		//$(".notification-panel").hide();
        $(".notification-panel").slideUp(1000);
	}, 5000);
}

```

下面是后台代码,先说一下实现思路:
1.在后台管理系统中编辑待推送数据并完成推送消息操作;
2.spring websocket 检测到用户登录，按某种规则将用户信息保存到redis；
3.定时轮训查看待推送信息，当检测到用户在线时进行推送，更新数据库为已推送；

其中使用到了使用redis（订阅和发布）功能进行数据推送,下面上代码：

spring websocket handler 监听用户登录的代码:
```java
package com.bim.bdip.cloud.home.web;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.mapper.EntityWrapper;
import com.bim.bdip.cloud.home.constant.BizServiceDefine;
import com.bim.bdip.cloud.home.constant.ConstantDefine;
import com.bim.bdip.cloud.home.core.base.Parameter;
import com.bim.bdip.cloud.home.domain.api.ApiResultEntity;
import com.bim.bdip.cloud.home.model.BimMessageCenter;
import com.bim.bdip.cloud.home.model.BimUser;
import com.bim.bdip.cloud.home.provider.IBizProvider;
import org.apache.ibatis.session.RowBounds;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;
import org.redisson.api.RTopic;
import org.redisson.api.RedissonClient;
import org.redisson.api.listener.MessageListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import org.springframework.web.socket.server.support.HttpSessionHandshakeInterceptor;

import java.io.IOException;
import java.util.List;
import java.util.Map;

public class WebSocketHandler extends TextWebSocketHandler {
    private static final Logger logger = LogManager.getLogger(WebSocketHandler.class);
    @Autowired
    private RedissonClient redissonClient;

    @Autowired
    private IBizProvider bizProvider;

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {

    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {

        super.afterConnectionEstablished(session);
        Map<String, Object> attributes = session.getAttributes();

        BimUser user = (BimUser) attributes.get(ConstantDefine.LOGIN_SESSION_USER);

        if (user == null) {
            session.close();
        } else {
            System.out.println("检测到用户登录:" + user.getId() + "当前线程ID为:" + Thread.currentThread().getId());
            Long userId = user.getId();
            String topic = String.format("notification:%d", userId);
            RTopic<BimMessageCenter> rtopic = redissonClient.getTopic(topic);
            rtopic.removeAllListeners();

            String listenerKey = String.format("notification:%d:listeners", user.getId());
            redissonClient.getSet(listenerKey).delete();
            Integer listenerId = rtopic.addListener(new MessageListener<BimMessageCenter>() {
                @Override
                public void onMessage(String channel, BimMessageCenter msg) {
                    System.out.println("向用户推送消息:" + msg);
                    JSONObject jsonObject = new JSONObject();
                    jsonObject.put("type", "logMessage");
                    jsonObject.put("data", msg);
                    TextMessage textMessage = new TextMessage(jsonObject.toJSONString());
                    try {
                        session.sendMessage(textMessage);
                    } catch (IOException e) {
                        logger.error("Websocket Error.", e);
                    }
                }
            });

            redissonClient.getSet(listenerKey).add(listenerId);
            attributes.put(ConstantDefine.LISTENER_ID, listenerId);
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        Map<String, Object> attributes = session.getAttributes();

        BimUser user = (BimUser) attributes.get(ConstantDefine.LOGIN_SESSION_USER);
        Integer listenerId = (Integer) attributes.get(ConstantDefine.LISTENER_ID);
        if (user != null) {
            System.out.println("用户退出:" + user.getId());
            super.afterConnectionClosed(session, status);
            String topic = String.format("notification:%d", user.getId());
            String listenerKey = String.format("notification:%d:listeners", user.getId());
            redissonClient.getSet(listenerKey).remove(listenerId);
            RTopic<BimMessageCenter> rtopic = redissonClient.getTopic(topic);
            rtopic.removeListener(listenerId);
        }
    }

}

```

下面是定时任务,定时任务轮训待推送数据，如果检测到用户登录(通过redis)，就进行数据推送(通过redis topic):

```java
package com.bim.bdip.cloud.home.scheduled;

import com.baomidou.mybatisplus.mapper.EntityWrapper;
import com.bim.bdip.cloud.home.model.BimMessageCenter;
import com.bim.bdip.cloud.home.service.IBimMessageCenterService;
import org.apache.ibatis.session.RowBounds;
import org.redisson.api.RTopic;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;

@Service
@EnableScheduling
public class NotificationTask {

    @Autowired
    private RedissonClient redissonClient;

    @Autowired
    private IBimMessageCenterService messageCenterService;

    @Scheduled(cron="1 * * * * ?")
    public void scanNotifications() {EntityWrapper<BimMessageCenter> wrapper = new EntityWrapper<>();
        RowBounds rowBounds = new RowBounds(0, 10000000);
        wrapper.where("read_status = {0}", 0).and("notification_status = {0}", 0).and("message_type = {0}", "logMessage");

        List<BimMessageCenter> messageList = messageCenterService.selectPage(rowBounds, wrapper);
        System.out.println("轮训检测数据库数据" + messageList.size() + "当前线程ID为:" + Thread.currentThread().getId() + "当前时间为" + new Date().getTime());
        for(BimMessageCenter message : messageList) {
            String listenerKey = String.format("notification:%d:listeners", message.getReceiveId());
            if(redissonClient.getSet(listenerKey).size() > 0) {
                System.out.println("检测到用户" + message.getReceiveId() + "在线，推送消息");
                String topic = String.format("notification:%d", message.getReceiveId());
                RTopic<BimMessageCenter> rTopic = redissonClient.getTopic(topic);
                rTopic.publish(message);
                if(message.getNotificationStatus() != 2){
                    message.setNotificationStatus(2); // 已推送
                    this.messageCenterService.update(message);
                }
            }
        }
        System.out.println("轮训结束，当前时间为:" + new Date().getTime());
    }

}

```