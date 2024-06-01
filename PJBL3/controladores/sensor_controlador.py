from flask import Blueprint, request, render_template
from modelos.iot.sensores import Sensor
from utils.role import role_proibida
import flask_login

sensor = Blueprint("sensor",__name__, template_folder="views")

@sensor.route('/sensor_listar')
@flask_login.login_required
def sensor_listar():
    sensores = Sensor.get_sensors()
    return render_template("sensor_listar.html", sensores=sensores, role = flask_login.current_user.papel_id)

@sensor.route('/sensor_cadastrar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def sensor_cadastrar():
    return render_template("sensor_cadastrar.html", role = flask_login.current_user.papel_id)

@sensor.route('/sensor_adicionar', methods=['GET','POST'])
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def sensor_adicionar():
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    unidade = request.form.get("unidade")
    status = True if request.form.get("status") == "on" else False
    Sensor.save_sensor(nome, marca, modelo, unidade, status)
    sensores = Sensor.get_sensors()
    return render_template("sensor_listar.html", sensores=sensores, role = flask_login.current_user.papel_id)

@sensor.route('/sensor_deletar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def sensor_deletar():
    id = request.args.get('sensor', None)
    sensores = Sensor.delete_sensor(id)
    return render_template("sensor_listar.html", sensores=sensores, role = flask_login.current_user.papel_id)

@sensor.route('/sensor_alterar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def sensor_alterar():
    id = request.args.get('sensor', None)
    print(id)
    sensor = Sensor.get_single_sensor(id)
    return render_template("sensor_alterar.html", sensor=sensor, role = flask_login.current_user.papel_id)

@sensor.route('/sensor_atualizar', methods=['GET','POST'])
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def sensor_atualizar():
    id = request.form.get("id")
    nome = request.form.get("nome")
    marca = request.form.get("marca")
    modelo = request.form.get("modelo")
    unidade = request.form.get("unidade")
    status = True if request.form.get("status") == "on" else False
    sensores = Sensor.update_sensor(id, nome, marca, modelo, unidade, status )
    return render_template("sensor_listar.html", sensores = sensores, role = flask_login.current_user.papel_id)