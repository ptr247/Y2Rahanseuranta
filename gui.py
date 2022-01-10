from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox, QFormLayout, QFileDialog, QLineEdit, QCheckBox, QApplication, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt
from laskut import Laskut
import random


class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.lasku = ""

        self.outerLayout = QHBoxLayout()
        self.topLayout = QFormLayout()

        self.optionsLayout = QVBoxLayout()

        self.outerLayout.addLayout(self.topLayout)
        self.outerLayout.addLayout(self.optionsLayout)

        self.setLayout(self.outerLayout)





        self.init_window()
        self.init_examplechart()

        self.init_napit()
        self.init_lue()

    def init_examplechart(self):
        self.sarja = QPieSeries()
        lista1 = [[1,"Example1"], [2,"Example2"], [3,"Example3"], [4,"Example4"]]
        for i in lista1:
            self.sarja.append(i[1], i[0])

        self.slice = QPieSlice()
        self.slice = self.sarja.slices()[2]
        self.slice.setExploded(True)
        self.slice.setLabelVisible(False)
        self.slice.setPen(QPen(Qt.darkGreen, 2))
        self.slice.setBrush(Qt.green)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.sarja)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Piirakkamalli")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignLeft)


        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)

        self.topLayout.addWidget(self.chartview)


    def init_lue(self):
        self.lue = QPushButton("Lue uusi csv")
        self.lue.clicked.connect(self.lueklikattu)
        self.optionsLayout.addWidget(self.lue)

        self.yhdista = QPushButton("Yhdistä tilitapahtumia")
        self.yhdista.clicked.connect(self.yhdistaklikattu)
        self.optionsLayout.addWidget(self.yhdista)

        self.jaottelu = QCheckBox("Näytä luokittelematon")
        self.jaottelu.clicked.connect(self.jaotteluklikattu)
        self.optionsLayout.addWidget(self.jaottelu)
        self.jaottelu.setChecked(True)

    def jaotteluklikattu(self):

        try:
            if self.jaottelu.isChecked() == False:
                if self.lasku != "":

                    lista = Laskut.get_uusittulista(self.lasku)

                    if lista[0] != "" and len(lista) != 0:
                        self.init_chart(lista)
                    else:
                        alert = QMessageBox()
                        alert.setText("Tee luokittelu ensin")
                        alert.exec_()
                        self.jaottelu.setChecked(True)
                else:
                    alert = QMessageBox()
                    alert.setText("Tee luokittelu ensin")
                    alert.exec_()
                    self.jaottelu.setChecked(True)

            else:
                lista = Laskut.get_valmislista(self.lasku)

                self.init_chart(lista)

        except:
            alert = QMessageBox()
            alert.setText("Tee luokittelu ensin")
            alert.exec_()
            self.jaottelu.setChecked(True)



    def init_napit(self):
        self.tulot = QCheckBox("Näytä kokonaistulot")
        self.tulot.clicked.connect(self.tulotklikattu)

        self.menot = QCheckBox("Näytä kokonaismenot")
        self.menot.clicked.connect(self.menotklikattu)


        self.optionsLayout.addWidget(self.tulot)
        self.optionsLayout.addWidget(self.menot)

    def yhdistaklikattu(self):
        teksti, vastaus = QInputDialog.getText(self, "Luokittele tilitapahtumia", "Anna muodossa otsikko,tilitapahtuma,tilitapahtuma...")
        if vastaus == True:
            self.luokittele = teksti
            Laskut.luokittele(self.lasku, self.luokittele, self)






    def tulotklikattu(self):
        try:

            if self.tulot.isChecked() == True:


                self.kaikkitulot = QLabel()
                self.kaikkitulot.setText("Tulot: {}€".format(Laskut.get_tulot(self.lasku)))
                self.topLayout.addWidget(self.kaikkitulot)
            else:


                self.kaikkitulot.setParent(None)


        except:
            pass

    def menotklikattu(self):
        try:

            if self.menot.isChecked() == True:

                self.kaikkimenot = QLabel()
                self.kaikkimenot.setText("Menot: {}€".format(Laskut.get_menot(self.lasku)))
                self.topLayout.addWidget(self.kaikkimenot)
            else:

                self.kaikkimenot.setParent(None)


        except:
            pass


    def init_window(self):
        self.setGeometry(300,300,800,800)
        self.setWindowTitle("Rahanseuranta")
        self.show()

    def lueklikattu(self):
        alert = QFileDialog()
        self.tiedosto = alert.getOpenFileName(self, "Avaa CSV", 'c:\\',"CSV-tiedostot (*.csv)")

        if "" not in self.tiedosto:
            try:
                self.lasku = Laskut(self.tiedosto[0], self)
            except:
                virhe = QMessageBox()
                virhe.setText("Virhe tiedoston avaamisessa")
                virhe.exec_()




    def init_chart(self, lista):

        self.tulot.setChecked(False)
        self.menot.setChecked(False)



        self.topLayout.removeWidget(self.chartview)
        try:
            self.topLayout.removeWidget(self.kaikkitulot)
        except:
            pass
        try:
            self.topLayout.removeWidget(self.kaikkimenot)
        except:
            pass




        self.sarja = QPieSeries()
        for i in lista:
            slaissi = self.sarja.append(i[1] + " " + str("{:g}".format(float(i[0]))) + "€", i[0])
            slaissi.setBrush(QColor(random.randint(24,255),random.randint(24,255),random.randint(24,255),random.randint(24,255)))



        self.slice = QPieSlice()
        self.slice = self.sarja.slices()[random.randint(0,len(lista))-1]
        self.slice.setExploded(True)
        self.slice.setLabelVisible(False)
        self.slice.setPen(QPen(Qt.darkGreen,2))
        self.slice.setBrush(Qt.green)


        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.sarja)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Tilitapahtumat ladattu (Menot)")





        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignLeft)

        self.chartview = QChartView(self.chart)
        self.chartview.setRenderHint(QPainter.Antialiasing)


        self.topLayout.addWidget(self.chartview)

