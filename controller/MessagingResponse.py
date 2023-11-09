from model.User import User
#from flask import Flask, json,session, request, redirect, render_template, Response, abort, url_for, jsonify
#from datetime import datetime, timedelta
#import jwt
import requests
#from config import app_config, app_active
#config = app_config[app_active]


class MessagingResponseController():
    def __init__(self):
        self.user_model = User()

    def create_menu_response(self):

        menu_text = ("Bem-vindo ao nosso menu.\n"
                     "Por favor, escolha uma opção:\n"
                     "1. Opção 1\n"
                     "2. Opção 2\n"
                     "3. Opção 3\n"
                     "Digite 'sair' para sair do menu.")
        return menu_text    
    
    def send_menu_message():
   
        menu_text = ("Bem-vindo ao nosso menu.\n"
                        "Por favor, escolha uma opção:\n"
                        "1. Opção 1\n"
                        "2. Opção 2\n"
                        "3. Opção 3\n"
                        "Digite 'sair' para sair do menu.")
        return menu_text


    def enviar_mensagem_menu(self, numero, mensagem, send):

        if not mensagem:
      
            data = {
                "number": numero,
                "options": {
                    "delay": 1200,
                    "presence": "composing",
                    "linkPreview": True
                },
                "textMessage": {
                    "text": mensagem
                }
            }

            # URL para a qual você deseja fazer a solicitação POST
            post_url = "http://191.252.185.216:8081/message/sendText/ApiTest"  # Substitua com a URL apropriada

            # Cabeçalhos com a chave "Authorization" no formato API Key
            headers = {
                "apikey": "87F3F7D04B8A45D086187399E4AD6469",
                "Content-Type": "application/json"
            }
        
            # Depuração: Imprimir conteúdo da solicitação
            print("Solicitação POST:")
            print("URL:", post_url)
            print("Cabeçalhos:", headers)
            print("Dados:", data)

            # Faça a solicitação POST com o corpo da solicitação e cabeçalhos
            response = requests.post(post_url, json=data, headers=headers)
            return response
            # if send:
            #     response = requests.post(post_url, json=data, headers=headers)
            #     return response
            # else:
            #     return response

            # Depuração: Imprimir a resposta
            print("Resposta do servidor:")
            print("Status Code:", response.status_code)
            print("Conteúdo:", response.text)
            
            if response.status_code == 201:
                return "Solicitação GET processada com sucesso e dados enviados via POST."
            else:
                return data

       

    def verify_auth_token(self, access_token):
        status = 401    
        try:
            jwt.decode(access_token, config.SECRET, algorithm='HS256')
            message = 'Token válido'
            status = 200
        except jwt.ExpiredSignatureError:
            message = 'Token expirado, realize um novo login'
        except:
            message = 'Token inválido'

        return {
            'message': message,
            'status': status
        }
    
    def generate_auth_token(self, data, exp=30, time_exp=False):
        if time_exp == True:
            date_time = data['exp']
        else:
            date_time = datetime.utcnow() + timedelta(minutes=exp)

        dict_jwt = {
            'id': data['id'],
            'username': data['username'],
            "exp": date_time
        }
        access_token = jwt.encode(dict_jwt, config.SECRET, algorithm='HS256')
        return access_token