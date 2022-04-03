﻿

@[TOC](文章目录)

---

# 前言

之前买了2000块钱的数字货币包括狗狗币和shi币，但是每天要花很多时间去关注数字货币的涨停情况，为此感到很烦恼，于是自己写了代码挂在服务器上跑，能够每隔一个小时去爬取我关注的数字货币信息，若涨跌情况较大则发送邮件到我QQ邮箱，每天也会发邮件告知我涨跌情况，为此节约了很多时间。

在此，将我的创作过程和代码分享出来，希望能够帮助有类似烦恼的朋友。



---


# 一、下载需要的python第三方库

## 1. Beautifulsoup4 
安装：`pip install Beautifulsoup4`

Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库。它通过转换器实现文档导航,查找,修改文档的方式，最大的特点就是简单易用，不像正则和 xPath 需要刻意去记住很多特定语法。

## 2.Smtplib
安装：`pip install py-emails`

smtplib是一个 Python 库，用于使用简单邮件传输协议（SMTP）发送电子邮件。


## 3.Email
安装：`python3自带，不需要额外安装`

电子邮件包是一个用于管理电子邮件消息的库。它的特殊设计不用于向SMTP (RFC 2821)、NNTP或其他服务器发送任何电子邮件消息;这些是模块的函数，如smtplib和nntplib。

---

