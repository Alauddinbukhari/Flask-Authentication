from flask import Flask,request, render_template, redirect, url_for, session, flash
from config import Config
from forms.login_form import MyForm



app= Flask(__name__)
app.config.from_object(Config)



@app.route("/")
def home():
    
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form=MyForm()
    if login_form.validate_on_submit():
        print(login_form.data.email)
    return render_template("login.html",form =login_form)


@app.route("/signup")
def signup():
    return render_template("sign_up.html")


@app.route("/logout_password")
def forgot_password():
    return "<p>forgot password</p>"


if __name__=="__main__":
    app.run(port=5000,debug=True)

