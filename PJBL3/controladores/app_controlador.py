from flask import Flask, render_template, request, jsonify
from controladores.login_controlador import login
from controladores.sensor_controlador import sensor, sensores
from controladores.atuador_controlador import atuador
from modelos.db import db, instance
from flask_mqtt import Mqtt
import json

leitura = {}
mensagem={"Umidade 1": "34° c", "Photo-Resisto": "12"}

def create_app():
    app = Flask(__name__,
        template_folder="./views/",
        static_folder="./static/",
        root_path="./")
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_TLS_ENABLED'] = False
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(sensor, url_prefix='/')
    app.register_blueprint(atuador, url_prefix='/')
    mqtt_client = Mqtt(app)
    db.init_app(app)
    topico_receber = "Xp.Barragem/enviar"

    

    @app.route('/')
    def index():
        status=0
        return render_template("login.html", status=status)

    @app.route('/user_home')
    def user_home():
        return render_template("user_home.html")
    
    @app.route('/adm_home')
    def adm_home():
        return render_template("adm_home.html")
    
    """@app.route('/tempo_real_user')
    def tempo_real_user():
        global leitura
        for i in sensores:
            leitura[i]="Nenhum dado recebido"
        for i in leitura:
            if i in mensagem:
                leitura[i]=mensagem[i]
        return render_template("tempo_real_user.html", leitura=leitura)
    
    @app.route('/tempo_real')
    def tempo_real():
        global leitura
        leitura.clear()
        for i in sensores:
            leitura[i]="Nenhum dado recebido"
        for i in leitura:
            if i in mensagem:
                leitura[i]=mensagem[i]
        return render_template("tempo_real.html", leitura=leitura)
    
    @app.route('/comando_remoto')
    def comando_remoto():
        return render_template("comando_remoto.html")
    
    @app.route('/comando_remoto_user')
    def comando_remoto_user():
        return render_template("comando_remoto_user.html")
    
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
        global mensagem
        mensagem = json.loads(message.payload.decode())

    @app.route('/publish_message', methods=['POST'])
    def publish_message():
        request_data = request.get_json()
        topic = request_data.get('topic')
        message = json.loads(request_data.get('message'))

        for key, value in message.items():
            if value == 1:
                message[key] = True
            else:
                message[key] = False
        publish_result = mqtt_client.publish(topic, json.dumps(message))
        return jsonify(publish_result)"""

    return app