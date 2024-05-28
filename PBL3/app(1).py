
# app.py
from flask import Flask, render_template, request,redirect, url_for, jsonify
from user import user
from sensors import sensor_
from actuators import actuator_

from flask_mqtt import Mqtt
from flask_socketio import SocketIO

import flask_login
import models.user

import json


temperature= 10
huminity= 10

app= Flask(__name__)
## __name__ is the application name

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(sensor_, url_prefix='/')
app.register_blueprint(actuator_, url_prefix='/')

#app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_URL'] = '192.168.0.77'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

mqtt_client= Mqtt()
mqtt_client.init_app(app)


app.secret_key = 'd54gdh543trg@!54gdh'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# callback user_loader carrega o usuário
# carrega usuário da seção
@login_manager.user_loader
def user_loader(user):
    users =models.user.get_users()
    if user not in users:
        return
    user_ = models.user.User()
    user_.id = user
    return user_

# carrega usuário do Flask request
@login_manager.request_loader
def request_loader(request):
    user = request.form.get('user')
    users =models.user.get_users()
    if user not in users:
        return
    user_ = models.user.User()
    user_.id = user
    return user_





topic_subscribe = "/aula_flask/"

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/home')
@flask_login.login_required
def home():
    return render_template("home.html")





@app.route('/tempo_real')
@flask_login.login_required
def tempo_real():
    global temperature, huminity
    values = {"temperature":temperature, "huminity":huminity}
    return render_template("tr.html", values=values)

@app.route('/publish')
@flask_login.login_required
def publish():
    return render_template('publish.html')

@app.route('/publish_message', methods=['GET','POST'])
@flask_login.login_required
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe) # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    global temperature, huminity
    js = json.loads(message.payload.decode())
    if(js["sensor"]=="/aula_flask/temperature"):
        temperature = js["valor"]
    elif(js["sensor"]=="/aula_flask/huminity"):
        huminity = js["valor"]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) 