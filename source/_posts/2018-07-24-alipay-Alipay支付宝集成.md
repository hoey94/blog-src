---
layout: post
title: Alipay对接
date: 2018-06-24 00:00:00
categories: 后端
---

在开始开发之前，需要通过向阿里申请获取相关信息，主要就是审核，审核通过后会得到相关参数

随后与spring做集成,这边的思路是由spring容器去管理DefaultAlipayClient和AlipayPayment

AlipayPayment是我们自己写的接口

DefaultAlipayClient 是阿里提供给我们的接口

```xml
<bean class="com.alipay.api.DefaultAlipayClient" name="alipayClient" autowire="byName">
	<constructor-arg value="${alipay.gateway}"/>
	<constructor-arg value="${alipay.appId}"/>
	<constructor-arg value="${alipay.appPrivateKey}"/>
	<constructor-arg value="json"/>
	<constructor-arg value="utf-8"/>
	<constructor-arg value="${alipay.appPublicKey}"/>
	<constructor-arg value="RSA2"/>
</bean>
<bean class="com.bim.bdip.cloud.home.payment.AlipayPayment" name="alipayPayment" autowire="byName"/>
```

#### 购买界面入口

![image](http://ww1.sinaimg.cn/large/0066vfZIgy1ftky81canfj30ko0ijgoy.jpg)

```java
// 购买兑换码
@RequestMapping(method = RequestMethod.POST, value = "/buy", produces = "text/html")
@ResponseBody
public String buyRedeemCode(HttpServletRequest request, HttpServletResponse response) throws PaymentException, IOException {
	HttpSession session = request.getSession();
	BimUser bimUser = (BimUser) session.getAttribute(ConstantDefine.LOGIN_SESSION_USER);
	if (bimUser == null) {
		String page = "/page/bdip/baseModel/index";
		response.sendRedirect(page);
	}
	long uId = bimUser.getId();
	String redeemCodeLevel = request.getParameter("redeemCodeLevel");
	String paymentMethod = request.getParameter("paymentMethod");
	Object[] param = new Object[]{redeemCodeLevel, uId, paymentMethod};
	Parameter parameter = new Parameter(BizServiceDefine.bimOrderService, "buyRedeemCode").setParam(param);
	parameter = bizProvider.execute(parameter);
	BimOrder order = parameter == null ? null : (BimOrder) parameter.getModel();
	return alipayPayment.pay(order).getBody();
}
```

#### 业务层
1.锁定商品，禁止他人购买
2.生成订单

```java
@Override
public BimOrder buyRedeemCode(String redeemCodeLevel, Long uid, String paymentMethod) {
	BimOrder order = new BimOrder();
	BimRedeemLevel redeemLevel = new BimRedeemLevel();
	redeemLevel.setLevel(redeemCodeLevel);
	redeemLevel = bimRedeemLevelMapper.selectOne(redeemLevel);
	Wrapper<BimRedeemCode> wrapper = new EntityWrapper<>();
	wrapper = wrapper.where("redeem_level_id = {0}", redeemLevel.getId())
			.and("status = 0")            // 未售出
			.and("redeem_code_type = 1"); // 线上购买
	List<BimRedeemCode> bimRedeemCodes = bimRedeemCodeMapper.selectList(wrapper);
	if (bimRedeemCodes.size() == 0) {
		return null;
	}

	String subject = String.format("购买 %.2f埃币 兑换码", redeemLevel.getIcoinAmount());
	BimRedeemCode redeemCode = bimRedeemCodes.get(0);
	redeemCode.setStatus(ConstantDefine.REDEEM_CODE_STATUS_LOCKED);
	bimRedeemCodeMapper.updateById(redeemCode);
	order.setAmount(redeemLevel.getAmount());
	order.setPayExpireTime(new Date(new Date().getTime() + 1800000l)); // 半小时过期
	order.setCurrencyType(ConstantDefine.CURRENCY_CNY);
	order.setCommodityTypeId(1l);
	order.setPaymentMethod(paymentMethod);
	order.setCreatedRole(0); // 用户
	order.setUserId(uid);
	order.setProductId(redeemCode.getId());
	order.setSubject(subject);
	return this.addBimOrder(order);
}
```

#### alipayPayment 是为了对接做一个简单的封装。
1.alipayClient
2.returnUrl
3.notifyUrl
```java
@Service
public class AlipayPayment implements IPayment {

    private Logger logger = LogManager.getLogger(this.getClass());

    @Autowired
    private AlipayClient alipayClient;

    @Value("${alipay.returnUrl}")
    private String returnUrl;

    @Value("${alipay.notifyUrl}")
    private String notifyUrl;

    @Override
    public PaymentResult pay(BimOrder order) throws PaymentException {
        AlipayTradePagePayRequest request = new AlipayTradePagePayRequest();
        AlipayTradePagePayModel model = new AlipayTradePagePayModel();
        request.setReturnUrl(returnUrl);
        request.setNotifyUrl(notifyUrl);
        JSONObject bizContent = new JSONObject();
        bizContent.put("out_trade_no", order.getOrderNumber());
        bizContent.put("product_code", "FAST_INSTANT_TRADE_PAY");
//        bizContent.put("total_amount", order.getAmount());
        bizContent.put("total_amount", 0.01); // 设置消费金额
        bizContent.put("subject", order.getSubject());
        bizContent.put("body", order.getSubject());
        request.setBizContent(bizContent.toJSONString());
        PaymentResult paymentResult = new PaymentResult();
        try {
            AlipayResponse response = alipayClient.pageExecute(request);
            String body = response.getBody();
            paymentResult.setResultType(PaymentResultType.BODY);
            paymentResult.setBody(body);
        } catch (AlipayApiException e) {
            logger.catching(e);
            throw new PaymentException(e);
        }

        return paymentResult;
    }

    @Override
    public boolean refund(BimOrder order) {
        return false;
    }

    @Override
    public boolean cancel(BimOrder order) {
        return false;
    }
}
```

pay 接口负责将生成好的Order订单信息发送给阿里，然后阿里那边会返回一个结果

```java
public class PaymentResult {
    private String redirectUrl;
    private String body;
    private PaymentResultType resultType;
    private String orderNo;
    private Date expireTime;

    // ====== setter and getter =====
}

public enum PaymentResultType {
    REDIRECT,
    BODY
}
```

当用户支付以后，就会走我们写的回调函数,returnUrl 和 notifyUrl俩参数实现已经在Common-config.properties写好

alipay.returnUrl=http://cloud.bimbdip.com/callbacks/paymentReturn
alipay.notifyUrl=http://cloud.bimbdip.com/callbacks/paymentNotify

```java
@Controller
@Api(value = "回调")
@RequestMapping("/callbacks")
@PropertySources(value = {@PropertySource("classpath:Common-config.properties"), @PropertySource("classpath:user_space_size.properties")})
public class CallbacksController {
    @Autowired
    private IBizProvider bizProvider;

    @Autowired
    private AlipayClient alipayClient;

    @Value("${alipay.publicKey}")
    private String alipayPublicKey;

    @ApiOperation(value = "支付宝notify")
    @RequestMapping(method = RequestMethod.POST, value = "/alipayNotify", produces = "text/plain;charset=UTF-8")
    public
    @ResponseBody
    String alipayNotify(HttpServletRequest request, HttpServletResponse response) throws Exception {
        Map<String, String> map = new HashMap<>();
        for (String key : request.getParameterMap().keySet()) {
            map.put(key, request.getParameter(key));
        }

        boolean signatureVerified = AlipaySignature.rsaCheckV1(map, alipayPublicKey, "utf-8", "RSA2");
        if (signatureVerified) {
            String orderNumber = request.getParameter("out_trade_no");
            String paymentOrderNumber = request.getParameter("trade_no");
            this.alipayOrderPaid(orderNumber, paymentOrderNumber);
        }
        return "success";
    }

    /*
     * 支付宝Return
     */
    @ApiOperation(value = "支付宝return")
    @RequestMapping(method = RequestMethod.GET, value = "/alipayReturn")
    public String alipayReturn(HttpServletRequest request, HttpServletResponse response) throws AlipayApiException {
        Map<String, String> params = new HashMap<>();
        Map<String, String[]> requestParams = request.getParameterMap();
        for (Iterator<String> iter = requestParams.keySet().iterator(); iter.hasNext(); ) {
            String name = (String) iter.next();
            String[] values = (String[]) requestParams.get(name);
            String valueStr = "";
            for (int i = 0; i < values.length; i++) {
                valueStr = (i == values.length - 1) ? valueStr + values[i]
                        : valueStr + values[i] + ",";
            }
            //乱码解决，这段代码在出现乱码时使用
//            valueStr = new String(valueStr.getBytes("ISO-8859-1"), "utf-8");
            params.put(name, valueStr);
        }

        boolean signatureVerified = AlipaySignature.rsaCheckV1(params, alipayPublicKey, "utf-8", "RSA2");
        if (signatureVerified) {
            String orderNumber = request.getParameter("out_trade_no");
            String paymentOrderNumber = request.getParameter("trade_no");
            this.alipayOrderPaid(orderNumber, paymentOrderNumber);
        } else {
            return "forward:/page/bdip/user/index";
        }
        return "forward:/page/bdip/redeemcode/record";
    }

    private void alipayOrderPaid(String orderNumber, String paymentOrderNumber) {
        Object[] param = new Object[]{orderNumber, "ALIPAY", paymentOrderNumber};
        Parameter parameter = new Parameter(BizServiceDefine.bimOrderService, "orderPaid").setParam(param);
        bizProvider.execute(parameter);
    }
}
```

#### 关于returnUrl和notifyUrl

买家付款成功以后,支付宝那边会调用returnUrl接口，跳转到相应界面展示给用户看。只有当用户付款成功以后才有效

notifyUrl，是用户后台通信存在的，当用户付款成功以后，支付宝会调用这个接口，我们要做的就是在这个接口中修改订单状态以及商品状态，成功以后返回一个"success"即可

考虑到安全性问题代码中使用了RSA非对称加密协议对通信的信息进行加解密。(AlipaySignature.rsaCheckV1)

至此基础开发应该就已经结束了。根据实景情况做具体调整