# -*- coding: utf-8 -*-

# http://stu.AAA.go.kr/ 관할 교육청 주소 확인해주세요.
# schulCode= 학교고유코드
# schulCrseScCode= 1유치원2초등학교3중학교4고등학교
# schulKndScCode= 01유치원02초등학교03중학교04고등학교

# http://stu.kwe.go.kr/sts_sci_sf00_001.do      year list
# grade 2018
# schulCrseScCode=2
# term  1 = 1학기

# http://stu.kwe.go.kr/sts_sci_sf01_001.do      monthly list
# grade 2018
# schulCrseScCode=2
# month=03

# =================================================

# 음성인식, 크롤링, 현재시각 관련 임포트하기
import speech_recognition as sr
import requests
import re

# 크롤링
from bs4 import BeautifulSoup

# 현재 날짜가져오기
from datetime import datetime

# 렌덤 임포트
import random


# ==================================================
username = {'윤준영': 'K100001373', '김하율': 'K100003819',
            '정준섭': 'K100001354', '장정현': 'K100003714'}
# 변수 지정
requestToday = datetime.today()
requestYear = datetime.today().year
requestMonth = datetime.today().month
requestDay = datetime.today().day
requestWeekDay = datetime.today().weekday()
Today = datetime.today()
Year = datetime.today().year
Month = datetime.today().month
Day = datetime.today().day
WeekDay = datetime.today().weekday()
myWord = ' '
monday = {"1": "체육", "2": "수학", "3": "과학", "4": "국어", "5": "영어"}
tuesday = {"1": "수학", "2": "수학", "3": "체육", "4": "영어", "5": "과학"}
wednesday = {"1": "수학", "2": "영어", "3": "음악", "4": "과학", "5": "과학"}
thursday = {"1": "과학", "2": "과학", "3": "미술", "4": "미술", "5": "사회"}
friday = {"1": "사회", "2": "수학", "3": "도덕", "4": "영어", "5": "국어"}
say1 = ' '

while(1):
    input("당신의 이름은 무엇입니까? 엔터를 누르고 말씀하세요")
    name = ' '
    # 오디오 초기화하기
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("listening...")
        audio = r.listen(source)
        print("listening finish...")

    try:
        # 음성인식 결과 스트링으로 저장
        print("recognize")
        name = r.recognize_google(audio, language='ko-KR')
        print("recognize finish")
        print(name)

    except:
        print("Please, say!")
        continue
    if name in username:
        schoolcode = username[name]
        print("안녕하세요 %s 님?" % (name))
        break
    else:
        print("회원이 아닙니다, 다시 입력해주세요.")
        print("")
        continue


# 음성 인식 결과를 분석해서 급식 알려줄 날짜 구하기

def get_finaldate(saying):
    global requestToday
    global requestDay
    global requestYear
    global requestMonth
    global requestWeekDay
    #global requestDay
    # 음성 분석하기 함수로 만들기
    print(saying)
    if "오늘" in saying:
        print("오늘")
        pass
    elif "어제" in saying:
        print("어제")
        requestDay = requestDay - 1
        requestWeekDay = requestWeekDay - 1
    elif "내일" in saying:
        print("내일")
        requestDay = requestDay + 1
        requestWeekDay = requestWeekDay + 1
    elif ("모레" or "모래") in saying:
        print("모래")
        requestDay = requestDay + 2
        requestWeekDay = requestWeekDay + 2
    elif ("다음주" or "다음 주") in saying:
        print("다음주")
        requestDay = requestDay + 7

    if requestWeekDay > 6:
        requestWeekDay = requestWeekDay - 7
    return str(requestYear) + "." + str(requestMonth) + "." + str(requestDay)

# 해당하는 날짜를 주간식단에서 뽑아오기


