import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tokens

import requests
import json

apiurl = "https://developer-lostark.game.onstove.com/"
key = tokens.apikey

url = apiurl + "markets/options"
headers = { 'accept': 'application/json', 'authorization': 'bearer ' + key}

try:
    response = requests.get(url, headers=headers).json()
    with open("jsons/SearchOptions.json", 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent='\t')
except Exception as e:
    print(e)