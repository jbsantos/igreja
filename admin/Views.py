# -*- coding: utf-8 -*-
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
# Capítulo 10
from flask_login import current_user
from flask import redirect

from config import app_config, app_active

from model.User import User
from model.Category import Category
from model.Product import Product
import datetime
import sqlite3
import datetime
#import locale
#locale.setlocale(locale.LC_ALL,'pt_BR.ISO8859-1')
config = app_config[app_active]

class HomeView(AdminIndexView):
    extra_css = [config.URL_MAIN + 'static/css/home.css','https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
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
    @expose('/')
   
    def index(self):
        user_model = User()
        category_model = Category()
        product_model = Product()

        users = user_model.get_total_users()
        categories = category_model.get_total_categories()
        products = product_model.get_total_products()
        last_products = product_model.get_last_products()
        data_sistema  = str(datetime.datetime.now().strftime('%B'))

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
        
        return self.render('home_admin.html', report={
            'users': users[0],
            'categories': categories[0],
            'products': products[0]
        }, last_products=last_products, data_sistema=data_sistema)


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

class UserView(ModelView):
    column_labels = {
        'funcao': 'Função',
        'username': 'Nome de usuário',
        'email': 'E-mail',
        'date_created': 'Data de Criação',
        'last_update': 'Última atualização',        
        'active': 'Estado',
        'password': 'Senha',
    }

    column_descriptions = {
        'funcao': 'Função no painel administrativo',
        'username': 'Nome de usuário no sistema',
        'email': 'E-mail do usuário no sistema',
        'date_created': 'Data de Criação do usuário no sistema',
        'last_update': 'Última atualização desse usuário no sistema',        
        'active': 'Estado ativo ou inativo no sistema',
        'password': 'Senha do usuário no sistema',
    }

    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']

    form_widget_args = {
        'password': {
            'type': 'password'
        }
    }

    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'funcao']
    create_modal = True
    edit_modal = True
    can_export = True
    column_editable_list = ['username', 'email', 'funcao', 'active']
    column_sortable_list = ['username']
    column_default_sort = [('username', True), ('date_created', True)]
    column_details_exclude_list = ['password', 'recovery_code']
    column_export_exclude_list = ['password', 'recovery_code']

    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    def on_model_change(self, form, User, is_created):
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
            else:
                del form.password

    # Capítulo 10
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

# Capítulo 10
class RoleView(ModelView):
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

class CategoryView(ModelView):
    can_view_details = True

    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
            return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

class ProductView(ModelView):
    can_view_details = True
    
    def is_accessible(self):
        role = current_user.role
        if role == 1:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        elif role == 2:
            self.can_create = True
            self.can_edit = True
            self.can_delete = True
        elif role == 3:
            self.can_create = True
            self.can_edit = True
            self.can_delete = False

        return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')