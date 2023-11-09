# -*- coding: utf-8 -*-
from flask import Flask,session, request, redirect, render_template, Response, json, abort, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
import time
from flask_login import LoginManager, login_user, logout_user
import requests
from functools import wraps

# config import
from config import app_config, app_active

# controllers
from controller.User import UserController
from controller.Product import ProductController
from controller.MessagingResponse import MessagingResponseController
from admin.Admin import start_views
from flask_bootstrap import Bootstrap
import sqlite3
import datetime

config = app_config[app_active]
def init_db():
    conn = sqlite3.connect('contas.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            descricao TEXT,
            tipo TEXT,
            valor REAL
        )
    ''')

    conn.commit()
    conn.close()

init_db()
def create_app(config_name):
    app = Flask(__name__, template_folder='templates')

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'paper'
    # Inicialize a extensão da sessão
    # app.config['SESSION_TYPE'] = 'filesystem'
    

    db = SQLAlchemy(config.APP)
    migrate = Migrate(app, db)
    start_views(app,db)
    # Session(app)
    Bootstrap(app)
    db.init_app(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()
            try:
                result = user.verify_auth_token(request.headers['access_token'])
                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['message'])
            except KeyError as e:
                abort(401, 'Você precisa enviar um token de acesso')

        return verify_token

    @app.route('/')
    def index():

        conn = sqlite3.connect('contas.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM transacoes ORDER BY data ASC')
        transacoes = [
            {
                'id': row[0],
                'data': datetime.datetime.strptime(row[1], '%Y-%m-%d').strftime('%d/%m/%Y') if row[1] else '',
                'descricao': row[2],
                'tipo': row[3],
                'valor': row[4]
            } for row in cursor.fetchall()
        ]
        entradas = sum(transacao['valor'] for transacao in transacoes if transacao['tipo'] == 'Crédito')
        saidas = sum(-transacao['valor'] for transacao in transacoes if transacao['tipo'] == 'Débito')
        saldo_atual = entradas - saidas

        conn.close()

        return render_template('vendas.html', transacoes=transacoes, entradas=entradas, saidas=saidas, saldo_atual=saldo_atual)

        #return render_template('vendas.html')


    @app.route('/cadastrar_transacao', methods=['POST'])
    def cadastrar_transacao():
        data = request.form['data']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        valor = float(request.form['valor'])

        if tipo == 'Débito':
            valor = -valor

        conn = sqlite3.connect('contas.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO transacoes (data, descricao, tipo, valor) VALUES (?, ?, ?, ?)', (data, descricao, tipo, valor))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    @app.route('/login/')
    def login():
        return render_template('login.html', data={'status': 200, 'msg': None, 'type': None})

    @app.route('/login/', methods=['POST'])
    def login_post():
        user = UserController()

        email = request.form['email']
        password = request.form['password']

        result = user.login(email, password)

        if result:
            if result.role == 4:
                return render_template('login.html', data={'status': 401, 'msg': 'Seu usuário não tem permissão para acessar o admin', 'type':2})
            else:
                login_user(result)
                return redirect('/admin')
        else:
            return render_template('login.html', data={'status': 401, 'msg': 'Dados de usuário incorretos', 'type': 1})

    @app.route('/recovery-password/')
    def recovery_password():
        # Capítulo 11
        return render_template('recovery.html', data={'status': 200, 'msg': None, 'type': None})

    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        user = UserController()

        result = user.recovery(request.form['email'])

        # Capítulo 11 - Alterar parâmetros
        if result['status_code'] == 200 or result['status_code'] == 202:
            return render_template('recovery.html', data={'status': result['status_code'], 'msg': 'Você receberá um e-mail em sua caixa para alteração de senha.', 'type': 3})
        else:
            return render_template('recovery.html', data={'status': result['status_code'], 'msg': result['body'], 'type': 1})
    
    @app.route('/new-password/<recovery_code>')
    def new_password(recovery_code):
        user = UserController()
        result = user.verify_auth_token(recovery_code)
        
        if result['status'] == 200:
            res = user.get_user_by_recovery(str(recovery_code))
            if res is not None:
                return render_template('new_password.html', data={'status': result['status'], 'msg': None, 'type': None, 'user_id': res.id})
            else:
                return render_template('recovery.html', data={'status': 400, 'msg': 'Erro ao tentar acessar os dados do usuário. Tente novamente mais tarde.', 'type': 1})
        else:
            return render_template('recovery.html', data={'status': result['status'], 'msg': 'Token expirado ou inválido, solicite novamente a alteração de senha', 'type': 1})

    @app.route('/new-password/', methods=['POST'])
    def send_new_password():
        user = UserController()
        user_id = request.form['user_id']
        password = request.form['password']

        result = user.new_password(user_id, password)

        if result:
            return render_template('login.html', data={'status': 200, 'msg': 'Senha alterada com sucesso!', 'type': 3, 'user_id': user_id})
        else:
            return render_template('new_password.html', data={'status': 401, 'msg': 'Erro ao alterar senha.', 'type': 1, 'user_id': user_id})

    @app.route('/products/', methods=['GET'])
    @app.route('/products/<limit>', methods=['GET'])
    @auth_token_required
    def get_products(limit=None):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        product = ProductController()
        response = product.get_products(limit=limit)
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/product/<product_id>', methods=['GET'])
    @auth_token_required
    def get_product(product_id):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }
        
        product = ProductController()
        response = product.get_product_by_id(product_id = product_id)

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    @auth_token_required
    def get_user_profile(user_id):
        header = {
            'access_token': request.headers['access_token'],
            "token_type": "JWT"
        }

        user = UserController()
        response = user.get_user_by_id(user_id=user_id)

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), response['status'], header

    @app.route('/login_api/', methods=['POST'])
    def login_api():
        header = {}
        user = UserController()

        email = request.json['email']
        password = request.json['password']

        result = user.login(email, password)
        code = 401
        response = {"message": "Usuário não autorizado", "result": []}

        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username,
                    'email': result.email,
                    'date_created': result.date_created,
                    'active': result.active
                }

                header = {
                    "access_token": user.generate_auth_token(result),
                    "token_type": "JWT"
                }
                code = 200
                response["message"] = "Login realizado com sucesso"
                response["result"] = result

        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), code, header


    @app.route('/logout')
    def logout_send():
        logout_user()
        return render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3})

    @app.route('/enviar_mensagem_menu/<numero>/<mensagem>', methods=['GET','POST'])
    def enviar_mensagem_menu(numero, mensagem):
        print('chegou....')
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

        post_url = "http://191.252.185.216:8081/message/sendText/ApiTest"

        headers = {
            "apikey": "87F3F7D04B8A45D086187399E4AD6469",
            "Content-Type": "application/json"
        }

        response = requests.post(post_url, json=data, headers=headers)
        return response.status_cod
        if response.status_code == 200:
            return "Mensagem de amor enviada com sucesso!"
        else:
            return f"Falha ao enviar a mensagem: {response.text}"
        

    # Rota para receber notificações do webhook


    @app.route('/webhook', methods=['GET','POST'])
    def webhook():

        data = request.get_json()  # Obtém os dados JSON da solicitação

        menu = MessagingResponseController()
        usuario = UserController()
        resultado = str(usuario.usuarioWhatsapp(data))
        print(resultado)
        mensagem = menu.create_menu_response()
        print(resultado['key']['remoteJid'])
        if resultado['key']['remoteJid'] =='558187868425@s.whatsapp.net':
            envio = menu.enviar_mensagem_menu(numero, data, send='true')
        else:
            numero =  "5581986452028@s.whatsapp.net"
            print(resultado, 'esse é o resultado')

        exit()
        mensagem = menu.create_menu_response()
        a = 0
        if resultado:
            send ='true'
            a+=1

        else:
            send = 'false'
        if a == 1:
            send ='false'
            
        reulst = menu.enviar_mensagem_menu(numero, mensagem, send)

        

        #iar_mensagem_menu(numero, mensagem)
        #resposta = jesus()

        #print(resposta)
        #usuarioWhatsap = UserController.usuarioWhatsapp(data)
        

        # print(usuarioWhatsap)
        return "deu certo"

    
    
    @app.route('/acessar_sessao', methods=['GET', 'POST'])
    def acessar_sessao():
        telefone = session.get('remoteJid', 'Convidado')
        mensagem = session.get('message', 'Nenhum mensagem fornecida')
        nome = session.get('pushName')
        return f'Telefone: {telefone}, Mensagem: {mensagem}, Nome: {nome}'


    @app.route('/jesus', methods=['GET', 'POST'])
    def jesus():
        # Dados a serem enviados via POST (equivalente ao corpo da solicitação)
        data = {
            "number": "5581986452028",
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": True
            },
            "textMessage": {
                "text": 'teste zapp....'
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

        # Depuração: Imprimir a resposta
        # print("Resposta do servidor:")
        # print("Status Code:", response.status_code)
        # print("Conteúdo:", response.text)
       # webhook()
        
        if response.status_code == 201:
             return "Solicitação GET processada com sucesso e dados enviados via POST."
        else:
             return str(data)
        
    @login_manager.user_loader
    def load_user(user_id):
        user = UserController()
        return user.get_admin_login(user_id)


    return app



