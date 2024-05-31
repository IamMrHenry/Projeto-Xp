from modelos.db import db

class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'
    id= db.Column('id', db.Integer, primary_key=True)
    nome= db.Column(db.String(50), nullable = False)
    marca= db.Column(db.String(50))
    modelo= db.Column(db.String(50))
    status= db.Column(db.Boolean, nullable= False, default= False)
    data_criacao = db.Column(db.DateTime, nullable=False)

    sensores = db.relationship('Sensor', backref='dispositivos', lazy=True)
    atuadores = db.relationship('Atuador', backref='dispositivos', lazy=True)