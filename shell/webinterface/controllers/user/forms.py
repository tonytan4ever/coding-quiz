from flask_security.forms import RegisterForm
from wtforms import TextField
from wtforms.validators import Required


class ExtendedRegisterForm(RegisterForm):
    username = TextField('User Name', [Required()])
