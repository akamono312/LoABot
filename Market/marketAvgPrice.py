import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tokens
import discord
import json
import datetime
import pytz
import requests

apiurl="https://developer-lostark.game.onstove.com/markets/items/"
key=tokens.apikey

def market_item(item_name : str):
    with open("./market/itemcode.json","r",encoding="UTF-8") as file:
        itemcode=json.load(file)
    item_id=itemcode[item_name]['id']
    selected_item=itemcode[item_name]['Name']
    url=apiurl+item_id
    headers={'accept': 'application/json', 'authorization': 'bearer '+tokens.apikey,'Content-Type':'application/json'}
    try:
        response=requests.get(url,headers=headers).json()

        for i in response:
            if (i.get("TradeRemainCount")==0) or (i.get("TradeRemainCount")==None):
                embed=discord.Embed(title="**:gem: "+selected_item+"의 시세**",timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
                if i.get("Stats")[0].get("TradeCount")==0:
                    embed.add_field(name=":moneybag: 금일 평균가 : :x: 거래량이 없습니다.",value='\n', inline=False)
                else:    
                    embed.add_field(name=":moneybag: 금일 평균가 : "+str(i.get("Stats")[0].get("AvgPrice")),value='\n', inline=False)
                if i.get("Stats")[1].get("TradeCount")==0:
                    embed.add_field(name=":moneybag: 금일 평균가 : :x: 거래량이 없습니다.",value='\n', inline=False)
                else:
                    embed.add_field(name=":moneybag: 전일 평균가 : "+str(i.get("Stats")[1].get("AvgPrice")), value='\n',inline=False)
                embed.set_footer(text="Made by.ㅈㅇㅈ#0081")
                return embed
    except Exception as e:
        embed=discord.Embed(title="오류 발생",timestamp=datetime.datetime.now(pytz.timezone('UTC')),color=0x9B0000)
        embed.add_field(name=e,value="\n",inline=False)
        return embed