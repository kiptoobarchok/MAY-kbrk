from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, DateField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class AddLessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date_posted = DateField('Date', validators=[DataRequired()])
    lesson_id = IntegerField('Lesson ID')
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
