import requests
import time
import random
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime

# URL SERVIDOR FLASK
server_flask = 'http://localhost:5000'  

class TelaPrincipal(QWidget):
    def __init__(self,):
        super().__init__()
    
        self.initUI()

    def initUI(self):
        # Widgets
        self.botao_ultima_leitura = QPushButton('Última Leitura',self)
        self.dados = QLabel('Mensagens:', self)
        self.botao_datahora = QPushButton('DataHora',self)
        self.data = QLineEdit(self)
        self.hora = QLineEdit(self)
        self.botao_cancelar = QPushButton('X',self)

        # Posicionar os widgets na tela
        self.botao_ultima_leitura.setGeometry(10, 10, 120, 30)  # X, Y, Width, Height
        self.botao_datahora.setGeometry(150, 10, 120, 30)
        self.data.setGeometry(150, 60, 120, 30)
        self.hora.setGeometry(150, 90, 120, 30)
        self.dados.setGeometry(10, 200, 800, 30)
        self.botao_cancelar.setGeometry(750, 10, 40, 30)

        #Estilização
        self.botao_cancelar.setStyleSheet("background-color: red; color: black;")   
        

        self.botao_ultima_leitura.clicked.connect(self.retornar_dado)
        self.botao_datahora.clicked.connect(self.retornar_datahora)
        self.botao_cancelar.clicked.connect(self.close)

        self.dadothread = RetornarDadoThread()
        self.datathread = RetornarDadoDataHoraThread()

        self.dadothread.dado_recebido.connect(self.atualizar_dado)
        self.datathread.dado_recebido.connect(self.atualizar_dado)
        self.setWindowTitle('Consumidor')
        self.setGeometry(560, 200, 800, 600)
    
    def atualizar_dado(self, data):
        print("Received JSON data:", data)
        dados = ""
        
        try:
            for d in data['dados']:
                dados += (f"Id: {d['id']} " +
                    f"Temperatura: {d['temperatura']} " +
                    f"Luminosidade: {d['luminosidade']} " +
                    f"Umidade: {d['umidade']} " +
                    f"Data: {d['data']} " +
                    f"Hora: {d['hora']}\n"
                )
        except:
            dados = "Dado não encontrado!"
        
        print(dados)

        self.dados.setText(dados)
    
    def retornar_dado(self):
        self.dadothread.start()
    
    def retornar_datahora(self):
        self.datathread.getdata(self.data.text())
        self.datathread.gethora(self.hora.text())
        self.datathread.start()
    

class RetornarDadoThread(QThread):
    dado_recebido = pyqtSignal(dict)

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.rodando = True

    def run(self):
        response = requests.get(f'{server_flask}/dados/ultimaleitura')
        self.dado_recebido.emit(response.json())


class RetornarDadoDataHoraThread(QThread):
    dado_recebido = pyqtSignal(dict)

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.rodando = True
        self.data = ''
        self.hora = ''

    def run(self):
        data = self.data
        hora = self.hora
        response = requests.get(f'{server_flask}/dados/datahora/{data}{hora}')
        self.dado_recebido.emit(response.json())
    
    def getdata(self, data):
        self.data = data
    
    def gethora(self, hora):
        self.hora = hora



if __name__ == '__main__':
    #Cria uma instancia da aplicação PyQt, necessária para configurar a interface gráfica e o loop de eventos
    app = QApplication(sys.argv)
    #Cria uma instância da classe TelaLogin, que representa a tela de login da aplicação
    ui = TelaPrincipal()
    #Mostra a tela de login
    ui.show()
    #app.exec inicia o loop de eventos da aplicação, que aguarda por cliques de mouse e pressionamentos de teclas por exemplo
    #sys.exit termina a aplicação quando tem um retorno de 0, ou seja, quando app.exec_() retornar 0, a aplicação será terminada
    sys.exit(app.exec_())