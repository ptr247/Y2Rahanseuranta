
from PyQt5.QtWidgets import QMessageBox

class Laskut():


    def __init__(self, tiedosto ,gui):
        self.tiedosto = tiedosto
        self.gui = gui
        self.avaa_tiedosto(self.tiedosto, self.gui)
        self.tulot = self.tulot
        self.menot = self.menot
        self.valmislista = self.valmislista
        self.uusittulista = ""

    def get_uusittulista(self):
        return self.uusittulista

    def get_tulot(self):
        return self.tulot

    def get_menot(self):
        return self.menot

    def get_tiedosto(self):
        return self.tiedosto

    def get_valmislista(self):
        return self.valmislista

    def avaa_tiedosto(self, tiedosto, gui):
        self.puhdaslista = []
        self.csv = open(tiedosto, "r")
        self.otsikko = self.csv.readline()
        self.tapahtumalista = self.csv.readlines()
        for i in self.tapahtumalista:
            i = i.strip()
            i = i.split(";")
            self.puhdaslista.append(i)

        self.piirakkalista = []
        self.tulot = 0
        self.menot = 0
        for i in self.puhdaslista:
            if i[1][0] == "-":
                lista = list(i[1][1:])
                if "," in lista:
                    index = lista.index(",")
                    lista[index] = "."
                    str = "".join(lista)

                self.menot = self.menot + float(str)
                self.piirakkalista.append([float(str), i[5]])
            else:
                lista = list(i[1])
                if "," in lista:
                    index = lista.index(",")
                    lista[index] = "."
                    str = "".join(lista)
                self.tulot = self.tulot + float(str)



        self.laskesamatyhteen(self.piirakkalista,gui)



    def laskesamatyhteen(self, lista, gui):
        self.yhteenlaskettu = {}
        self.valmislista = []
        for i in lista:
            if i[1] not in self.yhteenlaskettu:
                self.yhteenlaskettu[i[1]] = i[0]
            else:
                self.yhteenlaskettu[i[1]] = self.yhteenlaskettu[i[1]] + i[0]
        for i in self.yhteenlaskettu:
            self.valmislista.append([self.yhteenlaskettu[i],i])
        gui.jaottelu.setChecked(True)
        gui.init_chart(self.valmislista)


    def luokittele(self,str, gui):
        gui.jaottelu.setChecked(False)
        try:
            self.uusittulista = []
        except:
            pass
        try:
            for i in self.valmislista:
                self.uusittulista.append(i)
        except:
            pass
        try:
            lista = str.split(",")

            count = 0
            summa = 0
            self.otsikko = ""
            for i in lista:

                if count == 0:
                    self.otsikko = i
                else:
                    for x in self.valmislista:
                        if x[1] == i:
                            summa = summa + x[0]
                            self.uusittulista.remove(x)
                count = count + 1

            if summa != 0:
                self.uusittulista.append([summa, self.otsikko])
                gui.init_chart(self.uusittulista)
            else:
                alert = QMessageBox
                QMessageBox.setText("Virhe syötteessä")
                alert.exec_()



        except:
            alert = QMessageBox()
            alert.setText("Virhe syötteessä")
            alert.exec_()









