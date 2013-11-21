from flask import Flask, render_template, redirect, request, g, session, url_for, flash
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

app = Flask(__name__)
app.config.from_object(config)

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

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route("/post/<int:id>")
def view_post(id):
    post = Post.query.get(id)
    return render_template("post.html", post=post)

@app.route("/post/new")
@login_required
def new_post():
    return render_template("new_post.html")

@app.route("/post/new", methods=["POST"])
@login_required
def create_post():
    form = forms.NewPostForm(request.form)
    if not form.validate():
        flash("Error, all fields are required")
        return render_template("new_post.html")

    post = Post(title=form.title.data, body=form.body.data)
    current_user.posts.append(post) 
    
    model.session.commit()
    model.session.refresh(post)

    return redirect(url_for("view_post", id=post.id))

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
    x_json = request.form.get("x")
    x_data = json.loads(x_json)
    print "Xxxxxxxxxx!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


    f_s = 20.0 # hz
    PSD_array = []

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # PSD FOR PLOTTING
    PSD_list = []

    #Calculate PSD for each second in the input
    for x in x_data:
        if len(x) == 20:
            fft_x = np.fft.fft(x)
            n = len(fft_x)
            freq = np.fft.fftfreq(n, 1/f_s)
            print "freq:", freq

            #Calculate absolute value of fft_x
            fft_x_abs = np.abs(fft_x)

            #Take first half of FFT array  + 1 to access 10th element?
            half_n = np.ceil(n/2.0) + 1
            freq_half = freq[:half_n]
            fft_x_half = fft_x_abs[:half_n]
            print "freq_half", freq_half
            print "fft_half", fft_x_half
            # Square magnitude of FFT to find PSD
            PSD_x_total = np.power(fft_x_half, 2)

            #Select target frequencies at 1, 3, 6, 10hz
            target_PSD = {}
            target_PSD["1hz"] = fft_x_half[1]
            target_PSD["3hz"] = fft_x_half[3]
            target_PSD["6hz"] = fft_x_half[6]
            target_PSD["10hz"] = fft_x_half[10]

            target_PSD_list = []
            PSD_dict = {}
            target_PSD_list.append(fft_x_half[1])
            target_PSD_list.append(fft_x_half[3])
            target_PSD_list.append(fft_x_half[6])
            target_PSD_list.append(fft_x_half[10])

            
            PSD_dict["timestamp"]= str(datetime.now())
            PSD_dict["data"] = target_PSD_list
            PSD_list.append(PSD_dict)
    

            #Append 1hz, 3hz, 6hz, and 10hz elements to total PSD array
            PSD_array.append(target_PSD)
            # print PSD_array
            json_PSD = json.dumps(PSD_array, separators=(',',':'))

            # print json_PSD
    print PSD_list
    print 
    return render_template("output.html", json_PSD = json_PSD)


@app.route("/output")
def chart():
    return render_template("output.html")


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

if __name__ == "__main__":
    app.run(debug=True)
