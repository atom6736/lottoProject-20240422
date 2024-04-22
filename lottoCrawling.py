#본격적으로 크롤링해와서 만들어보기. test에서 만든 것을 함수로 만들어보자.

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

from sqlalchemy import create_engine  # 필요한 것이 create_engine이라 그것만 불러옴.import
import pandas as pd
import pymysql


# 방금 만든 Test를 복붙한 후 개조
def get_lottoNumber(count): #로또 추첨회차를 입력 받음. 카운트라는 값으로 20을 넣으면 20회차를 반환받고, 1000회차면 그것을 반환받고.
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={count}"
    html = requests.get(url).text  # 텍스트로 받아서 url을 찍어줌.
    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find('p', {'class': 'desc'}).text  # 로또 추첨일. 문자로 바꾸어 저장.
    lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")  # 스트링(문자열)을 데이트타입으로 바꾸어주는 명령문.
    lottoNumber = soup.find('div', {'class': 'num win'}).find('p').text.strip().split('\n')
    lottoNumberList = []

    for num in lottoNumber:
        num = int(num)  # 문자열 번호를 정수로 바꾸어.
        lottoNumberList.append(num)

    bonusNumber = int(soup.find('div', {'class': 'num bonus'}).find('p').text.strip())  # 보너스번호 추출.

    lottoDic = {'lottoDate': lottoDate, 'lottoNumber':lottoNumberList, 'bonusNumber':bonusNumber}

    return lottoDic # 크롤링한 값을 딕셔너리형태로 넣어서 반환하겠다는 것.

def get_recent_lottocount():  # 최신 로토 회차 크롤링 함수
    url = "https://dhlottery.co.kr/common.do?method=main"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    recent_count = soup.find("strong", {'id':'lottoDrwNo'}).text.strip()
    recent_count = int(recent_count)
    return recent_count+1 # 아래 레인지에 넣을 것이니까 최신회차 숫자보다 하나 많은 것을 넣어주어야 함.



lottodf_list = []

# print(get_recent_lottocount()) #위의 함수가 최신회차를 잘 가져오는지를 화인

for count in range(1,get_recent_lottocount()):
    lottoResult = get_lottoNumber(count)

    lottodf_list.append({
        'count': count, #로또 추첨회차
        'lottoDate': lottoResult['lottoDate'], # 로또 추첨일
        'lottoNum1': lottoResult['lottoNumber'][0], # 로또 당첨 번호 중 첫번째 번호
        'lottoNum2': lottoResult['lottoNumber'][1],
        'lottoNum3': lottoResult['lottoNumber'][2],
        'lottoNum4': lottoResult['lottoNumber'][3],
        'lottoNum5': lottoResult['lottoNumber'][4],
        'lottoNum6': lottoResult['lottoNumber'][5],
        'bonusNum' : lottoResult['bonusNumber']  # 로또 보너스 번호
    })

    print(f"{count}회 처리중...")

# print(lottodf_list) # 워낙많으니 출력하는데 시간이 걸림. 그리고 클래스에서 모두가 접속해 하면 ban당할 수도 있으니 약간 딜레이 주어야 하기도 함.
#잘 오는 걸 확인하고는 프린트문 주석처리.

lottoDF = pd.DataFrame(data=lottodf_list, columns=['count', 'lottoDate',
    'lottoNum1','lottoNum2','lottoNum3','lottoNum4','lottoNum5','lottoNum6','bonusNum'])

print(lottoDF)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4") #스키마만 만들어주면 됨.
engine.connect()

lottoDF.to_sql(name="lotto_tbl", con=engine, if_exists='append', index=False)



