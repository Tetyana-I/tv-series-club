import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

# from flask_bcrypt import Bcrypt

from forms import RegisterForm, CollectionForm, NewShowForCollectionForm

from models import db, connect_db, User, Show, Collection, CollectionShow
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
# db.create_all()

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


def get_show_info(show_id):
    """ Get show info and return show-info-object or False"""
    resp = requests.get(f"http://api.tvmaze.com/shows/{show_id}")
    show_data=resp.json()
    if show_data:
        show = {
            'id': show_id,
            'title': show_data['name'],
            'language': show_data['language'],  
            'premiered': show_data['premiered'],
            'official_site': show_data['officialSite'],
            'average_rate': show_data['rating']['average'],
            'img_large_url': show_data['image']['original'],
            'img_small_url': show_data['image']['medium']
        }
        return show
    return False

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
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    query = request.args["search-query"]
    resp = requests.get("http://api.tvmaze.com/search/shows", params={'q': query})
    shows_data=resp.json()
    return render_template("search.html", shows=shows_data)


# @app.route('/shows/<int:show_id>')
# def show_details(show_id):
#     """ page with detail information about the show """
#     if not g.user:
#         flash("Access unauthorized. Please, log in.", "danger")
#         return redirect("/")
#     resp = requests.get(f"http://api.tvmaze.com/shows/{show_id}")
#     show_data=resp.json()
#     if show_data:
#         show = {
#             id: show_id,
#             'title': show_data['name'],
#             'language': show_data['language'],  
#             'premiered': show_data['premiered'],
#             'official_site': show_data['officialSite'],
#             'average_rate': show_data['rating']['average'],
#             'img_large_url': show_data['image']['original']
#         }
#     else:
#         flash("No information about this show", "danger")
#         return redirect('/user')
  
#     return render_template("show.html", show=show)

@app.route('/shows/<int:show_id>')
def show_details(show_id):
    """ page with detail information about the show """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
   
    show = get_show_info(show_id)
    if show:
        return render_template("show.html", show=show)
    flash("No information about this show", "danger")
    return redirect('/user')
  
    

#######################################################################
# work with collections
#######################################################################

@app.route('/collections')
def all_collections():
    """ all collections list """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    collections = Collection.query.all()
    return render_template("collections.html", collections=collections)


@app.route('/user/collections')
def user_collections():
    """ page with user's collection list """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    collections = Collection.query.filter_by(user_id=g.user.id).all()
    return render_template("collections.html", collections=collections)


@app.route('/collections/add', methods=["POST", "GET"])
def add_collection():
    """ Handles a new collection form, adds a personal user collection """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    form = CollectionForm()
    name = form.name.data
    description = form.description.data
    if form.validate_on_submit():
        collection = Collection(name=name, description=description, user_id=g.user.id)
        db.session.add(collection)
        db.session.commit()
        flash('Your new collection sucessfully added!', 'success')
        return redirect("/collections")
    return render_template("new_collection.html", form=form) 

@app.route('/collections/<int:collection_id>')
def shows_in_collection(collection_id):
    """ List of shows in collection """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    collection = Collection.query.get_or_404(collection_id)
    return render_template('/shows_in_collection.html', collection = collection)


@app.route("/user/collections/<int:collection_id>/delete", methods=["POST"]) 
def delete_collection(collection_id):
    """Delete a collection""" 
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    collection=Collection.query.get_or_404(collection_id) 
    db.session.delete(collection)
    db.session.commit()
    flash('Your collection was deleted','secondary')    
    return redirect("/collections")  


@app.route('/user/collections/<int:collection_id>/edit', methods=["POST", "GET"])
def edit_collection(collection_id):
    """ handle a collection edit form, add a personal user collection """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    collection= Collection.query.get_or_404(collection_id)    
    form = CollectionForm(obj=collection)
    if form.validate_on_submit():
        collection.name = form.name.data
        collection.description = form.description.data
        try:
            db.session.commit()
            flash('Your collection sucessfully updated!', 'success')
            return redirect("/collections")
        except IntegrityError:
            flash("Name already taken. Please pick another", 'danger')
    return render_template("/edit_collection.html", form=form) 



##########################################################################
# shows and collections mapping
##########################################################################

@app.route("/shows/<int:show_id>/add", methods=["GET", "POST"])
def add_show_to_collection(show_id):
    """Add a show to collection."""
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    # check if the show is already in the database, add to the database if not
    show_in_db = Show.query.get(show_id)
    if show_in_db == None:
        new_show = get_show_info(show_id)
        show_in_db = Show(id=show_id, title=new_show['title'], img_small_url=new_show['img_small_url'])
        db.session.add(show_in_db)
        db.session.commit()

    form = NewShowForCollectionForm()
    form.collection.choices = [(c.id, c.name) for c in g.user.user_collections]
    collection_id=form.collection.data
    if form.validate_on_submit():
        collection_show = CollectionShow(collection_id=collection_id, show_id=show_id)
        db.session.add(collection_show)
        db.session.commit()
        flash('The show was sucessfully added to the collection!', 'success')
        return redirect(f"/collections/{collection_id}")

    return render_template("add_show_to_collection.html", form=form)

@app.route("/collections/<int:collection_id>/<int:show_id>/delete", methods=['POST'])
def delete_show_from_collection(collection_id,show_id):
    """ Delete the show from the collection """
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    row_to_delete = CollectionShow.query.filter(CollectionShow.collection_id == collection_id, CollectionShow.show_id == show_id).first()
    db.session.delete(row_to_delete)
    db.session.commit()
    flash('The show was deleted from the collection','secondary')    
    return redirect(f"/collections/{collection_id}")  