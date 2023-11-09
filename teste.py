from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Rota para receber uma solicitação GET
@app.route('/get_request', methods=['GET'])
def get_request():
    # Os dados a serem enviados via POST, incluindo a API Key
    data = {
        "number": "5581986452028",
        "options": {
            "delay": 1200,
            "presence": "composing",
            "linkPreview": True
        },
        "textMessage": {
            "text": "Deus é fiel sempre, conseguir, glória a Deus...."
        },
        "apiKey": "87F3F7D04B8A45D086187399E4AD6469"  # Adicione a API Key aqui
    }

    # URL para a qual você deseja fazer a solicitação POST
    post_url = "http://191.252.185.216:8081/message/sendText/ApiTest"  # Substitua com a URL apropriada
    headers = {
            "apikey": "87F3F7D04B8A45D086187399E4AD6469",
            "Content-Type": "application/json"
        }
    # Faça a solicitação POST
    response = requests.post(post_url, json=data, headers=headers)

    # Verifique a resposta do servidor de destino (opcional)
    print(response.status_code, 'chegou...')
    if response.status_code == 200:
        return "Solicitação GET processada com sucesso e dados enviados via POST."
    else:
        #print(response.__dict__)
        return "Erro ao fazer a solicitação POST."

if __name__ == '__main__':
    app.run(host='191.252.185.216',port='8082',debug=True)
