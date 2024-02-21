from wtforms import Form, PasswordField, StringField


class RegisterForm:
    def __init__(self):
        self.username = None
        self.email = None
        self.password = None
        self.confirm_password = None
