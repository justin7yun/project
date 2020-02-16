save0 = []
save1 = []
save2 = []
tem0 = 0
tem1 = 0
tem2 = 0
a = 0
count = 0
while(1):
    print('1.약수 구하기\n2.공약수 구하기\n3.최소공배수 구하기')
    option = input('어떤거?: ')
    if option == '1':
        input0 = input('약수(꼭 숫자만): ') 
        while(2):
            a+=1
            tem0 = int(input0) / int(a)
            if tem0.is_integer():
                save0.append(tem0)
            
            if a == int(input0):
                save0.sort()
                print(save0)
                a = 0 
                tem0 = 0
                save0 = []
                print('')
                break

    elif option == '2':
        input1 = input('첮번째 약수(꼭 숫자만): ')
        input2 = input('두번째 약수(꼭 숫자만): ')
        while(3):
            a+=1
            tem1 = int(input1) / int(a)
            if tem1.is_integer():
                save1.append(tem1)
            
            if int(a) == int(input1):
                save1.sort()
                a = 0
                break
                

        while(4):
            a+=1
            tem2 = int(input2) / int(a)
            if tem2.is_integer():
                save2.append(tem2)
            
            if int(a) == int(input2):
                save2.sort()

                qwer = list(set(save1) & set(save2))
                qwer.sort() 
                print(qwer)
                a = 0 
                tem1 = 0
                save1 = []
                tem2 = 0
                save2 = []
                print('')
                break
    elif option == '3':
        input1 = input('첮번째 숫자: ')
        input2 = input('두번째 숫자: ')
        a = 0

        while(5):
            a+=1
            tem1 = int(input1) * int(a)
            save1.append(tem1)
            if int(a) == int(100):
                a = 0
                break
        while(6):
            a+=1
            tem2 = int(input2) * int(a)
            save2.append(tem2)
            if int(a) >= int(100):
                print(save1)
                print(save2)
                save0 = list(set(save1) & set(save2))
                save0.sort()
                print(save0[0])
                a = 0
                save0 = []
                save1 = []
                save2 = []
                tem1 = 0
                tem2 = 0
                break
    else:
        print('not exist')