import random 

input("팀 선정을 시작하시려면 앤터를 눌러주세요")
print("")
friend = []
teama = []
teamb = []
teamcount = 0
classcount = 0
a = 0
b = 0
exit1 = 0

while(1):
    if exit1 == int(1):
        break
    classinput = input("우리반 친구들을 한명씩 적어주세요: ")
    if classinput != "":
        friend.append(classinput)
        while(1):
            if exit1 == int(1):
                break
            classinput = input("우리반 친구들을 한명씩 적어주세요: ")
            if classinput != "":
                friend.append(classinput)
                while(1):
                    classinput = input("우리반 친구들을 한명씩 적어주세요(더이상 없으시면 아무것도 쓰지마시고 앤터를 눌러주세요): ")
                    if classinput != "":    
                        friend.append(classinput)
                    else:
                        exit1 += 1
                        break
            else:
                print("친구들이 2명 이상 존재해야 합니다.") 
                print("")
    else:
        print("빈칸은 적으실수 없습니다.")
        print("")

random.shuffle(friend)

print('')
print("우리반친구들")
print(friend)
print('')

a = len(friend)
b = a / 2.0
bb = a / 2
print("")
teama = []
teamb = []
lll = len(friend)
if float(b).is_integer():
    print("학생 수가 짝수이므로 'a팀 %d명', 'b팀 %d명' 으로 뽑겠습니다."% (bb, bb))
    print("")
    while teamcount < int(bb):
        aaa = friend.pop()
        teama.append(aaa)
        teamcount += 1
    teamcount = 0
    while teamcount < int(bb):
        bbb = friend.pop()
        teamb.append(bbb)
        teamcount += 1
else:
    teamcount = 0
    d = int(a) + 1
    ddd = int(d) / 2
    c = float(d) - float(ddd) - 1.0
    print("학생 수가 홀수이므로 'a팀 %d명', 'b팀 %d명' 으로 뽑겠습니다."% (ddd, c))
    print("")
    while teamcount < int(ddd):
        aaaa = friend.pop()
        teama.append(aaaa)
        teamcount += 1
    teamcount = 0
    while teamcount < int(c):
        bbbb = friend.pop()
        teamb.append(bbbb)
        teamcount += 1

print("========================")
print("팀 선정 결과를 알려드리겠습니다.")
print("팀 a 는", teama, "입니다.")
print("팀 b 는", teamb, "입니다.")
print("========================")