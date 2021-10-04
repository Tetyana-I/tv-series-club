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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    user_collections = db.relationship('Collection', cascade="all, delete")


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

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Text, nullable=False)
    img_small_url = db.Column(db.Text, nullable=True, default="https://tinyurl.com/tv-missing")

    collections = db.relationship('Collection', secondary='collections_shows', backref='shows')    


class Collection(db.Model):
    """Collection model."""

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    

class CollectionShow(db.Model):
    """Mapping collections to shows."""

    __tablename__ = 'collections_shows' 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id', ondelete='cascade'))
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id',  ondelete='cascade'))

