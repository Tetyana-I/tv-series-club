from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired


class RegisterForm(FlaskForm):
    """ Form for register new user. """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class CollectionForm(FlaskForm):
    """Form for adding collections."""

    name = StringField("Collection name",  validators=[InputRequired(message="Please enter a collection name")])
    description = TextAreaField("Description") 
     
class NewShowForCollectionForm(FlaskForm):
    """Form for adding a show to collection."""

    collection = SelectField('Choose a collection', coerce=int)