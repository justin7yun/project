import sqlite3
import serial
import time, datetime
import threading
import emg
import re
import matplotlib.pyplot as plot

i = 0
aa = 0
mainconn = sqlite3.connect('nanodust.db')
mainc = mainconn.cursor()

def insert(nanodust, temparature, huminity, reserved1, reserved2):
    print("test")
    c.execute('''INSERT INTO arduinodata VALUES('%s', '%s', '%s', '%s', '%s', '%s')''' % (datetime.datetime.now(), nanodust, temparature, huminity, reserved1, reserved2))
    conn.commit()
 
print("Start")
while True:
    try:
        #ls -lart /dev 터미널에 입력하여 tty.찾기
        port="/dev/tty.HC-06-DevB"
        bluetooth=serial.Serial(port, 9600)
        print("Connected")
        print('connecting')
        bluetooth.flushInput()
        break
    except Exception as ex:
        print('bluetooth not conneced')
        a = input('reconnect?(y/n): ')
        if a == 'y':
            continue
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
            #print ('bluedata', bluedigit)
            #print('''INSERT INTO arduinodata VALUES('%s', '%s', '%s', '%s', '%s', '%s')''' %(datetime.datetime.now(), bluedigit[0],bluedigit[1],bluedigit[2],'0','0'))
            c.execute('''INSERT INTO arduinodata VALUES('%s', '%s', '%s', '%s', '%s', '%s')''' % (datetime.datetime.now(), bluedigit[0],bluedigit[1],bluedigit[2],'0','0'))
            conn.commit()
            #insert(bluedigit[0],bluedigit[1],bluedigit[3],0,0)
            #print("Bluetooth Pairing:"+emg.emg[aa]+"\r", end="")

        except Exception as ex:
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
def firedetection():
    firecount1=1
    firecount2=1
    firecount3=0
    timecount = 0
    current = datetime.datetime.now()
    oneminutebefore = current - datetime.timedelta(minutes=1)
    mainc.execute("SELECT * FROM arduinodata WHERE createDate > '%s'" % (oneminutebefore)) 
    dustdata = mainc.fetchall()
    firecount3 = int(data[1])
    for data in dustdata:
        firecount2+=int(data[1])
        firecount1+=1
        count1 = count
        count2 = count22
    ab = int(firecount2)/int(firecount1)
    time.sleep(1)
    timecount+=1
    if timecount == '10':
        timecount = 0
        memory = ab - firecount3
        if memory >= 100 or memory >= -100:
            cs.addsms("01077470779", "화재가 감지되었습니다.")



if __name__ == "__main__":
    t = threading.Thread(target=collectdata, args=())
    t.start()
    while True:
        count1 = 0
        count2 = 0
        count=1
        count22=1
        print("\nservise list\n>>Draw graph(press enter)\n>>onemunitebefore nanodust(press number '1' and press enter)\n")
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
            print("Done")
            bluetooth.close()
            exit() 
        else:
            print('notexist')
    bluetooth.close()
    print("Done")
    exit()