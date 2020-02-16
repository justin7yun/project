#_*_ coding: utf-8 _*_
import re
import numpy as np
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('TestHistory.json', scope)
client = gspread.authorize(creds)

sheet = client.open('LawCode').sheet1
testhistory = sheet.get_all_records()

# rletTypeCd: A01=아파트, A02=오피스텔, B01=분양권, 주택=C03, 토지=E03, 원룸=C01, 상가=D02, 사무실=D01, 공장=E02, 재개발=F01, 건물=D03
# tradeTypeCd (거래종류): all=전체, A1=매매, B1=전세, B2=월세, B3=단기임대
# hscpTypeCd (매물종류): 아파트=A01, 주상복합=A03, 재건축=A04 (복수 선택 가능)
# cortarNo(법정동코드): (예: 1168010600 서울시, 강남구, 대치동)
# A01%3AA03%3AA04
# C02%3AC03%3AC04%3AC06
def get_naver_realasset(area_code, npage=1):
    url = 'http://land.naver.com/article/articleList.nhn?' \
        + 'rletTypeCd=C03&tradeTypeCd=all&hscpTypeCd=C02%3AC03%3AC04%3AC06' \
        + '&cortarNo=' + str(area_code) \
        + '&page=' + str(npage)
    print(url)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    table = soup.find('table')
    trs = table.tbody.find_all('tr')
    if '등록된 매물이 없습니다' in trs[0].text:
        return pd.DataFrame()
    
    value_list = []

    # 거래, 종류, 확인일자, 매물명, 면적(㎡), 층, 매물가(만원), 연락처
    for tr in trs[::2]:
        tds = tr.find_all('td')
        cols = [' '.join(td.text.strip().split()) for td in tds]

        if '_thumb_image' not in tds[3]['class']: # 현장확인 날짜와 이미지가 없는 행
            cols.insert(3, '')

        # print(cols)
        거래 = cols[0]
        종류 = cols[1]
        확인일자 = datetime.strptime(cols[2], '%y.%m.%d.')
        현장확인 = cols[3]
        매물명 = cols[4]
        면적 = cols[5]
        공급면적 = 0
        전용면적 = 0
        if len(re.findall('대지면적(.*?)㎡', 면적)) > 0:
            공급면적 = re.findall('대지면적(.*?)㎡', 면적)[0].replace(',', '')
        if len(re.findall('연면적(.*?)㎡', 면적)) > 0:
            전용면적 = re.findall('연면적(.*?)㎡', 면적)[0].replace(',', '')
        공급면적 = float(공급면적)
        전용면적 = float(전용면적)
        층 = cols[6]
        if cols[7].find('호가일뿐 실거래가로확인된 금액이 아닙니다') >= 0:
            pass # 단순호가 별도 처리하고자 하면 내용 추가
        # print(cols[7].split('/')[0].split(' ')[0].replace(',', ''))
        매물가 = int(cols[7].split('/')[0].split(' ')[0].replace(',', '')) 
        연락처 = cols[8]
        
        if 종류 != '전원주택':
            continue
        if 매물가 > 10000:
            continue
        value_list.append([거래, 종류, 확인일자, 현장확인, 매물명, 공급면적, 전용면적, 층, 매물가, 연락처])
        
    cols = ['거래', '종류', '확인일자', '현장확인', '매물명', '공급면적', '전용면적', '층', '매물가', '연락처']
    df = pd.DataFrame(value_list, columns=cols)

    return df

if __name__ == "__main__":
    area_code = '1168010600' # 강남구, 대치동 (법정동 코드 https://goo.gl/P6ni8Q 참조)

    df = pd.DataFrame()
    while True:
        # for p in range(4173025021, 4173038031): # 최대 100 페이지
        search0 = input('Level0?')
        search1 = input('Level1?')
        search2 = input('Level2?')
        if search0 == 'q':
            break
        for testh in testhistory:
            if (search0=='' or (search0 in testh['Level0'])) and (search1=='' or (search1 in testh['Level1'])) and (search2=='' or (search2 in testh['Level2'])):
                area_code = testh['Level7']
                if area_code == '':
                    continue
                # print('area_code', area_code)
                for i in range(1,3):
                    # print(i)
                    df_tmp = get_naver_realasset(area_code, i)
                    time.sleep(1)
                    if len(df_tmp) <= 0:
                        break
                    df = df.append(df_tmp, ignore_index=True)
                    print('Page %d appended.' % i)
        # print(len(df))
        for i in range(0,len(df)):
            #cols = ['거래', '종류', '확인일자', '현장확인', '매물명', '공급면적', '전용면적', '층', '매물가', '연락처']
            print(df.iloc[i]['거래'], df.iloc[i]['종류'], df.iloc[i]['확인일자'], df.iloc[i]['현장확인'], df.iloc[i]['매물명'], df.iloc[i]['공급면적'], \
            df.iloc[i]['전용면적'], df.iloc[i]['층'], df.iloc[i]['매물가'], df.iloc[i]['연락처'])

        # df = get_naver_realasset('4173025021', 1) # 60 페이지
        # print(df)