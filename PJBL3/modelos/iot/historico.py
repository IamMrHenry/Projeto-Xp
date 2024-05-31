from modelos.db import db
from modelos.iot.dispositivo import Dispositivo
from modelos.iot.sensores import Sensor
from datetime import datetime

class Dados(db.Model):
    __tablename__ = 'dados'
    id= db.Column('id', db.Integer, nullable = False, primary_key=True)
    horario = db.Column(db.DateTime(), nullable = False)
    sensor_id= db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable = False)
    valor = db.Column( db.String(50), nullable = True)


    def save_read(nome, valor):
        dispositivo = Dispositivo.query.filter(Dispositivo.nome == nome).first()
        if dispositivo is None:
            return None  
        sensor = Sensor.query.filter(Sensor.dispositivo_id == dispositivo.id).first()
        if sensor is None:
            return None 
        if (sensor is not None) and (dispositivo.status==True):
            dados = Dados( horario = datetime.now(), sensor_id = sensor.id, valor = valor )
            db.session.add(dados)
            db.session.commit()
    
    def get_read(id, start, end):
        sensor = Sensor.query.filter(Sensor.dispositivo_id == id).first()
        read = Dados.query.filter(Dados.sensor_id == sensor.id,
                                Dados.horario > start,
                                Dados.horario<end).all()
        return read
    
    def get_latest_read(nome):
        dispositivo = Dispositivo.query.filter(Dispositivo.nome == nome).first()
        if dispositivo is None:
            return None  
        sensor = Sensor.query.filter(Sensor.dispositivo_id == dispositivo.id).first()
        if sensor is None:
            return None  
        read = Dados.query.filter(Dados.sensor_id == sensor.id).order_by(Dados.id.desc()).first()
        if read is None:
            return None
        return read.valor
