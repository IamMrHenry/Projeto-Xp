#app_controller.py
from flask import Flask, render_template, request, jsonify
from modelo.db import db, instance
from controllers.sensor_controller import sensor_
from controllers.atuador_controller import actuator_
from controllers.read_controller import read_
from controllers.write_controller import write_
import json
from flask_mqtt import Mqtt
from modelo.iot.read import Read
from modelo.iot.write import Write

def create_app():
    app = Flask(__name__,
        template_folder="./views/",
        static_folder="./static/",
        root_path="./")
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = '' # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = '' # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000 # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False # If your broker supports TLS, set it True
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read_, url_prefix='/')
    app.register_blueprint(write_, url_prefix='/')
    db.init_app(app)
    mqtt_client= Mqtt()
    mqtt_client.init_app(app)
    topic_subscribe = "/aula_flask/temperature"
    topic_send = "/actuator"

    @app.route('/')
    def index():
        return render_template("home.html")
    @app.route('/home')
    def home():
        return render_template("home.html")
    

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe) # subscribe topic
        else:
            print('Bad connection. Code:', rc)
    
    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        if(message.topic==topic_subscribe):
            try:
                with app.app_context():
                    Read.save_read(message.topic, message.payload.decode())
            except:
                pass
    @app.route('/publish')
    def publish():
        return render_template('publish.html')

    @app.route('/publish_message', methods=['GET','POST'])
    def publish_message():
        request_data = request.get_json()
        print(request_data)
        publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
        if(request_data['topic']==topic_send):
            try:
                with app.app_context():
                    Write.save_write(request_data['topic'], request_data['message'])
            except:
                pass
        return jsonify(publish_result)

    return app