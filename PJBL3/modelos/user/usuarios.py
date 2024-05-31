from modelos.db import db
from modelos.user.papel import Papel

class Usuario(db.Model):
    __tablename__= "usuario"
    id = db.Column("id", db.Integer(), primary_key=True)
    papel_id = db.Column( db.Integer, db.ForeignKey(Papel.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    senha= db.Column(db.String(256) , nullable=False)

    def save_user(role_type_, username, email, senha):
        papel = Papel.get_single_role(role_type_)
        usuario = Usuario(papel_id = papel.id, username = username, email = email,
        senha = senha)
        db.session.add(usuario)
        db.session.commit()