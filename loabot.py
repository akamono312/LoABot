import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tokens
from Ssal.auctioncalculator import *
import discord
from discord.ext import commands
import asyncio

#############################################################
from market.marketAvgPrice import *
from gamecontents.gameContents import *
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.command(aliases=["경매장","시세"])
async def market(ctx, *item_name):
    item_name=' '.join(item_name)
    embed=market_item(item_name)
    await ctx.send(embed=embed)

@bot.command(aliases=["ㄷㅂㅅ","도비스"])
async def abyss(ctx):
    embed=abyssofweek()
    await ctx.send(embed=embed)  
#############################################################


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            sync_command=True,
            application_id=1069300492305444954
        )
        self.initial_extension = [
            "Cogs.Ping",
            "Cogs.Ssal"
        ]

    
    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        
        await bot.tree.sync()


    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("===============")
        game = discord.Game("....")
        await self.change_presence(status=discord.Status.online, activity=game)


# @bot.command(aliases=["ㅂㅂㄱ", "분배금", "qnsqorma"])
# async def qqr(ctx, price):  # ㅂㅂㄱ의 영어 타자
#     embed = auctioncalc(int(price))
#     await ctx.send(embed=embed)

# @bot.command(aliases=["지도", "전설지도", "we", "ㅈㄷ"])
# async def wleh(ctx):  # 지도의 영어 타자
#     embed = legendaryMap()
#     await ctx.send(embed=embed)

bot = MyBot()
bot.run(tokens.token)