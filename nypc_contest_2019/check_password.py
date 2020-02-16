def password_check(password):
    # Password = password

    passwordlen = len(password)
    if 8 =< passwordlen =< 15:
        
    else:
        return('invailid')

# mainroutain
while(1):
    pinput = input('비밀번호를 입력해주세요: ')
    
    answer = password_check(pinput)

    if answer == 'vailid':
        print('vailid')
        continue
    elif answer == 'invailid':
        print('invailid')
        continue

