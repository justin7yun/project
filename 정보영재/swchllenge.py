import sqlite3
import serial
import time, datetime
import threading
import emg
import re
import matplotlib.pyplot as plot
from matplotlib.image import imread
import sys
from PyQt5.QtWidgets import *
import subprocess 
#from PyQt5 import QtGui
#from PIL import Image

maincount = 0
i = 0
aa = 0
mainconn = sqlite3.connect('nanodust.db')
mainc = mainconn.cursor()
# mydata = mainc.execute('DELETE ALL')
# mainconn.commit
#app = QApplication(sys.argv)
#time.sleep(2)
#subprocess.call(['python3','test.py'])

def insert(nanodust, temparature, huminity, reserved1, reserved2):
    print("test")
    c.execute('''INSERT INTO arduinodata VALUES('%s', '%s', '%s', '%s', '%s', '%s')''' % (datetime.datetime.now(), nanodust, temparature, huminity, reserved1, reserved2))
    conn.commit()
 
print("Start")
while True:
    try:
        #ls -lart /dev 터미널에 입력하여 tty.찾기
        port="/dev/tty.HC-06-DevB"
        print(port)
        bluetooth=serial.Serial(port, 9600)
        print("Connected")
        print('connecting')
        bluetooth.flushInput()
        break
    except Exception as ex:
        print('bluetooth not conneced')
        a = input('reconnect?(y/n): ')
        if a == 'y':
            print('reconnecting')
        if a == 'n':
            exit()
        else:
            print('not exist')

