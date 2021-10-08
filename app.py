import os
import re

from flask import Flask, render_template, request, flash, redirect, session, g
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
import requests

from forms import RegisterForm, CollectionForm, NewShowForCollectionForm, CommentForm
from models import db, connect_db, User, Show, Collection, CollectionShow, Comment

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

###################################################################
# This will allow you to connect to Heroku Postgres services using SQLAlchemy >= 1.4.x
# source: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
###################################################################

# uri = os.getenv("DATABASE_URL")  # or other relevant config var
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# # rest of connection code using the connection string `uri`
# ###################################################################

# # Get DB_URI from environ variable or,
# # if not set there, use development local db.
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql:///tvclub_db'))


uri = os.getenv("DATABASE_URL", 'postgresql:///tvclub_db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`
app.config['SQLALCHEMY_DATABASE_URI'] = uri




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
    
    if not g.user:
        return redirect('/tvshow-club')
    return redirect('/user')


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
    return redirect('/')
    

@app.route('/user')
def user_desktop():
    """ Homepage for logged-in users """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    comments = Comment.query.order_by(Comment.timestamp.desc()).limit(20).all()
    return render_template("recent_comments.html", comments = comments)
    

@app.route('/users/<int:user_id>/profile', methods=["GET", "POST"])
def profile_edit(user_id):
    """Update profile for a current user."""
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    form = RegisterForm(obj=user)
    if form.validate_on_submit():
        if Bcrypt().check_password_hash(g.user.password, form.password.data):
            user.username=form.username.data
            try:
                db.session.commit()
                flash('Successfully updated your profile!', 'success')
                return redirect('/user')
            except IntegrityError:
                flash("Username/email already taken. Please pick another", 'danger')
        else:
            flash("Invalid password!", "danger")
    return render_template("edit_user.html", form=form)


######################################################################
# user's flow handling
######################################################################


@app.route('/search')
def show_search_results():
    """ returns a list of show-instances as a result of search query """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    query = request.args["search-query"]
    resp = requests.get("http://api.tvmaze.com/search/shows", params={'q': query})
    shows_data=resp.json()
    return render_template("search.html", shows=shows_data)


@app.route('/shows/<int:show_id>')
def show_details(show_id):
    """ page with detail information about the show """
    
    if not g.user:
        flash("Access unauthorized. Please, log in.", "danger")
        return redirect("/")
    show = get_show_info(show_id)
    if show:
        session["current_show_id"] = show_id
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
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    collections = Collection.query.all()
    return render_template("collections.html", collections=collections)


@app.route('/user/collections')
def user_collections():
    """ page with user's collection list """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    collections = Collection.query.filter_by(user_id=g.user.id).all()
    return render_template("collections.html", collections=collections)


@app.route('/collections/add', methods=["POST", "GET"])
def collection_add():
    """ Handles a new collection form, adds a personal user collection """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
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
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    collection = Collection.query.get_or_404(collection_id)
    return render_template('/shows_in_collection.html', collection = collection)


@app.route("/user/collections/<int:collection_id>/delete", methods=["POST"]) 
def collection_delete(collection_id):
    """Delete a collection""" 
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    collection=Collection.query.get_or_404(collection_id) 
    db.session.delete(collection)
    db.session.commit()
    flash('Your collection was deleted','secondary')    
    return redirect("/collections")  


@app.route('/user/collections/<int:collection_id>/edit', methods=["POST", "GET"])
def collection_edit(collection_id):
    """ handle a collection edit form """
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    collection= Collection.query.get_or_404(collection_id)    
    form = CollectionForm(obj=collection)
    if form.validate_on_submit():
        collection.name = form.name.data
        collection.description = form.description.data
        try:
            db.session.commit()
            flash('Your collection was sucessfully updated!', 'success')
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
        flash("Access unauthorized. Please, register or log in.", "danger")
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
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    row_to_delete = CollectionShow.query.filter(CollectionShow.collection_id == collection_id, CollectionShow.show_id == show_id).first()
    db.session.delete(row_to_delete)
    db.session.commit()
    flash('The show was deleted from the collection','secondary')    
    return redirect(f"/collections/{collection_id}")  


#######################################################################
# comments
#######################################################################


@app.route('/comments/add', methods=["GET", "POST"])
def comment_add():
    """Add a comment """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    g.show = Show.query.get_or_404(session['current_show_id'])
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, user_id=session[CURR_USER_KEY], show_id=session["current_show_id"])
        g.user.user_comments.append(comment)
        db.session.commit()
        return redirect("/comments")
    return render_template('new_comment.html', form=form)


@app.route('/comments')
def show_all_comments():
    """ Show list of comments from the most recent to oldest """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template("comments.html", comments = comments)


@app.route('/user/comments')
def user_comments():
    """ Show list of the current user comments """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    comments = Comment.query.filter(Comment.user_id == session[CURR_USER_KEY]).order_by(Comment.timestamp.desc()).all()
    return render_template("comments.html", comments = comments)


@app.route('/comments/show')
def comments_for_show():
    """ Show list of comments for the show from the most recent to oldest """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    show_id = session['current_show_id']
    comments = Comment.query.filter(Comment.show_id == show_id).order_by(Comment.timestamp.desc()).all()
    return render_template("comments.html", comments = comments)
    

@app.route('/comments/<int:comment_id>/delete', methods = ['POST'])
def comment_delete(comment_id):
    """ Delete comment """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    comment=Comment.query.get_or_404(comment_id) 
    if comment.user_id == g.user.id:
        db.session.delete(comment)
        db.session.commit()
        flash(f'{g.user.username}, your comment was deleted','secondary') 
    else:
        flash("Access unauthorized", "danger")
    return redirect("/comments") 


@app.route('/comments/<int:comment_id>/edit', methods=["POST", "GET"])
def comment_edit(comment_id):
    """ handle a comment edit form """
    
    if not g.user:
        flash("Access unauthorized. Please, register or log in.", "danger")
        return redirect("/")
    comment= Comment.query.get_or_404(comment_id)    
    form = CommentForm(obj=comment)
    if form.validate_on_submit():
        comment.text = form.text.data
        try:
            db.session.commit()
            flash('Your comment was sucessfully updated!', 'success')
            return redirect("/comments")
        except:
            flash("Something went wrong, we couldn't save changes, sorry", 'danger')
    return render_template("/edit_comment.html", form=form) 