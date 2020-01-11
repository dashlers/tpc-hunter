import requests
from bs4 import BeautifulSoup
import datetime
import time

TOKEN = ""
RECEIVER = ""
WANTED = ""
APPID = ""

def do_search(wanteditem):
    searchurl = "https://tipidpc.com/itemsearch.php?sec=s&namekeys=" + wanteditem
    r = requests.get(searchurl)
    soup = BeautifulSoup(r.text, 'html.parser')
    itemlist = soup.find_all('ul')[2].find_all('li')
    output = []
    for i in itemlist:
        item = {}
        item["title"] = i.find_all('a')[0].text
        item["price"] = i.find_all('h3')[0].text
        item["uri"] = i.find_all('a')[0]['href']
        item["seller"] = i.find_all('a')[1].text
        rawdate = i.text.split('\n')[-1][3:-1]
        item["date"] = datetime.datetime.strptime(rawdate, '%b %d %Y %I:%M %p')
        output.append(item)
    return output
    
def update_me(item):
    messij = item["title"] + " for " + item["price"] + r" at https://tipidpc.com/" + item["uri"]
    bigreq = r"https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/" + APPID + "/requests?access_token=" + TOKEN
    payload = {"outboundSMSMessageRequest": {
                    "senderAddress": APPID,
                    "outboundSMSTextMessage": {
                        "message" : messij},
                    "address" : [RECEIVER]}}
    r = requests.post(bigreq, json = payload)

results = do_search(WANTED)
allresults = results

while True:
    results = do_search(WANTED)
    for item in results:
        if item not in allresults:
            allresults.append(item)
            print("added",item["title"])
            update_me(item)
    time.sleep(3600)
