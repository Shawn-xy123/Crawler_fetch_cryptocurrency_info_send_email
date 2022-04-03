import smtplib
# from email.mime.text import MIMEText
from email.mime.text import MIMEText

#reference:https://zhuanlan.zhihu.com/p/24180606
def send_email(content):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'
    #163用户名
    mail_user = '@前面部分'
    #密码(部分邮箱为授权码)
    mail_pass = 'xxxx'
    #邮件发送方邮箱地址
    sender = 'xxxx@163.com'
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['xxxx@qq.com']

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题
    message['Subject'] = 'Binance'

    #发送方信息
    message['From'] = sender
    #接受方信息
    message['To'] = receivers[0]

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP_SSL(host=mail_host)
        #连接到服务器
        smtpObj.connect(mail_host,465)
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

if __name__=="__main__":
    w=['name', 'price', '24_change', '7d_change']
    w=str(w)
    send_email(w)