def get_lunch(code, ymd, weekday):
    global schoolcode
    schMmealScCode = code  # int 1조식2중식3석식
    schYmd = ymd  # str 요청할 날짜 yyyy.mm.dd
    if weekday == 5 or weekday == 6:  # 토요일,일요일 버림
        element = " "  # 공백 반환
    else:
        # int 요청할 날짜의 요일 0월1화2수3목4금5토6일 파싱한 데이터의 배열이 일요일부터 시작되므로 1을 더해줍니다.
        num = weekday + 1
        URL = (
            "http://stu.kwe.go.kr/sts_sci_md01_001.do?"
            "schulCode=%s"
            "&schulCrseScCode=2"
            "&schulKndScCode=02"
            "&schMmealScCode=%d&schYmd=%s" % (
                schoolcode, schMmealScCode, schYmd)
        )
        # http://stu.AAA.go.kr/ 관할 교육청 주소 확인해주세요.
        # schulCode= 학교고유코드
        # schulCrseScCode= 1유치원2초등학교3중학교4고등학교
        # schulKndScCode= 01유치원02초등학교03중학교04고등학교
        # print(URL)
        # 기존 get_html 함수부분을 옮겨왔습니다.
        html = ""
        resp = requests.get(URL)
        if resp.status_code == 200:  # 사이트가 정상적으로 응답할 경우
            html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        element_data = soup.find_all("tr")
        element_data = element_data[2].find_all('td')
        try:
            element = str(element_data[num])

            # filter
            element_filter = ['[', ']', '<td class="textC last">',
                              '<td class="textC">', '</td>', '&amp;', '(h)', '.']
            for element_string in element_filter:
                element = element.replace(element_string, '')
            # 줄 바꿈 처리
            element = element.replace('<br/>', '\n')
            # 모든 공백 삭제
            element = re.sub(r"\d", "", element)

        # 급식이 없을 경우
        except:
            element = " "  # 공백 반환
    return element


def weekday(교시, 날짜):
    print("교시: %d 날짜: %d"%(교시, 날짜))
    global WeekDay
    global monday
    global tuesday
    global wednesday
    global thursday
    global friday
    print(WeekDay, 교시)
    if int(날짜) == 0:
        print(monday[str(교시)])
    elif int(날짜) == 1:
        print(tuesday[str(교시)])
    elif int(날짜) == 2:
        print(wednesday[str(교시)])
    elif int(날짜) == 3:
        print(thursday[str(교시)])
    elif int(날짜) == 4:
        print(friday[str(교시)])


# =====================================================


def food():
    global requestToday
    global requestDay
    global requestYear
    global requestMonth
    global requestWeekDay
    global myWord
    requestToday = datetime.today()
    requestYear = datetime.today().year
    requestMonth = datetime.today().month
    requestDay = datetime.today().day
    requestWeekDay = datetime.today().weekday()
    # 0 월요일 1 화요일 2 수요일 3 목요일 4 금요일 5토요일 6일요일
    input("앤터를 누르고 말씀하세요")

    # 오디오 초기화하기
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("listening...")
        audio = r.listen(source)
        print("listening finish...")

    try:
        # 음성인식 결과 스트링으로 저장
        print("recognize")
        myWord = r.recognize_google(audio, language='ko-KR')
        print("recognize finish")

    except:
        print("Please, say!")

    # 최종 날짜 하나의 스트링으로 만들기
    finalDate = get_finaldate(myWord)

    # 현재는 초등학교만 다루고 있음.
    # 2라는 숫자를 유,초,중,고에 따라 1, 2, 3, 4로 변경 하면 됨.

    print(requestWeekDay)
    diet = get_lunch(2, finalDate, requestWeekDay)

    # 출력하기
    if int(5) == requestWeekDay or int(6) == requestWeekDay:
        print("토요일이나 일요일은 급식먹는 날이 아닙니다.")
    else:
        print(diet, "입니다.")


