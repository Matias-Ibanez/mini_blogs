from flask_wtf import FlaskForm
from pyexpat.errors import messages
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, URL, Email


class BlogForm(FlaskForm):
    title = StringField('Título del blog', validators=[DataRequired()])
    subtitle = StringField('Subtítulo', validators=[DataRequired()])
    name = StringField('Tu nombre', validators=[DataRequired()])
    image_url = StringField('URL de la imagen', validators=[URL()])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class RegisterForm(FlaskForm):
    name = StringField('Tu nombre', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')