from flask import Blueprint, request, render_template, request, jsonify
from modelos.iot.comando import Comando
from modelos.iot.atuadores import Atuador


comando = Blueprint("comando",__name__, template_folder="views")

@comando.route("/comandos_historicos")
def history_write():
    atuador = Atuador.get_atuador()
    write = {}
    return render_template("comandos_historicos.html", atuador = atuador, write = write)

@comando.route("/get_comandos", methods=['POST'])
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Comando.get_write(id, start, end)
        atuador = Atuador.get_atuador()
        return render_template("comandos_historicos.html", atuador = atuador, write = write)