# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from firebase_admin import db
from bs4 import BeautifulSoup
import ast
import requests
import json
# For cost control, you can set the maximum number of containers that can be
# running at the same time. This helps mitigate the impact of unexpected
# traffic spikes by instead downgrading performance. This limit is a per-function
# limit. You can override the limit for each function using the max_instances
# parameter in the decorator, e.g. @https_fn.on_request(max_instances=5).
set_global_options(max_instances=10)

initialize_app()
#
#
@https_fn.on_request()
def mackolik(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")


@https_fn.on_request(timeout_sec=540)
def digersekme(req: https_fn.Request) -> https_fn.Response:
    butunmaclar = maclar(get_match_code())
    matchRef = db.reference("maclar") 
    for key, value in butunmaclar.items():
        matchRef.update({key: value})
    return https_fn.Response("hello")
def maclar(matches):
    butunhepsi = {}
    index = 0
    for match_code in matches: 
        match_code = int(match_code)
        
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'})



        
        url = f"https://arsiv.mackolik.com/Match/Default.aspx?id={match_code}"

        req = session.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        tables = soup.find_all('a', attrs={'class':'compare-rate-bg-up'})
        title = soup.find_all('title')
        title = str(title)
        title = title.split("@")
        title = title[0]
        title = title.split(">")
        title = title[1]
        

        odds_data = []
        
        
        for table in tables:
            table = str(table)
            data = table.split('"')[3][30:]
            

            if data not in odds_data:
                odds_data.append(data)
                
            
        iddaa = {}
        iddaa["Taraflar"] = title.replace("/","-")
        iddaa["Maç Kodu"] = match_code
        for i in odds_data:
            i = i[:-1]
            i = ast.literal_eval(i)
            
            for count in range(len(i[1])):
                iddaa_name = (i[0]+" "+i[1][count]).replace("/","-")
                oran = i[2][count]
                if oran == "-":
                    oran = "1"
                iddaa_name = iddaa_name.replace(".","'nci")
                iddaa[iddaa_name] = oran
        butunhepsi[str(match_code)] = iddaa    
        index += 1
        print(f"{index}/{len(matches)}")
        
        
        #return butunhepsi  
    return butunhepsi
        
def get_match_code():
    url = "https://arsiv.mackolik.com/Iddaa-Programi"
    

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'})

    req = session.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    tables = soup.find_all('a', attrs={'class':'iddaa-rows-style'}, href=True)

    matches = []


    for i in tables:
        
       
        i = str(i)
        if "popMatch" in i:
            match_code = i[54:61]
            
            matches.append(match_code)
            #break
        
    return matches