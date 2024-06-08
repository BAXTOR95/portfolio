from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (
    StringField,
    TextAreaField,
    DateField,
    SelectField,
    SubmitField,
    PasswordField,
    BooleanField,
    MultipleFileField
)
from wtforms.validators import DataRequired, Email, URL


# WTForm for sending a message to the blog owner
class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


class ProjectForm(FlaskForm):
    category = SelectField(
        'Category',
        choices=[
            ('Scripting', 'Scripting'),
            ('Web Development', 'Web Development'),
            ('GUI Desktop App', 'GUI Desktop App'),
            ('Game', 'Game'),
            ('HTTP Requests & APIs', 'HTTP Requests & APIs'),
            ('Image Processing & Data Science', 'Image Processing & Data Science'),
            ('Web Scraping', 'Web Scraping'),
            ('GUI Automation', 'GUI Automation'),
            ('Automation', 'Automation'),
            ('Data Science', 'Data Science'),
        ],
        validators=[DataRequired()],
    )
    client = StringField('Client', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    url = StringField('Project URL', validators=[DataRequired(), URL()])
    description = TextAreaField('Description', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    images = MultipleFileField(
        'Project Images',
        validators=[FileAllowed(['jpg', 'png'], 'Images only!'), FileRequired()],
        render_kw={'multiple': True},
    )
    submit = SubmitField('Submit')


class EditProjectForm(ProjectForm):
    images = MultipleFileField(
        'Project Images',
        validators=[FileAllowed(['jpg', 'png'], 'Images only!')],
        render_kw={'multiple': True},
    )
    submit = SubmitField('Update Project')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
