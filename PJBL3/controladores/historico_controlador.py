from flask import Blueprint, request, render_template, request, jsonify
from modelos.iot.historico import Dados
from modelos.iot.sensores import Sensor
from utils.role import role_proibida
import flask_login

historico = Blueprint("historico",__name__, template_folder="views")

@historico.route('/tempo_real')
@flask_login.login_required
@role_proibida("Operador")
def tempo_real():
    leitura = {}
    sensores = Sensor.get_sensors()
    for i in sensores:
        leitura[i.nome] = Dados.get_latest_read(i.nome)
    read = {}
    return render_template("tempo_real.html", leitura = leitura, role = flask_login.current_user.papel_id, sensors = sensores, read=read)

@historico.route("/get_dados", methods=['POST'])
@flask_login.login_required
@role_proibida("Operador")
def get_dados():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Dados.get_read(id, start, end)
        sensores = Sensor.get_sensors()
        leitura={}
        for i in sensores:
            leitura[i.nome] = Dados.get_latest_read(i.nome)
        return render_template("tempo_real.html", leitura= leitura,sensors = sensores, read = read, role = flask_login.current_user.papel_id)