@app.route('/ckusu', methods = ['POST'])
def ckUSU():
    data = request
    print(data.json)
    usuEmail = data.json['email']
    usuSenha = data.json['senha']
    usuarios = USU.query.all()
    usuList = []
    for usua in usuarios:
        print(usua)
        usuList.append(USU.format_usu(usua))
    return {"usus": usuList}
