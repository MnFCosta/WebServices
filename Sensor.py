import requests
import time
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
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
        self.botao_criar_dado = QPushButton('Criar dado', self)
        self.botao_parar = QPushButton('Parar criação',self)
        self.botao_cancelar = QPushButton('X',self)

    
        self.setWindowTitle('Sensor')
        self.setGeometry(560, 200, 800, 600)

        # Posicionar os widgets na tela
        self.botao_criar_dado.setGeometry(10, 10, 100, 30)
        self.botao_parar.setGeometry(120, 10, 100, 30)
        self.botao_cancelar.setGeometry(750, 10, 40, 30)

        #Estilização
        self.botao_cancelar.setStyleSheet("background-color: red; color: black;")   
        
        # Configurar layout

        self.botao_criar_dado.clicked.connect(self.criar_dado)
        self.botao_parar.clicked.connect(self.parar_thread)
        self.botao_cancelar.clicked.connect(self.close)
    
    def criar_dado(self):
        self.dadothread = CriarDadoThread()
        self.dadothread.start()
    
    def parar_thread(self):
        self.dadothread.stop()
            


class CriarDadoThread(QThread):

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.rodando = True

    def run(self):
        while self.rodando == True:
            temp = random.randint(0,40)
            umidade = random.randint(0,100)
            luminosidade = ['Baixa', 'Média', 'Alta']
            data_hora_atual = datetime.now()
            data = data_hora_atual.strftime("%d-%m-%Y")
            hora = data_hora_atual.strftime("%H:%M")

            
            dado = {'temperatura': f'{temp}°C', 'umidade': f'{umidade}%', 'luminosidade': f'{random.choice(luminosidade)}', 'data': f'{data}', 'hora': f'{hora}'}
            response = requests.post(f'{server_flask}/dados', json=dado)

            print(response)
            time.sleep(10)

        print("Thread Parada")

    def stop(self):
        self.rodando = False
    
    

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