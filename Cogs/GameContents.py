import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tokens
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import pytz
import requests
import asyncio

apiurl="https://developer-lostark.game.onstove.com/gamecontents/challenge-abyss-dungeons"
key=tokens.apikey

class GameContents(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="도비스", description="금주의 도전 어비스 던전을 확인합니다.")
    async def abyss(self, interaction: discord.Interaction) -> None:
        embed = self.abyssofweek()
        await interaction.response.send_message(embed=embed)

    def abyssofweek(self):
        url=apiurl
        headers={'accept': 'application/json', 'authorization': 'bearer ' + key,'Content-Type':'application/json'}
        try:
            response=requests.get(url,headers=headers).json()
            dungeonlist=[]
            for dungeon in response: 
                dungeonlist.append(dungeon.get("Name"))
            embed=discord.Embed(title="**:calendar_spiral: 금주의 도전 어비스 던전**", timestamp=datetime.datetime.now(pytz.timezone('UTC')),color=0x00ff00)
            embed.add_field(name=f':video_game: {str(dungeonlist[0])}',value="\n",inline="False")
            embed.add_field(name=f':video_game: {str(dungeonlist[1])}',value="\n",inline="False")
            embed.set_footer(text="Made by.ㅈㅇㅈ#0081")
            return embed
        except Exception as e:
            embed=discord.Embed(title="오류 발생",timestamp=datetime.datetime.now(pytz.timezone('UTC')),color=0x9B0000)
            embed.add_field(name=e,value="\n",inline=False)
            return embed

async def setup(bot) -> None:
    await bot.add_cog(GameContents(bot))