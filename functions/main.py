from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app,db
import flask
from get_odds import get_odds
from get_match_code import get_match_code

set_global_options(max_instances=10)
initialize_app()
app = flask.Flask(__name__)

@app.get("/")
def home():
    return flask.Response(status=201, response="Server is alive")

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