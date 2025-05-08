from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string, random


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # creating the foreign key relationship
    # backref -> no need to define the relationship in the other table
    bookmarks = db.relationship("Bookmark", backref="user")
         
    def __repr__(self) -> str:
        return f"User >>> {self.username}"
    

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Creating the short url function
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        
        while True:    
            picked_chars = ''.join(random.choices(characters, k=3))
            link = self.query.filter_by(short_url=picked_chars).first()

            if not link:
                return picked_chars

    def __repr__(self) -> str:
        return f"Bookmark >>> {self.url}"
    