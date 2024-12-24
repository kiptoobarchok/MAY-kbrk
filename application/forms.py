from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField, DateField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
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

class AddLessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date_posted = DateField('Date', validators=[DataRequired()])
    scripture_reading = TextAreaField('Scripture Reading', validators=[DataRequired()])
    memory_verse = TextAreaField('Memory Verse', validators=[DataRequired()])
    introduction = TextAreaField('Introduction')
    conclusion = TextAreaField('Conclusion')
    submit = SubmitField('Add Lesson')

class AddBodyForm(FlaskForm):
    question = TextAreaField('Question')
    answers = TextAreaField('Answers')
    lesson_id = IntegerField('Lesson ID')
    submit = SubmitField('Add Q&A')


class CreateAnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Announcement')
    post = SubmitField('Make Announcement')

class UpdateAnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Announcement')
    post = SubmitField('Update Announcement')


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