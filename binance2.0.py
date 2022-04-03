from bs4 import BeautifulSoup
from send_email import send_email
import urllib.request, urllib.error
from time import sleep
#重新换了个网站实时更新

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



if __name__=="__main__":

    detect(is_instant=True)
    while True:
        detect()

    # all,is_send=cap_information()
    # print(all)
    # if is_send:
    #     send_email(str(all))

