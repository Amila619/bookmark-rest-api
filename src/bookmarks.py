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
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        all_bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)
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
            ],

            "meta" : {
                "page": all_bookmarks.page,
                "pages": all_bookmarks.pages,
                "total_count": all_bookmarks.total,
                "prev_page": all_bookmarks.prev_num,
                "next_page": all_bookmarks.next_num,
                "has_next": all_bookmarks.has_next,
                "has_prev": all_bookmarks.has_prev

            }


        }, HTTP_200_OK 


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return {
            "messsage" : "Item not found"
        }, HTTP_404_NOT_FOUND
        
    return {
        "id" : bookmark.id,
        "url" : bookmark.url,
        "short_url" : bookmark.short_url,
        "body" : bookmark.body,
        "created_at" : bookmark.created_at,
        "updated_at" : bookmark.updated_at,
        "visit" : bookmark.visits 
    }, HTTP_200_OK


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return {
            "messsage" : "Item not found"
        }, HTTP_404_NOT_FOUND
        
    db.session.delete(bookmark)
    db.session.commit()

    return {}, HTTP_204_NO_CONTENT


@bookmarks.put('<int:id>')
@jwt_required()
def modify_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return {
            "messsage" : "Item not found"
        }, HTTP_404_NOT_FOUND

    body = request.json['body']
    url = request.json['url']

    if not validators.url(url):
        return {
            "error" : "Enter a valid url"
        }, HTTP_400_BAD_REQUEST
    
    bookmark.url = url
    bookmark.body = body
    db.session.commit()

    return {
        "id" : bookmark.id,
        "url" : bookmark.url,
        "short_url" : bookmark.short_url,
        "body" : bookmark.body,
        "created_at" : bookmark.created_at,
        "updated_at" : bookmark.updated_at,
        "visit" : bookmark.visits 
    },  HTTP_200_OK


@bookmarks.get('/stats')
@jwt_required()
def get_stats():
    current_user = get_jwt_identity()

    items = Bookmark.query.filter_by(user_id=current_user).all()

    return {
        "data" : [
            {
                "visits" : item.visits,
                "url" : item.url,
                "id" : item.id,
                "short_url" : item.short_url
            } for item in items
        ]
    }, HTTP_200_OK