from flask import Blueprint, request, jsonify
from app.services.forum_services import post_blog,get_blogs
from app.middleware.auth import token_required
from app.middleware.rate_limit import rate_limit

forum_bp = Blueprint('forum', __name__)

@forum_bp.post("/blog")
@rate_limit
@token_required
def create_blog(current_user):
    data = request.get_json()
    data['username'] = current_user['username']  # Token'dan kullanıcı adını al
    
    result, status_code = post_blog(data)
    return jsonify(result), status_code

@forum_bp.get("/blog")
@rate_limit
def read_blogs():
    result, status_code = get_blogs()
    return jsonify(result), status_code



