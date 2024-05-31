from flask import Flask
from modelos import *
from modelos.user.papel import Papel
from modelos.user.usuarios import Usuario

def criar_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        Papel.save_role( "Administrador", "Usuário full" )
        Papel.save_role( "Usuáios Comum", "Usuário com limitações")
        Usuario.save_user("Administrador","Gabriel", "gabriel@email.com","123")

