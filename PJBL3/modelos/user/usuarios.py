from modelos.db import db
from modelos.user.papel import Papel
from datetime import datetime
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__= "usuario"
    id = db.Column("id", db.Integer(), primary_key=True)
    papel_id = db.Column( db.Integer, db.ForeignKey(Papel.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    senha= db.Column(db.String(256) , nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)

    def save_user(papel, username, email, senha):
        papel = Papel.get_single_role(papel)
        usuario = Usuario(papel_id = papel.id, username = username, email = email,
        senha = senha, data_criacao = datetime.now())
        db.session.add(usuario)
        db.session.commit()

    def get_usuarios():
        usuarios = Usuario.query.join(Papel, Papel.id == Usuario.papel_id)\
                .add_columns(Papel.nome, Usuario.id, 
                Usuario.username, Usuario.email).all()
        return usuarios
    
    def get_single_usuario(id):
        usuario = Usuario.query.filter(Usuario.id == id)\
                .add_columns(Usuario.papel_id, Usuario.id, 
                Usuario.username, Usuario.email).first()
        return usuario
        
    def update_usuario(id,username, papel, email, senha):
        usuario = Usuario.query.filter(Usuario.id == id).first()
        if usuario is not None:
            usuario.username = username
            usuario.email = email
            usuario.senha = senha
            usuario.papel_id = int(papel)
            usuario.data_criacao = datetime.now()
            db.session.commit()
            return Usuario.get_usuarios()
    
    def delete_usuario(id):
        usuario = Usuario.query.filter(Usuario.id == id).first()
        db.session.delete(usuario)
        db.session.commit()
        return Usuario.get_usuarios()
    
    def get_user_id(user_id):
        id = Usuario.query.filter_by(id = user_id).first()
        if id is not None:
            return id
    def validate_user(email,password):
        user = Usuario.query.filter(Usuario.username == email and Usuario.senha ==password).first()
        if(user==None):
            return None
        else:
            return user

