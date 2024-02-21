from flask import Flask, flash, redirect, render_template, session
from forms import LoginForm, RegisterForm

from models import User, connect_db, db

app = Flask(__name__)

app.secret_key = "123-456-789"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_user"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    print("This is the home page")
    return render_template("home.html", title="Home")


@app.route("/register")
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        print("This is the register page")
        return render_template("register.html", title="Register", form=form)
    print("This is the register page")
    return render_template("register.html", title="Register")


@app.route("/login")
def login():
    print("This is the login page")
    return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run()
