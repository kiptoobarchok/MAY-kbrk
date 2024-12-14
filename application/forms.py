from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from application.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired(), Length(min=2 , max=20)])
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=2 , max=10)])
    email = StringField('Email',validators=[DataRequired(), Email()] )
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password =  PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password =  PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])
    submit = SubmitField('Sign up')

    #custom validation for username

    def validate_username(self, username):
        user  = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose another')
    
    # email validation
    def validate_email(self, email):
        user  = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose another')
 

class LoginForm(FlaskForm):
    # flash message
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password =  PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired( )])
    submit = SubmitField('announce')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    profile = FileField('Update dp', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('update')

    #custom validation for username

    def validate_username(self, username):
        if username.data != current_user.username:
            user  = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please choose another')
    
    # email validation
    def validate_email(self, email):
        if email.data != current_user.email:
            user  = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken. Please choose another')
    


class AddLessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    scripture_reading = TextAreaField('scripture_reading', validators=[DataRequired()])
    memory_verse = TextAreaField('memory_verse', validators=[DataRequired()])
    introduction = TextAreaField('introduction')
    conclusion = TextAreaField('conclusion')
    submit = SubmitField('add lesson')


class AddBodyForm(FlaskForm):
    question = TextAreaField('question')
    answers = TextAreaField('answers')
    lesson_id = IntegerField('Lesson ID')
    submit = SubmitField('add questions and answers')


 