"""User View tests."""

# run these tests like:
#    FLASK_ENV=production python -m unittest tests/test_user_views.py


import os
from unittest import TestCase

from models import db, User

# BEFORE we import our app, we set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///tvclub-test"


# import app

from app import app, CURR_USER_KEY, do_logout

# Create tables 

db.create_all()

# Don't have WTForms use CSRF

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test clients. """

        User.query.delete()
        self.client = app.test_client()
        self.testuser = User.register(username="testuser", password="testpassword")
        # self.user2 = User.register(username="user2",  password="seconduser")
        db.session.commit()


    def tearDowm(self):
        """Clean up any fouled transaction."""
        
        db.session.rollback()

    def test_startpage(self):
        """ test redirect not logged-in users to correct homepage """
       
        with self.client as client: 
            res = client.get('/')     
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/tvshow-club")

            res = client.get('/', follow_redirects=True)  
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4>New to TV-Club?</h4>', html)

    def test_register(self):
        """ test handling registration """
        
        with self.client as client: 
            # shows a register form
            res = client.get('/register')  
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1><b>Welcome to TV-Club!</b></h1>', html)
            
            # registers a new user
            res = client.post("/register", data={'username': 'testuser2', 'password': 'testpassword2'}, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Welcome to the club! Successfully created your account!', html)
    

    def test_register_user_same_username(self):
        """ fails to register a user with the username already in a database """
        
        with self.client as client:         
            res = client.post("/register", data={'username': 'testuser', 'password': 'testpasswordnew'}, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Username is already taken. Please pick another', html)
            
            # stays on the same page
            self.assertIn('<h1><b>Welcome to TV-Club!</b></h1>', html)


    def test_login(self):
        """ test login handling"""
        with self.client as client: 
            # shows a login form
            res = client.get('/login')  
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1><b>Welcome back!</b></h1>', html)
            
            # login an existing user
            res = client.post("/login", data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('Hello, testuser!', html)
        
    
    def test_login_invalid_credentials(self):
        """ test login user with invalid credentials """
        with self.client as client: 
            # login an existing user
            res = client.post("/login", data={'username': 'testuser4', 'password': 'testpassword'}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('Invalid credentials.', html)

            # stays on the same page  
            self.assertIn('<h1><b>Welcome back!</b></h1>', html)


