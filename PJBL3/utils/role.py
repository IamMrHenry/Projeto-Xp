from functools import wraps
from flask import abort
from flask_login import current_user, login_manager
from flask import redirect, url_for, request
from modelos.user.usuarios import Papel

def role_proibida(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            papel = Papel.get_single_role(role)
            if current_user.is_authenticated and current_user.papel_id != papel.id:
                return f(*args, **kwargs)  # Permite o acesso se o usuário tiver o papel necessário
            return redirect(url_for("login.logi", next=request.url))
        return decorated_function
    return decorator