# -*- coding: utf-8 -*-

import requests
import urllib
import re
import uuid
import os


file_download_path = 'D:\\uploadImg\\img'
post_path = 'E:\\Workspaces\\github\\blog\\source\\_posts'

# 上传file到sm网站
def to_sm(file):
    url = 'https://sm.ms/api/upload'
    file={'smfile':file}
    result = requests.post(url,data=None,files=file)
    dict_result = result.json()
    code = dict_result['code']
    url = ''
    if 'success' == code:
        url = dict_result['data']['url']
    else:
        print(dict_result)
        url = 'zyhuploaderror123'
    
    return url
    

# 使用正则找到文章中所有的图片,剔除i.loli.net的
def find(contents):
    result = re.sub('[a-zA-z]+://[ww1][^\s]*\.jpg',replace,contents)
    #print(result)
    return result

def random():
    return str(uuid.uuid4()).replace('-','')

def download(url):
    # 获取后缀
    file_suff = url.split('.')[-1]
    # 随机生成名字
    filename = random() +'.'+ file_suff
    # 获取绝对路径
    real_path = file_download_path + '/' + filename
    # 存到本地
    urllib.request.urlretrieve(url,real_path)
    return real_path

# 替换匹配的url
def replace(re_obj):
    url = re_obj.group()
    print('匹配到待替换路径%s' % url)
    # 下载到本地
    real_path = download(url)
    print('将其下载到本地%s' % real_path)

    # 上传到sm服务器
    new_url = ''
    with open(real_path,'rb') as file:
        #new_url = url + 'zyh123'
        new_url = to_sm(file)
        if 'zyhuploaderror123' == new_url:
            print("-------%s 上传SM失败，不进行替换---------" % url)
            new_url = url
        else:
            print('上传到sm服务器,新的url为%s' % new_url)
        
    return new_url
    
# 清空文件
def set_empty(file):
    file.seek(0)
    file.truncate()

# 从文件中读取数据
def read(path):
    with open(path,'r+', encoding='UTF-8') as file:
        # 读数据到Contents
        contents = file.read().rstrip()
        # 删除尾部空格
        #print(contents.rstrip()) 
        newContents = find(contents)
        set_empty(file)
        file.write(newContents)

# 测试下载
def test_download():
    url = 'http://ww1.sinaimg.cn/large/0066vfZIgy1fpgvn41tp7j30q30tq4qp.jpg'
    real_path = download(url)
    print(real_path)        

# 测试上传sm
def test_to_sm():
    new_url = 'zyhuploaderror'
    with open('/home/zyh/projects/spider/img/fe52bb737dd54edbaea137fde0d7ba64.jpg','rb') as file:
        #new_url = url + 'zyh123'
        new_url = to_sm(file)
    print(new_url)

if __name__ =='__main__':

    files_path = os.listdir(post_path)
    for path in files_path:
        deal_post = post_path + "/" + path
        print("开始处理%s" % deal_post)
        read(deal_post)


    
    
    
    
    


