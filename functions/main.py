from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app,db
import flask
from bs4 import BeautifulSoup
import ast
import requests
import json
from odds import maclar
from get_match_code import get_match_code

set_global_options(max_instances=10)
initialize_app()
app = flask.Flask(__name__)

@app.get("/")
def home():
    return flask.Response(status=201, response="Server is alive")

@app.get("/refresh")
def refreshMatchList():
    try:
        refreshedMatches = maclar(get_match_code())
        matchesRef = db.reference("matches")
        matchesRef.set({})
        for key, value in refreshedMatches.items():
            matchesRef.update({key: value})
        return flask.Response(status=201, response="Success")
    except Exception as a:
        return flask.Response(status=201, response=str(a))


@app.get("/details")
@app.get("/details/<id>")
def matchDetails(id=None):
    if id is not None:
        return db.reference(f"/matches/{id}").get()
    else:
        matches_ref=db.reference("/matches").get()
        result = [
            {key: value.get("Taraflar")}
            for key, value in matches_ref.items()
        ]
        return 

@https_fn.on_request()
def httpsflaskexample(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()