import requests
import time
import random
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor
from datetime import datetime

# URL SERVIDOR FLASK
server_flask = 'http://localhost:5000'  

class TelaPrincipal(QWidget):
    def __init__(self,):
        super().__init__()
    
        self.initUI()

        self.dado_thread_rodando = False

    def initUI(self):
        # Widgets
        self.label = QLabel('Sensor inativo', self)
        self.botao_criar_dado = QPushButton('Criar dado', self)
        self.botao_parar = QPushButton('Parar criação',self)
        self.botao_cancelar = QPushButton('X',self)
        self.quadrado = QuadradoWidget(self)

    
        self.setWindowTitle('Sensor')
        self.setGeometry(100, 100, 400, 300)

        # Posicionar os widgets na tela
        self.label.setGeometry(10,90,100,30)
        self.botao_criar_dado.setGeometry(10, 10, 100, 30)
        self.botao_parar.setGeometry(120, 10, 100, 30)
        self.botao_cancelar.setGeometry(350, 10, 40, 30)
        self.quadrado.setGeometry(125, 120, 200, 200)

        #Estilização
        self.botao_cancelar.setStyleSheet("background-color: red; color: black;")
        
        # Configurar layout

        self.botao_criar_dado.clicked.connect(self.criar_dado)
        self.botao_parar.clicked.connect(self.parar_thread)
        self.botao_cancelar.clicked.connect(self.close)
    
    def criar_dado(self):
        if not self.dado_thread_rodando:
            self.label.setText('Criando dados')
            self.quadrado.cor_quadrado = QColor(0, 217, 14)
            self.quadrado.update()
            self.dadothread = CriarDadoThread()
            self.dadothread.start()
            self.dado_thread_rodando = True
    
    def parar_thread(self):
        if self.dado_thread_rodando:
            self.label.setText('Sensor Inativo')
            self.quadrado.cor_quadrado = QColor(255, 0, 0)
            self.quadrado.update()
            self.dadothread.stop()
            self.dado_thread_rodando = False
            


class CriarDadoThread(QThread):

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.rodar = True

    def run(self): 
        while self.rodar == True:
            temp = random.randint(0,40)
            umidade = random.randint(0,100)
            luminosidade = ['Baixa', 'Média', 'Alta']
            data_hora_atual = datetime.now()
            data = data_hora_atual.strftime("%d-%m-%Y")
            hora = data_hora_atual.strftime("%H:%M")

            
            dado = {'temperatura': f'{temp}°C', 'umidade': f'{umidade}%', 'luminosidade': f'{random.choice(luminosidade)}', 'data': f'{data}', 'hora': f'{hora}'}
            requests.post(f'{server_flask}/dados', json=dado)

            time.sleep(10)

    def stop(self):
        self.rodar = False

#Widgets
class QuadradoWidget(QWidget):
    cor_quadrado = QColor(255, 0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(self.cor_quadrado)
        
        painter.drawRect(0, 0, 150, 150)
    
    

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