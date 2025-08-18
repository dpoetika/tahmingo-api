import requests
from bs4 import BeautifulSoup

def check(match_code): 
   
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'})
    url = f"https://arsiv.mackolik.com/Match/Default.aspx?id={match_code}"
    print(url)

    req = session.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    
    statistic = soup.find('div', attrs={'id':'dvOPTAStats'},recursive = True).get_text(strip = True,separator="_").split("_")
    corners = statistic[16:19:2]

    match_score = soup.find('div', attrs={'class':'match-score'},recursive = True).get_text(strip = True,separator="_")
    hf_match_score_link = soup.find('a', attrs={'class':'mac-plus-link'},recursive = True).get_attribute_list("href")

    request = session.get("https:"+hf_match_score_link[0])
    soup = BeautifulSoup(request.content, 'html.parser')
    hf_match_score = soup.find('div', attrs={'class':'mac-ht'},recursive = True).get_text()
    
    return {
        "İlk Yarı":hf_match_score.replace("İY","").strip(),
        "Maç Sonucu":match_score,
        "Korner":corners,
        }

