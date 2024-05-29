from flask import Blueprint, request, render_template
from modelos.iot.sensores import Sensor

sensor = Blueprint("sensor",__name__, template_folder="views")

"""@sensor.route('/sensor_listar')
def sensor_listar():
    return render_template("sensor_listar.html", sensores=sensores)

@sensor.route('/sensor_listar_user')
def sensor_listar_user():
    return render_template("sensor_listar_user.html", sensores=sensores)

@sensor.route('/sensor_cadastrar')
def sensor_cadastrar():
    return render_template("sensor_cadastrar.html")

@sensor.route('/sensor_adicionar', methods=['GET','POST'])
def sensor_adicionar():
    global sensores
    if request.method == 'POST':
        tipo = request.form['tipo']
        modelo = request.form['modelo']
    else:
        tipo = request.args.get('tipo', None)
        modelo = request.args.get('modelo', None)
    sensores[tipo] = modelo
    return render_template("sensor_listar.html", sensores=sensores)

@sensor.route('/sensor_deletar')
def sensor_deletar():
    global sensores
    sensor = request.args.get('sensor', None)
    sensores.pop(sensor)
    return render_template("sensor_listar.html", sensores=sensores)

@sensor.route('/sensor_alterar')
def sensor_alterar():
    global sensores
    sensor = request.args.get('sensor', None)
    return render_template("sensor_alterar.html", tipo=sensor, modelo=sensores[sensor])

@sensor.route('/sensor_atualizar', methods=['GET','POST'])
def sensor_atualizar():
    id = request.form.get("id")
    tipo = request.form.get("tipo")
    modelo = request.form.get("modelo")
    if tipo in sensores:
        sensores[tipo] = modelo
    else:
        sensores.pop(id)
        sensores[tipo] = modelo
    return render_template("sensor_listar.html", sensores = sensores)"""