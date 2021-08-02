
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableView
import sqlite3



class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName("Table")
        Table.resize(1300, 700)
        

        hosp=sqlite3.connect('hospital_data.db')
        curs=hosp.cursor()
        curs.execute('Select count(*) from data')
        row=curs.fetchone()
        counts=row[0]
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        Table.setWindowIcon(icon)
        Table.setStyleSheet("background:url(icons/username_background.PNG);background-repeat: no-repeat;background-position: center;")
        self.centralwidget = QtWidgets.QWidget(Table)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(120, 11, 1100, 700))
        self.tableWidget.setStyleSheet("background:rgb(248,248,248)")
        self.tableWidget.setRowCount(counts)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(['ID','First Name','Last Name','Gender','Age','Blood Group','Contact No','Mail ID','Disease','Doctor','Result'])
        self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.tableWidget.setItem(0,0, QtWidgets.QTableWidgetItem('ID'))
        # self.tableWidget.setItem(0,1, QtWidgets.QTableWidgetItem('First Name'))
        # self.tableWidget.setItem(0,2, QtWidgets.QTableWidgetItem('Last Name'))
        # self.tableWidget.setItem(0,3, QtWidgets.QTableWidgetItem('Gender'))
        # self.tableWidget.setItem(0,4, QtWidgets.QTableWidgetItem('Age'))
        # self.tableWidget.setItem(0,5, QtWidgets.QTableWidgetItem('Blood Group'))
        # self.tableWidget.setItem(0,6, QtWidgets.QTableWidgetItem('Contact No'))
        # self.tableWidget.setItem(0,7, QtWidgets.QTableWidgetItem('Mail ID'))
        # self.tableWidget.setItem(0,8, QtWidgets.QTableWidgetItem('Disease'))
        # self.tableWidget.setItem(0,9, QtWidgets.QTableWidgetItem('Doctor'))

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "Patients Details"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Table = QtWidgets.QWidget()
    ui = Ui_Table()
    ui.setupUi(Table)
    Table.show()
    sys.exit(app.exec_())
