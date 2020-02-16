import time

emg = [0] * 19
emg[1] = ('|=-        |')
emg[2] = ('|-=-       |')
emg[3] = ('| -=-      |')
emg[4] = ('|  -=-     |')
emg[5] = ('|   -=-    |')
emg[6] = ('|    -=-   |')
emg[7] = ('|     -=-  |')
emg[8] = ('|      -=- |')
emg[9] = ('|       -=-|')
emg[10] = ('|        -=|')
emg[11] = ('|       -=-|')
emg[12] = ('|      -=- |')
emg[13] = ('|     -=-  |')
emg[14] = ('|    -=-   |')
emg[15] = ('|   -=-    |')
emg[16] = ('|  -=-     |')
emg[17] = ('| -=-      |')
emg[18] = ('|-=-       |')

exit = 0

def start():
    global exit
    aa = 0
    exit = 0
    while True:
        if int(exit) >= int(1):
            break
        print(emg[aa] + "\r", end="")
        time.sleep(0.05)
        if int(aa) >= int(18):
            aa = 1
        else:
            aa += 1

def close():
    global exit
    exit += 1

start()
