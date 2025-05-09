from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from .http_status_codes import *
import validators
from .database import Bookmark, db

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()

    if request.method == 'POST':
        body = request.json['body']
        url = request.json['url']

        if not validators.url(url):
            return {
                "error" : "Enter a valid url"
            }, HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return {
                "error" : "Url already exists"
            }
        
        bookmark=Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return {
                "id" : bookmark.id,
                "url" : bookmark.url,
                "short_url" : bookmark.short_url,
                "body" : bookmark.body,
                "created_at" : bookmark.created_at,
                "updated_at" : bookmark.updated_at
            }, HTTP_201_CREATED
    else:
        all_bookmarks = Bookmark.query.filter_by(user_id=current_user).all()
        return {"data" : [
            {
                "id" : bookmark.id,
                "url" : bookmark.url,
                "short_url" : bookmark.short_url,
                "body" : bookmark.body,
                "created_at" : bookmark.created_at,
                "updated_at" : bookmark.updated_at,
                "visit" : bookmark.visits 
            } for bookmark in all_bookmarks
        ]}, HTTP_200_OK 