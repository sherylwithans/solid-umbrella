from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class PostForm(FlaskForm):
    num_days = StringField('Number of days to include in topic analysis:',
        validators=[DataRequired()])
    num_topics = StringField('Number of topics to generate:',
        validators=[DataRequired()])
    # content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Generate')
           