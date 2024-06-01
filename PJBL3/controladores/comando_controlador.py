from flask import Blueprint, request, render_template, request, jsonify
from modelos.iot.comando import Comando
from modelos.iot.atuadores import Atuador
from utils.role import role_proibida
import flask_login

comando = Blueprint("comando",__name__, template_folder="views")

@comando.route('/comando_remoto')
@flask_login.login_required
@role_proibida("Estático")
def comando_remoto():
    atuador = Atuador.get_atuador()
    write = {}
    return render_template("comando_remoto.html",atuadores = atuador, write = write, role = flask_login.current_user.papel_id)


@comando.route("/get_comandos", methods=['POST'])
@flask_login.login_required
@role_proibida("Estático")
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Comando.get_write(id, start, end)
        atuador = Atuador.get_atuador()
        return render_template("comando_remoto.html", atuadores = atuador, write = write, role = flask_login.current_user.papel_id)