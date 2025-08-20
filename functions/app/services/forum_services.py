from firebase_admin import db
from datetime import datetime,timezone
def post_blog(data):
    username = data.get('username')
    coupon = data.get('coupons')
    title = data.get('title')
    id = data.get('id')
    
    if not (username and coupon):
        return {"error": "Invalid Credentials"}, 401
    
    try:
        ref = db.reference(f"users/{username}/blogs")
        
        ref.child(id).set({
            "coupon": coupon,
            "odd": coupon["odd"],
            "title":title,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        return {"message": "Success"}, 201
    except Exception as err:
        return {"error": str(err)}, 401
    
def get_blogs():
    try:
        users_ref = db.reference("users").get() or {}

        all_blogs = {}

        for username, user_data in users_ref.items():
            blogs = user_data.get("blogs", {})
            all_blogs[username] = blogs  # Kullanıcıya ait blogs sözlüğü

        return {"blogs": all_blogs, "message": "Success"}, 200
    except Exception as err:
        return {"error": str(err)}, 401
