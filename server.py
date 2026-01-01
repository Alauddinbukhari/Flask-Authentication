from flask import Flask, request, render_template, redirect, url_for, session, flash
from config import Config
from forms.login_form import MyForm
from forms.sign_up_form import Signup
from models.user import db
from models.user import User
from flask_bcrypt import Bcrypt
from functools import wraps
from authlib.integrations.flask_client import OAuth
import os


def login_required(f):
    wraps(f)
    def wrapper_function(*args,**kwargs):
        if 'user_id'not in session:
            flash('you need to login first danger')
            
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return wrapper_function


app= Flask(__name__)
app.config.from_object(Config)



oauth= OAuth(app)

bcrypt= Bcrypt(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()


google = oauth.register( name="google",
                         client_id=os.getenv("GOOGLE_CLIENT_ID"),
                         client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
                         server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
                        client_kwargs={ "scope": "openid email profile" })

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
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id']= user.id
            session['username']= user.username
           
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
        hashed= bcrypt.generate_password_hash(password=password)

        new_user = User(
            username=f"{first_name} {last_name}",
            email=email,
            password=hashed
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

        
     
    return render_template("sign_up.html",form = sign_up_form)


@app.route("/secure")
@login_required
def secure():
    return "<p>secure page</p>"




@app.route("/forgot_password")
def forgot_password():
    return "<p>forgot password</p>"



@app.route("/login/google")
def login_google():
    redirect_uri = url_for("auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)




@app.route("/auth/callback")
def auth_callback():
    token = oauth.google.authorize_access_token() # 2. Fetch user info using discovery metadata user_info = oauth.google.get("userinfo").json()
    user_info = oauth.google.parse_id_token(token)
  
    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        user = User(
            username=user_info["name"],
            email=user_info["email"],
            password=None  # OAuth users don't need password
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session["username"] = user.username

    return redirect(url_for("home"))




if __name__=="__main__":
    app.run(port=5000,debug=True)

