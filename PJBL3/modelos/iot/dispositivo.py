from modelos.db import db
class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'
    id= db.Column('id', db.Integer, primary_key=True)
    nome= db.Column(db.String(50))
    marca= db.Column(db.String(50))
    modelo= db.Column(db.String(50))
    ativo= db.Column(db.Boolean, nullable= False, default= False)

sensores = db.relationship('Sensor', backref='dispositivos', lazy=True)
atuadores = db.relationship('Atuador', backref='dispositivos', lazy=True)