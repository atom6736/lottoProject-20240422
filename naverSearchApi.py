# 검색 불러오기 한 것을 함수 내지 모듈로 만들어 본다.
# 네이버에서 서치해주는 부분 따로, 앱을 만드는 부분 따로, 앱에서는 앱만 관리, 서치해주는 부분은 따로 관리
# 이렇게 분리하면 키가 도난당해 그것이 바뀌거나 등 수정해야 할 때 매우 용이.

from urllib.request import *
from urllib.parse import quote
import json
import datetime

class NaverApi:
    def getRequestUrlCode(self, url):
        requestUrl = Request(url)

        client_id = "9ugJtb3ghQVaEQat1pwQ"
        client_secret = "qYws9KEdW8"

        requestUrl.add_header("X-Naver-Client-Id", client_id)
        requestUrl.add_header("X-Naver-Client-Secret", client_secret)

        naverResult = urlopen(requestUrl) # 네이버에서 요청에 의한 결과(응답)을 반환
        if naverResult.getcode() == 200: #200이면응답결과가 정상
            print(f"네이버 api 요청 정상 진행 : {datetime.datetime.now()}")
            return naverResult.read().decode('utf-8')
        #응답결과가 정상이면 utf-8로 네이버에서 받은 결과를 utf-8로 인코딩해서 반환하겠다는 것.
        else:
            print(f"네이버 api 요청 실패 : {datetime.datetime.now()}")
            return None
        #응답결과가 에러이면 아무것도 반화하지 마라.

    def getNaverSearch(self, node, keyword,start,display):
        baseUrl = "https://openapi.naver.com/v1/search/" #네이버 api 기본 url
        node = f"{node}.json"
        params = f"?query={quote(keyword)}&start={start}&display={display}"

        url = baseUrl+node+params

        result = self.getRequestUrlCode(url)

        if result !=None: # none이면 네이버에서 결과값이 뭔가 왔다는 것.
            return json.loads(result) # json 형태로 반환
        else:
            print("네이버 응답 실패! 에러발생!")
            return None









