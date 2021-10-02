"""SQLAlchemy models for TV-Club."""

# from datetime import datetime

from enum import unique
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """ Connect the database to app """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def register(cls, username, password):
        """ Registers new user. Hashes password and adds user to system. """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Show(db.Model):
    """User in the system."""

    __tablename__ = 'shows'

    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    language = db.Column(db.Text, nullable=False, default="Unknown")
    premiered = db.Column(db.Text, nullable=False, default="Unknown")
    official_site = db.Column(db.Text, nullable=True, default="Unknown")
    average_rate = db.Column(db.Text, nullable=True, default="Unknown")
    img_large_url = db.Column(db.Text, nullable=True, default="https://tinyurl.com/tv-missing")
    img_small_url = db.Column(db.Text, nullable=True, default="https://tinyurl.com/tv-missing")
    
