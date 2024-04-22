import requests
from bs4 import BeautifulSoup
from datetime import datetime # 날짜열을 쓰기 위해 내장 모듈을 불러옴.

url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=1116"

html = requests.get(url).text #텍스트로 받아서 url을 찍어줌.

print(html)

soup = BeautifulSoup(html, 'html.parser')

date = soup.find('p',{'class':'desc'}).text #로또 추첨일. 문자로 바꾸어 저장.
lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")  # 스트링(문자열)을 데이트타입으로 바꾸어주는 명령문.

print(lottoDate)

print(date)

lottoNumber = soup.find('div', {'class':'num win'}).find('p').text.strip().split('\n')
# 로또 당첨번호 6개를 리스트로 변환하여 반환. div, num win 을 찾은 뒤 그 안에서 다시 p로 찾아서 문자로 바꾼후 자와 공백제거
# 위를 정수로 바꾸는 방법은 빈리스트를 하나 만든 후 숫자를 빼서 빈리스트에 추가하는 형태로 정수변환.

lottoNumberList = []

for num in lottoNumber:
    num = int(num) #문자열 번호를 정수로 바꾸어.
    lottoNumberList.append(num)

print(lottoNumberList)

# print(lottoNumber)

bonusNumber = int(soup.find('div', {'class':'num bonus'}).find('p').text.strip()) # 보너스번호 추출.
# 보너스번호는 1개이니까 위를 전부 int로 감싸서 정수로 변환.(보너스번호 1개 반환)

print(bonusNumber)

