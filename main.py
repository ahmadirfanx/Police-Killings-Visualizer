import sys, random, csv
import os, matplotlib, numpy as np
from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pyqtgraph as pg
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries, QPieSeries, QPieSlice
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QPainter, QPen
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from scipy import stats
from scipy.stats import ttest_ind

class Ui(QtWidgets.QMainWindow):
    months=['January','February','March','April','May','June','July','August','September','October','November','December']
    monthIndex=list(range(0,12))
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('homePage.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'button1')
        self.button.clicked.connect(self.monthlyKillingsGraph)

        self.button = self.findChild(QtWidgets.QPushButton, 'button2')
        self.button.clicked.connect(self.raceBarChart)

        self.button = self.findChild(QtWidgets.QPushButton, 'button3')
        self.button.clicked.connect(self.create_RacialPiechart)

        self.button = self.findChild(QtWidgets.QPushButton, 'button4')
        self.button.clicked.connect(self.ageWiseBarGraph)

        self.button = self.findChild(QtWidgets.QPushButton, 'button5')
        self.button.clicked.connect(self.create_GenderPiechart)

        self.button = self.findChild(QtWidgets.QPushButton, 'button6')
        self.button.clicked.connect(self.create_StatePiechart)

        self.button = self.findChild(QtWidgets.QPushButton, 'button7')
        self.button.clicked.connect(self.create_fleeChart)

        self.button = self.findChild(QtWidgets.QPushButton, 'button8')
        self.button.clicked.connect(self.create_MentalillnessChart)

        self.button = self.findChild(QtWidgets.QPushButton, 'ViewStatsBtn')
        self.button.clicked.connect(self.ViewStatTools)

        self.button = self.findChild(QtWidgets.QPushButton, 'TtestBtn')
        self.button.clicked.connect(self.performTtestForMonths)

        #self.pushButton.clicked.connect(self.window2)

        self.show()

    def pressed(self):
        pass

    def monthlyKillingsGraph(self):
        monthlyKills=[0]*12 #BWHO
        with open('killings.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            yearSelect=str(self.yearSelector1.currentText())
            monthCount='1'
            for row in reader:
                if monthCount=='10' or monthCount=='11' or monthCount=='12':
                    nextMonth=monthCount+'/'+yearSelect
                else:
                    nextMonth= '0'+monthCount+'/'+yearSelect
                for m in monthlyKills:
                    if nextMonth in row[2]:
                        monthlyKills[int(monthCount)-1]+=1
                        break
                    monthCount= str(int(monthCount)+1)
                    if monthCount=='10' or monthCount=='11' or monthCount=='12':
                        nextMonth=monthCount+'/'+yearSelect
                    else:
                        nextMonth= '0' + monthCount+'/'+yearSelect
                monthCount='1'
        print (monthlyKills)
        self.plotGraph(self.monthIndex,monthlyKills)

    def compareTwoGroups_withTtest(self, arr_1, arr_2):
        stat, p = ttest_ind(arr_1, arr_2)
        return p

    def ViewStatTools(self):
        #Mean
        text = str(self.comboBox1.currentText())
        self.lineEdit.setText(str(round(self.findMean(), 2)))
        print(str(round(self.findMean(), 2)))
        #Median
        self.lineEdit2.setText(str(round(self.findMedian(), 2)))
        print(str(round(self.findMedian(), 2)))
        #Max
        self.lineEdit3.setText(str(round(self.findMax(), 2)))
        print(str(round(self.findMax(), 2)))
        #Min
        self.lineEdit4.setText(str(round(self.findMin(), 2)))
        print(str(round(self.findMean(), 2)))
        #StdDev
        self.lineEdit5.setText(str(round(self.findStd(), 2)))
        print(str(round(self.findStd(), 2)))

    def performTtestForMonths(self):
        year1=str(self.comboYear.currentText())
        year2=str(self.comboYear2.currentText())
        month1=str(self.comboMonth.currentText())
        month2=str(self.comboMonth2.currentText())
        file1=year1+'.csv'
        file2=year2+'.csv'
        kills1=[]
        kills2=[]
        kills1=self.retreiveMonthlyKills(month1, file1)
        kills2=self.retreiveMonthlyKills(month2, file2)
        print ('months check: ', kills1, kills2)
        stat, p = ttest_ind(kills1, kills2)
        text='The probability of the events being same: '+str(round(p, 2))
        if p>0.05:
            text+=' Based on the T-test, we say that the events are likely to be different'
        elif p<=0.05:
            text+= ' Based on the T-test, so we say that the events are not likely to be same'
        self.textEdit1.clear()
        self.textEdit1.insertPlainText(text)
        print (text)


    def retreiveMonthlyKills(self,month, filename):
        print (month, filename)
        monthlyKills=[0]* 30
        with open(filename,encoding = "ISO-8859-1") as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for row in csvReader:
                if row[6]==month and int(row[7])<=30:
                    monthlyKills[int(row[7])-1]+=1
        print ('monthlyKills for ', month , filename , ': ', monthlyKills)
        return monthlyKills

    def findYearlyKills(self, filename):
        months=['January','February','March','April','May','June','July','August','September','October','November','December']
        KillingList=[]
        kills=0
        with open(filename,encoding = "ISO-8859-1") as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for mon in months:
                with open(filename,encoding = "ISO-8859-1") as File:
                    csvReader = csv.reader(File)
                    next(csvReader)
                    for row in csvReader:
                        if row[6]==mon:
                            kills+=1
                    KillingList.append(kills)
                    kills=0
        return KillingList

    def PerformTtestForYears(self):
        killings15=[]
        killings16=[]
        d = os.path.dirname(__file__) # directory of script
        path1 = r'{}/CSVfiles/2015.csv'.format(d) # path to be created
        path2 = r'{}/CSVfiles/2016.csv'.format(d) # path to be created
        killings15= self.findYearlyKills(path1)
        killings16= self.findYearlyKills(path2)
        print ('killings: ', killings15, killings16)
        self.compareTwoGroups_withTtest(killings15, killings16)

    def findMean(self):
        values=[]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            for row in csvReader:
                values.append(row[5])
        values = list(map(int, values[1:]))
        return (np.mean(values[1:]))

    def findMax(self):
        values=[]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            for row in csvReader:
                values.append(row[5])
        values = list(map(int, values[1:]))
        return (np.max(values[1:]))

    def findMin(self):
        values=[]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            for row in csvReader:
                values.append(row[5])
        values = list(map(int, values[1:]))
        return (np.min(values[1:]))

    def findMedian(self):
        values=[]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            for row in csvReader:
                values.append(row[5])
        values = list(map(int, values[1:]))
        return (np.median(values[1:]))

    def findStd(self):
        values=[]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            for row in csvReader:
                values.append(row[5])
        values = list(map(int, values[1:]))
        return (np.std(values[1:]))

    def create_MentalillnessChart(self):
        file="killings.csv"
        illness=[0,0]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for row in csvReader:
                if row[10]=='TRUE':
                    illness[0]+=1
                else:
                    illness[1]+=1
        titles=['True', 'False']
        title='Signs of Mental Illness'
        self.create_piechart(titles, illness, 2, title)

    def create_fleeChart(self):
        file="killings.csv"
        flee = [0,0,0,0]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for row in csvReader:
                if row[12]== 'Not fleeing':
                    flee[0]+=1
                elif row[12]== 'Car':
                    flee[1]+=1
                elif row[12]=='Foot':
                    flee[2]+=1
                else:
                    flee[3]+=1
        self.w = Window2()
        self.w.show()
        set0 = QBarSet('Not Fleeing')
        set1 = QBarSet('Car')
        set2 = QBarSet('Foot')
        set3 = QBarSet('Other')
        file="killings.csv"
        #appending graph values here
        set0.append(flee[0])
        set1.append(flee[1])
        set2.append(flee[2])
        set3.append(flee[3])
        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Mode of Fleeing')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        msg = ('Flee')
        axisX = QBarCategoryAxis()
        axisX.append(msg)
        axisY = QValueAxis()
        axisY.setRange(0, 250)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QChartView(chart)
        self.w.setCentralWidget(chartView)

    def create_StatePiechart(self):
        file="killings.csv"
        states = [0,0,0,0,0]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for row in csvReader:
                if row[9]== 'CA':
                    states[0]+=1
                elif row[9]== 'TX':
                    states[1]+=1
                elif row[9]== 'FL':
                    states[2]+=1
                elif row[9]=='AZ':
                    states[3]+=1
                else:
                    states[4]+=1
        names=['California', 'Texas', 'Florida', 'Arizona', 'Other']
        title="State-wise Distribution"
        self.create_piechart(names, states, 5, title)

    def create_GenderPiechart(self):
        gender = [0,0]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for row in csvReader:
                if row[6]== 'M':
                    gender[0]+=1
                else:
                    gender[1]+=1
        titles=['Males', 'Females']
        title='Gnder Distribution'
        self.create_piechart(titles, gender,2, title)

    def create_RacialPiechart(self):
        names=['Black','White', 'Hispanic', 'Other']
        raceKill=[0,0,0,0] #BWHO
        with open('killings.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[7]=='B':
                    raceKill[0]+=1
                elif row[7]=='W':
                    raceKill[1]+=1
                elif row[7]=='H':
                    raceKill[2]+=1
                else:
                    raceKill[3]+=1
        title="Racial Distribution"
        self.create_piechart(names,raceKill,4, title)

    def create_piechart(self, names, appendList, rg, title):
        self.w = Window2()
        self.w.show()
        series = QPieSeries()
        print(names, appendList)
        for x in range(rg):
            series.append(names[x], appendList[x])
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(title)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.w.setCentralWidget(chartview)

    def ageWiseBarGraph(self):
        self.w = Window2()
        self.w.show()
        set0 = QBarSet('below 25')
        set1 = QBarSet('25 to 35')
        set2 = QBarSet('36 to 45')
        set3 = QBarSet('46 to 55')
        set4 = QBarSet('above 55')
        file="killings.csv"
        ageSet = [0,0,0,0,0]
        with open('killings.csv') as File:
            csvReader = csv.reader(File)
            next(csvReader)
            for row in csvReader:
                if int(row[5]) < 25:
                    ageSet[0]+=1
                elif int(row[5]) >=25 and int(row[5])<= 35:
                    ageSet[1]+=1
                elif int(row[5]) >35 and int(row[5])<=45:
                    ageSet[2]+=1
                elif int(row[5]) >45 and int(row[5])<= 55:
                    ageSet[3]+=1
                else:
                    ageSet[4]+=1
        print (ageSet)
        set0.append(ageSet[0])
        set1.append(ageSet[1])
        set2.append(ageSet[2])
        set3.append(ageSet[3])
        set4.append(ageSet[4])
        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Age wise comparison')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        msg = ('Death Toll')
        axisX = QBarCategoryAxis()
        axisX.append(msg)
        axisY = QValueAxis()
        axisY.setRange(0, 200)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QChartView(chart)
        self.w.setCentralWidget(chartView)

    def plotGraph(self, axisX, axisY):
        self.w = Window2()
        self.w.show()
        self.w.graphWidget = pg.PlotWidget()
        self.w.setCentralWidget(self.w.graphWidget)
        # plot data: x, y values
        self.w.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
        self.w.graphWidget.plot(axisX, axisY, symbol='+', symbolSize=30, symbolBrush=('b'))

    def raceBarChart(self):
        janKills=[0,0,0,0] #BWHO
        febKills=[0,0,0,0]
        marchKills=[0,0,0,0]
        aprilKills=[0,0,0,0]
        with open('killings.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if '01/15' in row[2]:
                    if row[7]=='B':
                        janKills[0]+=1
                    elif row[7]=='W':
                        janKills[1]+=1
                    elif row[7]=='H':
                        janKills[2]+=1
                    else:
                        janKills[3]+=1
                elif '02/15' in row[2]:
                    if row[7]=='B':
                        febKills[0]+=1
                    elif row[7]=='W':
                        febKills[1]+=1
                    elif row[7]=='H':
                        febKills[2]+=1
                    else:
                        febKills[3]+=1
                elif '03/15' in row[2]:
                    if row[7]=='B':
                        marchKills[0]+=1
                    elif row[7]=='W':
                        marchKills[1]+=1
                    elif row[7]=='H':
                        marchKills[2]+=1
                    else:
                        marchKills[3]+=1
                elif '04/15' in row[2]:
                    if row[7]=='B':
                        aprilKills[0]+=1
                    elif row[7]=='W':
                        aprilKills[1]+=1
                    elif row[7]=='H':
                        aprilKills[2]+=1
                    else:
                        marchKills[3]+=1
        finalAppend=[]
        finalAppend.append(janKills)
        finalAppend.append(febKills)
        finalAppend.append(marchKills)
        finalAppend.append(aprilKills)
        self.w = Window2()
        self.w.show()
        set0 = QBarSet('Black')
        set1 = QBarSet('White')
        set2 = QBarSet('Hispanic')
        set3 = QBarSet('Other')
        print(finalAppend)
        for x in range(4):
            set0.append(janKills[x])
        for x in range(4):
            set1.append(febKills[x])
        for x in range(4):
            set2.append(marchKills[x])
        for x in range(4):
            set3.append(aprilKills[x])
        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Monthly racial Death comparison')
        chart.setAnimationOptions(QChart.SeriesAnimations)
        months = ('Jan', 'Feb', 'Mar', 'Apr')
        axisX = QBarCategoryAxis()
        axisX.append(months)
        axisY = QValueAxis()
        axisY.setRange(0, 100)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QChartView(chart)
        self.w.setCentralWidget(chartView)

    def window2(self):                                             # <===
        self.w = Window2()
        self.w.show()


class Window2(QtWidgets.QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.title = "First Window"
        self.top = 300
        self.left = 500
        self.width = 600
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()