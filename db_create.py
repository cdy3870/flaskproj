from app import db
from models import BlogPosts

db.create_all()

db.session.add(BlogPosts("Good", "I\'m good"))
db.session.add(BlogPosts("Well", "I\'m well"))

db.session.commit()