from PyQt5.QtWidgets import *
import datetime
import DBAPI

class ShowOrderDetailWindow(QWidget):

    def __init__(self, orderNo):
        super().__init__()

        self.orderNo = orderNo

        self.query = DBAPI.DB_Queries()
        self.orderDetails = self.query.selectOrderDetailsByOrderNo(self.orderNo)

        self.setupUI()

    def setupUI(self):

        # 윈도우 설정
        self.setWindowTitle("주문 상세 내역")
        self.setGeometry(0, 0, 800, 500)

        # 위젯 생성
        self.orderDetailLbl = QLabel("주문 상세 내역")
        self.orderNoLbl1 = QLabel("주문번호:")
        self.orderNoLbl2 = QLabel("0")
        self.orderNoLbl2.setText(self.orderNo)
        self.productNumLbl1 = QLabel("상품개수:")
        self.productNumLbl2 = QLabel("0")
        self.productNumLbl2.setText(str(len(self.orderDetails)))
        self.sumOfOrderLbl1 = QLabel("주문액:")
        self.sumOfOrderLbl2 = QLabel("0")
        self.sumOfOrderLbl2.setText(str(sum([x['상품주문액'] for x in self.orderDetails])))
        self.fileOutputlLbl = QLabel("파일 출력")

        self.fileOutputRadioBtn1 = QRadioButton("CSV")
        self.fileOutputRadioBtn1.setChecked(True)
        self.fileOutputRadioBtn1.clicked.connect(self.fileOutputRadioBtn_Clicked)
        self.fileOutputRadioBtn2 = QRadioButton("JSON")
        self.fileOutputRadioBtn2.clicked.connect(self.fileOutputRadioBtn_Clicked)
        self.fileOutputRadioBtn3 = QRadioButton("XML")
        self.fileOutputRadioBtn3.clicked.connect(self.fileOutputRadioBtn_Clicked)
        self.dataFormat = "CSV"

        self.saveButton = QPushButton("저장")
        self.saveButton.clicked.connect(self.saveButton_Clicked)

        self.orderDetailTable = QTableWidget()
        self.orderDetailTable.setColumnCount(len(self.orderDetails[0]))
        columnNames = list(self.orderDetails[0].keys())
        self.orderDetailTable.setHorizontalHeaderLabels(columnNames)
        self.orderDetailTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.updateTable()

        # 레이아웃의 생성, 위젯 연결
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.orderNoLbl1)
        hLayout1.addWidget(self.orderNoLbl2)
        hLayout1.addWidget(self.productNumLbl1)
        hLayout1.addWidget(self.productNumLbl2)
        hLayout1.addWidget(self.sumOfOrderLbl1)
        hLayout1.addWidget(self.sumOfOrderLbl2)
        hLayout1.addStretch(1)

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.fileOutputRadioBtn1)
        hLayout2.addWidget(self.fileOutputRadioBtn2)
        hLayout2.addWidget(self.fileOutputRadioBtn3)
        hLayout2.addStretch(1)
        hLayout2.addWidget(self.saveButton)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.orderDetailLbl)
        vLayout.addLayout(hLayout1)
        vLayout.addWidget(self.orderDetailTable)
        vLayout.addWidget(self.fileOutputlLbl)
        vLayout.addLayout(hLayout2)

        self.setLayout(vLayout)

    def saveButton_Clicked(self):
        writeFile = DBAPI.WriteFile()

        if self.dataFormat == "CSV":
            writeFile.writeCSV(self.orderNo, self.orderDetails)
        elif self.dataFormat == "JSON":
            writeFile.writeJSON(self.orderNo, self.orderDetails)
        else:
            writeFile.writeXML(self.orderNo, self.orderDetails)


    def fileOutputRadioBtn_Clicked(self):
        if self.fileOutputRadioBtn1.isChecked():
            self.dataFormat = "CSV"
        elif self.fileOutputRadioBtn2.isChecked():
            self.dataFormat = "JSON"
        else:
            self.dataFormat = "XML"

    def updateTable(self):
        self.orderDetailTable.setRowCount(len(self.orderDetails))

        if len(self.orderDetails) > 0:
            self.orderDetails.sort(key=lambda x: x['orderLineNo'])

            for rowIDX, value in enumerate(self.orderDetails):
                for columnIDX, (k, v) in enumerate(value.items()):
                    if v == None:
                        continue
                    elif isinstance(v, datetime.date):
                        item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                    else:
                        item = QTableWidgetItem(str(v))

                    self.orderDetailTable.setItem(rowIDX, columnIDX, item)

        self.orderDetailTable.resizeColumnsToContents()
        self.orderDetailTable.resizeRowsToContents()