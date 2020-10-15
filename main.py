from functions import functions
from database import database

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QHeaderView
import sys, os

class gui(QMainWindow):
    def __init__(self):
        self.funct = functions()
        self.db = database()
        self.dolarHoy = self.db.get_data('dolar','latest_dolar_hoy')
        self.dolarBlueHoy = self.db.get_data('dolar','latest_dolar_hoy_blue')

        super().__init__()

        uic.loadUi(r"F:\PROYECTOS\PYTHON\STEAM-CASES\CASES-TEST GUI\gui.ui", self)

        # TITULO DE LA VENTANA
        self.setWindowTitle('CSGO CASES MANAGER')

        # BOTONES 
        self.actualizarPrecioDolar.clicked.connect(self.actualizarPrecioDolarFunct)
        self.actualizarPrecioCajas.clicked.connect(self.actualizarPrecioCajasFunct)
        self.boton_exit.clicked.connect(self.exitButton)

        # SETEO DOLAR Y DATOS DE LA TABLA APENAS INICIA EL PROGRAMA
        self.dolar_text.setText('Dolar: '+str(self.dolarHoy) +'  |  Blue: '+ str(self.dolarBlueHoy))
        self.winningOrNot()
        self.datosTabla()


    def datosTabla(self):
        # CONFIGURO LA TABLA
        self.cajas_tabla.setColumnCount(4)
        self.cajas_tabla.setRowCount(0)
        self.cajas_tabla.verticalHeader().setDefaultSectionSize(30)
        self.cajas_tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cajas_tabla.clearContents()

        # HEADERS DE LA TABLA
        headers = ('CASE', 'BUYED AT (USD)','PRICE (USD)', 'WINNING')
        self.cajas_tabla.setHorizontalHeaderLabels(headers)

        # LLENO DE DATOS LA TABLA
        casesprice = self.funct.cases_prices()
        row = 0
        for endian in casesprice:
            self.cajas_tabla.setRowCount(row + 1)
            idDato = QTableWidgetItem(endian[0])
            self.cajas_tabla.setItem(row, 0, idDato)
            self.cajas_tabla.setItem(row, 1, QTableWidgetItem(str(endian[1])))
            self.cajas_tabla.setItem(row, 2, QTableWidgetItem(str(endian[2])))
            self.cajas_tabla.setItem(row, 3, QTableWidgetItem(str(endian[3])))
            row += 1

    def actualizarPrecioDolarFunct(self):
        log = self.funct.get_dolar()
        self.logs_text.insertPlainText(log)
        self.dolar_text.setText('Dolar: '+str(self.dolarHoy) +'  |  Blue: '+ str(self.dolarBlueHoy))

    def actualizarPrecioCajasFunct(self):
        log = self.funct.get_case()
        self.logs_text.insertPlainText(log)
        self.datosTabla()
        self.winningOrNot()
    
    def winningOrNot(self):
        total_winning = self.funct.im_i_winning()
        self.winning_text.setText(f'Actualmente estas ganando {total_winning[0]} USD' if total_winning[1] else f'Actualmente estas perdiendo {total_winning[0]} USD' )

    def exitButton(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = gui()
    app.setStyle('Fusion')
    GUI.show()
    sys.exit(app.exec_())