#_*_ coding: utf-8 _*_
from bs4 import BeautifulSoup
import requests

strFirst = ''
# web_url에 원하는 웹의 URL을 넣어주시면 됩니다.
def trade_spider(abc,num):
    page=1
    global strFirst
    while page <= max_pages:
        url = 'https://comcream.x-y.net/iot/setpoint.php?id=justin&point=' % (abc,page)
        source_code = requests.get(url)
        plaint_text = source_code.text
        soup = BeautifulSoup(plaint_text,'html.parser')
        nameList = soup.find_all('a',{'class':'fnt15'})
        if len(nameList) > 0:
            if strFirst == nameList[0]:
                break
            strFirst = nameList[0]
        for name in nameList:
            strname = name.get_text()
            aName = strname.split(' ')
            sName = aName[0]
            if sName[-1] == '다':
                continue
            print(aName[0])
        page+=1
        #print (page)

if __name__ == '__main__':
    while True:
        strWord = input('끝말 잇기 게임: 입력 하세요.')
        trade_spider(100, strWord[-1])
