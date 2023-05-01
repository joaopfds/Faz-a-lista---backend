from flask import Flask, jsonify, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:b2HniV8IfDcjqLkMYmsO@containers-us-west-173.railway.app:6695/railway"
app.config['JSON_AS_ASCII'] = False
CORS(app)

db = SQLAlchemy(app)

class USU(db.Model):

    __tablename__='usu'
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

@app.route('/all')
def getUSU():
    usus = USU.query.all()
    usus_list = []
    for usu in usus:
        usus_list.append(format_usu(usu))
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

class Itens(db.Model):

    __tablename__='Itens'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String)
    listaid = db.Column(db.Integer)

    def __repr__(self):
        return f"Itens: {self.conteudo, self.listaid}"

    def __init__(self, conteudo, listaid):
        self.conteudo = conteudo
        self.listaid = listaid

def format_Itens(Itens):
    return {
        "conteudo": Itens.conteudo,
        "listaid": Itens.listaid
    }

@app.route('/insereListaUsuNCad', methods = ['POST'])
def insereItens():
    listaItem = request.json['item']
    Conteudo = ""
    evento = Itens(Conteudo, listaItem)
    #db.session.add(evento)
    #db.session.commit()
    return format_Itens(evento)




class Lista(db.Model):

    __tablename__='Lista'
    id = db.Column(db.Integer, primary_key=True)
    USUID = db.Column(db.Integer)
    DESCRICAO = db.Column(db.String) 

    def __repr__(self):
        return f"LISTA: {self.DESCRICAO}"

    def __init__(self, DESCRICAO):
        self.DESCRICAO = DESCRICAO

    def __init__(self, DESCRICAO, USUID):
        self.DESCRICAO = DESCRICAO
        self.USUID = USUID

def format_Lista(lista):
    return {
        "DESCRICAO": lista.DESCRICAO,
        "USUID": lista.USUID
    }



@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅 xo xo"})


if __name__ == '__main__':

    app.run(debug=True, port=os.getenv("PORT", default=5000))