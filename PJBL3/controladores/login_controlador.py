import flask_login
from flask_login import LoginManager, logout_user
from modelos.user.usuarios import Usuario
from flask import Blueprint, request, render_template, flash


login_manager = LoginManager()
login = Blueprint("login",__name__, template_folder="views")



@login_manager.user_loader
def get_user(user_id):
    return Usuario.query.filter_by(id = user_id).first()

@login.route('/login')  # Defina a rota da página de login
def logi():
    # Sua lógica de renderização da página de login aqui
    return render_template('login.html')

@login.route('/user_validar', methods=['POST'])
def usuario_validar():
    if request.method == 'POST':
        email = request.form['user']
        senha = request.form['senha']
        user = Usuario.validate_user(email, senha)
        if(user == None):
            flash('usuário e/ou senha incorreta!')
            return render_template('login.html')
        else:
            print(user)
            flask_login.login_user(user)
            return render_template('home.html', role = flask_login.current_user.papel_id)
    else:
        return render_template('login.html')

@login.route('/logoff')
@flask_login.login_required
def logoff():
    logout_user()
    return render_template("login.html")