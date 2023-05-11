from flask import Flask, jsonify, render_template, request, logging
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:m5FGONigT78417TQZdyS@containers-us-west-173.railway.app:6695/railway"
app.config['JSON_AS_ASCII'] = False
CORS(app)

db = SQLAlchemy(app)

class USU(db.Model):

    __tablename__='USU'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)

    def __repr__(self):
        return f"USU: {self.nick, self.email, self.senha}"

    def __init__(self, nick, email, senha):
        self.nick = nick
        self.email = email
        self.senha = senha

def format_usu(USU):
    return {
        "nick": USU.nick,
        "id" : USU.id,
        "email": USU.email,
        "senha" : USU.senha
    }

@app.route('/user_all')
def getUSU():
    usus = USU.query.all()
    usus_list = []
    for usu in usus:
        usus_list.append(format_usu(usu))
        print(usus_list)
    return {"usus": usus_list}

@app.route('/insereusu', methods = ['POST'])
def insereUSU():
    usuNick = request.json['nick']
    usuEmail = request.json['email']
    usuSenha = request.json['senha']
    evento = USU(usuNick, usuEmail, usuSenha)
    db.session.add(evento)
    db.session.commit()
    return format_usu(evento)

class USUComp(db.Model):

    __tablename__='USU'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)

    def __repr__(self):
        return f"USU: {self.id, self.nick, self.email, self.senha}"

    def __init__(self, id, nick, email, senha):
        self.id = id
        self.nick = nick
        self.email = email
        self.senha = senha

def format_USUCompleto(USUCompleto):
    return {
        "nick": USUCompleto.nick,
        "id" : USUCompleto.id,
        "email": USUCompleto.email,
        "senha" : USUCompleto.senha
    }

@app.route('/fazlogin', methods = ['POST'])
def fazLogin():
    return print("aqui", request)
    Res = []
    USUCompletoEmail = request.json['email']
    USUCompletoSenha = request.json['password']
    print(USUCompletoEmail, USUCompletoSenha)
    evento = USUComp.query.all()
    for USUCompleto in evento:
        if USUCompleto.email == USUCompletoEmail and USUCompleto.senha == USUCompletoSenha :
            evento = USUComp(USUCompleto.id, USUCompleto.nick, USUCompleto.email, USUCompleto.senha)
            Res.append(format_USUCompleto(evento))
            #login_user(USUCompleto)
            print(Res)
            return Res

class ITEM(db.Model):
    __tablename__='ITENS'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String)
    lista_id = db.Column(db.Integer)

    def __repr__(self):
        return f"Itens: {self.conteudo, self.lista_id}"

    def __init__(self, conteudo, lista_id):
        self.conteudo = conteudo
        self.lista_id = lista_id

    def __init__(self, conteudo):
        self.conteudo = conteudo

def format_Itens(Itens):
    return {
        "id": Itens.id,
        "conteudo": Itens.conteudo,
        "listaid": Itens.lista_id
    }

@app.route('/item_all')
def getItem():
    Itens = ITEM.query.all()
    itens_list = []
    for item in Itens:
        itens_list.append(format_Itens(item))
    return {"itens": itens_list}

@app.route('/insereListaUsuNCad', methods = ['POST'])
def insereItens():
    Conteudo = request.json['item']
    evento = ITEM(Conteudo)
    #db.session.add(evento)
    #db.session.commit()
    return format_Itens(evento)


class Lista(db.Model):

    __tablename__='LISTA'
    id = db.Column(db.Integer, primary_key=True)
    usu_id = db.Column(db.Integer)
    descricao = db.Column(db.String) 

    def __repr__(self):
        return f"LISTA: {self.descricao}"

    def __init__(self, descricao):
        self.DESCRICAO = descricao

    def __init__(self, descricao, usu_id):
        self.descricao = descricao
        self.usu_id = usu_id

def format_Lista(lista):
    return {
        "id": lista.id,
        "descricao": lista.descricao,
        "usu_id": lista.usu_id
    }

@app.route('/lista_all')
def getLista():
    listas = Lista.query.all()
    lista_list = []
    for lista in listas:
        lista_list.append(format_Lista(lista))
    return {"itens": lista_list}




@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅 xo xo"})


if __name__ == '__main__':

    app.run(debug=True, port=os.getenv("PORT", default=5000))