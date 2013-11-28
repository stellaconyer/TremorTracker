### Launch server using gunicorn gunicorn, bind to all addresses
### gunicorn -k flask_sockets.worker --bind 0.0.0.0:8000 views:app


from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify
from model import User, Post
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import json
import numpy as np
import requests
from datetime import datetime
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import fft as fft
import os
import logging
import redis
import gevent

app = Flask(__name__)
app.config.from_object(config)
app.debug = 'DEBUG' in os.environ
sockets = Sockets(app)

# REDIS_URL = os.environ['REDISCLOUD_URL']
REDIS_CHAN = 'chat'

sockets = Sockets(app)
redis = redis.StrictRedis(host="localhost", port=6379, db=0)

LOG_FILENAME = 'log.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,)


# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)

# @app.route("/")
# def index():
#     posts = Post.query.all()
#     return render_template("index.html", posts=posts)

class ChatBackend(object):
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                app.logger.info(u'Sending message: {}'.format(data))
                yield data

    def register(self, client):
        """Register a WebSocket connection for Redis updates."""
        self.clients.append(client)

    def send(self, client, data):
        """Send given data to the registered client.
        Automatically discards invalid connections."""
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """Listens for new messages in Redis, and sends them to clients."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Maintains Redis subscription in the background."""
        gevent.spawn(self.run)

chats = ChatBackend()
chats.start()




    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("login.html")

    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")

    login_user(user)
    return redirect(request.args.get("next", url_for("index")))


@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/send_pkg", methods=["POST"])
def send_pkg():

    # print request.form
    samples_json = request.form.get("samples")
    print samples_json
    samples_data = json.loads(samples_json)
    print samples_data

    PSD_list = fft.combined_fft(samples_data)

    # json_PSD = jsonify(PSD_list)
    json_PSD = json.dumps(PSD_list, separators=(',',':'))
    print json_PSD.__class__
    return render_template("d3_output.html", json_PSD = json_PSD)



@app.route("/d3_output")
def d3_chart():
    return render_template("d3_output.html")


@app.route("/d3_output_2")
def d3_chart_2():
    return render_template("d3_output_2.html")

@app.route("/drugs")
def drug_form():
    return render_template("drugs.html")

@app.route("/drugs", methods = ["POST"])
def search_drugs():
    drug = request.form["search_term"]
    url_param = 'http://rxnav.nlm.nih.gov/REST/drugs?name=' + drug
    print url_param
    headers = {'accept':'application/json'} 
    r = requests.get(url_param, headers = headers)
    drug_data = r.json()
    return render_template("drug_output.html", drug_data = drug_data)

@app.route("/live_chart")
def live_chart():
    return render_template("live_chart.html")

@app.route('/')
def record():
    return render_template('recording.html')



# @sockets.route('/echo')
# def echo_socket(ws):
#     while True:
#         data = ws.receive()
#         print "HEY GUYS!!!!!!!!!!!!!!!!!!!!!!", data
#         samples_data = json.loads(data)
#         PSD_list = fft.combined_fft(samples_data)
#         json_PSD = json.dumps(PSD_list, separators=(',',':'))
#         ws.send(json_PSD)


@sockets.route('/submit')
def inbox(ws):
    """Receives incoming chat messages, inserts them into Redis."""
    while ws.socket is not None:
        # Sleep to prevent *contstant* context-switches.
        gevent.sleep(0.1)
        message = ws.receive()
        if message:
            convert_message = json.loads(message)
        # message = json.dumps(convert_message, separators=(',',':'))
            # print "!!!!!!!!!!!!!!!!"
            # if convert_message.get("samples"):
            #     # app.logger.info(u'Inserting message: {}'.format(convert_message))
            #     # redis.publish(REDIS_CHAN, message)
            #     print "Samples"
            # else:
            app.logger.info(u'Inserting message: {}'.format(convert_message))
            redis.publish(REDIS_CHAN, message)

@sockets.route('/receive')
def outbox(ws):
    """Sends outgoing chat messages, via `ChatBackend`."""
    chats.register(ws)

    while ws.socket is not None:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep()


if __name__ == "__main__":
    app.run(debug=True)

