from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from .http_status_codes import *
import validators
from .database import User, db
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

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
    
    if User.query.filter_by(email=email).first():
        return {"error" : "Email is already taken"}, HTTP_409_CONFLICT    

    if User.query.filter_by(username=username).first():
        return {"error" : "Username is already taken"}, HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return {
        "message" : "User created successfully"
    } 


@auth.post('/login')
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
                refresh = create_refresh_token(str(user.id))
                access = create_access_token(str(user.id))

                return {
                    "user" : {
                        "user_id" : user.id,
                        "refresh" : refresh,
                        "access" : access
                    }
                }, HTTP_201_CREATED

    return {"error" : "wrong credentials"}, HTTP_401_UNAUTHORIZED


@auth.get("/me")
@jwt_required()
def me():  
    id = get_jwt_identity()

    user = User.query.filter_by(id=id).first()

    if user is not None:
        return {"user" : {
            "username" : user.username,
            "email" : user.email 
        }}, HTTP_200_OK
    
    return {"message" : "User does not exist"}, HTTP_204_NO_CONTENT


@auth.post("/token/refresh")
@jwt_required(refresh=True)
def refresh_user_token():
    id = get_jwt_identity()
    new_access_token = create_access_token(str(id))

    return {
        "new_access_token" : new_access_token
    }, HTTP_201_CREATED
