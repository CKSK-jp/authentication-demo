from flask import Flask, flash, redirect, render_template, request, session, url_for
from psycopg2 import IntegrityError

from forms import FeedbackForm, LoginForm, RegisterForm
from models import AuthUser, Feedback, connect_db, db

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
    if "user_id" in session:
        user = AuthUser.query.filter_by(id=session["user_id"]).first()
        if user:
            username = user.username
            return redirect(url_for("welcome", username=username))
    return render_template("home.html", title="Home")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    A function to handle user registration. It processes the registration form, validates the input, creates a new user account, and handles any errors that may occur during the process.
    """
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
    """
    A function for handling user login. It handles both GET and POST requests for the /login route. It initializes a LoginForm, validates the form input, authenticates the user, and redirects to the welcome page upon successful login. If the credentials are invalid, it flashes an error message and renders the login page again.
    """
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


@app.route("/users/<username>", methods=["GET"])
def welcome(username):
    """
    A function to handle the welcome page for a specific user.

    Args:
        username (str): The username of the user to welcome.

    Returns:
        render_template: The rendered welcome page.
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    user = AuthUser.query.filter_by(username=username).first_or_404()

    feedback_list = Feedback.query.all()

    return render_template(
        "welcome.html", title="Welcome", user=user, feedback_list=feedback_list
    )


@app.route("/users/<username>/account", methods=["GET"])
def show_account(username):
    """
    A function to handle the account page for a specific user.

    Args:
        username (str): The username of the user to show the account for.

    Returns:
        render_template: The rendered account page.
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    user = AuthUser.query.filter_by(username=username).first_or_404()

    return render_template("account.html", title="Account Details", user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """
    Delete a user by username and return a redirect to the home page.

    :param username: the username of the user to be deleted
    :return: a redirect to the home page
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    user = AuthUser.query.get(session["user_id"])

    if user.username != username:
        flash("You cannot access this page", category="error")
        return redirect(url_for("login"))

    user = AuthUser.query.filter_by(username=username).first()

    if user:
        for feedback in user.feedback:
            db.session.delete(feedback)

        db.session.delete(user)
        db.session.commit()
        session.pop("user_id")
        flash("Account deleted", category="success")
    return render_template("home.html", title="Home")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """
    Add a feedback entry for a specific user.

    :param username: the username of the user to add feedback for
    :return: a redirect to the welcome page
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    user = AuthUser.query.get(session.get("user_id"))

    if user is None or user.username != username:
        flash("You cannot access this page", category="error")
        return redirect(url_for("login"))

    if request.method == "POST":
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback = Feedback(title=title, content=content, username=username)

            db.session.add(feedback)
            db.session.commit()

            feedback_list = Feedback.query.all()

            flash("Feedback added", category="success")
            return render_template(
                "welcome.html",
                title="Welcome",
                user=user,
                feedback_list=feedback_list,
            )
    else:
        form = FeedbackForm()
        return render_template(
            "feedback_form.html", title="Add Feedback", user=user, form=form
        )


@app.route("/feedback/<int:feedback_id>", methods=["GET"])
def show_feedback(feedback_id):
    """
    Show a specific feedback entry for a specific user.

    :param feedback_id: the ID of the feedback entry to show
    :return: a redirect to the welcome page
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    feedback = Feedback.query.get(feedback_id)
    user = AuthUser.query.get(session["user_id"])

    if not feedback:
        flash("Feedback not found", category="error")
        return redirect(url_for("welcome"), username=user.username)

    if user.username != feedback.username:
        return render_template("feedback.html", title="Feedback", feedback=feedback)
    else:
        return render_template(
            "feedback.html", title="Feedback", feedback=feedback, user=user
        )


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """
    Edit a feedback entry for a specific user.

    :param feedback_id: the ID of the feedback entry to edit
    :return: a redirect to the welcome page
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    feedback = Feedback.query.get(feedback_id)
    user = AuthUser.query.get(session["user_id"])

    if not feedback:
        flash("Feedback not found", category="error")
        return redirect(url_for("welcome"), username=user.username)

    if user.username != feedback.username:
        flash("You cannot access this page", category="error")
        return redirect(url_for("login"))

    if request.method == "POST":
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()

            feedback_list = Feedback.query.all()

            flash("Feedback updated", category="success")
            return render_template(
                "welcome.html",
                title="Edit Feedback",
                user=user,
                form=form,
                feedback_list=feedback_list,
            )
        else:
            flash("Feedback not updated", category="error")
            return render_template(
                "feedback_form.html", title="Edit Feedback", user=user, form=form
            )

    else:
        form = FeedbackForm(obj=feedback)
        return render_template(
            "feedback_form.html", title="Edit Feedback", user=user, form=form
        )


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """
    Delete a feedback entry for a specific user.

    :param feedback_id: the ID of the feedback entry to delete
    :return: a redirect to the welcome page
    """
    if "user_id" not in session:
        flash("You must be logged in to view this page", category="error")
        return redirect(url_for("login"))

    feedback = Feedback.query.get(feedback_id)
    user = AuthUser.query.get(session["user_id"])

    if not feedback:
        flash("Feedback not found", category="error")
        return redirect(url_for("welcome", username=user.username))

    if user.username != feedback.username:
        flash("You cannot access this page", category="error")
        return redirect(url_for("login"))

    db.session.delete(feedback)
    db.session.commit()

    print("loading welcome page, feedback deleted", user.username)
    flash("Feedback deleted", category="success")
    return redirect(url_for("welcome", username=user.username))


if __name__ == "__main__":
    app.run(debug=True)
