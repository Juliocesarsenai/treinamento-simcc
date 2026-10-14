from flask import Blueprint, jsonify, request
from dao.dao_pesquisadores import (
    consultar_pesquisadores,
    criar_pesquisador,
    atualizar_pesquisador,
    apagar_pesquisador
)

rest_pesquisador = Blueprint("rest_pesquisador", __name__)

# 1. READ (Listar todos os pesquisadores)
@rest_pesquisador.route("/pesquisadores", methods=["GET"])
def listar():
    dados = consultar_pesquisadores()
    return jsonify(dados), 200

# 2. CREATE (Criar um novo pesquisador)
@rest_pesquisador.route("/pesquisadores", methods=["POST"])
def criar():
    data = request.get_json()
    criar_pesquisador(data["pesquisadores_id"], data["lattes_id"], data["nome"])
    return jsonify({"mensagem": "Pesquisador criado com sucesso!"}), 201

# 3. UPDATE (Atualizar um pesquisador existente)
@rest_pesquisador.route("/pesquisadores/<id>", methods=["PUT"])
def atualizar(id):
    data = request.get_json()
    atualizar_pesquisador(id, data["lattes_id"], data["nome"])
    return jsonify({"mensagem": "Pesquisador atualizado com sucesso!"}), 200

# 4. DELETE (Apagar um pesquisador)
@rest_pesquisador.route("/pesquisadores/<id>", methods=["DELETE"])
def apagar(id):
    apagar_pesquisador(id)
    return jsonify({"mensagem": "Pesquisador apagado com sucesso!"}), 200