import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tokens
import discord
import requests
import json
from urllib import parse
import math

apiurl = "https://developer-lostark.game.onstove.com/"
key = tokens.apikey

'''
16인 레이드 추가될 시 주석 해제
'''
def auctioncalc(price: int):
    fair = []
    fair4 = math.floor(price * 0.95 * 3/4)
    fair8 = math.floor(price * 0.95 * 7/8)
    # fair16 = math.floor(price * 0.95 * 3/4)
    fairfield = math.floor(price * 0.95 * 10/11)

    fair.append(fair4)
    fair.append(fair8)
    fair.append(fairfield)
    # fair.append(fair16)
    
    embed = discord.Embed(title=":moneybag: 경매 입찰 적정가 계산기", description=f"[:coin:`{price}`]")
    embed.add_field(name="손익분기점", value=f"4인: [:coin:`{fair[0]}`]\n8인: [:coin:`{fair[1]}`]", inline=False)
    embed.add_field(name="적정입찰가", value=f"4인: [:coin:`{math.floor(fair[0]/1.1)}`]\n8인: [:coin:`{math.floor(fair[1]/1.1)}`]", inline=False)
    embed.add_field(name="필보입찰가", value=f"[:coin:`{fair[2]}`]", inline=False)
    embed.set_footer(text="Made by 우사니#3136")
    return embed


def legendaryMap():
    '''
    은축가 각각 12, 8, 4개 solar grace, blessing, protection
    명파주머니(대) 8개 honor shard pouch
    3티어 1레벨 보석 40개
    '''
    gemprice = get_gemprice()
    solarprice = get_solar_price()
    print(gemprice, solarprice)
    

def get_gemprice():
    url = apiurl + "auctions/items/"
    headers = {'accept': 'application/json', 'authorization': 'bearer ' + key, 'Content-Type': 'application/json'} 
    with open("search_gem.json", encoding='utf-8') as f:
        data = json.load(f)
    try:
        response = requests.post(url, json=data, headers=headers).json()
        # print(response.text)
        # with open("result.json", 'w', encoding='utf-8') as f:
        #     json.dump(response.json(), f, ensure_ascii=False, indent='\t')

        index = 0
        sum = 0
        for i in response['Items']:
            index = index + 1
            if index == 5 or index == 6:
                sum += i['AuctionInfo']['BuyPrice']
            if index == 6: break
        
        sum = math.floor(sum/2)
        
        # print(sum)
        return sum * 40

    except Exception as e:
        print(e)

def get_solar_price():
    url = apiurl + 'markets/items/'
    with open("search_solar.json", encoding='utf-8') as f:
        data = json.load(f)
    headers = {'accept': 'application/json', 'authorization': 'bearer ' + key, 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers).json()
        # print(response)
        solar = {}
        for i in response['Items']:
            solar[i['Name']] = i['CurrentMinPrice']

        sum = solar['태양의 은총'] * 12 + solar['태양의 축복'] * 8 + solar['태양의 가호'] * 4
        # print(sum)
        return sum        

    except Exception as e:
        print(e)



if __name__ == '__main__':
    legendaryMap()