from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app,db
import flask
from get_odds import get_odds
from get_match_code import get_match_code
from check import check
set_global_options(max_instances=10)
initialize_app()
app = flask.Flask(__name__)

@app.get("/")
def home():
    return flask.Response(status=201, response="Server is alive")


@app.post("/login")
def login():
    try:
        data = flask.request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not (username and password):
            return flask.Response(status=401, response="Username and password required")
        
        # Get user from database
        user_ref = db.reference(f"users/{username}")
        user_data = user_ref.get()
        
        if not user_data:
            return flask.Response(status=401, response="User not found")
        
        # Check password
        stored_password = user_data.get('password')
        if stored_password != password:
            return flask.Response(status=401, response="Invalid password")
        
        # Return user info (excluding password)
        user_info = {
            "username": username,
            "balance": user_data.get('Balance', 0),
            "coupons": user_data.get('coupons', {})
        }
        
        return flask.Response(
            status=200, 
            response=flask.json.dumps(user_info),
            mimetype='application/json'
        )
        
    except Exception as err:
        print("Login error:", str(err))
        return flask.Response(status=401, response=str(err))

@app.post("/register")
def register():
    try:
        data = flask.request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not (username and password):
            return flask.Response(status=401, response="Username and password required")
        
        # Check if user already exists
        user_ref = db.reference(f"users/{username}")
        existing_user = user_ref.get()
        
        if existing_user:
            return flask.Response(status=401, response="User already exists")
        
        # Create new user
        user_data = {
            "password": password,
            "Balance": 200,
            "coupons": {}
        }
        
        user_ref.set(user_data)
        
        return flask.Response(status=201, response="User created successfully")
        
    except Exception as err:
        print("Register error:", str(err))
        return flask.Response(status=401, response=str(err))

@app.get("/refresh")
def refreshMatchList():
    detailedRef = db.reference("matchesDetailed")
    matchesRef = db.reference("matches")

    matchesRef.set({})
    detailedRef.set({})
    index = 0
    try:
        match_codes = get_match_code()
        for match_code in match_codes:
            data = get_odds(match_code)
            allOdds=data[0]
            sumOdds=data[1]
            matchesRef.update(sumOdds)
            detailedRef.update(allOdds)
            if index == 2:
                break
            index +=1
        return flask.Response(status=201, response="Success")
    except Exception as a:
        return flask.Response(status=401, response=str(a))

@app.get("/check")
def checkCoupons():
    try:
        users = db.reference("users").get()  
        if not users:
            return flask.Response(status=200, response="No users found")

        for username, userData in users.items():
            
            if not userData:
                continue
            print(f"username : {username}")
            print(f"userData : {userData}")
            coupons = userData.get("coupons", {})
            print(f"coupons : {coupons}")
            if not coupons:
                continue

            for couponId, coupon in coupons.items():
                print(f"coupon : {coupon}")
                matches = coupon.get("matches", [])
                print(f"matches : {matches}")
                if not matches:
                    continue
                
                all_correct = True
                for match in matches:  # 🔹 matches artık liste, her eleman dict
                    print(f"match : {match}")
                    isTrue = check(
                        match.get("id"),
                        match.get("iddaa"),
                        match.get("tahmin")
                    )
                    if not isTrue:
                        all_correct = False
                        break

                if all_correct:
                    win_amount = float(coupon.get("bet", 0)) * float(coupon.get("odd", 1))
                    balance_ref = db.reference(f"users/{username}/Balance")
                    current_balance = balance_ref.get() or 0
                    balance_ref.set(current_balance + win_amount)

        return flask.Response(status=201, response="Success")

    except Exception as err:
        print("checkCoupons error:", str(err))
        return flask.Response(status=401, response=str(err))


@app.post("/coupons")
def postCoupons():
    data = flask.request.get_json()
    username = data.get('username')
    coupons = data.get('coupons')
    if not (username and coupons):
        return flask.Response(status=401, response="Invalid Credentials")
    
    ref = db.reference(f"users/{username}/coupons")
    try:
        odd = 1
        matches = []  # tüm maçları buraya toplayacağız
        for coupon in coupons:
            matches.append({
                "id": coupon["id"],
                "taraflar": coupon["Taraflar"],
                "iddaa": coupon["iddaa"],
                "oran": coupon["Oran"],
                "tahmin":coupon["Tahmin"]
            })
            odd *= float(coupon["Oran"])  # çarpım hesabı

        # bütün maçları ve hesaplanan odd'u tek kupon altında push et
        ref.push({
            "matches": matches,
            "odd": odd
        })
        return flask.Response(status=201, response="Success")
    except Exception as err:
        print(str(err))
        return flask.Response(status=401, response={"msg": str(err)})
        
@app.get("/details")
@app.get("/details/<id>")
def matchDetails(id=None):
    if id is not None:
        return db.reference(f"/matchesDetailed/{id}").get()
    else:
        matches_ref=db.reference("/matches").get()
        return matches_ref

@https_fn.on_request()
def httpsflaskexample(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()