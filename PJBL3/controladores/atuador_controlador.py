from flask import Blueprint, request, render_template
from modelos.iot.atuadores import Atuador

atuador = Blueprint("atuador",__name__, template_folder="views")

@atuador.route('/atuador_listar')
def atuador_listar():
    atuadores = Atuador.get_atuador()
    return render_template("atuador_listar.html", atuadores=atuadores)


@atuador.route('/atuador_cadastrar')
def atuador_cadastrar():
    return render_template("atuador_cadastrar.html")

@atuador.route('/atuador_adicionar', methods=['GET','POST'])
def atuador_adicionar():
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    status = True if request.form.get("status") == "on" else False
    Atuador.save_atuador(nome, marca, modelo, status)
    atuadores = Atuador.get_atuador()
    return render_template("atuador_listar.html", atuadores=atuadores)

@atuador.route('/atuador_deletar')
def atuador_deletar():
    id = request.args.get('atuador', None)
    atuadores = Atuador.delete_atuador(id)
    return render_template("atuador_listar.html", atuadores=atuadores)

@atuador.route('/atuador_alterar')
def atuador_alterar():
    id = request.args.get('atuador', None)
    atuadores = Atuador.get_single_atuador(id)
    return render_template("atuador_alterar.html", atuadores=atuadores)

@atuador.route('/atuador_atualizar', methods=['GET','POST'])
def atuador_atualizar():
    id = request.form.get("id")
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    status = True if request.form.get("status") == "on" else False
    atuadores = Atuador.update_atuador(id, nome, marca, modelo, status )
    return render_template("atuador_listar.html", atuadores = atuadores)