def time2():
    global Today
    global Year
    global Month
    global Day
    global WeekDay
    global monday
    global tuesday
    global wednesday
    global thursday
    global friday
    global say1
    print(WeekDay)
    if "1교시" in say1 or "일교시" in say1:
        weekday(1, WeekDay)
    elif "2교시" in say1 or "이교시" in say1:
        weekday(2, WeekDay)
    elif "3교시" in say1 or "삼교시" in say1:
        weekday(3, WeekDay)
    elif "4교시" in say1 or "사교시" in say1:
        weekday(4, WeekDay)
    elif "5교시" in say1 or "오교시" in say1:
        weekday(5, WeekDay)
    elif "6교시" in say1 or "육교시" in say1:
        if WeekDay == 0:
            print("6교시가 없어요.")
        elif WeekDay == 1:
            print(tuesday[6])
        elif WeekDay == 2:
            print("6교시가 없어요.")
        elif WeekDay == 3:
            print(thursday[6])
        elif WeekDay == 4:
            print("6교시가 없어요.")
        else:
            print("그런 교시는 존재하지 않으므로 안녕히 가세요")
    else:
        if WeekDay == 0:
            print(monday)
        elif WeekDay == 1:
            print(tuesday)
        elif WeekDay == 2:
            print(wednesday)
        elif WeekDay == 3:
            print(thursday)
        elif WeekDay == 4:
            print(friday)
        else:
            print("당신이 말한날은 학교에 가는 날이 아니에요.")


def time():
    while(1):
        global Today
        global Year
        global Month
        global Day
        global WeekDay
        global monday
        global tuesday
        global wednesday
        global thursday
        global friday
        global say1

        # print(Today)
        # print(Year)
        # print(Month)
        # print(Day)
        # print(WeekDay)
        input("앤터를 누르고 말씀하세요")

        # 오디오 초기화하기
        r = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("listening...")
            audio = r.listen(source)
            print("listening finish...")

        try:
            # 음성인식 결과 스트링으로 저장
            print("recognize")
            say1 = r.recognize_google(audio, language='ko-KR')
            print("recognize finish")
            print(say1)

        except:
            print("Please, say!")
            continue
        Today = datetime.today()
        Year = datetime.today().year
        Month = datetime.today().month
        Day = datetime.today().day
        WeekDay = datetime.today().weekday()

        if "메뉴" in say1:
            break

        if "월요일" in say1:
            WeekDay = 0
            time2()
            continue
        elif "화요일" in say1:
            WeekDay = 1
            time2()
            continue
        elif "수요일" in say1:
            WeekDay = 2
            time2()
            continue
        elif "목요일" in say1:
            WeekDay = 3
            time2()
            continue
        elif "금요일" in say1:
            WeekDay = 4
            time2()
            continue
        elif "토요일" in say1:
            print("토요일은 학교에 가지 않습니다.")
            continue
        elif "일요일" in say1:
            print("일요일은 학교에 가지 않습니다.")
            continue

        elif "내일" in say1 or '네일' in say1:
            if int(WeekDay) > int(6):
                WeekDay -= 7
                WeekDay += 1
            else:
                WeekDay += 1
            time2()

        elif "모레" in say1 or '모래' in say1:
            if int(WeekDay) > int(6):
                WeekDay -= 7
                WeekDay += 2
            else:
                WeekDay += 2
            time2()
        elif "어제" in say1 or '어재' in say1:
            if int(WeekDay) < int(1):
                WeekDay += 7
                WeekDay -= 1
            else:
                WeekDay -= 1
            time2()
        elif '오늘' in say1:
            time2()
        else:
            print("언제 시간표를 말하시는 건가요?")
            continue


