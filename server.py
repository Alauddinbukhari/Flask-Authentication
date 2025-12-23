from flask import Flask,request, render_template, redirect, url_for, session, flash
from config import Config
from forms.login_form import MyForm
from forms.sign_up_form import Signup
from models.user import db
from models.user import User
from flask_bcrypt import Bcrypt

app= Flask(__name__)
app.config.from_object(Config)

bcrypt= Bcrypt(app)

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
    
    

    if sign_up_form.validate_on_submit():
        first_name = sign_up_form.first_name.data
        last_name = sign_up_form.last_name.data
        email = sign_up_form.email.data
        password = sign_up_form.password.data

        new_user = User(
            username=f"{first_name} {last_name}",
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

        
     
    return render_template("sign_up.html",form = sign_up_form)







@app.route("/forgot_password")
def forgot_password():
    return "<p>forgot password</p>"


if __name__=="__main__":
    app.run(port=5000,debug=True)

