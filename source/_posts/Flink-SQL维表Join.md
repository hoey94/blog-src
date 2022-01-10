### 1. 维表

#####  HBase数据

```sql
put 'ods:dim_province','1','field:province_id','1'
put 'ods:dim_province','1','field:province_name','上海'
put 'ods:dim_province','1','field:region_name','浦东新区'
put 'ods:dim_province','3','field:province_id','3'
put 'ods:dim_province','3','field:province_name','上海'
put 'ods:dim_province','3','field:region_name','金桥'
put 'ods:dim_province','28','field:province_id','28'
put 'ods:dim_province','28','field:province_name','河南'
put 'ods:dim_province','28','field:region_name','洛阳'
put 'ods:dim_province','29','field:province_id','29'
put 'ods:dim_province','29','field:province_name','河南'
put 'ods:dim_province','29','field:region_name','郑州'
create 'ods:dim_province',{NAME => 'field', VERSIONS => 1}
```
##### HBase Flink DDL

```sql
CREATE TABLE dim_province_hbase (
 rowkey STRING,
    field ROW<
        province_id VARCHAR,  -- 省份id
        province_name  VARCHAR, -- 省份名称
        region_name VARCHAR -- 区域名称
    >,
     PRIMARY KEY (rowkey) NOT ENFORCED
) WITH (
    'connector' = 'hbase-2.2',
    'table-name'='ods:dim_province',
    'zookeeper.quorum'='localhost:2181',
    'sink.buffer-flush.interval'='200ms',
    'sink.buffer-flush.max-rows'='100000',
    'null-string-literal'='\N'
);
```

##### Mysql 数据

```sql
DROP TABLE IF EXISTS `dim_province`;
CREATE TABLE `dim_province` (
  `province_id` bigint NOT NULL,
  `province_name` varchar(255) DEFAULT NULL,
  `region_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`province_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dim_province
-- ----------------------------
BEGIN;
INSERT INTO `dim_province` VALUES (1, '上海', '浦东新区');
INSERT INTO `dim_province` VALUES (3, '上海', '金桥');
INSERT INTO `dim_province` VALUES (28, '河南', '洛阳');
COMMIT;

```

##### Mysql Flink DDL

```sql
CREATE TABLE dim_province (
    province_id BIGINT,  -- 省份id
    province_name  VARCHAR, -- 省份名称
    region_name VARCHAR -- 区域名称
) WITH (
    'connector' = 'jdbc',
	'url' = 'jdbc:mysql://127.0.0.1:3306/test?characterEncoding=utf-8&useSSL=false&rewriteBatchedStatements=true&serverTimezone=Asia/Shanghai',
	'table-name' = 'dim_province',
	'driver' = 'com.mysql.jdbc.Driver',
	'sink.buffer-flush.interval' = '200ms',
	'sink.buffer-flush.max-rows' = '100000',
    'username' = 'root',
    'password' = 'root'
);
```



### 2. Kafka

```json
{"order_id":1,"currency":"CN","amount":100,"ts":1573445919}
{"order_id":1,"currency":"CN","amount":100,"ts":1573445919}
```



##### Flink DDL

```sql
CREATE TABLE user_behavior (
    user_id BIGINT, -- 用户id
    item_id BIGINT, -- 商品id
    cat_id BIGINT,  -- 品类id
    action STRING,  -- 用户行为
    province INT,   -- 用户所在的省份
    ts     BIGINT,  -- 用户行为发生的时间戳
    proctime as PROCTIME(),   -- 通过计算列产生一个处理时间列
    eventTime AS TO_TIMESTAMP(FROM_UNIXTIME(ts, 'yyyy-MM-dd HH:mm:ss')), -- 事件时间
    WATERMARK FOR eventTime as eventTime - INTERVAL '5' SECOND  -- 在eventTime上定义watermark
) WITH (
    'connector'='kafka',
    'topic'='user_behavior',
    'properties.bootstrap.servers'='localhost:9092',
    'scan.startup.mode'='group-offsets',
    'properties.group.id'='user_behavior_group',
    'properties.fetch.max.bytes'='5242880',
    'properties.allow.auto.create.topics'='false',
    'properties.enable.auto.commit'='true',
    'format'='json',
    'properties.auto.offset.reset'='earliest'
);
```



### 3. Join

```sql
SELECT
  u.user_id, 
  u.item_id,
  u.cat_id,
  u.action,  
  p.field.province_id,
  p.field.province_name,
  p.field.region_name
FROM user_behavior AS u LEFT JOIN dim_province_hbase FOR SYSTEM_TIME AS OF u.proctime AS p
ON cast(u.province as STRING) = p.rowkey;
```