def cleaning(usay):
    while(1):
        break1 = 0
        i = 0
        if int(break1) >= 1:
            break
        print("-------------------------------------------")
        print("| 청소당번 및 발표순서 모드입니다, 무엇을 도와드릴까요 |")
        print("-------------------------------------------")

        classmate = ["개똥이", "사람", "똥개", "짱구", "유리",
                     "맹구", "주먹밥", "훈이", "수지", "고양이", "똥고집", "왕고집"]
        classmate2 = ["개똥이", "사람", "똥개", "짱구", "유리",
                      "맹구", "주먹밥", "훈이", "수지", "고양이", "똥고집", "왕고집"]

        random.shuffle(classmate)
        random.shuffle(classmate2)

        if '청소' and '발표'in usay or '청소' and '발표' not in usay:
            # 오디오 초기화하기
            input("청소당번을 뽑을까요 아니면 발표할 사람을 뽑을까요?앤터를 누르고 말씀하세요\n")
            r = sr.Recognizer()
            mic = sr.Microphone()

            with mic as source:
                print("listening...")
                audio = r.listen(source)
                print("listening finish...")

            try:
                # 음성인식 결과 스트링으로 저장
                print("recognize")
                Answer = r.recognize_google(audio, language='ko-KR')
                print("recognize finish")

            except:
                print("Please, say!")
                continue
            print(Answer)

            if Answer == '0':
                break
            else:
                if '1' in Answer or '일' in Answer:
                    print ("칠판 청소할 사람은? ")
                    print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
                    print ("바닥 쓸 사람은?")
                    print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
                    print ("창문 닦을 사람은?")
                    print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
                    print ("책장 정리할 사람은?")
                    print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
                    print ("계단 청소할 사람은?")
                    print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
                    print ("복도 쓸 사람은?")
                    print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")

                elif '2' in Answer or '이' in Answer:
                    while i < 12:
                        Answer = input("발표할 사람을 뽑을까요? (Y,N)")
                        if Answer == "Y":
                            print ("%d 번째 발표할 사람은? " % (i + 1))
                            print ("%s 입니다." % (classmate2.pop()))
                        elif Answer == "N":
                            break
                        else:
                            print ("다음에 다시 찾아와 주세요...")
                            break
                        i += 1

        if '청소당번' in usay or '청소 당번' in usay:
            print ("칠판 청소할 사람은? ")
            print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
            print ("바닥 쓸 사람은?")
            print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
            print ("창문 닦을 사람은?")
            print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
            print ("책장 정리할 사람은?")
            print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
            print ("계단 청소할 사람은?")
            print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
            print ("복도 쓸 사람은?")
            print (classmate.pop(), "그리고", classmate.pop(), "입니다. \n")
            break
        if '발표순서' in usay or '발표 순서' in usay:
            while i < 12:
                Answer = input("발표할 사람을 뽑을까요? (Y,N)")
                if Answer == "Y":
                    print ("%d 번째 발표할 사람은? " % (i + 1))
                    print ("%s 입니다." % (classmate2.pop()))
                elif Answer == "N":
                    break
                else:
                    print ("다음에 다시 찾아와 주세요...")
                    break
                i += 1


