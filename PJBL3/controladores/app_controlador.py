from flask import Flask, render_template, request, jsonify
from controladores.login_controlador import login
from controladores.sensor_controlador import sensor
from controladores.atuador_controlador import atuador
from controladores.comando_controlador import comando
from controladores.historico_controlador import historico
from modelos.iot.sensores import Sensor
from modelos.iot.historico import Dados
from modelos.db import db, instance
from flask_mqtt import Mqtt
import json

# 1. Esse é o arquivo central que determina todas as rotas que o flask pode tomar para acessar as partes do 
# site, a função abaixo (def create_app()) é onde todas essa rotas estão definidas.

def create_app():
    
    # 2. Aqui nós definimos a localizão dos arquivos HTML, CSS e Imagens usadas no site.
    app = Flask(__name__,
        template_folder="./views/",
        static_folder="./static/",
        root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    
    # 3. Aqui nós definimos a conexão com o MQTT Broker.
    app.config['MQTT_BROKER_URL'] = 'broker.mqttdashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_TLS_ENABLED'] = False
    mqtt_client = Mqtt(app)
    topico_receber = "Xp.Barragem/enviar"


    # 4. Aqui nós usamos a função register_blueprint() para conectar diferentes arquivos que separam o código.

    # 5. Essa blueprint se refere ao processos de login do site, para entender mais sobre vá ao ponto 5.1. no
    # arquivo login_controlador.py encontrado na mesma pasta que esse arquivo.
    app.register_blueprint(login, url_prefix='/')

    # 6. Essa blueprint é destinada aos processos relacionados ao sensores, para entender mais sobre vá ao 
    # ponto 6.1. no arquivo sensor_controlador.py encontrado na mesma pasta que esse arquivo.
    app.register_blueprint(sensor, url_prefix='/')

    # 7. Essa blueprint é destinada aos processos referentes ao atuadores, para entender mais sobre vá ao 
    # ponto 7.1. no arquivo atuador_controlador.py encontrado na mesma pasta que esse arquivo. 
    app.register_blueprint(atuador, url_prefix='/')

    # 8. Essa blueprint é sobre o armazenamento e leitura de comandos passados, para entender mais sobre vá ao 
    # ponto 8.1. no arquivo comando_controlador.py encontrado na mesma pasta que esse arquivo.
    app.register_blueprint(comando, url_prefix='/')

    # 9. Essa blueprint é sobre o armazenamento e leitura de dados passados, para entender mais sobre vá ao 
    # ponto 9.1. no arquivo historico_controlador.py encontrado na mesma pasta que esse arquivo.
    app.register_blueprint(historico, url_prefix='/')

    # 10. Aqui são definidas as informações da conexão com o banco de dados.
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

# 11. O flask usa rotas ara determinas dos diferentes caminhos e processo por trás do site, abaixo estão 
# escritos cada rota e seu destino.


    # 11.1. Rota inicial, essa é a rota usada ao abrir o site pela primeira vez, usada para direcionar o usuário
    # para a página de login
    @app.route('/')
    def index():
        return render_template("login.html", status=False)
    
    # 11.2. Essa é a rota para á pagina inicial do site, ela se adapta para os diferentes papéis dentro do
    # sistema.
    @app.route('/home')
    def home():
        return render_template("home.html")
    
    # 11.3. Rota para a página de visualização em tempo real dos dados dos sensores
    @app.route('/tempo_real')
    def tempo_real():
        leitura = {}
        sensores = Sensor.get_sensors()
        for i in sensores:
            leitura[i.nome] = Dados.get_latest_read(i.nome)
        return render_template("tempo_real.html", leitura = leitura)
    
    # 11.4. Rota para a página de controle remoto dos atuadores da Barragem
    @app.route('/comando_remoto')
    def comando_remoto():
        return render_template("comando_remoto.html")
    
# 12. Aqui estão as funções usadas pelo Flask para lidar com os processos do MQTT

    # 12.1. Função destinada a lidar com a conexão com o MQTT
    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Conectado com Sucesso')
            mqtt_client.subscribe(topico_receber)
        else:
            print('Conexão ruim. Código:', rc)

    # 12.2 Função para avisar que o cliente está desconectado do MQTT
    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Desconectado")

    # 12.3 Função para receber mensagens do MQTT
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
            except json.JSONDecodeError as e:
                print(f"Falha ao decodificar a mensagem JSON: {e}")


    # 12.4 Rota para enviar mensagens para o MQTT
    @app.route('/publish_message', methods=['POST'])
    def publish_message():
        return jsonify()

# 13. Retorna o app com todas as rotas e conexões para o arquivo app.py para serem inicializado ao rodar o
# programa    
    return app