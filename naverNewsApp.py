import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from naverSearchApi import *

import webbrowser

form_class = uic.loadUiType("ui/naverNewsSearchAppUi.ui")[0] # 외부에서 ui불러오기

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("네이버 뉴스 검색 앱")
        self.setWindowIcon(QIcon("img/news.png"))
        self.statusBar().showMessage("Naver News Search Application v1.0")

        self.searchBtn.clicked.connect(self.searchBtn_clicked)
        self.result_table.doubleClicked.connect(self.link_doubleClicked)
        # 테이블의 항목이 더블클릭되면 괄호 안의 link_doubleClicked함수 호출

    def searchBtn_clicked(self):
        keyword = self.input_keyword.text() # 사용자가 입력한 검색 키워드 가져오기

        if keyword =="":
            QMessageBox.warning(self,"입력오류!","검색어는 필수 입력사항입니다.")
        else:
            naverApi = NaverApi() # import된 naverSearchApi 내의 NaverApi 클래스로 객체 생성
            searchResult = naverApi.getNaverSearch("news",keyword, 1, 10)
            # print(searchResult)
            newsResult = searchResult['items']
            self.outputTable(newsResult)

    def outputTable(self, newsResult): # 뉴스검색결과를 테이블위젯에 출력하는 함수
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.result_table.setColumnCount(3) #출력되는 테이블을 3열로 설정. 제목, 링크, 시간?
        self.result_table.setRowCount(len(newsResult)) # 출력되는 행은 뉴스의 내용이나 갯수에 따라 가변적. 그래도 출력되는 테이블의 행 갯수 설정.
        # newsResult 내의 원소 갯수만큼 줄 갯수를 설정. 가변적인 것을 len으로 카운트하는 것.

        #테이블의 첫 행(열 이름) 설정
        self.result_table.setHorizontalHeaderLabels(["기사제목","기사링크","게시시간"])
        # 각 칼럼의 넓이 지정(총 길이 620을 3등분)
        self.result_table.setColumnWidth(0, 300)
        self.result_table.setColumnWidth(1, 200)
        self.result_table.setColumnWidth(2, 120)
        # 테이블에 출력되는 검색결과를 더블클릭하면 수정할 수 있게 되어서 그걸 못하게 해주는 기능 추가
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, news in enumerate(newsResult): # enumerate에서 i는 여부터 9까지 변할 것임.
            newsTitle = news['title'] #뉴스제목
            newsTitle = newsTitle.replace('&quot','').replace(';','').replace('<b>','').replace('</b>','')
            newsLink = news['originallink'] # 뉴스의 오리지널 링크 url
            newsDate = news['pubDate'] # 뉴스게시일
            newsDate = newsDate[0:25]

            self.result_table.setItem(i, 0, QTableWidgetItem(newsTitle))
            self.result_table.setItem(i, 1, QTableWidgetItem(newsLink))
            self.result_table.setItem(i, 2, QTableWidgetItem(newsDate))

    def link_doubleClicked(self): # 링크를 더블클릭하면 호출되는 함수 만들기
        selectedRow = self.result_table.currentRow() # 현재 더블클릭하여 선택되어 있는 행의 인덱스를 가져온다.
        selectedLink = self.result_table.item(selectedRow, 1).text() #현재 더블클릭한 셀의 텍스트를 가져오게 된다. 열은 가운데로 고정
        webbrowser.open(selectedLink)



app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())


