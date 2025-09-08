from flask_wtf import FlaskForm
from pyexpat.errors import messages
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL, Email


class BlogForm(FlaskForm):
    title = StringField('Título del blog', validators=[DataRequired()])
    subtitle = StringField('Subtítulo', validators=[DataRequired()])
    name = StringField('Tu nombre', validators=[DataRequired()])
    image_url = StringField('URL de la imagen', validators=[URL()])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    submit = SubmitField('Enviar')