# 二、申请额外的邮箱
## 1.注册一个网易邮箱
网易邮箱:[官网](https://mail.163.com/)

注册一个邮箱，用其他邮箱也行。
		
## 2.开通电子邮箱的SMTP功能
登录后选择设置 $\rightarrow$POP3/SMTP/IMAP$\rightarrow$开启服务
![在这里插入图片描述](https://img-blog.csdnimg.cn/9ed891638a7e4303a6dbdc9c9e2b1171.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)

点击开启两个SMTP服务，发送短信后，转到以下界面:
![在这里插入图片描述](https://img-blog.csdnimg.cn/b5f18a90a9d84fb6be636e63b356eb18.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
记录授权密码后，点击确定，对于POP3/SMTP服务也进行一样的操作。


---

# 三、代码实现
## 1.发送邮件模块
### 1.1 导入三方库
````python
from selenium import webdriver
from PIL import Image
from aip import AipOcr
import time
````
### 1.2 编写发送函数
````python
def send_email(content):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'
    #163用户名
    mail_user ='邮箱名(@前面部分)'
    #密码(部分邮箱为授权码)
    mail_pass = '之前的授权密码'
    #邮件发送方邮箱地址
    sender = 'xxxx@163.com'
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['xxxx@qq.com']

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题
    message['Subject'] = '数字货币信息'

    #发送方信息
    message['From'] = sender
    #接受方信息
    message['To'] = receivers[0]

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass)
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        #退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
````
将该函数写入到send_email.py文件中，为后面做准备。
## 2.爬虫模块
### 2.1 导入三方库
````python
from bs4 import BeautifulSoup
from send_email import send_email
import urllib.request, urllib.error
from time import sleep
````
其中send_mail是刚刚写的py文件，也可以将send_email函数写到同一个py文件中，则不用引入了。
### 2.2 获取HTML内容
本次所选用网站为[比特币中文网](https://www.ibtctrade.com/cryptocurrency)，其中包含了各种数字货币的信息以及涨跌情况。获取网页HTML内容函数如下:
````python
def askURL(url):
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
    request=urllib.request.Request(url,headers=head)
    html_content=0
    try:
        response=urllib.request.urlopen(request)
        html_content=response.read().decode('utf-8')
        # print(html_content)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html_content
````
输入为网址url，其中
````python
head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
````
在连接网页时很重要，绝大部分网站都会拒绝爬虫的访问，而加个head可以伪装，该函数的返回值为网页的HTML内容。


### 2.3 从HTML内容获取信息
首先到网页上，查看信息，到[比特币中文网](https://www.ibtctrade.com/cryptocurrency)，按F12，再选取元素，我们这里选择狗狗币，得到结果如下:
![在这里插入图片描述](https://img-blog.csdnimg.cn/b14ddb88f564416ca2e4d3c9468fdc3e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
可以看到，不同的数字货币的信息根据标签`a`的herf属性来区分狗狗币的`herf`属性为`herf='/trade/doge`,而查看shib的`herf`属性为`herf='/trade/shib`,在继续查看其他数字货币的`herf`属性，发现都是`herf='/trade/币名`。

为此我们可以根据不同的`herf`属性来获取不同数字货币的信息。

下面我们来从HTML内容中来获取信息，首先将获得HTML内容利用BeautifulSoup来解析:
````python
soup = BeautifulSoup(html_content, "html.parser")
````
之后在根据不同币名，来获得`a`标签的`herf`的不同属性，根据属性来获取关于该数字货币的全部信息:
````python
tags="/trade/"+currency_name
all_content=soup.find('a',href=tags)
````
到此，我们已经获取想要的数字货币的全部信息，但我只想要它的名称、价格、24小时涨跌情况和交易情况，为此我们进一步进行分析，按F12选取货币的名字:
![在这里插入图片描述](https://img-blog.csdnimg.cn/87b82ee213944317b5a628d3a7accee8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
发现定位到了一个`strong`标签处，为此我们在之前获取的狗狗币所有信息中找寻`strong`标签即可获取名称:
````python
name=all_content.find('strong').string.strip()
````
下一步继续分析发现，其他的信息都在`li`标签中：
![在这里插入图片描述](https://img-blog.csdnimg.cn/934e8ac66d664c0bad3175332b731816.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_17,color_FFFFFF,t_70,g_se,x_16)
分析发现第一个`li`标签的信息是排名信息，我们不需要跳过，第二个`li`标签中的信息是名称和图标信息，我们已经获取名称所以也不需要。第三、四、五个`li`标签分别是价格信息、涨跌信息、交易信息，这些是我们需要的，为此我们可以采用一个循环来获取:
````python
    contents=all_content.find_all('li')
    price = 0
    change_24h = 0
    trade_24h = 0
    for i,change in enumerate(contents):
        if i==0:
            pass
        elif i==2:
            price=change.string.strip()
        elif i==3:
            change_24h = change.string.strip()
        elif i==4:
            trade_24h=change.string.strip()

    all_info=[name,price,change_24h,trade_24h]
````
到此我们获取我们想要的全部信息。
整体函数如下:
````python
    def getData(currency_name,url='https://www.ibtctrade.com/cryptocurrency'):
    datalist=[]
    html_content= askURL(url)  # 保存网页源码
    # 逐一解析

    # print(html_content)
    is_send=False
    tags="/trade/"+currency_name
    soup = BeautifulSoup(html_content, "html.parser")
    all_content=soup.find('a',href=tags)
    name=all_content.find('strong').string.strip()
    contents=all_content.find_all('li')
    price = 0
    change_24h = 0
    trade_24h = 0
    for i,change in enumerate(contents):
        if i==0:
            pass
        elif i==2:
            price=change.string.strip()
        elif i==3:
            change_24h = change.string.strip()
            x = float(change_24h.split('%')[0])
            if x>=3 or x<=-3:
                is_send=True
        elif i==4:
            trade_24h=change.string.strip()

    all_info=[name,price,change_24h,trade_24h]
    return all_info,is_send
````
其中加了一个`is_send`用来决定是否发送邮件，当24h涨跌超过3%则发送邮件进行提醒。

### 2.4 定时爬取
````python
#每一个小时看一次，12个小时发送一次
def detect(time=1*60*60,is_instant=False):

    doge_name ='doge'
    shib_name ='shib'
    if is_instant:
        shib_info, shib_send = getData(shib_name)
        doge_info, doge_send = getData(doge_name)
        all_info =str(['name', 'price', '24h_change','24h_trade'])
        all_info+='\n'+str(doge_info)
        all_info+='\n'+str(shib_info)
        send_email(all_info)
    else:
        sleep(time)
        shib_info, shib_send = getData(shib_name)
        doge_info, doge_send = getData(doge_name)
        if shib_send or doge_send:
            all_info = str(['name', 'price', '24h_change', '24h_trade'])
            all_info += '\n' + str(doge_info)
            all_info += '\n' + str(shib_info)
            send_email(all_info)
````
该函数输入`time`表示检测间隔时间，默认为1个小时，`is_instant`表示是否立即检测并发送邮件。
最后只需利用死循环，在服务器上一直跑`detect()`函数即可。


---


# 总结
以上就是今天要讲的内容，本文介绍了利用python爬虫来获取数字货币信息，并利用python发送邮件到邮箱。



