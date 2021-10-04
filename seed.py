""" Seed file to make sample data to tvclub_db """

from models import User, Show, Collection, CollectionShow, db 
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If query isn't empty, empty it
User.query.delete()
Show.query.delete()
Collection.query.delete()
CollectionShow.query.delete()


# Add users
u1 = User.register(username="testuser", password="testpassword")
u2 = User.register(username="testuser2", password="testpassword2")

db.session.add_all([u1, u2])
db.session.commit()

# Add shows
# s1 = Show(id=530, title="Show1")
# s2 = Show(id=431, title="Show2")
# s3 = Show(id=130, title="Show3")
# s4 = Show(id=335, title="Show4")

# db.session.add_all([s1, s2, s3, s4])
# db.session.commit()

# Add collection
c1 = Collection(name="Breakfast shows", description="Light and positive shows", user_id=u1.id)
c2 = Collection(name="Best mini shows", description="6-10 episodes TV shows", user_id=u1.id)

db.session.add_all([c1, c2])
db.session.commit()

# Add collection-show connections
# uc1 = CollectionShow(collection_id=c1.id, show_id=530)
# uc2 = CollectionShow(collection_id=c1.id, show_id=431)
# uc3 = CollectionShow(collection_id=c1.id, show_id=130)
# uc4 = CollectionShow(collection_id=c2.id, show_id=335)


# db.session.add_all([uc1,uc2,uc3,uc4])
# db.session.commit()