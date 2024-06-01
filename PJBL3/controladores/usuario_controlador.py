from flask import Blueprint, request, render_template
from utils.role import role_proibida
from modelos.user.papel import Papel
from modelos.user.usuarios import Usuario
import flask_login

usuario = Blueprint("usuario",__name__, template_folder="views")

@usuario.route('/user_cadastrar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def user_cadastar():
    papel = Papel.get_role()
    return render_template("user_cadastrar.html", papel=papel)

@usuario.route('/user_adicionar', methods=['GET','POST'])
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def user_adicionar():
    if request.method == 'POST':
        papel = request.form['papel']
        usuario = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha']
        Usuario.save_user(papel, usuario, email,senha)
    return render_template("user_listar.html", usuarios=Usuario.get_usuarios(), role = flask_login.current_user.papel_id)

@usuario.route('/user_listar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def user_listar():
    return render_template("user_listar.html", usuarios=Usuario.get_usuarios(), role = flask_login.current_user.papel_id)

@usuario.route('/user_deletar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def user_deletar():
    id = request.args.get('user', None)
    usuario = Usuario.get_single_usuario(id)
    if usuario.papel_id != 1:
        Usuario.delete_usuario(id)
    return render_template("user_listar.html", usuarios=Usuario.get_usuarios(), role = flask_login.current_user.papel_id)

@usuario.route('/user_alterar')
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def user_alterar():
    id = request.args.get('user', None)
    user = Usuario.get_single_usuario(id)
    print(user)
    papel = Papel.get_role()
    return render_template("user_alterar.html", usuarios=user, papel=papel, role = flask_login.current_user.papel_id)

@usuario.route('/user_atualizar', methods=['GET','POST'])
@flask_login.login_required
@role_proibida("Operador")
@role_proibida("Estático")
def user_atualizar():
    id = request.form.get("id")
    usuario = request.form.get("nome")
    senha = request.form.get("senha")
    email = request.form.get("email")
    papel = request.form.get("papel")
    usuarios = Usuario.update_usuario(id, usuario,papel,email,senha)
    return render_template("user_listar.html", usuarios = usuarios, role = flask_login.current_user.papel_id)