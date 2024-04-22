import pymysql
import pandas as pd

import matplotlib.pyplot as plt

from collections import Counter

dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='lottodb')

sql = "select * from lotto_tbl"

cur = dbConn.cursor()
cur.execute(sql)

#보내준 것을 페치올로 받고.
dbresult = cur.fetchall()

lotto_df = pd.DataFrame(dbresult, columns=['회차','추첨일', '당첨번호1','당첨번호2',
                                           '당첨번호3','당첨번호4','당첨번호5','당첨번호6','보너스번호'])
# print(lotto_df)

#여러가지 방법이 있는데 6개 번호가 중복해서 무수하게 나옴.
# 그러면 제일 쉬운 방법은 6개의 번호를 그냥 전부 가져와서 리스트에 넣어버리는 방법
#그런다음 거기서 빈도수만 찾으면 됨. 몇 번 나왔는지. 그다음에 그 빈도수를 가지고 (막대)그래프를 그리면 되는 것.
#따라서 처음에 할 일은 6개의 번호만 빼오는 것.
#그래서 df 를 다시 만듬.

lotto_num_df = pd.DataFrame(lotto_df.iloc[0:,2:]) #보너스번호 포함 번호만 뽑아냄.

print(lotto_num_df)
print(lotto_num_df['당첨번호1'])


lotto_num_list = list(lotto_num_df['당첨번호1'])+list(lotto_num_df['당첨번호2'])+list(lotto_num_df['당첨번호3'])+list(lotto_num_df['당첨번호4'])+list(lotto_num_df['당첨번호5'])+list(lotto_num_df['당첨번호6'])+list(lotto_num_df['보너스번호'])

print((len(lotto_num_list)))

# print(lotto_num_df.value_counts()) # 각 번호들이 몇 번 카운트되었는지 만들어줌.
#하지만 가독성도 좋고 고치기 좋게 아래와 같이 코딩함. 1116*7 대략 8천개의 숫자를 리스트에 넣고 포문으로 돌려 빈도수를 찾을수도 있음. 좀 무식한 방법이지만.
# list(lotto_num_df[])

# for i in range(1,46):
#     count = 0
#     for num in lotto_num_list:
#         if num == i:
#             count = count + 1
#
#     print(f"{i}의 빈도수 : {count}")

n_lotto_data = Counter(lotto_num_list) # 빈도수 계산 모듈 사용.
## 빈도수의 내림차순으로 딕셔너리로 출력해줌.

print(n_lotto_data)


data = pd.Series(n_lotto_data)
data = data.sort_index()
data.plot(figsize=(20,30), kind='barh', grid=True, title="lotto KOR DATA")

plt.show()

cur.close()
dbConn.close()



