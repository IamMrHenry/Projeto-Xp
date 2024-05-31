from modelos.db import db
from modelos.iot.dispositivo import Dispositivo
from datetime import datetime

class Atuador(db.Model):
    __tablename__ = 'atuadores'
    id= db.Column('id', db.Integer, primary_key=True)
    dispositivo_id = db.Column( db.Integer, db.ForeignKey(Dispositivo.id))

    def save_atuador(nome, marca, modelo, status):
        dispositivo = Dispositivo(nome = nome, marca = marca,
        modelo = modelo, status = status, data_criacao = datetime.now())
        atuador = Atuador(dispositivo_id = dispositivo.id)
        dispositivo.atuadores.append(atuador)
        db.session.add(dispositivo)
        db.session.commit()
        
    def get_atuador():
        atuador = Atuador.query.join(Dispositivo, Dispositivo.id == Atuador.dispositivo_id)\
                .add_columns(Dispositivo.id, Dispositivo.nome,
                Dispositivo.marca, Dispositivo.modelo,
                Dispositivo.status, Dispositivo.data_criacao).all()
        return atuador
    
    def get_single_atuador(id):
        atuador = Atuador.query.filter(Atuador.dispositivo_id == id).first()
        if atuador is not None:
            atuador = Atuador.query.filter(Atuador.dispositivo_id == id)\
                .join(Dispositivo).add_columns(Dispositivo.id, Dispositivo.nome, Dispositivo.marca,
                Dispositivo.modelo, Dispositivo.status).first()
            return [atuador]
        
    def update_atuador(id,nome, marca, modelo, status):
        dispositivo = Dispositivo.query.filter(Dispositivo.id == id).first()
        atuador = Atuador.query.filter(Atuador.dispositivo_id == id).first()
        if dispositivo is not None:
            dispositivo.nome = nome
            dispositivo.marca = marca
            dispositivo.modelo = modelo
            dispositivo.status = status
            dispositivo.data_criacao = datetime.now()
            db.session.commit()
            return Atuador.get_atuador()

    def delete_atuador(id):
        dispositivo = Dispositivo.query.filter(Dispositivo.id == id).first()
        atuador = Atuador.query.filter(Atuador.dispositivo_id == id).first()
        db.session.delete(atuador)
        db.session.delete(dispositivo)
        db.session.commit()
        return Atuador.get_atuador()