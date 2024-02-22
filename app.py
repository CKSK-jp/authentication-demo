from flask import Flask, flash, redirect, render_template, request, session, url_for
from psycopg2 import IntegrityError

from forms import LoginForm, RegisterForm
from models import AuthUser, connect_db, db

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


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "GET":
        return render_template("register.html", title="Register", form=form)

    if form.validate_on_submit():
        username = form.username.data
        # email = form.email.data
        password = form.password.data

        try:
            if AuthUser.query.filter_by(username=username).first():
                flash("Username already exists", category="error")
            else:
                user = AuthUser.register(username, password)
                db.session.add(user)
                db.session.commit()
                flash("Account created, please log in", category="success")
                return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash(
                "There was an error creating your account, please try again",
                category="error",
            )

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Login", form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = AuthUser.authenticate(username, password)

        if user:
            session["user_id"] = user.id
            print("succesfully logged in!")
            return redirect(url_for("welcome", username=username))

    flash("Invalid credentials", category="error")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect(url_for("home"))


@app.route("/user/<username>", methods=["GET"])
def welcome(username):
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    user = AuthUser.query.get(session["user_id"])

    if user.username != username:
        flash("You cannot access this page", category="error")
        return redirect(url_for("login"))

    print("This is the welcome page")
    return render_template("welcome.html", title="Welcome", user=user)


if __name__ == "__main__":
    app.run()
