import sqlite3
import random
import datetime

conn = sqlite3.connect('movieinfo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS members(id text, pwd text, age text, call text)''')
c.execute('''CREATE TABLE IF NOT EXISTS ticket(id text, name text, date text, hall text)''')

movielist = {"1":"어벤져스: 인피니티 워", "2":"블랙팬서", "3":"쥬라기 원드: 폴른 킹덤", "4":"인크레더블2", "5":"데드풀2", "6":"레디 플레이어 원"
            ,"7":"오퍼레이션 레드 씨", "8":"앤트맨과 와스프", "9":"당인가탐안2", "10":"미션임파서블"}
moviemoney = {1:10000, 2:10000, 3:10000, 4:10000, 5:10000, 6:10000, 7:10000, 8:10000, 9:10000,
            10:10000, }

def login(id, password):
    print("")
    c.execute("SELECT * FROM members WHERE id = '%s' and pwd = '%s'" % (id, password))
    look = c.fetchone()
    if (look != None):
        return True
    else:
        return False

def intomember():
    while True:
        print("회원가입을 시작합니다..")
        id = input("사용하실 아이디를 입력해주세요: ")
        password = input("사용하실 비밀번호를 입력해주세요: ")
        age = int(input("당신의 나이를 입력해주세요: "))
        call = int(input("당신의 연락처를 입력해주세요(-빼고 숫자만 입력해주세요): "))
        c.execute("SELECT * FROM members WHERE id = '%s'" % id)
        look = c.fetchone()
        if (look != None):
            print("\n이미 사용중인 아이디 입니다.\n")
            a = input("다시 하시겠습니까?(y/n)")
            if a == 'y':
                continue
            else:
                break
        else:
            c.execute('''INSERT INTO members VALUES('%s', '%s', '%s', '%s')''' % (id, password, age, call))
            conn.commit()
            print("\n축하합니다! %s 님의 아이디가 생성되었습니다!\n" % id)
            break

def printlist(a):
    global movielist
    if str(a) == str(1):
        print("| 1.로그인 | 2.회원가입 | 3.프로그램 종료 |\n")
    if str(a) == str(2):
        print("| 1.영화 예매 | 2.영화 예매 취소 | 3.내가 예매한 영화 보기 | 4.로그아웃 | 5.회원정보 변경 |")
    if str(a) == 'movie':
        print(movielist)

def movieticket(username):
    global movielist
    global moviemoney
    printlist('movie')
    ticket = input("무엇을 보시겠습니까?: ")
    if int(ticket) == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10:
        select = movielist[str(ticket)]
        c.execute("SELECT * FROM ticket WHERE id = '%s' and name = '%s'" % (username, select))
        look = c.fetchone()
        if (look == False):
            a = input("정말로 %s 를 보시겠습니까?(y/n)" % select)
            if a == 'y':
                return_money = 0
                if ticket in movielist:
                    money2 = 0
                    money = moviemoney[int(ticket)]
                    print("%s 원 입니다."%(money))
                    pay_money = input("돈을 내주세요: ")
                    money2 += int(pay_money)
                    while(1):
                        if int(money2) >= int(money):
                            random1 = random.randint(1,10)
                            return_money = int(money2) - int(money)
                            print("거스름돈은 %d 원 입니다."%(return_money))
                            c.execute('''INSERT INTO ticket VALUES('%s', '%s', '%s', '%s')''' % (username, select, datetime.datetime.now(), random1))
                            conn.commit()
                            print("%s 를 예매하셨습니다. %d 관으로 오세요\n" % (select, random1))
                            break
                        else:
                            print("%d 원중에 %d 원을 넣으셨습니다."%(money, money2))
                            pay_money = input("돈을 더 내주세요: ")
                            money2 += int(pay_money)
                else:
                    print("그런 영화는 없습니다.")
        else:
            print("이 영화는 이미 예약하셨습니다.")
    else:
        print("그런 영화는 없습니다.")

def seemymovie(username):
    print("==============================")
    c.execute("SELECT * FROM ticket WHERE id = '%s'" % (username))
    look = c.fetchone()
    if (look == None):
        print("==없음==")
    else:
        c.execute("SELECT * FROM ticket WHERE id = '%s'" % (username))
        looks = c.fetchall()
        for look in looks:
            print("123123")
            print(looks)
    print("==============================")

# def cancel(username):
#
# def changeaccount(username):

print("안녕하세요?\n영화 예매 프로그램입니다.\n")
while True:
    printlist(1)
    user = input("원하시는 서비스 번호를 입력해주세요: ")
    print("")
    if int(user) == int(1):
        id = input("당신의 아이디를 입력해주세요: ")
        password = input("당신의 비밀번호를 입력해주세요: ")
        if login(id, password) == True:
            print("로그인 되었습니다.")
            print("안녕하세요 %s 님?\n" % id)
            while True:
                printlist(2)
                print("")
                collect = input("원하시는 서비스 번호를 입력해주세요: ")
                if int(collect) == int(1):
                    movieticket(id)
                # if int(collect) == int(2):
                elif int(collect) == int(3):
                    seemymovie(id)
                else:
                    print("잘못입력하셨습니다.")
        else:
            print("아이디나 비밀번호가 일치하지 않습니다.\n")
    elif int(user) == int(2):
        intomember()
    elif int(user) == int(3):
        exit(1)
    else:
        print("잘못입력하였습니다.")
