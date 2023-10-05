import requests
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime

# URL SERVIDOR FLASK
server_flask = 'http://localhost:5000'  

class TelaGerenciar(QWidget):
    def __init__(self,):
        super().__init__()
    
        self.initUI()

    def initUI(self):
        # Widgets
        #Deletar
        self.ldeletar = QLabel('ID do dado:', self)
        self.id_deletar = QLineEdit(self)
        self.botao_deletar = QPushButton('Deletar',self)

        #Editar
        self.leditar = QLabel('ID:', self)
        self.id_editar = QLineEdit(self)
        self.lluminosidade = QLabel('Luminosidade:', self)
        self.luminosidade = QComboBox(self)
        self.luminosidade.addItems(['Baixa', 'Média', 'Alta'])
        self.ltemp = QLabel('Temperatura:', self)
        self.temp = QLineEdit(self)
        self.lumidade = QLabel('Umidade:', self)
        self.umidade = QLineEdit(self)

        self.botao_editar = QPushButton('Editar',self)

        self.botao_voltar = QPushButton('<',self)
        self.botao_cancelar = QPushButton('X',self)

        # Posicionar os widgets na tela
        self.ldeletar.setGeometry(10, 30, 200, 20)
        self.id_deletar.setGeometry(10, 50, 100, 20)
        self.botao_deletar.setGeometry(120, 50, 80, 20)

        self.leditar.setGeometry(10, 90, 200, 20)
        self.id_editar.setGeometry(10, 110, 100, 20)
        self.lluminosidade.setGeometry(120, 90, 200, 20)
        self.luminosidade.setGeometry(120, 110, 100, 20)
        self.ltemp.setGeometry(230, 90, 200, 20)
        self.temp.setGeometry(230, 110, 100, 20)
        self.lumidade.setGeometry(340, 90, 200, 20)
        self.umidade.setGeometry(340, 110, 100, 20)
        self.botao_editar.setGeometry(450, 110, 80, 20)


        self.botao_voltar.setGeometry(10, 2, 20, 20)
        self.botao_cancelar.setGeometry(590, 2, 20, 20)

        #Estilização
        self.botao_deletar.setStyleSheet("background-color: red; color: black;")   
        self.botao_cancelar.setStyleSheet("background-color: red; color: black;")   
        

        self.botao_deletar.clicked.connect(self.deletar_dado)
        self.botao_editar.clicked.connect(self.editar_dado)
        self.botao_voltar.clicked.connect(self.voltar)
        self.botao_cancelar.clicked.connect(self.close)

        self.deletarthread = DeletarDadoThread()
        self.editarthread = EditarDadoThread()

        self.setWindowTitle('Gerenciar Dados')
        self.setGeometry(530, 100, 620, 300)
    
    def editar_dado(self):
        self.editarthread.getid(self.id_editar.text())
        self.editarthread.getluminosidade(self.luminosidade.currentText())
        self.editarthread.gettemp(self.temp.text())
        self.editarthread.getumidade(self.umidade.text())
        self.editarthread.start()

    
    def deletar_dado(self):
        self.deletarthread.getid(self.id_deletar.text())
        self.deletarthread.start()
        self.id_deletar.clear()
        
    def voltar(self):
        self.tela_gerenciar = TelaPrincipal()
        self.tela_gerenciar.show()
        self.close()
    

