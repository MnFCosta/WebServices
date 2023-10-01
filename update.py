import requests
import time
import sys
import random


# URL SERVIDOR FLASK
base_url = 'http://localhost:5000' 


id = 1
temp = random.randint(0,40)
umidade = random.randint(0,100)
luminosidade = ['Baixa', 'Média', 'Alta']

dado = {'temperatura': f'{temp}°C', 'umidade': f'{umidade}%', 'luminosidade': f'{random.choice(luminosidade)}',}
response = requests.put(f'{base_url}/dados/{id}', json=dado,)
print(f'Atualizar informações do dado com ID: {id}')
