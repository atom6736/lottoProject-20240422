#sqlAlchemy 패키지 사용 연습. DB로 변환해주는 패키지

from sqlalchemy import create_engine  # 필요한 것이 create_engine이라 그것만 불러옴.import
import pandas as pd
import pymysql

# 이제 간단한 Dataframe을 만들어보자.

data = {'학번': range(2000,2015), '성적': [70,60,100,90,50,75,85,99,78,63,100,100,100,100,100]}
# data = {'학번': range(2000,2015), '성적': [70,60,100,90,50,75,85,99,78,63,100,100,100,100,100]}
# 새로 추가된 데이터만 기존 테이블에 추가됨.


df = pd.DataFrame(data=data, columns=['학번','성적'])

print(df) #위와 같이 코딩하여 찍어보면 데이터프레임을 만들어줌.
#이것을 DB로 바로 넘겨보려고 함.

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4") #스키마만 만들어주면 됨.
#엔진을 만든 후 엔진을 어딘가에 저장해야 함. 작명하여 저장.
#그러면 크리에이트 엔진이 위 정보에 접속함. 그러면 연결을 만들어주어야 함.
engine.connect() # 이렇게 하면 통로가 생기게 됨.

df.to_sql(name="test_tbl", con=engine, if_exists='append', index=False)
#실행시킨 후 확인해보면 자동으로 테이블이 sql에 생긴것이 확인됨. 이것이orm기술. 이니 데이터가 있으면 뒤에 추가하라가append.





