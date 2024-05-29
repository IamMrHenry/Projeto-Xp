from modelos.db import db
from modelos.iot.dispositivo import Dispositivo

class Sensor(db.Model):
    __tablename__ = 'sensores'
    id= db.Column('id', db.Integer, primary_key=True)
    dispositivos_id = db.Column( db.Integer, db.ForeignKey(Dispositivo.id))
    unidade = db.Column(db.String(50))
    topico = db.Column(db.String(50))

"""    def save_sensor(name, brand, model, topic, unit, is_active):
        device = Dispositivo(name = name, brand = brand,
        model = model, is_active = is_active)
        sensor = Sensor(devices_id = device.id, unit= unit, topic = topic)
        device.sensores.append(sensor)
        db.session.add(device)
        db.session.commit()
    
    def get_sensors():
        sensors = Sensor.query.join(Dispositivo, Dispositivo.id == Sensor.dispositivos_id)\
                .add_columns(Dispositivo.id, Dispositivo.nome,
                Dispositivo.marca, Dispositivo.modelo,
                Dispositivo.ativo, Sensor.topico,
                Sensor.unidade).all()
        return sensors
    def get_single_sensor(id):
        sensor = Sensor.query.filter(Sensor.dispositivos_id == id).first()
        if sensor is not None:
            sensor = Sensor.query.filter(Sensor.dispositivos_id == id)\
                .join(Dispositivo).add_columns(Dispositivo.id, Dispositivo.nome, Dispositivo.marca,
                Dispositivo.modelo, Dispositivo.ativo, Sensor.topico, Sensor.unidade).first()
            return [sensor]
        
    def update_sensor(id,name, brand, model, topic, unit, is_active):
        device = Dispositivo.query.filter(Dispositivo.id == id).first()
        sensor = Sensor.query.filter(Sensor.dispositivos_id == id).first()
        if device is not None:
            device.nome = name
            device.marca = brand
            device.modelo = model
            sensor.topico = topic
            sensor.unidade = unit
            device.ativo = is_active
            db.session.commit()
            return Sensor.get_sensors()
    
    def delete_sensor(id):
        device = Dispositivo.query.filter(Dispositivo.id == id).first()
        sensor = Sensor.query.filter(Sensor.dispositivos_id == id).first()
        db.session.delete(sensor)
        db.session.delete(device)
        db.session.commit()
        return Sensor.get_sensors()"""