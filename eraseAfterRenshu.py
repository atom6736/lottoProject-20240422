import os
import sys
import urllib.request
client_id = "9ugJtb3ghQVaEQat1pwQ"
client_secret = "qYws9KEdW8"
encText = urllib.parse.quote("축구")
url =  "https://openapi.naver.com/v1/search/news?query=" + encText

request = urllib.request.Request(url)
request.add_header("X-Naver-client-Id",client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
# print('12')
response = urllib.request.urlopen(request)
print('14')
rescode = response.getcode()
print('15')
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

#에러 찾기 성공했다. 얏호호.. 어느 단계에서 오류 또는 오타가 발생했는지 프린트문으로 추적하며 찾아냈다.

