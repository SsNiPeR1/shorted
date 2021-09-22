from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import regexp


class UrlForm(FlaskForm):
    url = StringField("URL to shorten: ", validators=[regexp("^(https?:\/?\/?)?[a-z?A-Z?0-9?_?\-]+\.?[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+/?.*$")])
    submit = SubmitField()