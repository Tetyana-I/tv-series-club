import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

# from flask_bcrypt import Bcrypt

from forms import RegisterForm
from models import db, connect_db, User, Show

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///tvclub_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a real secret")
# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################################################
# User signup/login/logout
##############################################################################

@app.before_request
def add_user_to_g():
    """ Adding current user to Flask global if this user is logged in. """
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """ Log in user. """

    session[CURR_USER_KEY] = user.id


def do_logout():
    """ Logout user. """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def startpage():
    """ Redirect to homepage """
    return redirect('/tvshow-club')

@app.route('/tvshow-club')
def landing_page():
    """ Start page of app with invitation to register/login """
    return render_template('homepage_anon.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    """ Handle user registration."""

    form = RegisterForm()
    if form.validate_on_submit():
        user = User.register(username=form.username.data, password=form.password.data)
        try:
            db.session.commit()
        except IntegrityError:
            flash("Username is already taken. Please pick another", 'danger')
            return render_template('register.html', form=form)
        flash('Welcome to the club! Successfully created your account!', 'primary')
        do_login(user)
        return redirect('/user')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/user")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("You logout successfully", "secondary")
    return redirect('/register')
    

@app.route('/user')
def user_desktop():
    # 
    return render_template('homepage.html')


######################################################################
# user's flow handling
######################################################################

@app.route('/search')
def show_search_results():
    """ returns a list of show-instances as a result of search query """
    query = request.args["search-query"]
    resp = requests.get("http://api.tvmaze.com/search/shows", params={'q': query})
    shows_data=resp.json()
    return render_template("search.html", shows=shows_data)


@app.route('/shows/<int:show_id>')
def show_details(show_id):
    """ page with detail information about the show """
    resp = requests.get(f"http://api.tvmaze.com/shows/{show_id}")
    show_data=resp.json()
    if show_data:
        show = Show(
            id = show_id,
            title = show_data['name'],
            language = show_data['language'],  
            premiered = show_data['premiered'],
            official_site = show_data['officialSite'],
            average_rate = show_data['rating']['average'],
            img_large_url = show_data['image']['original'],
            img_small_url = show_data['image']['medium']
        )
    else:
        flash("No information about this show", "danger")
        return redirect('/user')
  
    return render_template("show.html", show=show)

        # if not g.user:
        # flash("Access unauthorized. Please, log in.", "danger")
        # return redirect("/")