from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel

import sys

#------------------------------------------------------------------
# Inicialização do projeto
app = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Projeto CondaConta')
spec.register(app)
database = TinyDB('database.json')
#------------------------------------------------------------------

#------------------------------------------------------------------
#  Criação das contas e inserção delas dentro do banco TinyDB
conta_corrente = {
    "titularidade":"Willian Freitas",
    "tipo":"Corrente",
    "saldo":1000
}

conta_poupanca = {
    "titularidade":"Willian Freitas",
    "tipo":"Poupanca",
    "saldo":1
}

database.insert(conta_corrente)
database.insert(conta_poupanca)
#------------------------------------------------------------------

#------------------------------------------------------------------
# Modelos como os dados serão representados
class Saldo(BaseModel):
    titularidade: str
    tipo: str

class Transferencia(BaseModel):
    titularidade: str
    valor: str
    tipo: str

#------------------------------------------------------------------
#  Rotas que serão utilizadas pela API
#------------------------------------------------------------------
@app.post('/saldo')
@spec.validate(body=Request(Saldo))
def busca_saldo():
    """
    Retorna o saldo da conta
    variaveis:
        cpf - INT - CPF da conta
        titularidade - STR - titular da conta
        tipo - STR - Tipo da conta, se é Corrente ou Poupanca
    """
    conta = request.context.body.dict()
    query = Query()
    busca = database.search((query.titularidade==conta["titularidade"]) & (query.tipo==conta["tipo"]))
    resultado = {
        'titular': busca[0]['titularidade'],
        'saldo': busca[0]['saldo'],
        'tipo de conta': busca[0]['tipo']
    }
    return jsonify(resultado)


@app.post('/transferencia')
@spec.validate(body=Request(Transferencia))
def investimento():
    """
    Faz a transferencia de uma conta Corrente para uma Poupanca e vice-versa com mesma titularidade
    variaveis:
        cpf - INT - CPF da conta
        titularidade - STR - titular da conta
        tipo - STR - Pode ser do tipo Investimento ou Resgate
    """
    transferencia = request.context.body.dict()
    query = Query()
    busca = database.search((query.titularidade==transferencia["titularidade"]))
    if len(busca) < 2:
        return "Este titular possui apenas uma conta."
    else:
        if transferencia["tipo"] == "Investimento":

            if busca[0]['tipo'] == "Corrente":
                saldo_corrente = busca[0]['saldo'] - int(transferencia["valor"])
                saldo_poupanca = busca[1]['saldo'] + int(transferencia["valor"])
                database.update({'saldo':saldo_corrente}, query.tipo == "Corrente")
                database.update({'saldo':saldo_poupanca}, query.tipo == "Poupanca")
                return "Saldo atualizado com sucesso."
            
            if busca[0]['tipo'] == "Poupanca":
                saldo_poupanca = busca[1]['saldo'] + int(transferencia["valor"])
                saldo_corrente = busca[0]['saldo'] - int(transferencia["valor"])
                database.update({'saldo':saldo_poupanca}, query.tipo == "Poupanca")
                database.update({'saldo':saldo_corrente}, query.tipo == "Corrente")
                return "Saldo atualizado com sucesso."
        
        if transferencia["tipo"] == "Resgate":

            if busca[0]['tipo'] == "Corrente":
                saldo_corrente = busca[0]['saldo'] + int(transferencia["valor"])
                saldo_poupanca = busca[1]['saldo'] - int(transferencia["valor"])
                database.update({'saldo':saldo_corrente}, query.tipo == "Corrente")
                database.update({'saldo':saldo_poupanca}, query.tipo == "Resgate")
                return "Saldo atualizado com sucesso."
            
            if busca[0]['tipo'] == "Poupanca":
                saldo_poupanca = busca[1]['saldo'] - int(transferencia["valor"])
                saldo_corrente = busca[0]['saldo'] + int(transferencia["valor"])
                database.update({'saldo':saldo_poupanca}, query.tipo == "Poupanca")
                database.update({'saldo':saldo_corrente}, query.tipo == "Corrente")
                return "Saldo atualizado com sucesso."

if __name__ == "__name__":
    app.run(debug=True)