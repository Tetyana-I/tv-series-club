"""User model tests."""

# run these tests like:
# python -m unittest test_user_model.py

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

import os
from unittest import TestCase
from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///tvclub-test"

from app import app


db.create_all()


class UserModelTestCase(TestCase):
    """Tests for user model."""

    def setUp(self):
        """Creates test client, adds sample data."""

        User.query.delete()
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_repr(self):
        """ Does the repr method work as expected? """
        
        u = User(username="testuser1", password="HASHED_PASSWORD")
        db.session.add(u)
        db.session.commit()
        self.assertEqual(repr(u), f"<User #{u.id}: testuser1>")


    def test_register(self):
        """ Does User.register successfully create a new user given valid credentials? """
        
        # successfully create a user
        self.assertIsInstance(User.register(username="test2", password="hashed_password"), User)
        

    def test_authenticate(self):
        """ Does User.authenticate fail to return a user when the username is invalid?
        Does User.authenticate fail to return a user when the password is invalid?"""

        u = User.register(username="testuser3", password="testpassword")
        db.session.add(u)
        db.session.commit()

        # username is invalid
        self.assertFalse(User.authenticate(username='testuser', password='testpassword'))

        # password is invalid
        self.assertFalse(User.authenticate(username='testuser3', password='password'))

        # valid credentials
        self.assertIsInstance(User.register(username="testuser3", password="testpassword"), User) 

