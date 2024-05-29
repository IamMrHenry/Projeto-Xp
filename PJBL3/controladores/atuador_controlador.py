from flask import Blueprint, request, render_template

atuadores = {
    "Led": "Desligado",
    "Buzzer": "Desligado",
    "Servo Motor": "Fechado",
}

atuador = Blueprint("atuador",__name__, template_folder="views")

"""@atuador.route('/atuador_listar')
def atuador_listar():
    return render_template("atuador_listar.html", atuadores=atuadores)

@atuador.route('/atuador_listar_user')
def atuador_listar_user():
    return render_template("atuador_listar_user.html", atuadores=atuadores)

@atuador.route('/atuador_cadastrar')
def atuador_cadastrar():
    return render_template("atuador_cadastrar.html")

@atuador.route('/atuador_adicionar', methods=['GET','POST'])
def atuador_adicionar():
    global atuadores
    if request.method == 'POST':
        tipo = request.form['tipo']
        modelo = request.form['modelo']
    else:
        tipo = request.args.get('tipo', None)
        modelo = request.args.get('modelo', None)
    atuadores[tipo] = modelo
    return render_template("atuador_listar.html", atuadores=atuadores)

@atuador.route('/atuador_deletar')
def atuador_deletar():
    global atuadores
    atuador = request.args.get('atuador', None)
    atuadores.pop(atuador)
    return render_template("atuador_listar.html", atuadores=atuadores)

@atuador.route('/atuador_alterar')
def atuador_alterar():
    global atuadores
    atuador = request.args.get('atuador', None)
    return render_template("atuador_alterar.html", tipo=atuador, modelo=atuadores[atuador])

@atuador.route('/atuador_atualizar', methods=['GET','POST'])
def atuador_atualizar():
    id = request.form.get("id")
    tipo = request.form.get("tipo")
    modelo = request.form.get("modelo")
    if tipo in atuadores:
        atuadores[tipo] = modelo
    else:
        atuadores.pop(id)
        atuadores[tipo] = modelo
    return render_template("atuador_listar.html", atuadores = atuadores)"""