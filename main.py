from flask import Flask, jsonify, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:b2HniV8IfDcjqLkMYmsO@containers-us-west-173.railway.app:6695/railway"
app.config['JSON_AS_ASCII'] = False

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

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅 xo xo"})


if __name__ == '__main__':

    app.run(debug=True, port=os.getenv("PORT", default=5000))