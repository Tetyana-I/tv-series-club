from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired


class RegisterForm(FlaskForm):
    """ Form for register new user. """

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=40, message='Password length should be from 6 to 40 characters')])

class CollectionForm(FlaskForm):
    """Form for adding collections."""

    name = StringField("Collection name",  validators=[InputRequired(message="Please enter a collection name")])
    description = TextAreaField("Description") 
     
class NewShowForCollectionForm(FlaskForm):
    """Form for adding a show to collection."""

    collection = SelectField('Choose a collection', coerce=int)

class CommentForm(FlaskForm):
    """Form for adding/editing comments."""

    text = TextAreaField('text', validators=[InputRequired(), Length(max=140, message='Comment text should not exceed 140 characters')])