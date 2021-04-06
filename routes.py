from flask import Flask, request

from main import insertUsuario

from carregar_modelo import main

app = Flask("Modelo")

@app.route("/olamundo", methods=["GET"])
def olaMundo():
    return {"Olá" : "Mundo"}

@app.route("/cadastro/usuario", methods=["POST"])
def cadastraUsuario():

    body = request.get_json()

    if("name" not in body):
        return {"status":400, "message": "Nome é obrigatório"}

    user = insertUsuario(body["name"], body["email"], body["password"])

    return geraResponse(200, "Usuário criado", "user", user)

def geraResponse(status, message, nome_conteudo=False, conteudo=False):
    response = {}
    response["status"] = status
    response["message"] = message

    if(nome_conteudo and conteudo):
        response[nome_conteudo] = conteudo
    
    return response

app.run()
