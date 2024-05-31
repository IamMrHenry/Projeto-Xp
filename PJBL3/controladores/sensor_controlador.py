from flask import Blueprint, request, render_template
from modelos.iot.sensores import Sensor

sensor = Blueprint("sensor",__name__, template_folder="views")

@sensor.route('/sensor_listar')
def sensor_listar():
    sensores = Sensor.get_sensors()
    return render_template("sensor_listar.html", sensores=sensores)

@sensor.route('/sensor_cadastrar')
def sensor_cadastrar():
    return render_template("sensor_cadastrar.html")

@sensor.route('/sensor_adicionar', methods=['GET','POST'])
def sensor_adicionar():
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    unidade = request.form.get("unidade")
    status = True if request.form.get("status") == "on" else False
    Sensor.save_sensor(nome, marca, modelo, unidade, status)
    sensores = Sensor.get_sensors()
    return render_template("sensor_listar.html", sensores=sensores)

@sensor.route('/sensor_deletar')
def sensor_deletar():
    id = request.args.get('sensor', None)
    sensores = Sensor.delete_sensor(id)
    return render_template("sensor_listar.html", sensores=sensores)

@sensor.route('/sensor_alterar')
def sensor_alterar():
    id = request.args.get('sensor', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("sensor_alterar.html", sensor=sensor)

@sensor.route('/sensor_atualizar', methods=['GET','POST'])
def sensor_atualizar():
    id = request.form.get("id")
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    unidade = request.form.get("unidade")
    status = True if request.form.get("status") == "on" else False
    sensores = Sensor.update_sensor(id, nome, marca, modelo, unidade, status )
    return render_template("sensor_listar.html", sensores = sensores)