import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tokens
import discord
import datetime
import pytz
import requests

apiurl="https://developer-lostark.game.onstove.com/gamecontents/challenge-abyss-dungeons"
key=tokens.apikey

def abyssofweek():
    url=apiurl
    headers={'accept': 'application/json', 'authorization': 'bearer '+key,'Content-Type':'application/json'}
    try:
        response=requests.get(url,headers=headers).json()
        dungenlist=[]
        for dungen in response: 
            dungenlist.append(dungen.get("Name"))
        embed=discord.Embed(title="**:calendar_spiral: 금주의 도전 어비스 던전**",timestamp=datetime.datetime.now(pytz.timezone('UTC')),color=0x00ff00)
        embed.add_field(name=":video_game:"+str(dungenlist[0]),value="\n",inline="False")
        embed.add_field(name=":video_game:"+str(dungenlist[1]),value="\n",inline="False")
        embed.set_footer(text="Made by.ㅈㅇㅈ#0081")
        return embed
    except Exception as e:
        embed=discord.Embed(title="오류 발생",timestamp=datetime.datetime.now(pytz.timezone('UTC')),color=0x9B0000)
        embed.add_field(name=e,value="\n",inline=False)
        return embed