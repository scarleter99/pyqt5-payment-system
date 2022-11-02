from PyQt5.QtWidgets import *
import sys, datetime
import DBAPI, GUI_ShowOrderDetail

class SearchOrderWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.lastClicked = 'name'
        self.comboBoxValue = 'ALL'

        self.query = DBAPI.DB_Queries()
        self.orders = self.query.selectAllOrder()

        self.setupUI()

    def setupUI(self):
        # 윈도우 설정
        self.setWindowTitle("주문 검색")
        self.setGeometry(0, 0, 1500, 800)

        # 위젯 생성
        self.paymentSearchLbl = QLabel("주문 검색")
        self.nameLbl = QLabel("고객:")
        self.countryLbl = QLabel("국가:")
        self.cityLbl = QLabel("도시:")
        self.paymentNumLbl1 = QLabel("검색된 주문의 개수:")
        self.paymentNumLbl2 = QLabel("0")
        self.paymentNumLbl2.setText(str(len(self.orders)))

        self.nameComboBox = QComboBox()
        self.nameComboBox.activated[str].connect(self.nameComboBox_Activated)
        self.countryComboBox = QComboBox()
        self.countryComboBox.activated[str].connect(self.countryComboBox_Activated)
        self.cityComboBox = QComboBox()
        self.cityComboBox.activated[str].connect(self.cityComboBox_Activated)

        self.nameComboBox.addItem('ALL')
        self.countryComboBox.addItem('ALL')
        self.cityComboBox.addItem('ALL')

        self.names = self.query.selectAllName()
        self.countries = self.query.selectAllCountry()
        self.citys = self.query.selectAllCity()

        for name in self.names:
            for k, v in name.items():
                self.nameComboBox.addItem(v)

        for country in self.countries:
            for k, v in country.items():
                self.countryComboBox.addItem(v)

        for city in self.citys:
            for k, v in city.items():
                self.cityComboBox.addItem(v)

        self.searchButton = QPushButton("검색")
        self.searchButton.clicked.connect(self.searchButton_Clicked)
        self.resetButton = QPushButton("초기화")
        self.resetButton.clicked.connect(self.resetButton_Clicked)

        self.orderTable = QTableWidget()
        self.orderTable.cellClicked.connect(self.orderTable_CellClicked)
        self.orderTable.setColumnCount(len(self.orders[0]))
        columnNames = list(self.orders[0].keys())
        self.orderTable.setHorizontalHeaderLabels(columnNames)
        self.orderTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.updateTable()

        # 레이아웃의 생성, 위젯 연결
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.nameLbl)
        hLayout1.addWidget(self.nameComboBox,1)
        hLayout1.addWidget(self.countryLbl)
        hLayout1.addWidget(self.countryComboBox, 1)
        hLayout1.addWidget(self.cityLbl)
        hLayout1.addWidget(self.cityComboBox, 1)
        hLayout1.addWidget(self.searchButton)

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.paymentNumLbl1)
        hLayout2.addWidget(self.paymentNumLbl2, 1)
        hLayout2.addWidget(self.resetButton)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.paymentSearchLbl)
        vLayout.addLayout(hLayout1)
        vLayout.addLayout(hLayout2)
        vLayout.addWidget(self.orderTable)

        self.setLayout(vLayout)

    def nameComboBox_Activated(self, text):
        self.comboBoxValue = text
        self.lastClicked = 'name'

    def countryComboBox_Activated(self, text):
        self.comboBoxValue = text
        self.lastClicked = 'country'

        if self.comboBoxValue == 'ALL':
            citys = self.query.selectAllCity()
        else:
            citys = self.query.selectCityByCountry(self.comboBoxValue)

        self.cityComboBox.clear()

        print(citys)
        print(self.comboBoxValue)

        for city in citys:
            for k, v in city.items():
                self.cityComboBox.addItem(v)

    def cityComboBox_Activated(self, text):
        self.comboBoxValue = text
        self.lastClicked = 'city'

    def searchButton_Clicked(self):
        if self.comboBoxValue == 'ALL':
            self.orders = self.query.selectAllOrder()
        elif self.lastClicked == 'name':
            self.orders = self.query.selectOrderByName(self.comboBoxValue)
        elif self.lastClicked == 'country':
            self.orders = self.query.selectOrderByCountry(self.comboBoxValue)
        elif self.lastClicked == 'city':
            self.orders = self.query.selectOrderByCity(self.comboBoxValue)

        self.updateTable()
        self.paymentNumLbl2.setText(str(len(self.orders)))

    def resetButton_Clicked(self):
        self.nameComboBox.clear()
        self.countryComboBox.clear()
        self.cityComboBox.clear()

        self.nameComboBox.addItem('ALL')
        self.countryComboBox.addItem('ALL')
        self.cityComboBox.addItem('ALL')

        for name in self.names:
            for k, v in name.items():
                self.nameComboBox.addItem(v)

        for country in self.countries:
            for k, v in country.items():
                self.countryComboBox.addItem(v)

        for city in self.citys:
            for k, v in city.items():
                self.cityComboBox.addItem(v)

        self.lastClicked = 'name'
        self.comboBoxValue = 'ALL'
        self.searchButton_Clicked()

    def orderTable_CellClicked(self):
        orderNo = self.orderTable.item(self.orderTable.currentRow(), 0).text()
        self.showOrderDetailWindow = GUI_ShowOrderDetail.ShowOrderDetailWindow(orderNo)
        self.showOrderDetailWindow.show()

    def updateTable(self):
        self.orderTable.setRowCount(len(self.orders))

        if len(self.orders) > 0:
            for rowIDX, value in enumerate(self.orders):
                for columnIDX, (k, v) in enumerate(value.items()):
                    if v == None:
                        continue
                    elif isinstance(v, datetime.date):
                        item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                    else:
                        item = QTableWidgetItem(str(v))

                    self.orderTable.setItem(rowIDX, columnIDX, item)

        self.orderTable.resizeColumnsToContents()
        self.orderTable.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    searchOrderWindow = SearchOrderWindow()
    searchOrderWindow.show()
    app.exec_()