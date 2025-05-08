from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from .http_status_codes import *
import validators
from .database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return {"error" : "Password is too short"}, HTTP_400_BAD_REQUEST
    
    if len(username) < 3:
        return {"error" : "User is too short"}, HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:
        return {"error" : "Username should be alphanumeric, also no spaces"}, HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return {"error" : "Email is not valid"}, HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return {"error" : "Email is already taken"}, HTTP_409_CONFLICT    

    if User.query.filter_by(username=username).first() is not None:
        return {"error" : "Username is already taken"}, HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return {
        "message" : "User created successfully"
    } 


@auth.get("/me")
def me():
    return {"user" : ""}


