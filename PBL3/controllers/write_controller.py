from flask import Blueprint, request, render_template, request, jsonify
from modelo.iot.write import Write
from modelo.iot.atuadores import Actuator


write_ = Blueprint("write_",__name__, template_folder="views")

@write_.route("/history_write")
def history_write():
    actuator = Actuator.get_actuator()
    write = {}
    return render_template("history_write.html", actuators = actuator, write = write)

@write_.route("/get_write", methods=['POST'])
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Write.get_write(id, start, end)
        actuator = Actuator.get_actuator()
        return render_template("history_write.html", actuators = actuator, write = write)