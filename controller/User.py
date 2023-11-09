from model.User import User
from flask import jsonify
from datetime import datetime, timedelta
import jwt
from config import app_config, app_active
import app
config = app_config[app_active]
import requests
from controller.MessagingResponse import MessagingResponseController
from controller.Email import EmailController

class UserController():
    def __init__(self):
        self.user_model = User()
        self.message_controller = MessagingResponseController()

        

    def usuarioWhatsapp(self,data):
        if data is not None:

            if "event" in data:
                # É um objeto "event"
                event_data = data["event"]
                
                if event_data == 'send.message':
                    key = data["data"]['key']
                    print('chegou')
                    return key
                    
                elif event_data == 'messages.upsert':
                    key = data["data"]['key']
                    mensagem = data["data"]['message']
                    if key['remoteJid'] =='558191911574@s.whatsapp.net':
                        id = key['id']
                        fromMe = key['fromMe']  
                        if not fromMe:
                            # Dicionário de opções

                            # # Rota para lidar com mensagens recebidas
                            # @app.route('/webhook', methods=['POST'])
                            # def webhook():
                            #     user_message = request.values.get('Body', '').strip().lower()

                            #     response = MessagingResponse()
                            #     if user_message in options:
                            #         response.message(options[user_message])
                            #     elif user_message == 'menu':
                            #         return send_menu_message()
                            #     else:
                            #         response.message("Opção inválida. Digite 'menu' para exibir as opções.")

                            #     return str(response)
                            # Acessar todas as informações do JSON
                            event = data.get('event')
                            instance = data.get('instance')
                            remote_jid = data.get('data', {}).get('key', {}).get('remoteJid')
                            from_me = data.get('data', {}).get('key', {}).get('fromMe')
                            key_id = data.get('data', {}).get('key', {}).get('id')
                            push_name = data.get('data', {}).get('pushName')
                            conversation = data.get('data', {}).get('message', {}).get('conversation')
                            message_type = data.get('data', {}).get('message', {}).get('messageType')
                            message_timestamp = data.get('data', {}).get('message', {}).get('messageTimestamp')
                            owner = data.get('data', {}).get('owner')
                            destination = data.get('destination')
                            date_time = data.get('date_time')
                            sender = data.get('sender')
                            server_url = data.get('server_url')
                            apikey = data.get('apikey')

                            # Imprimir todas as informações
                            print(f'Event: {event}')
                            print(f'Instance: {instance}')
                            print(f'Remote JID: {remote_jid}')
                            print(f'From Me: {from_me}')
                            print(f'Key ID: {key_id}')
                            print(f'Push Name: {push_name}')
                            print(f'Conversation: {conversation}')
                            print(f'Message Type: {message_type}')
                            print(f'Message Timestamp: {message_timestamp}')
                            print(f'Owner: {owner}')
                            print(f'Destination: {destination}')
                            print(f'Date and Time: {date_time}')
                            print(f'Sender: {sender}')
                            print(f'Server URL: {server_url}')
                            print(f'API Key: {apikey}')
                            dados_pessoais = {
                                "event":event, 
                                "remote_jid": remote_jid,
                                "from_me":from_me,
                                "key_id":key_id,
                                "push_name":push_name,
                                "conversation":conversation,
                                "message_timestamp":message_timestamp,
                                "date_time":date_time



                            }
                            return dados_pessoais
                            #resultado = app.enviar_mensagem_de_amor(str(numero_destino), str(mensagem))
                            #return resultado
                        else:
                            print('é outra pessoa ')
                            return key
                            

                        print('pois não, o que deseja?')
                        return data
                        #print('é celular e sobreaviso')
                    elif key['remoteJid'] =='558195024094@s.whatsapp.net':
                        print('é celular e maiara')
                        mensagem = data["data"]['message']
                        numero_destino = 5581995024094
                        print(numero_destino, 'número de destino')
                        mensagem_de_amor = 'Podem existir mil obstáculos, mas nada fará com que meu amor por ti morra. Atravessarei até os maiores mares, mas não existirá água suficiente que afogue o amor que sinto por você.'

                        #saudacao = app.enviar_mensagem_de_amor(str(numero_destino), str(mensagem_de_amor))
                        #instrucao = app.instrucao(str(numero_destino), str(mensagem_de_amor))
                        envio = MessagingResponseController()
                        resultado = envio.enviar_mensagem_menu('558195024094@s.whatsapp.net', data,send='true')
                        return resultado
                        #print(resultado, 'resultado de envio 00000000')
                    else:
                        if key['remoteJid'] =='558187868425@s.whatsapp.net':
                            print('é celular e maiara')
                            mensagem = data["data"]['message']
                            numero_destino = 558187868425
                            envio = MessagingResponseController()
                            resultado = envio.enviar_mensagem_menu('558187868425@s.whatsapp.net', data,send='true')
                            return resultado
                            print(numero_destino, 'número de destino')
                            mensagem_de_amor = 'Fala meu amor, você é tudo de bom'

                            #resultado = app.enviar_mensagem_de_amor(str(numero_destino), str(mensagem_de_amor))
                            #print(resultado, 'resultado de envio 00000000')
                            #print('é o número de maiara')
                            return 'se o número for igual 558195024094@s.whatsapp.net'

                    #key = data["data"]['key']
                    #mensagem = data["data"]['message']
                    # aqui é a resposta que dou vai para extendedTextMessage e não conversation
                    if "extendedTextMessage" in mensagem:
                        #print(key['remoteJid'], 'esse remote amensagem é  upsert e o texto: '+str(mensagem['extendedTextMessage']['text']))

                        # numero_destino = 5581986452028
                        # print(numero_destino, 'enviou para esse número ')
                        # mensagem_de_amor = "Teste zap... automático"
                        # resultado = enviar_mensagem_de_amor(str(numero_destino), str(mensagem_de_amor))
                        # print(resultado, 'resultado de envio 00000000')
                        return 'se mensagem for extendedTextMessage'
                    else:
                        return data
                        print(data)
                       # return 'se não for extendedTextMessage'
                        print(data)
                    # aqui vai aparecer as mensagem que recebo de outra pessoa
                        # print(key['remoteJid'], 'esse mensagem é  upsert '+str(mensagem['conversation']))
                        
                        # session['remoteJid'] = key
                        # session['message'] = mensagem
                        
                        # session['pushName'] =data["data"]['pushName']
                        # print(session['pushName'], 'teste pushName')
                        #return str(data)
                elif event_data =='connection.update':
                    return 'esse é connection.update'
                elif event_data =='messages.delete':
                    return 'esse é delete'
                elif event_data == 'messages.update':

                    return  data['data']
                elif event_data =='conversation_updated':
                    return 'event conversation_updated'
                elif event_data =='call':
                    
                    return 'event call'
                else:   
                    print(data)
                    return 'se não for call antes é o  print do data'
                    #
                    # print('mensagem - ', data['conversation']['messages'][0]['content'])
                    # print('nome- ', data['conversation']['messages'][0]['sender']['name'])    
                    # print('sender- ', data['conversation']['meta']['sender']['identifier'])                
                    # print('deve ser delete ou outros ')
                print("Recebi um objeto 'event': ")
               
                return 'recebi event'              
        
            elif "account" in data:
                # É um objeto "account"
                account_data = data["account"]
                # Faça o que você precisa com os dados da conta
                print("Recebi um objeto 'account'")
                #response = {'message': 'Webhook recebido com sucesso account '}
                #return jsonify(response), 200  # Responde com status HTTP 200 (OK)rn render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3})
                return 'account de data'
            elif "additional_attributes" in data:
                # É um objeto "additional_attributes"
                account_data = data["additional_attributes"]
                # Faça o que você precisa com os dados da conta
                #print("Recebi um objeto 'additional_attributes'")
                #response = {'message': 'Webhook recebido com sucesso additional_attributes '}
                #return jsonify(response), 200  # Responde com status HTTP 200 (OK)rn render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3})
                return 'additional_attributes de data'
            else:
                print("Tipo de objeto desconhecido")
                #response = {'message': 'Webhook recebido com sucesso '}
                #return jsonify(response), 200  # Responde com status HTTP 200 (OK)rn render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3})
                return 'diferente de account e outros'
        #print("Dados recebidos do webhook:")
        #response = {'message': 'Webhook recebido com sucesso '}
        #return jsonify(response), 200  # Responde com status HTTP 200 (OK)rn render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type':3})
    def login(self, email, password):
        self.user_model.email = email
        
        result = self.user_model.get_user_by_email()
        if result is not None:
            res = self.user_model.verify_password(password, result.password) 
            if res:
                return result
            else:
                return {}
        return {}
    
    def get_admin_login(self, user_id):
        self.user_model.id = user_id

        response = self.user_model.get_user_by_id()
        return response

    def recovery(self, to_email):
        self.user_model.email = to_email
        res = self.user_model.get_user_by_email()

        if res is not None:
            user_id = res.id
            username = res.username

            recovery_code = self.generate_auth_token({
                'id': user_id,
                'username': username
            }, exp=5)
            recovery_code = recovery_code.decode("utf-8")
            try:
                self.user_model.id = res.id
                res = self.user_model.update({
                    'recovery_code': recovery_code
                })

                if res:
                    content_text = 'Olá %s. Para realizar a alteração de senha, você precisa acessar a seguinte url: %snew-password/%s' % (username, config.URL_MAIN, recovery_code)
                else:
                    return {
                       'status_code' : 401,
                        'body' : 'Erro ao gerar código de envio',
                    }

            except:
                return {
                    'status_code' : 401,
                    'body' : 'Erro ao gerar código de envio',
                }

            try:
                result = self.email_controller.send_email(to_email, 'Recuperação de senha', content_text)
            except:
                return {
                    'status_code' : 401,
                    'body' : 'Erro no serviço de e-mail. Por favor. Entre em contato com o administrador.',
                }
        else:
            result =  {
                    'status_code' : 401,
                    'body' : 'Usuário inexistente',
            }

        return result 

    def get_user_by_recovery(self, recovery_password):
        self.user_model.recovery_code = recovery_password
        return self.user_model.get_user_by_recovery()

    def new_password(self, user_id, password):
        self.user_model.set_password(password)
        self.user_model.id = user_id

        return self.user_model.update({
            'password': self.user_model.password
        })

    def get_user_by_id(self, user_id):    
        result = {}
        try:
            self.user_model.id = user_id
            res = self.user_model.get_user_by_id()
            result = {
                'id': res.id,
                'name': res.username,
                'email': res.email,
                'date_created': res.date_created
            }

            status = 200

        except Exception as e:
            print(e)
            result = []
            status = 400
        finally:
            return {
                'result': result,
                'status': status
            }

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