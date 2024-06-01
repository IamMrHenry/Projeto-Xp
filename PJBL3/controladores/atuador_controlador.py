from flask import Blueprint, request, render_template
from modelos.iot.atuadores import Atuador
from utils.role import role_proibida
import flask_login

atuador = Blueprint("atuador",__name__, template_folder="views")

@atuador.route('/atuador_listar')
@flask_login.login_required
def atuador_listar():
    atuadores = Atuador.get_atuador()
    return render_template("atuador_listar.html", atuadores=atuadores, role = flask_login.current_user.papel_id)


@atuador.route('/atuador_cadastrar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def atuador_cadastrar():
    return render_template("atuador_cadastrar.html")

@atuador.route('/atuador_adicionar', methods=['GET','POST'])
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def atuador_adicionar():
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    status = True if request.form.get("status") == "on" else False
    Atuador.save_atuador(nome, marca, modelo, status)
    atuadores = Atuador.get_atuador()
    return render_template("atuador_listar.html", atuadores=atuadores, role = flask_login.current_user.papel_id)

@atuador.route('/atuador_deletar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def atuador_deletar():
    id = request.args.get('atuador', None)
    atuadores = Atuador.delete_atuador(id)
    return render_template("atuador_listar.html", atuadores=atuadores, role = flask_login.current_user.papel_id)

@atuador.route('/atuador_alterar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def atuador_alterar():
    id = request.args.get('atuador', None)
    print(id)
    atuadores = Atuador.get_single_atuador(id)
    return render_template("atuador_alterar.html", atuadores=atuadores, role = flask_login.current_user.papel_id)

@atuador.route('/atuador_atualizar', methods=['GET','POST'])
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def atuador_atualizar():
    id = request.form.get("id")
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    status = True if request.form.get("status") == "on" else False
    atuadores = Atuador.update_atuador(id, nome, marca, modelo, status )
    return render_template("atuador_listar.html", atuadores = atuadores, role = flask_login.current_user.papel_id)