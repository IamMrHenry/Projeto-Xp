from modelos.db import db
from modelos.iot.dispositivo import Dispositivo
from datetime import datetime

class Sensor(db.Model):
    __tablename__ = 'sensores'
    id= db.Column('id', db.Integer, primary_key=True)
    dispositivo_id = db.Column( db.Integer, db.ForeignKey(Dispositivo.id))
    unidade = db.Column(db.String(50))

    dados = db.relationship('Dados', backref='dispositivos', lazy=True)

    def save_sensor(nome, marca, modelo, unidade, status):
        dispositivo = Dispositivo(nome = nome, marca = marca,
        modelo = modelo, status = status, data_criacao = datetime.now())
        sensor = Sensor(dispositivo_id = dispositivo.id, unidade= unidade)
        dispositivo.sensores.append(sensor)
        db.session.add(dispositivo)
        db.session.commit()
    
    def get_sensors():
        sensores = Sensor.query.join(Dispositivo, Dispositivo.id == Sensor.dispositivo_id)\
                .add_columns(Sensor.id, Sensor.dispositivo_id, Dispositivo.nome,
                Dispositivo.marca, Dispositivo.modelo,
                Dispositivo.status, Dispositivo.data_criacao,
                Sensor.unidade).all()
        return sensores
    
    def get_single_sensor(id):
        sensor = Sensor.query.filter(Sensor.id == id).first()
        if sensor is not None:
            sensor = Sensor.query.join(Dispositivo, Dispositivo.id == sensor.dispositivo_id)\
                .add_columns(Sensor.id, Sensor.dispositivo_id, Dispositivo.nome, Dispositivo.marca,
                Dispositivo.modelo, Dispositivo.status, Sensor.unidade, Dispositivo.data_criacao).first()
            return [sensor]
        
    def update_sensor(id,nome, marca, modelo, unidade, status):
        sensor = Sensor.query.filter(Sensor.id == id).first()
        dispositivo = Dispositivo.query.filter(Dispositivo.id == sensor.dispositivo_id).first()
        if dispositivo is not None:
            dispositivo.nome = nome
            dispositivo.marca = marca
            dispositivo.modelo = modelo
            sensor.unidade = unidade
            dispositivo.status = status
            dispositivo.data_criacao = datetime.now()
            db.session.commit()
            return Sensor.get_sensors()
    
    def delete_sensor(id):
        sensor = Sensor.query.filter(Sensor.id == id).first()
        device = Dispositivo.query.filter(Dispositivo.id == sensor.dispositivo_id).first()
        db.session.delete(device)
        db.session.delete(sensor)
        db.session.commit()
        return Sensor.get_sensors()