def collectdata():
    global i
    global bluetooth
    global emg
    global aa
    #global c
    #global conn
    conn = sqlite3.connect('nanodust.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS arduinodata
	    (createDate date, nanodust text, temparature text, huminity text, reserved1 text, reserved2 text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS arduinocom
	    (eventname text, eventno text, reserved1 text, reserved2 text)''')
    c.execute('''DELETE FROM arduinocom''')
    c.execute('''INSERT INTO arduinocom VALUES('%s', '%s', '%s', '%s')''' % ('fire','0','0','0'))
    c.execute('''INSERT INTO arduinocom VALUES('%s', '%s', '%s', '%s')''' % ('dust','0','0','0'))
    while True:
        i+=1
        #print("Ping"+"\r", end = "")
        try:
            aa+=1
            bluetooth.write(b"BOOP "+str.encode(str(i)))
            input_data=bluetooth.readline()
            #print(input_data.decode())
            blueData = input_data.decode()
            bluedigit = re.findall(r"\d+", blueData)
            # print ('bluedata', bluedigit)
            #print('''INSERT INTO arduinodata VALUES('%s', '%s', '%s', '%s', '%s', '%s')''' %(datetime.datetime.now(), bluedigit[0],bluedigit[1],bluedigit[2],'0','0'))
            c.execute('''INSERT INTO arduinodata VALUES('%s', '%s', '%s', '%s', '%s', '%s')''' % (datetime.datetime.now(), bluedigit[0],bluedigit[1],bluedigit[2],'0','0'))
            conn.commit()
            #insert(bluedigit[0],bluedigit[1],bluedigit[3],0,0)
            #print("Bluetooth Pairing:"+emg.emg[aa]+"\r", end="")

        except Exception as ex:
            if maincount >= int(1):
                time.sleep(1)
                exit()
            else:
                #emg.close()
                print("\n"+"Not Connect")
                q = input('reconnect?(y/n)')
                if q == 'y':
                    try:
                        bluetooth.close()
                        port="/dev/tty.HC-06-DevB"
                        bluetooth=serial.Serial(port, 9600)
                        print("Connected")
                        print('connecting')
                        bluetooth.flushInput()
                        #emg.start()
                    except Exception as ex:
                        continue
                if q == 'n':
                    conn.close()
                    exit()
            if aa>12: 
                aa=0
            time.sleep(1)

# qwer = 0
# while(5):
#     for data in dustdata:
#         qwer = int(data[2])
#         #rewq += 1
#         break    

def firedetection():
    detectionconn = sqlite3.connect('nanodust.db')
    detectionc = detectionconn.cursor()
    count123=0
    while True:
        firecount1=1
        firecount2=1
        firecount4=1
        firecount5=1
        timecount = 0

        current = datetime.datetime.now()
        oneminutebefore = current - datetime.timedelta(seconds=10)
        #print(oneminutebefore)
        detectionc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
        dustdata = detectionc.fetchall()
        for data in dustdata:
            firecount1+=int(data[2])
            firecount2+=1
        average1 = int(firecount1) / int(firecount2)
        time.sleep(5 )
        current = datetime.datetime.now()
        oneminutebefore = current - datetime.timedelta(seconds=10)
        #print(oneminutebefore)
        detectionc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
        dustdata = detectionc.fetchall()
        for data in dustdata:
            firecount4+=int(data[2])
            firecount5+=1
        average2= int(firecount4) / int(firecount5)
        #####$print(average1,average2)
        average1 += 10
        if average1 <average2:
            count123+=1
            if count123 >=2:
                #온도 급격 상승후 온도가 80~100 이면 화재 경보 울리기
                print('온도 급격상승, 주의해주세요.')
                qwer = 0
                # rewq = 0
                detectionc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
                qwer = detectionc.fetchall()
                qwer = int(data[2])
                # rewq += 1
                mem = qwer
                if mem >= 80:
                    print('화재발생')
                    detectionc.execute("UPDATE arduinocom SET eventno='1' WHERE eventname='fire'")
                    detectionconn.commit()
                    # img = imread('inflammable-24043_640.png')
                    # plot.imshow(img)
                    # plot.show()
                    # label = QLabel()
                    # pixmap = QtGui.QPixmap('inflammable-24043_640.png')
                    # label.setPixmap(pixmap)
                    # label.show()
                    # app.exec_()
                    while(2):
                        qwer=0
                        time.sleep(1)
                        current = datetime.datetime.now()
                        oneminutebefore = current - datetime.timedelta(seconds=1)
                        detectionc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
                        qwer = detectionc.fetchall()
                        bNormal=False
                        for qw in qwer:
                            if int(qw[2]) <= int(30):
                                print('정상온도로 돌아왔습니다.')
                                detectionc.execute("UPDATE arduinocom SET eventno='0' WHERE eventname='fire'")
                                detectionconn.commit()
                                count123=0
                                bNormal=True
                        if bNormal == True:
                            break
        else:
            count123=0


if __name__ == "__main__":
    t = threading.Thread(target=collectdata, args=())
    a = threading.Thread(target=firedetection, args=())
    t.start()
    a.start()
    while True:
        count1 = 0
        count2 = 0
        count=1
        count22=1
        print("\nservise list\nDraw graph(press enter)\n1.onemunitebefore nanodust\n2.finish\n3.temperature graph\n")
        #emg.start()
        serv = input('원하시는 서비스 번호: ')
        if serv == '':
            x = [0,1,2,3,4]
            y = [99,1,4,2,3]
            current = datetime.datetime.now()
            oneminutebefore = current - datetime.timedelta(minutes=1)
            mainc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
            dustdata = mainc.fetchall()
            x.clear()
            y.clear()
            for data in dustdata:
                print (data[1])
                x.append(count)
                y.append(int(data[1]))
                count22+=int(data[1])
                count+=1
                count1 = count
                count2 = count22
            print(x)
            print(y)
            #print (oneminutebefore)

            plot.plot(x, y, label = 'Nanodust')

            plot.xlabel('time')
            plot.ylabel('dansity')

            plot.title('nanodust')

            plot.legend()
            plot.show()
            print("graph off/")
            time.sleep(1)
        elif serv == '1':
            current = datetime.datetime.now()
            oneminutebefore = current - datetime.timedelta(minutes=1)
            mainc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
            dustdata = mainc.fetchall()
            for data in dustdata:
                count22+=int(data[1])
                count+=1
                count1 = count
                count2 = count22
            ab = int(count22)/int(count)
            print(ab)
        elif serv == '2':
            maincount += 1
            print("Done")
            bluetooth.close()
            break
        elif serv == '3':
            x = [0,1,2,3,4]
            y = [99,1,4,2,3]
            current = datetime.datetime.now()
            oneminutebefore = current - datetime.timedelta(minutes=1)
            mainc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
            dustdata = mainc.fetchall()
            x.clear()
            y.clear()
            for data in dustdata:
                print (data[2])
                x.append(count)
                y.append(int(data[2]))
                count22+=int(data[2])
                count+=1
                count1 = count
                count2 = count22
            print(x)
            print(y)
            #print (oneminutebefore)

            plot.plot(x, y, label = 'temperature')

            plot.xlabel('time')
            plot.ylabel('temperature')

            plot.title('temperature')

            plot.legend()
            plot.show()
            print("graph off/")
            time.sleep(1)

        # elif serv == '3':
        #     mydata = mainc.execute('DELETE FROM arduinodata')
        #     print('삭제되었습니다.') 
        else:
            print('notexist')
raise SystemError("python is stoped!")