import time

loading = 0

def start():
    global loading
    while(1):
        if loading >= 100:
            print("100 cleared!")
            break
        loading += 1
        time.sleep(0.09)
        print("%d persent" % (loading) + "\r", end="")

def close():
    exit(1)

start()
