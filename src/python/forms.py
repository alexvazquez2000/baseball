from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class ParentForm(FlaskForm):
    name = StringField('Parent Name', validators=[DataRequired()])
    children = SelectMultipleField('Children', coerce=int)
    submit = SubmitField('Save')

class ChildForm(FlaskForm):
    name = StringField('Child Name', validators=[DataRequired()])
    submit = SubmitField('Add Child')

class TeamForm(FlaskForm):
    teamName = StringField('Team Name', validators=[DataRequired()])
    children = SelectMultipleField('Children', coerce=int)
    submit = SubmitField('Create Team')

