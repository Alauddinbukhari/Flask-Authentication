from flask import Flask,request, render_template, redirect, url_for, session, flash
from config import Config
from forms.login_form import MyForm
from forms.sign_up_form import Signup
from models.user import db
from models.user import User


app= Flask(__name__)
app.config.from_object(Config)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form=MyForm()
    if login_form.validate_on_submit():
        print(login_form.email.data)
        print(login_form.password.data)
        return redirect(url_for('home'))
    return render_template("login.html",form =login_form)


@app.route("/signup")
def signup():
    sign_up_form = Signup()
    return render_template("sign_up.html",form = sign_up_form)


@app.route("/logout_password")
def forgot_password():
    return "<p>forgot password</p>"


if __name__=="__main__":
    app.run(port=5000,debug=True)

