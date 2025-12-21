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
       
        email=login_form.email.data
        password=login_form.password.data

        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
        if user and user.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template("login.html",form =login_form)


@app.route("/signup",methods=['GET', 'POST'])
def signup():
    sign_up_form = Signup()
    
    print("METHOD:", request.method)
    print("FORM ERRORS:", sign_up_form.errors)
    print("IS SUBMITTED:", sign_up_form.is_submitted())
    print("VALIDATE:", sign_up_form.validate())

    if sign_up_form.validate_on_submit():
       print(sign_up_form.first_name.data)
       print(2)
       redirect(url_for("login"))

    return render_template("sign_up.html",form = sign_up_form)


@app.route("/logout_password")
def forgot_password():
    return "<p>forgot password</p>"


if __name__=="__main__":
    app.run(port=5000,debug=True)

