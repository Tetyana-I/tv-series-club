""" View tests."""

# run these tests like:
#    FLASK_ENV=production python -m unittest tests/test_views.py


import os
from unittest import TestCase

from models import db, User, Show, Comment

os.environ['DATABASE_URL'] = "postgresql:///tvclub-test"

from app import app, CURR_USER_KEY

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class ViewTestCase(TestCase):
    """Test views."""

    def setUp(self):
        """Create test clients. """

        User.query.delete()
        self.client = app.test_client()
        self.testuser = User.register(username="testuser", password="testpassword")
        db.session.commit()


    def tearDowm(self):
        """Clean up any fouled transaction."""
        
        db.session.rollback()

    def test_show_comments(self):
        """ Test show all comments page """
        
        with self.client as client:
            # no access if user not logged in
            res = client.get('/comments')     
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

            # check content of page
            s = Show(title="Seinfield") 
            db.session.add(s)
            db.session.commit()
            c = Comment(text="Check comment", user_id=self.testuser.id, show_id=s.id)
            db.session.add(c)
            db.session.commit()       
            with client.session_transaction() as session:
                u = User.register(username="user", password="password")
                db.session.commit()
                session[CURR_USER_KEY] = u.id
            res = client.get('/comments', follow_redirects=True)  
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="my-4">Comments</h1>', html)
            self.assertIn('Seinfield</a></b>', html)


    def test_show_details(self):
        """ Test showpage """
        
        with self.client as client:
            with client.session_transaction() as session:
                u = User.register(username="user3", password="password3")
                db.session.commit()
                session[CURR_USER_KEY] = u.id
            #  335 - code of Sherlock show on API
            res = client.get('/shows/335', follow_redirects=True)  
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Language:  <b>', html)
            self.assertIn('Sherlock', html)


    def test_collection_add(self):
        """ Test handling collection adding """
        
        with self.client as client:
            with client.session_transaction() as session:
                u = User.register(username="user4", password="password4")
                db.session.commit()
                session[CURR_USER_KEY] = u.id
            resp = client.post('/collections/add', data={
                    'name': 'Name of collection to tesst',
                    'description': "Description of the tested collection"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('Your collection was sucessfully added!', html)
