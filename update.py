import requests
import time
import sys
import random
from datetime import datetime


# URL SERVIDOR FLASK
base_url = 'http://localhost:5000' 


id = 1
temp = random.randint(0,40)
umidade = random.randint(0,100)
luminosidade = ['Baixa', 'Média', 'Alta']
data_hora_atual = datetime.now()
data = data_hora_atual.strftime("%d-%m-%Y")
hora = data_hora_atual.strftime("%H:%M")

            
dado = {'temperatura': f'{temp}°C', 'umidade': f'{umidade}%', 'luminosidade': f'{random.choice(luminosidade)}', 'data': f'{data}', 'hora': f'{hora}'}
response = requests.put(f'{base_url}/dados/{id}', json=dado,)
