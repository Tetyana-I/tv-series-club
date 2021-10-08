"""Collection, Comment, Show models tests."""

# run these tests like:
# python -m unittest tests/test_models.py

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

import os
from unittest import TestCase
from models import db, User, Show, Comment, Collection
from sqlalchemy.exc import IntegrityError

os.environ['DATABASE_URL'] = "postgresql:///tvclub-test"

from app import app

db.drop_all()
db.create_all()


class ModelTestCase(TestCase):
    """Tests for app models."""

    def setUp(self):
        """Creates test client, adds sample data."""

        Show.query.delete()
        Collection.query.delete()
        Comment.query.delete()

        self.client = app.test_client()


        
    def tearDown(self):
        """Clean up any fouled DB transaction."""

        db.session.rollback()

    def test_show(self):
        """ Test Show model """
        
        s = Show(title="Sherlock")
        db.session.add(s)
        db.session.commit()
        self.assertEqual(len(s.collections),0)
        self.assertEqual(s.title, 'Sherlock')
        self.assertEqual(s.img_small_url, 'https://tinyurl.com/tv-missing')

    def test_collection(self):
        """ Test Collection model """
        
        u = User.register(username="user", password="password")
        db.session.commit()
        c = Collection(name="Breakfast shows", description= "Light and positive shows", user_id=u.id)
        db.session.add(c)
        db.session.commit()
        self.assertEqual(len(c.shows),0)
        self.assertEqual(c.name, 'Breakfast shows')
        self.assertEqual(c.description, 'Light and positive shows')
        self.assertEqual(c.user_id, u.id)

    def test_not_unique_collection_name(self):
        """ Test not unique collection  """
        
        u = User.register(username="user2", password="password2")
        db.session.commit()
        c1 = Collection(name="Breakfast shows", description= "Light and positive shows", user_id=u.id)
        db.session.add(c1)
        db.session.commit()
        c2 = Collection(name="Breakfast shows", description= "Other funny shows", user_id=u.id)
        db.session.add(c2)
        self.assertRaises(IntegrityError, db.session.commit)


    def test_comment(self):
        """ Test Comment model """
        
        u = User.register(username="user3", password="password")
        db.session.commit()
        s = Show(title="Seinfield")
        db.session.add(s)
        db.session.commit()
        c = Comment(text="Comment text here", user_id=u.id, show_id=s.id)
        db.session.add(c)
        db.session.commit()
        self.assertEqual(c.text, 'Comment text here')
        self.assertEqual(c.user_id, u.id)
        self.assertEqual(c.show_id, c.id)
        self.assertEqual(c.user.username, 'user3')
        self.assertEqual(c.show.title, 'Seinfield')


# class Comment(db.Model):
#     """Comment model. """
#     __tablename__ = 'comments' 
      
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     text = db.Column(db.String(140), nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
#     show_id = db.Column(db.Integer, db.ForeignKey('shows.id',  ondelete='cascade')) 
    
#     user = db.relationship('User')
#     show = db.relationship('Show')