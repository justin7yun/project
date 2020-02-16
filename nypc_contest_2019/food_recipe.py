foodnum = input('')
foodstock = input('')
foodneed = input('')
foodstock1 = foodstock.split()
foodneed1 = foodneed.split()
canmade = []
divisioncount = 0

while(1):
    if int(divisioncount) < int(foodnum):
        if foodstock1[divisioncount] == '0':
            canmade.append(int(0))
            divisioncount +=1
            continue
        if foodneed1[divisioncount] == '0':
            canmade.append(int(0))
            divistioncount +=1
            continue
        canmadetest = ('%s // %s') % (foodstock1[divisioncount], foodneed1[divisioncount])
        canmadetest1 = eval(canmadetest)
        canmade.append(canmadetest1)
        divisioncount += 1  
        continue
    else:
        break

canmade.sort()
if canmade == []:
    print(int(0))
else:
    print(canmade[0])