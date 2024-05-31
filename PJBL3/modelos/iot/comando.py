from modelos.db import db
from modelos.iot.dispositivo import Dispositivo
from modelos.iot.atuadores import Atuador
from datetime import datetime

class Comando(db.Model):
    __tablename__ = 'write'
    id= db.Column('id', db.Integer, nullable = False, primary_key=True)
    comando = db.Column(db.DateTime(), nullable = False)
    atuador_id= db.Column(db.Integer, db.ForeignKey(Atuador.id), nullable = False)
    valor = db.Column( db.String(50), nullable = True)


    def save_write(nome, valor):
        atuador = Atuador.query.filter(Atuador.nome == nome).first()
        dispositivo = Dispositivo.query.filter(Dispositivo.id == atuador.dispositivo_id).first()
        if (atuador is not None) and (dispositivo.is_active==True):
            comando = Comando( write_datetime = datetime.now(), atuador_id = atuador.id, value = valor )
            db.session.add(comando)
            db.session.commit()

    def get_write(dispositivo_id, start, end):
        atuador = Atuador.query.filter(Atuador.dispositivo_id == dispositivo_id).first()
        write = Comando.query.filter(Comando.atuador_id == atuador.id,
                                Comando.comando > start,
                                Comando.comando <end).all()
        return write