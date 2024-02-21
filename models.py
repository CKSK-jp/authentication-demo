from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):

    __tablename__ = "users"


id = db.Column(db.Integer, primary_key=True)
email = db.Column(db.String(100), unique=True)
username = db.Column(db.String(100), unique=True)
password = db.Column(db.String(100))


@classmethod
def register(cls, username, email, password):
    hashed = bcrypt.generate_password_hash(password)
    hashed_utf8 = hashed.decode("utf8")
    return cls(username=username, email=email, password=hashed_utf8)