def team():
    while(1):
        print("----------------------------------")
        print("| 팀정하기 모드입니다, 무엇을 도와드릴까요? |")
        print("----------------------------------")
        team_1 = ["철수", "영희", "영철", "주언", "대성",
                  "민서", "재영", "하연", "항민", "민채", "동헌", "민아"]
        random.shuffle: team_1
        input("몇 팀으로 나누시겠습니까앤터를 누르고 말씀하세요")
        # 오디오 초기화하기
        r = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            print("listening...")
            audio = r.listen(source)
            print("listening finish...")

        try:
            # 음성인식 결과 스트링으로 저장
            print("recognize")
            num = r.recognize_google(audio, language='ko-KR')
            print("recognize finish")

        except:
            print("Please, say!")
            continue
        print(num)
        # 반복문 탈출
        if '메뉴' in num or '나가' in num:
            break
        elif '1' in num or '일' in num:
            print("1팀은", team_1, "입니다.")
        elif '2' in num or '이' in num:
            team_2 = [team_1.pop(), team_1.pop(), team_1.pop(),
                      team_1.pop(), team_1.pop(), team_1.pop()]
            print("1팀은", team_1, "입니다.")
            print()
            print("2팀은", team_2, "입니다.")
        elif '3' in num or '삼' in num:
            team_2 = [team_1.pop(), team_1.pop(), team_1.pop(), team_1.pop()]
            team_3 = [team_1.pop(), team_1.pop(), team_1.pop(), team_1.pop()]
            print ("1팀은", team_1, "입니다.")
            print()
            print ("2팀은", team_2, "입니다.")
            print()
            print ("3팀은", team_3, "입니다.")
        elif '4' in num or '사' in num:
            team_2 = [team_1.pop(), team_1.pop(), team_1.pop()]
            team_3 = [team_1.pop(), team_1.pop(), team_1.pop()]
            team_4 = [team_1.pop(), team_1.pop(), team_1.pop()]
            print ("1팀은", team_1, "입니다.")
            print()
            print ("2팀은", team_2, "입니다.")
            print()
            print ("3팀은", team_3, "입니다.")
            print()
            print ("4팀은", team_4, "입니다.")
        else:
            print("잘 알아듣지 못하였습니다. 다시한번 말씀해주세요")


def game():
    print("1단계, 2단계중 선택하세요.")
    choice = int(input())

    if choice == 1:
        questionNumber = random.randrange(1, 101)
        myChoice = 0
        time_count = 0
        print("게임시작!!!")
        while (myChoice != questionNumber):
            myChoice = int(input("1~100 사이의 숫자를 입력하세요 :"))
            time_count += 1

            if (myChoice > questionNumber):
                print("Down")
            elif (myChoice < questionNumber):
                print("Up")

    elif choice == 2:
        questionNumber = random.randrange(1, 1001)
        myChoice = 0
        time_count = 0
        print("게임시작!!!")
        while (myChoice != questionNumber):
            myChoice = int(input("1~1000 사이의 숫자를 입력하세요 :"))
            time_count += 1
            if (myChoice > questionNumber):
                print("Down")
            elif (myChoice < questionNumber):
                print("Up")
    print("당신은 %d 번 만에 맟추셨습니다." % time_count)


# ====================메인 프로그램 함수====================
def mode(usay):
    print(usay)
    # 급식

    if '급식' in usay or '1' in usay or '일' in usay:
        print('--------------------------------')
        print("| 급식 모드입니다, 무엇을 도와드릴까요? |")
        print('--------------------------------')
        food()

    elif '시간표' in usay or '2' in usay or '이' in usay:
        print("--------------------------------")
        print("| 시간표 모드입니다, 무엇을 도와드릴까요 |")
        print("--------------------------------")
        time()

    elif '청소' in usay or '발표순서' in usay or '3' in usay or '세번째' in usay:
        cleaning(usay)

    elif '팀' in usay or '4' in usay or '사' in usay or '네번째' in usay:
        team()
    elif '게임' in usay or '쉬는시간'in usay or '5' in usay or '오' in usay:
        game()
    elif "꺼" in usay or "종료" in usay:
        print("안녕히 게세요")
        exit()

    elif usay == '메뉴':
        print("-----------------------------------------------------------------")
        print("| 1.급식 | 2.시간표 | 3.청소당번 및 발표순서 | 4.팀정하기 | 5.쉬는시간 게임하기|")
        print("-----------------------------------------------------------------")
    else:
        print("잘 알아듣지 못하였습니다. 다시 말씀해주세요.")


while True:
    mode('메뉴')
    input("엔터를 누르고 말씀하세요")
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("listening...")
        audio = r.listen(source)
        print("listening finish...")

    try:
        # 음성인식 결과 스트링으로 저장
        print("recognize")
        word = r.recognize_google(audio, language='ko-KR')
        print("recognize finish")

    except:
        print("Please, say!")
        continue
    mode(word)