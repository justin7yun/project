#관리자 아이디가 있습니다.
import sqlite3
from enum import Enum
import datetime


conn = sqlite3.connect('bookinfo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS members
	(id text, pwd text, age text, school text, class text)''')

c.execute('''CREATE TABLE IF NOT EXISTS bookinfo
	(id text, bookName text, borrowDate date, returnDate date)''')

count = 0
#관리자 아이디.
#-아직 개발중이어서 '안녕하세요?관리자님' 이라는 문구밖에 나오지 않습니다.
sudoId = "root"
sudoPassword = "rhksflwk1234"
# 비밀번호 '관리자1234' 영어로 입력

class Member(Enum):
    PASSWORD=1
    AGE=2
    SCHOOL=3
    CLASS=4

def printbook(strID):
    print('')
    print('<당신이 빌린책>')
    print('==========================')
    c.execute("SELECT * FROM bookinfo WHERE id='%s'" % (strID))
    book = c.fetchone()
    if(book==None):
        print('==없음==')
    else:
        c.execute("SELECT * FROM bookinfo WHERE id='%s'" % (strID))
        books = c.fetchall()
        for book in books:
            print("%s ('빌린날짜'%s)" % (book[1],book[2]))
    print('==========================')
    print('')

print('도서관리 시스템입니다.')
print('고객님들의 모든 활동 정보는 컴퓨터 로컬에 저장됩니다.')
print('')

def createacount():
    print('회원 가입을 시작합니다.')
    Id = input('사용하실 아이디를 입력해주세요:')
    password = input('사용하실 비밀번호를 입력해주세요:')
    age = input('당신의 나이를 입력해주세요:')
    school = input('당신이 다니고 있는 학교는 어디입니까?:')
    school_class = input('당신은 몇반이십니까?:')
    c.execute("SELECT * FROM members WHERE id='%s'" % Id)
    member = c.fetchone()
    if(member!=None):
        print('이미 사용중인 아이디나 비밀번호입니다.')

    if Id == 'root':
        print('root는 관리자 아이디이므로 사용하실수 없습니다.')
    else:
        c.execute('''INSERT INTO members VALUES('%s', '%s', '%s', '%s', '%s')''' % (Id, password, age, school, school_class))
        print(Id,'님의 아이디가 생성되었습니다!')
        conn.commit()
    print('')

def print_acount(a):
    print(' '' \n============================')
    c.execute("SELECT * FROM members WHERE id='%s'" % (a))
    member = c.fetchone()
    if(member==None):
        print('회원정보가 존재하지않습니다.')
    else:
        print('당신의 아이디:', member[0])
        print('당신의 비밀번호:', member[1])
        print('당신의 나이:', member[2])
        print('당신의 학교:', member[3])
        print('당신의 반:', member[4])
    print('============================ \n'' ')

def login(a,b):
    c.execute("SELECT * FROM members WHERE id='%s' and pwd='%s'" % (a,b))
    member = c.fetchone()
    if(member==None):
        ret = False
    else:
        ret = True
    return ret

def delete_account(a,b):
    c.execute("DELETE FROM members WHERE id='%s' and pwd='%s'" % (a,b))
    conn.commit()
    print(a,'님의 아이디가 삭제되었습니다!')

def update_account(nEnum, strID):
    c.execute("SELECT * FROM members WHERE id='%s'" % (strID))
    member = c.fetchone()
    if(member==None):
        print('회원정보가 존재하지않습니다.')
        return
    if(nEnum == Member.PASSWORD):
        print('현재 비밀번호: ', member[1])
        cpassword = input('바꾸고싶은 비밀번호: ')
        c.execute("UPDATE members SET pwd='%s' WHERE id='%s'" % (cpassword,strID))
        conn.commit()
        print(strID,'님의 비밀번호가 변경되었습니다!')
        print_acount(strID)
    elif(nEnum == Member.AGE):
        cage = input('바꾸고싶은 나이: ')
        c.execute("UPDATE members SET age='%s' WHERE id='%s'" % (cage,strID))
        conn.commit()
        print(strID,'님의 나이가 변경되었습니다!')
        print_acount(strID)
    elif(nEnum == Member.SCHOOL):
        cschool = input('바꾸고싶은 학교: ')
        c.execute("UPDATE members SET school='%s' WHERE id='%s'" % (cschool,strID))
        conn.commit()
        print(strID,'님의 학교가 변경되었습니다!')
        print_acount(strID)
    elif(nEnum == Member.CLASS):
        cschool_class = input('바꾸고싶은 반: ')
        c.execute("UPDATE members SET class='%s' WHERE id='%s'" % (cschool_class,strID))
        conn.commit()
        print(strID,'님의 반이 변경되었습니다!')
        print_acount(strID)

def borrow_book(strID, strBook):
    c.execute("SELECT * FROM bookinfo WHERE id='%s' AND bookName='%s'" % (strID, strBook))
    books = c.fetchone()
    if(books!=None):
        print(strBook, '이(는) 이미 대출중인 책입니다.')
        printbook(a)
        print('')
        return
    c.execute('''INSERT INTO bookinfo VALUES('%s', '%s', '%s', '%s')''' % (strID, strBook, datetime.datetime.now(), ""))
    print(strBook,' 이(가) 대출 되었습니다!.')
    printbook(a)
    conn.commit()

def return_book(strID, strBook):
    c.execute("SELECT * FROM bookinfo WHERE id='%s' AND bookName='%s'" % (strID, strBook))
    books = c.fetchone()
    if(books!=None):
        c.execute("DELETE FROM bookinfo WHERE id='%s' AND bookName='%s'" % (strID, strBook))
        print(strBook,' 이(가) 반납 되었습니다!.')
        conn.commit()
        return
    print('그런책이 존재하지않습니다.')

# Main Routine Start
while(6):
    print('1)로그인 \n2)회원가입 \n3)종료\n'' ')
    msurvise = input('원하시는 서비스번호: ')
    if msurvise == '2':
        createacount()
    elif msurvise == '1':
        print('로그인해주세요')
        a = input('당신의 아이디:')
        b = input('당신의 비밀번호:')
        if login(a,b) == True:
            print('')
            print('로그인 되셨습니다.')
            print('')
            print('안녕하세요', a, ' 님')
            print('')
            while (2):
                print(' 1) 도서 대여하기 \n 2) 도서 반납하기 \n 3) 대출중인 도서 보기 \n 4) 로그아웃\n 5) 회원정보 바꾸기 \n '' ')
                survise = input('원하시는 서비스 번호를 입력해주세요 : ')
                print('')
                if survise == '1':
                    borrow = input('대출하실 책의 이름을 입력해주세요:')
                    borrow_book(a, borrow)
                elif survise == '2':
                    banap = input('반납하실 책의 이름을 입력해주세요:')
                    return_book(a, banap)
                    printbook(a)
                elif survise == '3':
                    printbook(a)
                elif survise == '4':
                    print('로그아웃 되었습니다.')
                    print('')
                    print('==========================')
                    print('')
                    break
                elif survise == '5':
                    cpassword=input('이 계정의 비밀번호를 입력해주세요: ')
                    if cpassword == b:
                        while(5):
                            print('')
                            print(' 아이디 변경불가 \n 1.비밀번호 바꾸기 \n 2.나이 바꾸기 \n 3.학교 바꾸기 \n 4.나의 학교 반 바꾸기 \n 5.회원 탈퇴하기 \n 6.나가기')
                            print('')
                            csurvise = input('원하시는 서비스 번호: ')
                            if csurvise =='1':
                                update_account(Member.PASSWORD,a)
                                print('메인화면으로 이동합니다, 다시 로그인해주세요.')
                                count+=1
                                break
                            elif csurvise == '2':
                                update_account(Member.AGE,a)
                            elif csurvise == '3':
                                update_account(Member.SCHOOL,a)
                            elif csurvise == '4':
                                update_account(Member.CLASS,a)
                            elif csurvise == '5':
                                cpassword2 = input('이 계정의 비밀번호를 입력해주세요: ')
                                if cpassword2 == b:
                                    print('비밀번호가 일치합니다.')
                                    delete_correct = input('정말로 이 계정을 삭제하시겠습니까?(y/n): ')
                                    if delete_correct == 'y':
                                        delete_account(a,b)
                                        print('===========================')
                                        print('')
                                        count += 1
                                        break
                                    elif delete_correct == 'n':
                                        print('회원탈퇴가 취소되었습니다.')
                                        print('')
                                    else:
                                        print('존재하지 않습니다.')
                                        print('')
                                else:
                                    print('비밀번호가 일치하지 않습니다')
                            elif csurvise == '6':
                                break
                            else:
                                print('존재하지않습니다')
                        if count>=1:
                            count = 0
                            break
                        else:
                            print('나가기.')
                            print('')


                    else:
                        print('비밀번호가 일치하지 않습니다.')

                else:       
                    print('존재하지 않습니다.')
        elif a == sudoId:   
            if b == sudoPassword:
                print('안녕하십니까 관리자님?')
                print('')
                while(1):
                    print('1. 모든 회원들보기 \n2. 회원 강탈시키기\n3. 나가기')
                    print('')
                    sudosurvise = input('원하는 서비스번호: ')
                    print('')
                    if sudosurvise == '1':
                    	print('')
					    print('==========================')
                        c.execute("SELECT * FROM members")
					    members = c.fetchall()
					    if(members==None):
					        print('==가입중인 회원이 존재하지 않습니다==')
					    else:
					        c.execute("SELECT * FROM members")
					        members = c.fetchall()
					        for member in members:
					            print("%s" % (member))
					    print('==========================')
					    print('')
                    elif sudosurvise == '2':
                        print('개발중')
                    elif sudosurvise == '3':
                        print('로그아웃됨...')
                        break
            else:
                print('당신의 아이디나 비밀번호가 일치하지 않거나 존재하지 않습니다.')
                print('')
        else:
            print('당신의 아이디나 비밀번호가 일치하지 않거나 존재하지 않습니다.')
            print('')

    elif msurvise == '3':
        print('안녕하가세요')
        conn.commit()
        break
    else:
        print('존재하지 않습니다.')