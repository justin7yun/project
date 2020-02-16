import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sqlite3
import time
import matplotlib.pyplot as plot
from matplotlib.image import imread

mainconn = sqlite3.connect('nanodust.db')
mainc = mainconn.cursor()
fire='0'
# w = QWidget()
# w.resize(250,150)
# w.move(300,300)
# w.setWindowTitle("Warning")
# w.window.updateScreen("adsfasd")
# w.show()
while True:
    mainc.execute("SELECT * FROM arduinocom WHERE eventname='fire'") 
    eventno = mainc.fetchall()
    for event in eventno:
        if fire != event[1]:
            print ('event: ', event[1])
            if event[1] == '1':
                print('fire') 
                fire=event[1]
                img = imread('inflammable-24043_640.png')
                plot.imshow(img) 
                plot.show()

            else:
                print('smile')
                fire=event[1]
                img = imread('inflammable-24043_640.png'
                plot.imshow(img)
                # plot.show()
                time.sleep(1)

#label.show()