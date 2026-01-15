from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLCDNumber, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

import os
import math
from tyylit import Tyylit as T

#Laskin käyttäen PySide6:tta
#Kaikki ominaisuudet määritellään Laskin-luokassa.

class Laskin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Koiralaskin")
        

        pääpaneeli = QWidget()
        self.setCentralWidget(pääpaneeli)
        self.tunnuskuva()
        self.määritä_valikko()
        self.määritä_widgetit()
        self.asettelu(pääpaneeli)
        self.setWindowIcon(QIcon(self.koirakuva))
        self.setStyleSheet(T.tyyli1)

    # Luodaan asettelut, joihin lisätään widgetit asettelut-funktiossa.

    def asettelu(self, paneeli):
        self.pääasettelu = QGridLayout(paneeli)
        self.näppäimistö = QGridLayout()
        self.napit_vasen_puoli = QGridLayout()
        self.napit_oikea_puoli = QGridLayout()
        self.asettelut()

    # Luodaan ylävalikko, josta voidaan valita teema ja poistua.

    def määritä_valikko(self):
        valikko = self.menuBar()

        asetukset = valikko.addMenu("Asetukset")
        sulje = valikko.addAction("Poistu")
        sulje.triggered.connect(lambda: self.sammutus())
        
        värit = asetukset.addMenu("Värit")
        väriteema1 = värit.addAction("Harmaa")
        väriteema2 = värit.addAction("Pinkki")
        väriteema3 = värit.addAction("Cessu")

        väriteema1.triggered.connect(lambda: self.valitse_teema(T.tyyli1))
        väriteema2.triggered.connect(lambda: self.valitse_teema(T.tyyli2))
        väriteema3.triggered.connect(lambda: self.valitse_teema(T.tyyli3))
    
    # Tässä funktiossa valitaan teema tyylit.py -tiedostosta.
    # @param stylesheet tyylit.py -tiedostosta

    def valitse_teema(self, tyyli):
        ikkuna = self.window()
        if tyyli == T.tyyli3:
            # Teemaan lisätty koira koristeeksi.
            ikkuna.setStyleSheet(tyyli)
            ikkuna.centralWidget().setStyleSheet(tyyli)
            self.yhtakuinnappi.setIcon(QIcon(self.koirakuva))
            ikkuna.update()
        else:
            ikkuna.setStyleSheet(tyyli)
            ikkuna.centralWidget().setStyleSheet(tyyli)
            self.yhtakuinnappi.setIcon(QIcon())
            ikkuna.update()
    
    #Tehdään tunnuskuva, jota käytetään myös yhdessä tyyleistä.
    
    def tunnuskuva(self):
        self.koirakuva = os.path.join(os.path.dirname(__file__), "pienikoira.ico")
        self.koirakuva = self.koirakuva.replace("\\", "/")
        
    #Tämä funktio kokoaa kaikki määritellyt widgetit ja toiminnallisuudet.

    def määritä_widgetit(self):
        self.määritä_näyttö()
        self.määritä_apumuuttujat()
        self.määritä_otsikko()
        self.määritä_nappulat()
        self.nappifunktiot()


    def määritä_näyttö(self):
        self.näyttö = QLCDNumber(10)
        self.näyttö.display("0")

    #Määritellään muuttujia laskimen tilan hallintaa varten.

    def määritä_apumuuttujat(self):
        self.syöte = ""
        self.nykyinen_arvo = 0.0
        self.nollaa = True
        self.odottava_operaatio = None

    #Määritellään teksti ja tyyli
    def määritä_otsikko(self):
        self.otsikko = QLabel("Nelilaskin")
        self.otsikko.setAlignment(Qt.AlignCenter)

    def määritä_nappulat(self):
        
        self.ykkönen = QPushButton("1")
        self.kakkonen = QPushButton("2")
        self.kolmonen = QPushButton("3")
        self.nelonen = QPushButton("4")
        self.vitonen = QPushButton("5")
        self.kutonen = QPushButton("6")
        self.seiska = QPushButton("7")
        self.kasi = QPushButton("8")
        self.ysi = QPushButton("9")
        self.nolla = QPushButton("0")

        self.lisäänappi = QPushButton("+")
        self.miinusnappi = QPushButton("-")
        self.kertonappi = QPushButton("x")
        self.jakonappi = QPushButton("/")
        self.neliöjuurinappi = QPushButton("√")

        self.yhtakuinnappi = QPushButton("=")
        self.yhtakuinnappi.setObjectName("Yhtakuin")
        self.pilkku = QPushButton(",")
        self.negaationappi = QPushButton("+/-")
        self.tyhjennä = QPushButton("C")
        self.takaisinnappi = QPushButton("DEL")
        

    #Määritellään, mikä on kunkin painikkeen funktio.

    def nappifunktiot(self):
        
        #Numeronäppäimet
        self.nolla.clicked.connect(lambda: self.lisää_numero(self.nolla))
        self.ykkönen.clicked.connect(lambda: self.lisää_numero(self.ykkönen))
        self.kakkonen.clicked.connect(lambda: self.lisää_numero(self.kakkonen))
        self.kolmonen.clicked.connect(lambda: self.lisää_numero(self.kolmonen))
        self.nelonen.clicked.connect(lambda: self.lisää_numero(self.nelonen))
        self.vitonen.clicked.connect(lambda: self.lisää_numero(self.vitonen))
        self.kutonen.clicked.connect(lambda: self.lisää_numero(self.kutonen))
        self.seiska.clicked.connect(lambda: self.lisää_numero(self.seiska))
        self.kasi.clicked.connect(lambda: self.lisää_numero(self.kasi))
        self.ysi.clicked.connect(lambda: self.lisää_numero(self.ysi))

        #Laskutoimitukset
        self.lisäänappi.clicked.connect(lambda: self.laskutoimitus(self.lisäänappi.text()))
        self.miinusnappi.clicked.connect(lambda: self.laskutoimitus(self.miinusnappi.text()))
        self.kertonappi.clicked.connect(lambda: self.laskutoimitus(self.kertonappi.text()))
        self.jakonappi.clicked.connect(lambda: self.laskutoimitus(self.jakonappi.text()))
        self.neliöjuurinappi.clicked.connect(lambda: self.laskutoimitus(self.neliöjuurinappi.text()))
        
        #Muut näppäimet
        self.yhtakuinnappi.clicked.connect(lambda: self.on_yhtä_kuin())
        self.pilkku.clicked.connect(lambda: self.lisää_pilkku())
        self.negaationappi.clicked.connect(lambda: self.negaatio())
        self.tyhjennä.clicked.connect(lambda: self.nollaa_näyttö())
        self.takaisinnappi.clicked.connect(lambda: self.kumita())

    def lisää_numero(self, nappula):

        #Estetään peräkkäiset nollat
        if (self.syöte == "" or self.syöte == "0") and nappula.text() == "0":
            return
        
        #Näytetään ensimmäinen numero
        if self.nollaa == True:
            self.syöte = nappula.text()
            self.nollaa = False

        elif self.syöte == "0":
            self.syöte = nappula.text()

        #Lisätään nappulan numero näytölle
        else:
            uusi_arvo = self.syöte+nappula.text()
            if len(uusi_arvo)>9:
                print("Liian pitkä")
                return
            self.syöte+=nappula.text()
        
        self.päivitä_näyttö()


    def lisää_pilkku(self):

        #Lisätään pilkku nollan tai "tyhjän syötteen" perään
        if self.nollaa == True:
            self.syöte = "0."
            self.nollaa = False
        #Ei lisätä pilkkua syötteen viimeiseksi merkiksi
        elif len(self.syöte) == 8:
            return
        #Lisätään pilkku muihin, jos ei ole jo pilkkua
        elif "." not in self.syöte:
            uusi_arvo=self.syöte+"."
            if len(uusi_arvo)>9:
                print("Liian pitkä")
                return
            self.syöte+="."
        
        self.päivitä_näyttö()

    # Kutsuu ehdollisesti laske-funktiota ja päivittää odottavan laskutoimituksen ja tarvittaessa nykyisen arvon.
    # @param laskutoimitus

    def laskutoimitus(self, operaatio):

        #Virheentarkistus
        if self.syöte == "Err" or not self.syöte:
            return
        elif "E" in self.syöte:
            self.syöte = self.syöte[:-1]+"0"
        
        arvo = float(self.syöte) if self.syöte else 0.0

        if self.odottava_operaatio:
            self.nykyinen_arvo = self.laske(
                self.nykyinen_arvo, arvo, self.odottava_operaatio
            )
        else:
            self.nykyinen_arvo = arvo
        
        #Erityistapaus, neliöjuuri, vain yksi operandi ja välitön piirto näytölle

        if operaatio == "√" and self.syöte != "" and self.syöte != "0" and "-" not in self.syöte and "r" not in self.syöte:
            temp = self.syöte
            self.syöte = "r"+str(self.nykyinen_arvo)

            if len(self.syöte)<=9:
                self.näyttö.display(self.syöte)
                self.odottava_operaatio = operaatio
                self.nollaa = True
                self.syöte = temp
                return
            else:
                self.syöte = temp
        elif operaatio == "√" and "-" in self.syöte:
            self.nollaa_näyttö()
            self.syöte = "Err"
            self.päivitä_näyttö()

        self.odottava_operaatio = operaatio

        self.nollaa = True
        self.päivitä_näyttö()

    # Suorittaa laskutoimitukset.
    # @param self, ensimmäinen operandi, toinen operandi, laskutoimitus

    def laske(self, a, b, operaatio):

        #Virheentarkistus syötteessä
        if a == "Err" or not a:
            return
        
        #Perus aritmetiikka
        match operaatio:
            case "+": return a + b
            case "-": return a - b
            case "x": return a * b
        self.päivitä_näyttö()

        #Virheentarkistus jakolaskussa
        if operaatio == "/" and b != 0:
            return a / b
        elif operaatio == "/" and b == 0:
            print("Virhe")
            self.nollaa_välimuisti()
            self.syöte = "0"
            return "Err"
        
        #Neliöjuuren virheenhallintalogiikka on laskutoimitus-funktiossa, koska se vaatii välittömän piirron näytölle, eikä käytä montaa operandia.

        elif operaatio == "√":
            self.päivitä_näyttö()
            return math.sqrt(a)
        
    # Kutsuu laske-funktiota
    # Päivittää ja näyttää laskutoimituksen tuloksen

    def on_yhtä_kuin(self):

        if not self.odottava_operaatio:
            return
        if self.syöte == "Err" or not self.syöte:
            return
        arvo = float(self.syöte) if self.syöte else 0.0
        tulos = self.laske(self.nykyinen_arvo, arvo, self.odottava_operaatio)
        
        #Pyöristys ja virheenhallinta

        if len(str(tulos))>9:

            tulos = str(tulos)

            if str(tulos)[8] == ".":
                tulos = tulos[0:8]+"E"
                print("Liian pitkä")
                self.näyttö.display(tulos)
                self.nollaa_välimuisti()
                self.syöte = tulos[0:7]+"00"
            if str(tulos)[-2] == ".":
                tulos = tulos[0:9]+"E"
                print("Liian pitkä")
                self.näyttö.display(tulos)
                self.nollaa_välimuisti()
                self.syöte = tulos[0:9]+"0"
            else:
                self.nollaa_välimuisti()
                self.syöte = tulos[0:10]
                self.näyttö.display(self.syöte)
            return

        #Joskus tulee tapaus, kun tulokseksi tulee 'None' tai tyhjä merkkijono tai ei määritelty (0/0).
        #Käsitellään tapaus.

        if not tulos:
            tulos = "0"
            self.nollaa_välimuisti()
            self.päivitä_näyttö()
        
        #Jos tulos on laillinen

        else:
            self.syöte = str(tulos)
            self.nollaa_välimuisti()
            self.päivitä_näyttö()
            #print(tulos)

    # Funktiot eri toiminnallisuuksille

    def negaatio(self):
        if self.syöte == "Err" or not self.syöte:
            return
        self.syöte = int(self.syöte)*-1 if self.syöte else "-0"
        self.syöte = str(self.syöte)
        self.päivitä_näyttö()
    
    def kumita(self):
        if not self.syöte:
            return
        elif self.syöte == "Err" or self.syöte == "None":
            self.syöte = "0"
        elif len(self.syöte)<2:
            self.syöte = "0"
        elif self.syöte[-2] == "." or self.syöte[-2] == "-":
            self.syöte = self.syöte[:-2]
        else:
            self.syöte = self.syöte[:-1]
        self.päivitä_näyttö()

    def päivitä_näyttö(self):
        self.näyttö.display(self.syöte if self.syöte else "0")

    def nollaa_välimuisti(self):
        self.odottava_operaatio = None
        self.nollaa = True
        self.operaatio = ""
        
    def nollaa_näyttö(self):
        self.nollaa_välimuisti()
        self.syöte = ""
        self.nykyinen_arvo = 0.0
        self.päivitä_näyttö()
    
    # Sammutusfunktio mukautetuilla nappuloilla ja teksteillä
    # Luodaan QMessageBox-ikkuna.

    def sammutus(self):
        exitlaatikko = QMessageBox()
        exitlaatikko.setIcon(QMessageBox.Question)
        exitlaatikko.setWindowTitle("Sammutus")
        exitlaatikko.setText("Suljetaanko laskin?")
        exitlaatikko.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        kylläpainike = exitlaatikko.button(QMessageBox.Yes)
        kylläpainike.setText("Kyllä")
        eipainike = exitlaatikko.button(QMessageBox.No)
        eipainike.setText("Ei")
        exitlaatikko.exec()

        if exitlaatikko.clickedButton() == kylläpainike:
            self.close()
            print("Suljetaan...")
        else:
            pass
    
    # Funktio, jossa määritellään widgettien paikat asettelussa. Asettelu on tehty nelilaskimen tyyliseksi.
    # Lisäksi säädetään hieman asettelujen kokoja.
    def asettelut(self):
        
        #Otsikko ja näyttö
        self.pääasettelu.addWidget(self.otsikko, 0,0)
        self.pääasettelu.addWidget(self.näyttö, 1,0)

        #Nappulat kahdessa asettelussa, oikealla puolella negaatio ja tavalliset aritmeettiset operaatiot, vasemmalla kaikki muut
        self.napit_vasen_puoli.addWidget(self.tyhjennä, 0, 0)
        self.napit_vasen_puoli.addWidget(self.neliöjuurinappi, 0, 1)
        self.napit_vasen_puoli.addWidget(self.takaisinnappi, 0, 2)

        #Numerot ja pilkku sekä yhtä kuin -nappi
        self.napit_vasen_puoli.addWidget(self.ykkönen, 1, 0)
        self.napit_vasen_puoli.addWidget(self.kakkonen, 1, 1)
        self.napit_vasen_puoli.addWidget(self.kolmonen, 1, 2)

        self.napit_vasen_puoli.addWidget(self.nelonen, 2, 0)
        self.napit_vasen_puoli.addWidget(self.vitonen, 2, 1)
        self.napit_vasen_puoli.addWidget(self.kutonen, 2, 2)

        self.napit_vasen_puoli.addWidget(self.seiska, 3, 0)
        self.napit_vasen_puoli.addWidget(self.kasi, 3, 1)
        self.napit_vasen_puoli.addWidget(self.ysi, 3, 2)

        self.napit_vasen_puoli.addWidget(self.nolla, 4, 0)
        self.napit_vasen_puoli.addWidget(self.pilkku, 4, 1)
        self.napit_vasen_puoli.addWidget(self.yhtakuinnappi, 4, 2)

        self.napit_oikea_puoli.addWidget(self.negaationappi, 0, 0)
        self.napit_oikea_puoli.addWidget(self.jakonappi, 1, 0)
        self.napit_oikea_puoli.addWidget(self.kertonappi, 2, 0)
        self.napit_oikea_puoli.addWidget(self.miinusnappi, 3, 0)
        self.napit_oikea_puoli.addWidget(self.lisäänappi, 4, 0)

        self.näppäimistö.addLayout(self.napit_vasen_puoli, 0, 0)
        self.näppäimistö.addLayout(self.napit_oikea_puoli, 0, 1)
        self.pääasettelu.addLayout(self.näppäimistö, 2, 0)
        self.pääasettelu.setRowStretch(0, 1)
        self.pääasettelu.setRowStretch(1, 3)
        self.pääasettelu.setRowStretch(2, 9)