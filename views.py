### Launch server using gunicorn gunicorn, bind to all addresses
### -k flask_sockets.worker --bind 0.0.0.0:8000 views:app


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

app = Flask(__name__)
app.config.from_object(config)
sockets = Sockets(app)

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

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        data = ws.receive()
        print "HEY GUYS!!!!!!!!!!!!!!!!!!!!!!", data
        samples_data = json.loads(data)
        PSD_list = fft.combined_fft(samples_data)
        json_PSD = json.dumps(PSD_list, separators=(',',':'))
        ws.send(json_PSD)

if __name__ == "__main__":
    app.run(debug=True)

