from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms import validators, ValidationError

class saveuserdata(Form):
    email = TextField("email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])