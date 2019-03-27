---
layout: post
title: FTP多线程批量文件下载

date: 2018-04-25 00:00:00
categories: 后端
tags: FTP
---

最近接到个业务需要使用FTP拉取服务器上数据。要求可以任意指定下载对应目录数据，并且目录结构保持要。处理的数据文件特点分散而且很大。处理的思路大概有两个，一个是在服务端压缩成zip，然后传过来。二是使用多线程单个单个文件传输。在这里我使用的是第二中方法。

----------

## 思路
1.服务端提供一个返回指定文件下的`List<String> files`

2.客户端拿到files文件列表，遍历单个单个文件请求服务端拉取数据

## FTP下载使用

```java

public static boolean downloadFromFtp(String middlePath, String fileName, String localPath) throws IOException {

        return downloadFromFtp(url, port, username, password,middlePath, fileName, localPath);
    }

    public static boolean downloadFromFtp(String url, int port, String
            username, String password, String path, String fileName, String localpath) throws IOException {
        boolean flag = false;
        FTPClient ftp = new FTPClient();//org.apache.commons.net.ftp
        int reply;
        try {
            if (port > -1) {
                ftp.connect(url, port);
            } else {
                ftp.connect(url);//ftp默认的端口是21
            }
            //很多人写的是用ftp.getReplyCode()给获取连接的返回值,但是这样会导致storeFileStream返回null
            ftp.login(username, password);
            ftp.enterLocalActiveMode();
            ftp.setFileType(FTPClient.BINARY_FILE_TYPE);
            reply = ftp.getReplyCode();
            if (!FTPReply.isPositiveCompletion(reply)) {
                ftp.disconnect();
                return flag;
            }
            //切换目录 此处可以判断,切换失败就说明ftp上面没有这个路径
            ftp.changeWorkingDirectory(path);
            //上传文件
            OutputStream out = null;
            InputStream in = null;
            //创建本地的文件时候要把编码格式转回来
            File localDir = new File(localpath +"/" + path);
            if(!localDir.exists()){
                localDir.mkdirs();
            }
            fileName = new String(fileName.getBytes("ISO-8859-1"), "utf-8");
            File localFile = new File(localpath + "/" + path + "/" + fileName);
            out = new FileOutputStream(localFile);
            //ftp.enterLocalPassiveMode();
            in = ftp.retrieveFileStream(fileName);
            byte[] byteArray = new byte[4096];
            int read = 0;
            while ((read = in.read(byteArray)) != -1) {
                out.write(byteArray, 0, read);
            }
            //这句很重要 要多次操作这个ftp的流的通道,要等他的每次命令完成
            ftp.completePendingCommand();
            out.flush();
            out.close();
            ftp.logout();
            flag = true;
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (ftp.isConnected()) {
                ftp.disconnect();
            }
        }
        return flag;
    }

```

downloadFromFtp传入参数说明String 
<table>
<tr>
    <td>参数</td>
    <td>解释</td>
</tr>
<tr>
    <td>url</td>
    <td>ftp的ip地址</td>
</tr>
<tr>
    <td>port</td>
    <td>ftp的端口(默认21)</td>
</tr>
<tr>
    <td>usernameport</td>
    <td>ftp用户名</td>
</tr>
<tr>
    <td>password</td>
    <td>ftp密码</td>
</tr>
<tr>
    <td>path</td>
    <td>特别重要，一开报输入流为null就是因为它写错了;假如你的ftp根目录为C:/ftp/,你想要下载C:/ftp/xxx/下的文件,那么path就要写xxx/</td>
</tr>
<tr>
    <td>fileName</td>
    <td>下载文件的名称</td>
</tr>
<tr>
    <td>localpath</td>
    <td>下载到本地的路径</td>
</tr>
</table>

## server返回制定文件列表

用户给定一个path，查处path下所有的文件，放在list，以json形式返回。
```java
    // 递归查询所有的文件
    public ArrayList listFiles(String path,ArrayList files){
        File directory = new File(path);
        File[] currentFiles = directory.listFiles();
        for (File file:currentFiles) {
            if (file.isDirectory()){
                listFiles(file.getPath(),files);
            }else{
                files.add(file);
            }
        }
        return files;
    }
```

## client获取返回列表下载文件

四类线程池基本的线程池概述，这边按需求选择，我这里选了定长线程池FixedThreadPool
* FixedThreadPool 定长的线程池，初始化时指定线程的个数，当线程池中线程被用完时，其他任务阻塞等待
* CachedThreadPool 不定长线程池，无限扩大的线程池，来几个任务分配几个线程。
* SimpleThreadPool 单例线程，底层采用LinkedBlockQueue实现，除了排在队列最前面的线程以外的其他线程都要等着。
* ScheduleThreadPol 在初始化时可以指定时间帮助我们处理延时任务和定时任务。


客户端的思路:
1.使用HttpClient从后台发送请求获取待下载files列表
2.将DownloadThread分配给FixedThreadPool运行

这边主要看DownloadThread.java如何编写，以及如何分配给fixedThreadPool

DownloadThread.java
```java
package com.bim.task;

import com.bim.common.FtpUtils;

import java.util.List;

public class DownLoadThread implements Runnable {

    List files = null;
    String ftpPath = null;
    String baseLocalPath = null;

    public  DownLoadThread(List files,String ftpPath,String baseLocalPath){
        this.files = files;
        this.ftpPath = ftpPath;
        this.baseLocalPath = baseLocalPath;
    }

    // 下载文件的具体业务
    // ftpPath ftp地址（c:/ftp）
    // baseLocalPath 目标地址
    private void downloadFile(String file,String ftpPath,String baseLocalPath) throws Exception{
        String dllPath = file.toString().replaceAll("\\\\","/");
        int lastIndexOf = dllPath.lastIndexOf("/");
        String middlePath = "/";
        if(ftpPath.length() - 1 <= lastIndexOf){
            middlePath = dllPath.substring(ftpPath.length(),lastIndexOf+1);
        }
        String fileName = dllPath.substring(lastIndexOf + 1,dllPath.length());
        System.out.println("filename" + fileName);
        System.out.println("baseLocalPath" + baseLocalPath);
        System.out.println("开始下载:" + middlePath + fileName + "到本地" + baseLocalPath);
        // 调用ftp下载文件
        FtpUtils.downloadFromFtp(middlePath,fileName,baseLocalPath);
        System.out.println(middlePath + fileName + "下载成功");

    }
    
    @Override
    public void run() {
        try{
            while(!files.isEmpty()){
                String file = null;
                synchronized(files){
                    file = (String) files.get(0);
                    files.remove(0);
                }
                downloadFile(file,ftpPath,baseLocalPath);
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

主程序拿到files后的逻辑代码部分
```java
public class PullFileClient {
     private static ExecutorService fixedThreadPool = Executors.newFixedThreadPool(10);
    
     public static void main(String[] args) throws IOException {

        Map<String,Object> resultMap = client.sendGet(requestUrl);
        Object code = resultMap.get("code");
        // 获取文件列表数据
        List files = (List) resultMap.get("data");
        // ftp的根目录 (c:/ftp)
        String ftpPath = "c:/FTP/";
        String baseLocalPath = "/home/zyh/Documents/tmp4/";
        fixedThreadPool.execute(new DownLoadThread(files,ftpPath,baseLocalPath));
        fixedThreadPool.shutdown();
    }
    
}
```