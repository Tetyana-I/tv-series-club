# """Does User.register fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""


# class ShowDetails(db.Model):
#     """User in the system."""

#     __tablename__ = 'shows'

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.Text, nullable=False)
#     language = db.Column(db.Text, nullable=False, default="Unknown")
#     premiered = db.Column(db.Text, nullable=False, default="Unknown")
#     official_site = db.Column(db.Text, nullable=True, default="Unknown")
#     average_rate = db.Column(db.Text, nullable=True, default="Unknown")
#     img_large_url = db.Column(db.Text, nullable=True, default="https://tinyurl.com/tv-missing")
#     img_small_url = db.Column(db.Text, nullable=True, default="https://tinyurl.com/tv-missing")

# Background image:
# https://images.unsplash.com/photo-1586899028174-e7098604235b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1171&q=80