from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from application.models import User


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('first name', validators=[DataRequired(), Length(min=2)])
    lastname = StringField('lastname', validators=[DataRequired(), Length(min=2)])
    profile = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    submit =SubmitField('Submit')

    # custom validation
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError('Username is taken. Please choose another.')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Username is taken. Please choose another.')



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first')
        

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='The passwords must match')])
    submit =SubmitField('Reset Password')
