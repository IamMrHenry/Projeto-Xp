from flask import Flask, render_template, request, jsonify
from controladores.sensor_controlador import sensor
from controladores.atuador_controlador import atuador
from controladores.comando_controlador import comando
from controladores.historico_controlador import historico
from controladores.usuario_controlador import usuario
from controladores.login_controlador import login_manager, login
from modelos.iot.sensores import Sensor
from modelos.iot.historico import Dados
from modelos.iot.comando import Comando
from utils.role import role_proibida
from modelos.db import db, instance
from flask_mqtt import Mqtt
import flask_login
import json


def create_app():
    

    app = Flask(__name__,
        template_folder="./views/",
        static_folder="./static/",
        root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'd54gdh543trg@!54gdh'
    login_manager.init_app(app)

    app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_TLS_ENABLED'] = False
    mqtt_client = Mqtt(app)
    topico_receber = "Xp.Barragem/enviar"

    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(sensor, url_prefix='/')
    app.register_blueprint(atuador, url_prefix='/')
    app.register_blueprint(comando, url_prefix='/')
    app.register_blueprint(historico, url_prefix='/')
    app.register_blueprint(usuario, url_prefix='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)


    @app.route('/')
    def index():
        return render_template("login.html")
    
    @app.route('/home')
    @flask_login.login_required
    def home():
        return render_template("home.html", role = flask_login.current_user.papel_id)
    

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Conectado com Sucesso')
            mqtt_client.subscribe(topico_receber)
        else:
            print('Conexão ruim. Código:', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Desconectado")

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        with app.app_context():
            try:
                mensagem = json.loads(message.payload.decode())
                sensores = Sensor.get_sensors()
                for sensor in sensores:
                    if sensor.nome in mensagem:
                        Dados.save_read(sensor.nome, mensagem[sensor.nome])
                    else:
                        print(f"A leitura para o sensor {sensor.nome} não foi encontrada na mensagem.") 
            except:
                pass

    @app.route('/publish_message', methods=['POST'])
    def publish_message():
        request_data = request.get_json()
        topic = request_data.get('topic')
        atuador = request_data.get('atuador')
        valor = request_data.get('valor')
        Comando.save_write(atuador, valor)
        messagem = {}
        messagem[atuador]=str(valor)
        message=messagem
        print(message)
        publish_result = mqtt_client.publish(topic, str(message))
        return jsonify()

    return app