from flask import Blueprint, request, render_template


login = Blueprint("login",__name__, template_folder="views")

"""@login.route('/user_validar', methods=['POST'])
def user_validar():
    if request.method == 'POST':
        user = request.form['user']
        senha = request.form['senha']
        if user in users and users[user][0] == senha:
            if  users[user][1] == "Administrador":
                return render_template('adm_home.html')
            else:
                return render_template('user_home.html')
        else:
            status = 1
            return render_template('login.html', status=status)
            
    else:
        status = 0
        return render_template('login.html', status=status)

@login.route('/user_listar')
def user_listar():
    global users
    return render_template("user_listar.html", users=users, status=0)

@login.route('/user_cadastrar')
def user_cadastar():
    return render_template("user_cadastrar.html")

@login.route('/user_adicionar', methods=['GET','POST'])
def user_adicionar():
    global users
    if request.method == 'POST':
        user = request.form['user']
        senha = request.form['senha']
    else:
        user = request.args.get('user', None)
        senha = request.args.get('senha', None)
        adm = request.form.get('role', None)
    users[user] = [senha, "Usuário"]
    return render_template("user_listar.html", users=users)

@login.route('/user_deletar')
def user_deletar():
    global users
    user = request.args.get('user', None)
    if users[user][1]=="Administrador":
        return render_template("user_listar.html", users=users, status=1)
    users.pop(user)
    return render_template("user_listar.html", users=users)

@login.route('/user_alterar')
def user_alterar():
    global users
    global roles
    user = request.args.get('user', None)
    return render_template("user_alterar.html", user=user)

@login.route('/user_atualizar', methods=['GET','POST'])
def user_atualizar():
    id = request.form.get("id")
    user = request.form.get("user")
    senha = request.form.get("senha")
    if user in users:
        users[user][0] = senha
    else:
        adm = users[id][1]
        users.pop(id)
        users[user] = [senha, adm]
    return render_template("user_listar.html", users = users)"""
