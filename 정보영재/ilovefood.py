weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일']
weekends = ['토요일', '일요일']
todaymenu = {"월요일" : "카레라이스, 팽이버섯된장국, 청경채겉절이, 김치, 샌드위치",

        "화요일" : "녹두밥, 쇠고기떡국, 임연수 어묵조림, 깻잎찜, 청포도",

        "수요일" : "곤드레밥, 열무된장국, 왕새우튀김, 오이소박이, 체리",

        "목요일" : "닭다리삼계탕/닭죽, 해물완자전, 오이배초무침, 깍두기, 포도",

        "금요일" : "비빔밥, 어묵무국, 무생채, 꿀떡, 우유, 요구르트"}
while(1):
    today = str(input('오늘은 무슨 요일입니까?: '))
    
    if today in weekdays:
        food = todaymenu[str(today)]
        print('')
        print('오늘의 급식 ', str(food),' 입니다.')
        print('')
    elif today == "토요일" or today == "일요일":
        print('')
        print(today, '에는 급식이 배급되지 않습니다.')
        print('')
    else:
        print('')
        print('그런날은 존재하지 않습니다.')
        print('')
