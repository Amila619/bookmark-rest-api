from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(80), unique=True, nullable=False)
    email = db.column(db.String(80), unique=True, nullable=False)
    password = db.column(db.Text, nullable=False)
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.DateTime, onupdate=datetime.now())

    # creating the foreign key relationship
    # backref -> no need to define the relationship in the other table
    bookmarks = db.relationship("Bookmark", backref="user")
         
    def __repr__(self) -> str:
        return f"User >>> {self.username}"
    

class Bookmark(db.Model):
    id = db.column(db.Integer, primary_key=True)
    body = db.column(db.Text, nullable=True)
    url = db.column(db.Text, nullable=False)
    short_url = db.column(db.String(3), nullable=True)
    visits = db.column(db.Integer, default=0)
    user_id = db.column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return f"Bookmark >>> {self.url}"
    