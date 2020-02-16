#_*_ coding: utf-8 _*_
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

aaa=0

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('TestHistory.json', scope)
client = gspread.authorize(creds)

sheet = client.open('MathContents').sheet1
testhistory = sheet.get_all_records()

MIN_PERIODIC = 99
total = len(testhistory)
#print(total)
point=0

def showList(Key,conditionKey,conditionValue,bQ):
    nIndex=0
    aRoot = []
    temp=''
    global point
    for testh in testhistory:
        if testh[Key] == '':
            continue
        if temp==testh[Key]:
            continue
        if conditionKey != '':
            if testh[conditionKey] != conditionValue:
                continue
        nIndex+=1
        aRoot.append(testh[Key])
        temp=testh[Key]
        if aaa == int(0):
            print('정답', '[',nIndex,']: ', testh[Key]) 
            print('')
        if bQ == True:
            strInput = '[' + str(nIndex) + '] ?'
            strQ = input(strInput)
            if strQ == testh[Key]:
                point = point + 1000
                print('You get the %d point^^' % point)
        print('')
        print('[',nIndex,']: ', testh[Key])
        print('')
    return aRoot

if __name__ == "__main__":
    while True:
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('1. Root\n2. Second\n3. Third\n4. Quit')
        search = input("Which one?")
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        if search == '4':
            break
        if search == '1':
            showList('WideCategory','','',True)
        elif search == '2':
            aaa = 1
            aFirst = showList('WideCategory','','',False)
            search2 = input("Which one?")
            print('2 Level: ', aFirst[int(search2)-1]) 
            aaa=0
            showList('MiddleCategory','WideCategory',aFirst[int(search2)-1],True)
        elif search == '3':
            aaa = 1
            aFirst = showList('WideCategory','','',False)
            search2 = input("Which one?")
            print('2 Level: ', aFirst[int(search2)-1])
            aSecond = showList('MiddleCategory','WideCategory',aFirst[int(search2)-1],)
            search3 = input("Which one?")
            print('3 Level: ', aSecond[int(search3)-1])
            aaa = 0
            showList('SmallCategory','MiddleCategory',aSecond[int(search3)-1],True)
    print('You got %d points.' % point)
    if (point/total*100) < int(20):
        print('좀더 힘네세요.')
    elif (point/total*100) > int(20):
        print('잘하고 있어요.')
    elif (point/total*100) > int(40):
        print('좀 하는데요.')
    elif (point/total*100) > int(60):
        print('가능성이 있습니다.')
    elif (point/total*100) > int(80):
        print('상당한 실력입니다.')
    elif (point/total*100) > int(95):
        print('완벽합니다.')
