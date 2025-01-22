from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField, DateField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from application.models import User


class LoginForm(FlaskForm):
    # < log in form >
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =  PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2)])
    role = SelectField('Role', choices=[('pastor', 'Pastor'),
                                        ('member', 'Member'),
                                        ('deacon', 'Deacon'),
                                        ('guest', 'Guest')], 
                                        validators=[DataRequired()], default='member')
    branch = SelectField('Branch', choices=[('kaborok', 'KABOROK'),
                                            ('kapsoit', 'KAPSOIT'),
                                            ('mwebe', 'MWEBE'),
                                            ('chemalal', 'CHEMALAL'),
                                            ('lolwet', 'LOLWET'),
                                            ('zimmerman', 'ZIMMERMAN'),
                                            ('mwiki', 'MWIKI'),
                                            ('isebania','ISEBANIA'),
                                            ('nyabangi', 'NYABANGI'),
                                            ('diaspora', 'DIASPORA'),
                                            ('other', 'OTHER')],              
                         validators=[DataRequired()])
    date_of_birth = DateField('Year of Birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=2), EqualTo('password', message="passwords must match")])
    submit = SubmitField('Submit')

    # custom validation to remove intergrity error
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is taken, please choose another!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is taken, please choose another!')
        

