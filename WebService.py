from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth
import random
from datetime import datetime


app = Flask(__name__)

# Dado inicial para testes
temp = random.randint(0,40)
umidade = random.randint(0,100)
luminosidade = ['Baixa', 'Média', 'Alta']
data_hora_atual = datetime.now()
data = data_hora_atual.strftime("%d-%m-%Y")
hora = data_hora_atual.strftime("%H:%M")

dados = [
    {'id': 1, 'temperatura': f'{temp}°C', 'umidade': f'{umidade}%', 'luminosidade': f'{random.choice(luminosidade)}', 'data': f'{data}','hora':f'{hora}',}
]

# Tratamento de erros
@app.errorhandler(404)
def erro(erro):
    return make_response(jsonify({'erro': 'Rota não encontrada!'}), 404)

# Rotas para a API
@app.route('/dados', methods=['GET'])
def obter_livros():
    return jsonify({'dados': dados})

@app.route('/dados/<int:id_dado>', methods=['GET'])
def obter_dado(id_dado):
     dado_encontrado = None
     for dado in dados:
         if dado['id'] == id_dado:
             dado_encontrado = dado
             break  

     if not dado_encontrado: 
         abort(404)
     return jsonify({'dados': dado_encontrado})

@app.route('/dados/ultimaleitura', methods=['GET'])
def obter_ultima_leitura():
     lendados = len(dados)
     dado = []
     dado.append(dados[lendados-1])

     if not lendados: 
         abort(404)
     return jsonify({'dados': dado})

@app.route('/dados/datahora/<datahora>', methods=['GET'])
def obter_datahora(datahora):
    dado = datahora
    data = dado[0:10]
    hora = dado[10:15]
    retorno = []

    for d in dados:
        if d['data'] == data and d['hora'] == hora:
            retorno.append(d)

    if not retorno: 
        abort(404)
    return jsonify({'dados': retorno})

@app.route('/dados', methods=['POST'])
def criar_dado():
    if not request.json or 'temperatura' not in request.json:
        abort(400)
    dado = {
        'id': dados[-1]['id'] + 1,
        'temperatura': request.json['temperatura'],
        'umidade': request.json['umidade'],
        'luminosidade': request.json['luminosidade'],
        'data': request.json['data'],
        'hora': request.json['hora'],
    }
    dados.append(dado)
    return jsonify({'dados': dados}), 201

@app.route('/dados/<int:id_dado>', methods=['PUT'])
def atualizar_dado(id_dado):
     dado = None
     for d in dados:
         if d['id'] == id_dado:
             dado = d
             break

     if not dado:
         abort(404)
     if not request.json:
         abort(400)

     dado['temperatura'] = request.json.get('temperatura', dado['temperatura'])
     dado['umidade'] = request.json.get('umidade', dado['umidade'])
     dado['luminosidade'] = request.json.get('luminosidade', dado['luminosidade'])
     dado['data'] = request.json.get('data', dado['data'])
     dado['hora'] = request.json.get('hora', dado['hora'])

     return jsonify({'dado': dado})

@app.route('/dados/<int:id_dado>', methods=['DELETE'])
def excluir_dado(id_dado):
    dado = None
    for d in dados:
         if d['id'] == id_dado:
             dado = d
             break


    if not dado:
        abort(404)
    return jsonify({'resultado': True})

if __name__ == "__main__":
    print('Servidor Flask rodando!')
    app.run(debug=True)
