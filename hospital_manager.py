from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLabel, QMessageBox,QWidget
import welcome
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import QTimer,Qt
import sqlite3

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(68,68)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation=QLabel(self)
        self.movie=QMovie(r"loading.gif")
        self.label_animation.setMovie(self.movie)

        timer=QTimer(self)
        self.startAnimation()
        timer.singleShot(5000,self.stopAnimation)
        
        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()


class Ui_MainWindow(object):
    def __init__(self):
        self.count=0
        self.all_users=set()

    def showDialog(self,title,message):     # message box
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()
    
    def func_for_username(self):
        users={}
        hosp=sqlite3.connect('hospital_data.db')
        curs=hosp.cursor()
        curs.execute('Select * from Employee')
        rows=curs.fetchall()
        for row in rows:
            users[row[0]]=row[1]
        if self.username_text.text().lower() in users.keys() and self.username_text.text()!='' and self.pass_text.text()!='': 
            if self.pass_text.text()==users[self.username_text.text().lower()]:
                self.window=QtWidgets.QWidget()
                self.ui= welcome.Ui_Form()
                self.ui.setupUi(self.window)
                self.window.show()
                self.username_text.setText('')
                self.pass_text.setText('')
            else:
                self.count+=1
                if self.count<=2:
                    self.showDialog('ERROR','Please enter the correct password') 
                    self.pass_text.setText('')
                elif self.count>2:
                    self.showDialog('ERROR','You have reached your limit')
                    quit()
        elif self.username_text.text()=='' or self.pass_text.text()=='':
            self.showDialog('ERROR','Please fill the credentials!!')
        else:
            self.username_text.setText('')
            self.pass_text.setText('')
            self.showDialog('ERROR','No such user exists""\n Please enter a valid username')

    def func_for_register(self):
        import smtplib 
        import random
        dlg = QMessageBox()
        dlg.setWindowTitle('NOTE')
        dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dlg.setText(' You need to get the One time password in order to continue!!!')
        value=dlg.exec_()
        if value==1024:
            try:
                self.loading_screen=LoadingScreen()
                self.showDialog('Wait','Processing...\n\n\n\n\n\nPress Ok')
                
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls() 
                s.login("Your mail id", "Your password") 
                OTP=random.randint(1000,9999)
                message = f"Your One type Verification code is {OTP}"
                s.sendmail("Your mail id", "Reciever's  mail id", message) 
                s.quit()
                while(True):
                    one_time_pass, ok = QtWidgets.QInputDialog.getText(MainWindow, "OTP", "Please enter the OTP in order to continue:")
                    if ok==True:
                        if int(one_time_pass)==OTP:
                            while(True):
                                if ok==True:
                                    user_id, ok = QtWidgets.QInputDialog.getText(MainWindow, "USER ID", "Please enter the ID:")
                                    self.all_users.clear()
                                    hosp=sqlite3.connect('hospital_data.db')
                                    curs=hosp.cursor()
                                    curs.execute('Select * from Employee')
                                    rows=curs.fetchall()
                                    for row in rows:
                                        self.all_users.add(row[0])
                                    if user_id.strip().lower() not in self.all_users:
                                        break
                                    else:
                                        self.showDialog('ERROR','The User Id already exists!!!\n Please create account with different ID')
                                else:
                                    break
                            if ok==True:
                                password, ok = QtWidgets.QInputDialog.getText(MainWindow, "PASSWORD", "Please enter the Password:")
                                if ok==True:
                                    hosp=sqlite3.connect('hospital_data.db')
                                    curs=hosp.cursor()
                                    curs.execute(f"Insert into Employee Values('{user_id.strip().lower()}','{password}')")
                                    hosp.commit()
                                    self.showDialog('SUCCESS','Sucessfuly created you account\n Now you can login to the Hospital')
                                    self.username_text.setText('')
                                    self.pass_text.setText('')
                                    break
                                else:
                                    break
                            else:
                                break
                        else:
                            self.showDialog('ERROR','Wrong Password')
                    else:
                        break
            except:
                self.showDialog('ERROR','Please check your network connectivity and try again after sometime!!!')


    def func_for_forgot(self):
        import smtplib 
        import random
        dlg = QMessageBox()
        dlg.setWindowTitle('NOTE')
        dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dlg.setText(' You need to get the One time password in order to continue!!!')
        value=dlg.exec_()
        if value==1024:
            try:
                self.loading_screen=LoadingScreen()
                self.showDialog('Wait','Processing...\n\n\n\n\n\nPress Ok')
                
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls() 
                s.login("Your mail id", "Your passsword") 
                OTP=random.randint(1000,9999)
                message = f"Your One type Verification code is {OTP}"
                s.sendmail("Your mail id", "Reciever's mail id", message) 
                s.quit()
                while(True):
                    one_time_pass, ok = QtWidgets.QInputDialog.getText(MainWindow, "OTP", "Please enter the OTP in order to continue:")
                    if ok==True:
                        if int(one_time_pass)==OTP:
                            self.ids=set()
                            self.ids.clear()
                            hosp=sqlite3.connect('hospital_data.db')
                            curs=hosp.cursor()
                            curs.execute(f"Select [User Name] from Employee")
                            rows=curs.fetchall()
                            for row in rows:
                                self.ids.add(row[0])
                            while(True):
                                user_id, ok = QtWidgets.QInputDialog.getText(MainWindow, "ID", "Please enter your ID to continue:")
                                if ok==True:
                                    if user_id.lower() in self.ids:
                                        password, ok = QtWidgets.QInputDialog.getText(MainWindow, "PASSWORD", "Please enter the new password:")
                                        curs.execute(f"Update Employee Set Password='{password}' where [User Name]='{user_id.lower()}'")
                                        hosp.commit()
                                        break
                                    else:
                                        self.showDialog('ERROR','No such User exists!!!\n Please Enter a valid Username')
                                elif ok!=True:
                                    break
                            break
                        elif ok!=True:
                            break
                        else:
                            self.showDialog('ERROR','Wrong OTP!!!\n Please enter the correct OTP')
                    else:
                        break
            except:
                self.showDialog('ERROR','Please check your network connectivity and try again after sometime!!!')
            

            


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(735, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r"icons/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background:url(icons/username_background.PNG);background-repeat: no-repeat;background-position: center;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.forgot_pass = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.forgot_pass.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.forgot_pass.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.forgot_pass.setIconSize(QtCore.QSize(0, 0))
        self.forgot_pass.setObjectName("forgot_pass")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.forgot_pass.setFont(font)
        self.forgot_pass.setStyleSheet("background:rgb(255,233,236)")
        self.horizontalLayout_4.addWidget(self.forgot_pass)
        self.register = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.register.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.register.setIconSize(QtCore.QSize(0, 0))
        self.register.setObjectName("register")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.register.setFont(font)
        self.register.setStyleSheet("background:rgb(255,233,236)")
        self.horizontalLayout_4.addWidget(self.register)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.submit_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.submit_btn.setFont(font)
        self.submit_btn.setStyleSheet("background:rgb(255, 153, 245)")
        self.submit_btn.setObjectName("submit_btn")
        self.horizontalLayout_3.addWidget(self.submit_btn)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.username_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.username_label.setFont(font)
        self.username_label.setStyleSheet("background:rgb(251, 215, 255)")
        self.username_label.setObjectName("username_label")
        self.horizontalLayout.addWidget(self.username_label)
        spacerItem4 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.username_text = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.username_text.setFont(font)
        self.username_text.setStyleSheet("background:rgb(251, 215, 255)")
        self.username_text.setObjectName("username_text")
        # self.username_text.cursorPositionAt()
        self.horizontalLayout.addWidget(self.username_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pass_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pass_label.setFont(font)
        self.pass_label.setStyleSheet("background:rgb(251, 215, 255)")
        self.pass_label.setObjectName("pass_label")
        self.horizontalLayout_2.addWidget(self.pass_label)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.pass_text = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.pass_text.setFont(font)
        self.pass_text.setStyleSheet("background:rgb(251, 215, 255)")
        self.pass_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_text.setObjectName("pass_text")
        self.horizontalLayout_2.addWidget(self.pass_text)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 2)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 4, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem9, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.submit_btn.clicked.connect(self.func_for_username)
        self.submit_btn.setShortcut('Ctrl+Return')
        self.forgot_pass.clicked.connect(self.func_for_forgot)
        self.register.clicked.connect(self.func_for_register)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Staff Login Page"))
        self.username_label.setText(_translate("MainWindow", "Enter your User ID:        "))
        self.pass_label.setText(_translate("MainWindow", "Enter your Password:    "))
        self.submit_btn.setText(_translate("MainWindow", "Submit"))
        self.forgot_pass.setText(_translate("MainWindow", "     Forgot Your Password"))
        self.register.setText(_translate("MainWindow", "                Register"))



if __name__ == "__main__":
    import sys 
    welcome.app
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(welcome.app.exec_())
