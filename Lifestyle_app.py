#!/usr/bin/env python3.8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication, QUrl, QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
#Py file from Github
import gather_keys_oauth2 as Oauth2
#external
import pandas as pd
#external
import fitbit
import sys
import sqlite3
from datetime import datetime, timedelta



#Get today's date
dow = datetime.today().strftime("%d/%m/%Y")
fitbitFormat = datetime.strftime(datetime.now(), '%Y-%m-%d')

# Global variables for SQLite function
date = dow
alcoG = 'n/a'
fruity = 'n/a'
systol = 'n/a'
diastol = 'n/a'
weight = 'n/a'
sleep = 'n/a'
wake = 'n/a'
goal = 'no goal'


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carebot")
        self.setGeometry(350, 350, 600, 600)
        self.UI()

    def UI(self):

        mainLayout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.tabAlco = QTabWidget()
        self.tabFruit = QTabWidget()
        self.tabFit = QTabWidget()
        self.tabDialog = QTabWidget()
        self.tabBP = QTabWidget()
        self.tabMH = QTabWidget()

        self.tabs.addTab(self.tabAlco, "Alcohol")
        self.tabs.addTab(self.tabFruit, "Fruit")
        self.tabs.addTab(self.tabBP, "Bloodpressure")
        self.tabs.addTab(self.tabFit, "Sleep and weight")
        self.tabs.addTab(self.tabDialog, "Goals")


        ##############################################

        # Alcohol slider on main tab
        vboxAlco = QVBoxLayout()
        self.mySlider = QSlider(Qt.Horizontal)
        vboxAlco.addWidget(self.mySlider)
        self.mySlider.setMinimum(0)
        self.mySlider.setMaximum(12)
        self.mySlider.setTickPosition(QSlider.TicksBelow)
        self.mySlider.setTickInterval(1)
        self.mySlider.valueChanged.connect(self.getValue)

        # Question text
        self.yestertext = QLabel("How many Beers did you have yesterday?")
        yesterfont = QFont("Roboto", 20)
        self.yestertext.setFont(yesterfont)
        self.yestertext.setAlignment(Qt.AlignCenter)
        vboxAlco.addWidget(self.yestertext)

        # Slider value label
        self.alcotext = QLabel("0 Beers")
        alcofont = QFont("Roboto", 30)
        self.alcotext.setFont(alcofont)
        self.alcotext.setAlignment(Qt.AlignCenter)
        vboxAlco.addWidget(self.alcotext)

        # Icon
        self.image = QLabel(self)
        pixmap = QPixmap("/Users/oliverjones/Desktop/Carebot_App/my_app_images/beer.png")
        smaller_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.image.setPixmap(smaller_pixmap)
        self.image.setAlignment(Qt.AlignCenter)
        vboxAlco.addWidget(self.image)

        # adding hbox layout to vbox for the submit button
        hboxbtn = QHBoxLayout()
        hboxbtn.addStretch()
        vboxAlco.addLayout(hboxbtn)

        self.newbtn = QPushButton("Submit")
        self.newbtn.clicked.connect(self.AlcoVal)
        self.newbtn.clicked.connect(self.UpdatedPop)
        hboxbtn.addWidget(self.newbtn)

        self.savebtn = QPushButton("Save input")
        self.savebtn.setFont(QFont("Roboto",20))
        self.savebtn.clicked.connect(self.SaveFunc)
        hboxbtn.addWidget(self.savebtn)

        # assign to tab
        self.tabAlco.setLayout(vboxAlco)

        #############################################

        # Fruit slider
        vboxF = QVBoxLayout()
        self.mySliderF = QSlider(Qt.Horizontal)
        vboxF.addWidget(self.mySliderF)
        self.mySliderF.setMinimum(0)
        self.mySliderF.setMaximum(6)
        self.mySliderF.setTickPosition(QSlider.TicksBelow)
        self.mySliderF.setTickInterval(1)
        self.mySliderF.valueChanged.connect(self.getFruitValue)

        # adding hbox layout to vbox for the submit button
        hboxbtnF = QHBoxLayout()
        hboxbtnF.addStretch()
        vboxF.addLayout(hboxbtnF)

        self.newbtnF = QPushButton("Submit")
        self.newbtnF.clicked.connect(self.printfruitVal)
        self.newbtnF.clicked.connect(self.UpdatedPop)
        hboxbtnF.addWidget(self.newbtnF)

        # Question text
        self.yesterFtext = QLabel("How many portions of fruit and veg did you have yesterday?")
        yesterFfont = QFont("Roboto", 16)
        self.yesterFtext.setFont(yesterFfont)
        self.yesterFtext.setAlignment(Qt.AlignCenter)
        vboxF.addWidget(self.yesterFtext)

        # Slider value label
        self.fruittext = QLabel("0 Portions")
        fruitfont = QFont("Roboto", 30)
        self.fruittext.setFont(fruitfont)
        self.fruittext.setAlignment(Qt.AlignCenter)
        vboxF.addWidget(self.fruittext)

        # Icon
        self.imageF = QLabel(self)
        pixmapF = QPixmap("/Users/oliverjones/Desktop/Carebot_App/my_app_images/vegetable-icon.png")
        smaller_pixmapF = pixmapF.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.imageF.setPixmap(smaller_pixmapF)
        self.imageF.setAlignment(Qt.AlignCenter)
        vboxF.addWidget(self.imageF)


        # assign to tab
        self.tabFruit.setLayout(vboxF)

        ##############################################

        # Bloodpressure tab
        vboxBP = QVBoxLayout()
        self.bptext = QLabel("Record blood pressure")
        self.BPtarget = QLabel("Goal = 130/75")
        BPfont = QFont("Roboto", 20)
        self.BPtarget.setFont(BPfont)
        self.mySysinput = QTextEdit()
        self.mySysinput.setFixedHeight(25)
        self.mySysinput.setFixedWidth(100)
        self.myDiainput = QTextEdit()
        self.myDiainput.setFixedHeight(25)
        self.myDiainput.setFixedWidth(100)

        hboxbtnBP = QHBoxLayout()
        hboxbtnBP.addStretch()
        vboxBP.addLayout(hboxbtnBP)
        self.BPbtn = QPushButton("Submit")
        self.BPbtn.clicked.connect(self.printBPVal)
        self.BPbtn.clicked.connect(self.UpdatedPop)
        hboxbtnBP.addWidget(self.BPbtn)

        vboxBP.addWidget(self.bptext)
        vboxBP.addWidget(self.mySysinput)
        vboxBP.addWidget(self.myDiainput)
        vboxBP.addWidget(self.BPtarget)

        self.BPimage = QLabel(self)
        pixmap = QPixmap("/Users/oliverjones/Desktop/Carebot_App/my_app_images/Blood_pressure _image.png")
        smaller_pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.BPimage.setPixmap(smaller_pixmap)
        self.BPimage.setAlignment(Qt.AlignCenter)
        vboxBP.addWidget(self.BPimage)

        self.tabBP.setLayout(vboxBP)

        ##############################################

        # Fitbit tab
        hboxW = QHBoxLayout()
        self.fitbtn = QPushButton("Get sleep data")
        self.fitbtn.clicked.connect(self.mysleepFunc1)
        hboxW.addWidget(self.fitbtn)

        self.sleeptext = QLabel("Asleep at: \n Unknown")
        sleepfont = QFont("Roboto", 12)
        self.sleeptext.setFont(sleepfont)
        self.sleeptext.setAlignment(Qt.AlignCenter)
        hboxW.addWidget(self.sleeptext)

        self.waketext = QLabel("Awake at: \n Unknown")
        wakefont = QFont("Roboto", 12)
        self.waketext.setFont(wakefont)
        self.waketext.setAlignment(Qt.AlignCenter)
        hboxW.addWidget(self.waketext)

        vboxW = QVBoxLayout()
        vboxW.addStretch()
        self.weighttxt = QLabel("Record weight (Kg)")
        vboxW.addWidget(self.weighttxt)

        self.myWinput = QTextEdit()
        self.myWinput.setFixedWidth(50)
        self.myWinput.setFixedHeight(25)
        vboxW.addWidget(self.myWinput)
        self.weightbtn = QPushButton("Submit")
        self.weightbtn.clicked.connect(self.myweightFunc)
        self.weightbtn.clicked.connect(self.UpdatedPop)
        vboxW.addWidget(self.weightbtn)

        self.fit_image = QLabel(self)
        pixmap = QPixmap("/Users/oliverjones/Desktop/Carebot_App/my_app_images/fitbit.png")
        smaller_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.fit_image.setPixmap(smaller_pixmap)
        self.fit_image.setAlignment(Qt.AlignBaseline)
        vboxW.addWidget(self.fit_image)

        hboxW.addLayout(vboxW)

        # assign to tab
        self.tabFit.setLayout(hboxW)

        ##############################################

        # Goals tab with dialog box
        vboxD = QVBoxLayout()
        self.Goaleditor = QTextEdit()
        vboxD.addWidget(self.Goaleditor)

        hboxD = QHBoxLayout()
        vboxD.addLayout(hboxD)
        hboxD.addStretch()

        self.well_image = QLabel(self)
        pixmap = QPixmap("/Users/oliverjones/Desktop/Carebot_App/my_app_images/Target-Image.png")
        smaller_pixmap = pixmap.scaled(230, 230, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.well_image.setPixmap(smaller_pixmap)
        self.well_image.setAlignment(Qt.AlignCenter)
        hboxD.addWidget(self.well_image)

        fileButton = QPushButton("Open file")
        fileButton.clicked.connect(self.openFile)
        hboxD.addWidget(fileButton)
        hboxD.addStretch()

        writeButton = QPushButton("Update file")
        writeButton.clicked.connect(self.getDialogtxt)
        writeButton.clicked.connect(self.UpdatedPop)
        hboxD.addWidget(writeButton)
        self.tabDialog.setLayout(vboxD)



        ##############################################

        # add all the tabs to the mainlayout
        mainLayout.addWidget(self.tabs)
        self.setLayout(mainLayout)
        self.show()

        ##############################################

    def mysleepFunc1(self):
        CLIENT_ID = '****'
        CLIENT_SECRET = '************************'

        server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
        server.browser_authorize()
        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
        auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                                     refresh_token=REFRESH_TOKEN)

        """Sleep data on the night of ...."""
        #set date to yesterday
        fit_statsSl = auth2_client.sleep(date=f'{fitbitFormat}')
        stime_list = []
        sval_list = []
        try:
            for i in fit_statsSl['sleep'][0]['minuteData']:
                stime_list.append(i['dateTime'])
                sval_list.append(i['value'])
            sleepdf = pd.DataFrame({'State': sval_list,
                                    'Time': stime_list})
            sleepdf['Interpreted'] = sleepdf['State'].map({'2': 'Awake', '3': 'Very Awake', '1': 'Asleep'})

            sleepdf = sleepdf.Time

            sleepdfH = sleepdf.head(1)
            sleepdfT = sleepdf.tail(1)

            bedtime = sleepdfH.to_string(index=False)
            wakeup = sleepdfT.to_string(index=False)

            self.sleeptext.setText(str(f"Asleep at \n {bedtime}"))
            global sleep
            sleep = bedtime
            self.waketext.setText(str(f"Awake at \n {wakeup}"))
            global wake
            wake = wakeup
        except IndexError:
            self.sleeptext.setText("Sync fitbit")
            self.waketext.setText("Sync fitbit")



    def myweightFunc(self):
        myWVal = self.myWinput.toPlainText()
        print(myWVal)
        global weight
        weight = myWVal

    def getValue(self):
        myVal = self.mySlider.value()
        if myVal == 1:
            self.alcotext.setText(str(f"{myVal} Beer"))
        elif myVal != 1:
            self.alcotext.setText(str(f"{myVal} Beers"))

    def getFruitValue(self):
        myFVal = self.mySliderF.value()
        if myFVal == 1:
            self.fruittext.setText(str(f"{myFVal} fruit/veg portion"))
        elif myFVal != 1:
            self.fruittext.setText(str(f"\n {myFVal} fruit/veg portions"))

    def AlcoVal(self):
        myVal = self.mySlider.value()
        print(myVal)
        global alcoG
        alcoG = myVal

    def printfruitVal(self):
        myValF = self.mySliderF.value()
        print(myValF)
        global fruity
        fruity = myValF

    def printBPVal(self):
        mySysVal = self.mySysinput.toPlainText()
        myDiaVal = self.myDiainput.toPlainText()
        print(mySysVal)
        global systol
        systol = mySysVal

        print(myDiaVal)
        global diastol
        diastol = myDiaVal

    def openFile(self):
        url = QFileDialog.getOpenFileName(self, "Open a file", "p", "All Files(*);;*txt")
        fileUrl = url[0]
        try:
            file = open(fileUrl, 'r')
        except OSError:
            return print("Must select a file!")

        content = file.read()
        self.Goaleditor.setText(content)

    def getDialogtxt(self):
        myDialogVal = self.Goaleditor.toPlainText()
        print(myDialogVal)
        global goal
        goal = myDialogVal
  
    def UpdatedPop(self):
        UpdateM = QMessageBox.information(self, "Info",
                                          "Submitted! Click save input on the Alcohol tab to store value in database")

    def SaveFunc(self):
        connection = sqlite3.connect('Carebot1_sql.db')
        cursor = connection.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS Carebot
                        (PID INTEGER PRIMARY KEY,
                          DATE INT,
                          ALCOHOL INT,
                          FRUIT INT,
                          SYSTOLIC INT,
                          DIASTOLIC INT,
                          WEIGHT INT,
                          SLEEP INT,
                          WAKE INT,
                          GOALS VARCHAR(500),'''

        cursor.execute(sql)
        sql = f"INSERT INTO Carebot (DATE, ALCOHOL,FRUIT,SYSTOLIC,DIASTOLIC,WEIGHT,SLEEP,WAKE,GOALS) VALUES ('{date}','{alcoG}','{fruity}','{systol}','{diastol}','{weight}','{sleep}','{wake}','{goal}')"
        cursor.execute(sql)
        connection.commit()
        sql = 'SELECT * FROM Carebot'
        cursor.execute(sql)

        rows = cursor.fetchall()
        for row in rows:
            print(row)

        connection.close()

        #close window
        self.close()



def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())


if __name__ == '__main__':
    main()
