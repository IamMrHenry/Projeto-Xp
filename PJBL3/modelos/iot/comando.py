from modelos.db import db
from modelos.iot.dispositivo import Dispositivo
from modelos.iot.atuadores import Atuador
from datetime import datetime

class Comando(db.Model):
    __tablename__ = 'write'
    id= db.Column('id', db.Integer, nullable = False, primary_key=True)
    horario = db.Column(db.DateTime(), nullable = False)
    atuador_id= db.Column(db.Integer, db.ForeignKey(Atuador.id), nullable = False)
    valor = db.Column( db.String(50), nullable = True)


    def save_write(nome, valor):
        dispositivos = Dispositivo.query.filter(Dispositivo.nome.like(f'%{nome}%')).all()
        for dispositivo in dispositivos:
            atuadores = Atuador.query.filter(Atuador.dispositivo_id == dispositivo.id).all()
            for atuador in atuadores:
                if dispositivo.status:
                    print(f"Adicionando comando para atuador {atuador.id}")
                    comando = Comando(horario=datetime.now(), atuador_id=atuador.id, valor=valor)
                    db.session.add(comando)

        try:
            db.session.commit()
            print("Comandos adicionados com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar comandos ao banco de dados: {e}")


    def get_write(id, start, end):
        atuador = Atuador.query.filter(Atuador.id == id).first()
        write = Comando.query.filter(Comando.atuador_id == atuador.id,
                                Comando.horario > start,
                                Comando.horario <end).all()
        return write