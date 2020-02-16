import requests
from  bs4 import BeautifulSoup

def spider(max_pages):
    page=1
    while page < max_pages:
        url='http://creativeworks.tistory.com/'+str(page)
        source_code=requests.get(url)
        plain_text=source_code.text
        soup=BeautifulSoup(plain_text,'lxml')
        # print(soup)
        for link in soup.select('a'):
            href="http://creativeworks.tistory.com"+link.get('href')
            title=link.string
            print(href)
            print(title)
        page +=1

spider(2)