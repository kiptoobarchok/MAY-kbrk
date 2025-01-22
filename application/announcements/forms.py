from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,  SubmitField, TextAreaField, SelectField


class CreateAnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Announcement')
    branch = SelectField('Branch', choices=[('kaborok', 'KABOROK'),
                                            ('kapsoit', 'KAPSOIT'),
                                            ('mwebe', 'MWEBE'),
                                            ('chemalal', 'CHEMALAL'),
                                            ('lolwet', 'LOLWET'),
                                            ('zimmerman', 'ZIMMERMAN'),
                                            ('mwiki', 'MWIKI'),
                                            ('isebania','ISEBANIA'),
                                            ('nyabangi', 'NYABANGI'),
                                            ('general', 'GENERAL')],              
                         validators=[DataRequired()])
    post = SubmitField('Make Announcement')

class UpdateAnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    branch = SelectField('Branch', choices=[('kaborok', 'KABOROK'),
                                            ('kapsoit', 'KAPSOIT'),
                                            ('mwebe', 'MWEBE'),
                                            ('chemalal', 'CHEMALAL'),
                                            ('lolwet', 'LOLWET'),
                                            ('zimmerman', 'ZIMMERMAN'),
                                            ('mwiki', 'MWIKI'),
                                            ('isebania','ISEBANIA'),
                                            ('nyabangi', 'NYABANGI'),
                                            ('general', 'GENERAL')],              
                         validators=[DataRequired()])
    content = TextAreaField('Announcement')
    post = SubmitField('Update Announcement')

