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
def auctioncalc(common_price: int):
    if common_price >= 100000:
        common_price = int(common_price * 0.95)
    price = []
    fair4 = math.floor(common_price * 0.95 * 3/4)
    fair8 = math.floor(common_price * 0.95 * 7/8)
    # fair16 = math.floor(common_price * 0.95 * 3/4)
    fairfield = math.floor(common_price * 0.95 * 29/30)

    price.append(fair4)
    price.append(fair8)
    price.append(fairfield)

    fair = []
    for i in range(3):
        fair.append(math.floor(price[i]/1.1))

    
    embed = discord.Embed(title=":scales: 경매 입찰 적정가 계산기", description=f"[:coin:`{common_price}`]")
    embed.add_field(name="손익분기점", value=f"4인: [:coin:`{price[0]}`]\n8인: [:coin:`{price[1]}`]", inline=False)
    embed.add_field(name="적정입찰가", value=f"4인: [:coin:`{fair[0]}`]\n8인: [:coin:`{fair[1]}`]", inline=False)
    embed.add_field(name="분배금", value=f"4인: [:coin:`{math.floor(fair[0] * 1/3)}`]\n8인: [:coin:`{math.floor(fair[1] * 1/7)}`]", inline=False)
    embed.add_field(name="필보입찰가", value=f"[:coin:`{price[2]}`]", inline=False)
    embed.set_footer(text="Made by 우사니#3136")
    return embed


def legendaryMap():
    '''
    은축가 각각 12, 8, 4개 solar grace, blessing, protection
    명파주머니(대) 8개 honor shard pouch
    3티어 1레벨 보석 40개
    '''
    gem_price = get_gem_price()
    overall_gem_price = gem_price * 40

    solar_price = get_solar_price()
    overall_solar_price = {}
    j = 12
    for i in solar_price:
        overall_solar_price[i] = solar_price[i] * j
        j -= 4

    honor_price = get_honor_price()
    overall_honor_price = honor_price * 8
    
    # print(overall_gem_price, overall_solar_price, overall_honor_price)

    price = 0
    for i in overall_solar_price:
        price += overall_solar_price[i]
    price += overall_gem_price
    price += overall_honor_price

    # print(price)

    price_message = price_format(price)
    honor_message = message_format(honor_price, overall_honor_price)
    gem_message = message_format(gem_price, overall_gem_price)

    embed=discord.Embed(title=":moneybag: 전설지도 입찰 적정가 계산기", description=price_message)
    embed.add_field(name="명예의 파편 주머니(대)", value=honor_message, inline=False)
    embed.add_field(name="3티어 1레벨 보석", value=gem_message, inline=False)
    # print(price_message)
    # print(honor_message)
    # print(gem_message)
    for i in solar_price:
        message = message_format(solar_price[i], overall_solar_price[i])
        # print(message)
        embed.add_field(name=i, value=message, inline=True)
    embed.set_footer(text="Made by 우사니#3136")

    return embed


def price_format(price: int):
    fairprice = math.floor(price * 0.95 * 29/30)
    distprice = math.floor(fairprice * 1/29)
    message = [
        f"가격: :coin:`{price}`",
        f"손익분기점: :coin:`{fairprice}`",
        f"적정입찰가: :coin:`{math.floor(fairprice/1.1)}`",
        f"분배금: :coin:`{distprice}`"
    ]
    return '\n'.join(message)


def message_format(price: int, overall_price: int):
    message = [
        f"시세: :coin:`{price}`",
        f"합계: :coin:`{overall_price}`"
    ]

    return '\n'.join(message)


def get_gem_price():
    url = apiurl + "auctions/items/"
    headers = {'accept': 'application/json', 'authorization': 'bearer ' + key, 'Content-Type': 'application/json'} 
    data = {
        "ItemLevelMin": 0,
        "ItemLevelMax": 1700,
        "ItemGradeQuality": 0,
        "Sort": "BUY_PRICE",
        "CategoryCode": 210000,
        "CharacterClass": "",
        "ItemTier": 3,
        "ItemGrade": "",
        "ItemName": "",
        "PageNo": 1,
        "SortCondition": "ASC"
    }
    try:
        response = requests.post(url, json=data, headers=headers).json()
        # print(response.text)
        # with open("result.json", 'w', encoding='utf-8') as f:
        #     json.dump(response.json(), f, ensure_ascii=False, indent='\t')

        index = 0
        sum = 0
        for item in response['Items']:
            index = index + 1
            if index == 5 or index == 6:
                sum += item['AuctionInfo']['BuyPrice']
            if index == 6: break
        
        sum = math.floor(sum/2)
        
        # print(sum)
        return sum

    except Exception as e:
        print(e)
        return -1


def get_solar_price():
    url = apiurl + 'markets/items/'
    data = {
        "Sort": "GRADE",
        "CategoryCode": 50020,
        "ItemTier":3,
        "ItemGrade": "",
        "ItemName": "태양의",
        "PageNo": 1,
        "SortCondition": "ASC"
    }
    headers = {'accept': 'application/json', 'authorization': 'bearer ' + key, 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers).json()
        # print(response)
        solar = {}
        for item in response['Items']:
            solar[item['Name']] = item['CurrentMinPrice']

        # print(sum)
        return solar       

    except Exception as e:
        print(e)
        return -1



def get_honor_price():
    url = apiurl + 'markets/items/'
    data = {
        "Sort": "GRADE",
        "CategoryCode": 50010,
        "ItemTier": 3,
        "ItemGrade": "",
        "ItemName": "명예의 파편 주머니(대)",
        "PageNo": 1,
        "SortCondition": "ASC"
    }
    headers = {'accept': 'application/json', 'authorization': 'bearer ' + key, 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=data, headers=headers).json()
        # print(response)
        return response['Items'][0]['CurrentMinPrice']

    except Exception as e:
        print(e)
        return -1


if __name__ == '__main__':
    legendaryMap()