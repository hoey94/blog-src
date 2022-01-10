----



title: FlinkDataStream Kafka2ES
date: 2022年01月10日10:18:26

----




```java
package Kafka2ES

import java.util

import org.apache.flink.api.common.functions.RuntimeContext
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.connectors.elasticsearch.{ElasticsearchSinkFunction, RequestIndexer}
import org.apache.flink.streaming.connectors.elasticsearch6.ElasticsearchSink
import org.apache.http.HttpHost
import org.elasticsearch.action.update.UpdateRequest
import org.elasticsearch.script.{Script, ScriptType}

case class Message(id: String, para_name: String, para_val: String)

object Demo1 {
  
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)

    val dataList = List(
      "MSG_001,id,sensor1"
//      "MSG_001,timestamp,1603766281"
//      "MSG_001,temperature,56",
//      "MSG_002,id,sensor2",
//      "MSG_002,timestamp,1603766282",
//      "MSG_002,temperature,57",
//      "MSG_003,id,sensor3",
//      "MSG_003,timestamp,1603766283",
//      "MSG_003,temperature,58",
//      "MSG_004,id,sensor4",
//      "MSG_004,timestamp,1603766284",
//      "MSG_004,temperature,59"
    )

    //Source操作
    val inputStream = env.fromCollection(dataList)

    val dataStream: DataStream[Message] = inputStream.map(row => {
      val lines = row.split(",")
        // 匹配
      Message(lines(0),lines(1),lines(2))
    })

    val httpHosts = new util.ArrayList[HttpHost]()
    httpHosts.add(new HttpHost("127.0.0.1", 9200))
    //创建一个ES Sink的builder
    val esSinkBuilder: ElasticsearchSink.Builder[Message] = new ElasticsearchSink.Builder[Message](
      httpHosts,
      new ElasticsearchSinkFunction[Message] {
        override def process(t: Message, runtimeContext: RuntimeContext, requestIndexer: RequestIndexer): Unit = {
          println("saving data:" + t)

          //包装成一个Map或者JsonObject格式
          val json = new util.HashMap[String, String]()
          val mesId = t.id
          var id = "";
          var timestamp = "";
          var temperature = "";
          if(t.para_name.equals("timestamp")){
            timestamp = t.para_val
            json.put("timestamp",timestamp)
  
          }
  
          if(t.para_name.equals("temperature")){
            temperature = t.para_val
            json.put("temperature",temperature)
  
          }
  
          if(t.para_name.equals("id")){
            id = t.para_val
            json.put("id",id)
          }


          //创建indexRequest准备发送数据
//          val indexRequest = Requests.indexRequest()
//            .index("ames_1")
//            .`type`("readingdata")
//            .id(mesId)
//            .source(json)
  
          val updateRequest = new UpdateRequest("ames_1", "readingdata", mesId).doc(json);
          updateRequest.docAsUpsert(true);
          
          //利用requestIndexer进行发送请求，写入数据
          requestIndexer.add(updateRequest)
          println("data 写入完成。。。")
        }
      }
    )


    //Sink操作
    dataStream.addSink(esSinkBuilder.build())

    env.execute("sink ES test")
  }
  
  
  
}
```