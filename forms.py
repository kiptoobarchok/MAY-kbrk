from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired(), Length(min=2 , max=10)])
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=2 , max=10)])
    email = StringField('Email',validators=[DataRequired(), Email()] )
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password =  PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password =  PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password =  PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')