class TelaPrincipal(QWidget):
    def __init__(self,):
        super().__init__()
    
        self.initUI()

    def initUI(self):
        # Widgets
        self.botao_ultima_leitura = QPushButton('Última Leitura',self)
        self.ldata = QLabel('Data:', self)
        self.lhora = QLabel('Hora:', self)
        self.data = QLineEdit(self)
        self.hora = QLineEdit(self)
        self.botao_datahora = QPushButton('Buscar',self)
        self.botao_gerenciar = QPushButton('Gerenciar Dados',self)
        self.botao_cancelar = QPushButton('X',self)

         # Criar widget da tabela
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 100, 602, 180)  
        self.tableWidget.setColumnCount(6) 
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Temperatura", "Luminosidade", "Umidade", "Data", "Hora"])

        self.tableWidget.verticalHeader().setVisible(False)

        # Posicionar os widgets na tela
        self.botao_ultima_leitura.setGeometry(10, 65, 120, 30)  # X, Y, Width, Height
        self.botao_datahora.setGeometry(270, 30, 120, 30)
        self.botao_gerenciar.setGeometry(140, 65, 120, 30)
        self.ldata.setGeometry(10, 5, 120, 30)
        self.lhora.setGeometry(140, 5, 120, 30)
        self.data.setGeometry(10, 30, 120, 30)
        self.hora.setGeometry(140, 30, 120, 30)
        self.botao_cancelar.setGeometry(590, 2, 20, 20)

        #Estilização
        self.botao_cancelar.setStyleSheet("background-color: red; color: black;")   
        

        self.botao_ultima_leitura.clicked.connect(self.retornar_dado)
        self.botao_datahora.clicked.connect(self.retornar_datahora)
        self.botao_gerenciar.clicked.connect(self.abrir_tela_gerenciar)
        self.botao_cancelar.clicked.connect(self.close)

        self.dadothread = RetornarDadoThread()
        self.datathread = RetornarDadoDataHoraThread()

        self.dadothread.dado_recebido.connect(self.atualizar_dado)
        self.datathread.dado_recebido.connect(self.atualizar_dado)
        self.setWindowTitle('Consumidor')
        self.setGeometry(530, 100, 620, 300)
    
    def atualizar_dado(self, data):
        try:
            self.tableWidget.setRowCount(0)
            for d in data['dados']:
                posicao = self.tableWidget.rowCount()
                self.tableWidget.insertRow(posicao)
                self.tableWidget.setItem(posicao, 0, QTableWidgetItem(str(d['id'])))
                self.tableWidget.setItem(posicao, 1, QTableWidgetItem(str(d['temperatura'])))
                self.tableWidget.setItem(posicao, 2, QTableWidgetItem(str(d['luminosidade'])))
                self.tableWidget.setItem(posicao, 3, QTableWidgetItem(str(d['umidade'])))
                self.tableWidget.setItem(posicao, 4, QTableWidgetItem(str(d['data'])))
                self.tableWidget.setItem(posicao, 5, QTableWidgetItem(str(d['hora'])))
        except:
           pass
        
        
    
    def retornar_dado(self):
        self.dadothread.start()
    
    def retornar_datahora(self):
        self.datathread.getdata(self.data.text())
        self.datathread.gethora(self.hora.text())
        self.datathread.start()
    
    def abrir_tela_gerenciar(self):
        self.tela_gerenciar = TelaGerenciar()
        self.tela_gerenciar.show()
        self.close()
    

class RetornarDadoThread(QThread):
    dado_recebido = pyqtSignal(dict)

    def __init__(self, parent=None,):
        super().__init__(parent)

    def run(self):
        response = requests.get(f'{server_flask}/dados/ultimaleitura')
        self.dado_recebido.emit(response.json())


class DeletarDadoThread(QThread):

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.id = ''

    def run(self):
       requests.delete(f'{server_flask}/dados/{self.id}',)
        
    
    def getid(self, id):
        self.id = id

class EditarDadoThread(QThread):

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.id = ''
        self.luminosidade = ''
        self.temp = ''
        self.umidade = ''

    def run(self):
       data_hora_atual = datetime.now()
       data = data_hora_atual.strftime("%d-%m-%Y")
       hora = data_hora_atual.strftime("%H:%M")
       dado = {'temperatura': f'{self.temp}°C', 'umidade': f'{self.umidade}%', 'luminosidade': f'{self.luminosidade}', 'data': f'{data}', 'hora': f'{hora}'}
       response = requests.put(f'{server_flask}/dados/{self.id}', json=dado,)
        
    
    def getid(self, id):
        self.id = id
    
    def getluminosidade(self, luminosidade):
        self.luminosidade = luminosidade

    def gettemp(self, temp):
        self.temp = temp

    def getumidade(self, umidade):
        self.umidade = umidade

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