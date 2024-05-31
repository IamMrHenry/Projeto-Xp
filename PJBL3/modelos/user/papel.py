from modelos.db import db


class Papel(db.Model):
    __tablename__ = 'papel'
    id = db.Column("id", db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(512))

    def save_role(nome, descricao):
        papel = Papel( nome = nome, descricao = descricao )
        db.session.add(papel)
        db.session.commit()

    def get_single_role(nome):
        papel = Papel.query.filter(Papel.nome == nome).first()
        return papel
    def get_role():
        papel = Papel.query.all()
        return papel
