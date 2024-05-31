from flask import Blueprint, request, render_template, request, jsonify
from modelos.iot.historico import Dados
from modelos.iot.sensores import Sensor

historico = Blueprint("historico",__name__, template_folder="views")

@historico.route("/dados_historicos")
def dados_historicos():
    sensors = Sensor.get_sensors()
    print(sensors)
    read = {}
    return render_template("dados_historicos.html", sensors = sensors, read = read)

@historico.route("/get_dados", methods=['POST'])
def get_dados():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Dados.get_read(id, start, end)
        sensors = Sensor.get_sensors()
        return render_template("dados_historicos.html", sensors = sensors, read = read)