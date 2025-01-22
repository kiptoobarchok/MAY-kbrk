from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField, DateField,  SelectField
from wtforms.validators import DataRequired, Length


class EventCreationForm(FlaskForm):
    month = StringField('Month', validators=[DataRequired(), Length(max=20)])
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
    
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    event_desc = StringField('Event Description', validators=[DataRequired(), Length(max=255)])
    event_venue = StringField('Event Venue', validators=[DataRequired(), Length(max=100)])
    event_status = SelectField(
        'Event Status',
        choices=[('done', 'Done'), ('postponed', 'Postponed'), ('scheduled', 'Scheduled')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
