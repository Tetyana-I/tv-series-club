""" Seed file to make sample data to tvclub_db """

from models import User, Show, Collection, CollectionShow, Comment, db 
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If query isn't empty, empty it
User.query.delete()
Show.query.delete()
Collection.query.delete()
CollectionShow.query.delete()
Comment.query.delete()

# Add users
u1 = User.register(username="testuser", password="testpassword")
u2 = User.register(username="testuser2", password="testpassword2")

db.session.add_all([u1, u2])
db.session.commit()


# Add shows
s1 = Show(id=335, title="Sherlock", img_small_url="https://static.tvmaze.com/uploads/images/medium_portrait/171/428042.jpg")
s2 = Show(id=41007, title="Loki", img_small_url="https://static.tvmaze.com/uploads/images/medium_portrait/320/801227.jpg")
s3 = Show(id=41524, title="The Morning Show", img_small_url="https://static.tvmaze.com/uploads/images/medium_portrait/361/903010.jpg")
s4 = Show(id=306, title="Broadchurch", img_small_url="https://static.tvmaze.com/uploads/images/medium_portrait/2/5036.jpg")
s5 = Show(id=353, title="Line of Duty", img_small_url="https://static.tvmaze.com/uploads/images/medium_portrait/302/755260.jpg")
s6 = Show(id=1371, title="Westworld", img_small_url="https://static.tvmaze.com/uploads/images/medium_portrait/241/602832.jpg")

db.session.add_all([s1, s2, s3, s4, s5, s6])
db.session.commit()


# Add collection
c1 = Collection(name="Best detective drama series", user_id=u2.id)
c2 = Collection(name="Best mini shows", description="6-10 episodes TV shows", user_id=u1.id)

db.session.add_all([c1, c2])
db.session.commit()

# Add collection-show connections
cs1 = CollectionShow(collection_id=c2.id, show_id=s1.id)
cs2 = CollectionShow(collection_id=c1.id, show_id=s5.id)
cs3 = CollectionShow(collection_id=c2.id, show_id=s2.id)
cs4 = CollectionShow(collection_id=c1.id, show_id=s4.id)
cs5 = CollectionShow(collection_id=c2.id, show_id=s3.id)
cs6 = CollectionShow(collection_id=c2.id, show_id=s6.id)

db.session.add_all([cs1, cs2, cs3, cs4, cs5, cs6])
db.session.commit()
