from flask import Flask,request, render_template, redirect, url_for, session, flash

app= Flask(__name__)



@app.route("/")
def home():
    
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        pass
    return render_template("login.html")


@app.route("/signup")
def signup():
    return "<p>signup</p>"


@app.route("/logout_password")
def forgot_password():
    return "<p>forgot password</p>"


if __name__=="__main__":
    app.run(port=5000,debug=True)

