import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from Ssal.auctioncalculator import *
import discord
from discord.ext import commands
import math

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

'''
봇이 반응을 해야하는 명령어인지 구분하기 위해 메세지 앞에 붙이는 접두사(prefix)를 설정합니다. 현재 !로 
설정되어있습니다. 이곳을 변경시 해당 문자로 명령어를 시작해야합니다. ext에선 discord.Client처럼 
str.startswith 메서드를 사용할 필요가 없습니다.
'''

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) # 토큰으로 로그인 된 bot 객체에서 discord.User 클래스를 가져온 뒤 name 프로퍼티를 출력
    print(bot.user.id) # 위와 같은 클래스에서 id 프로퍼티 출력
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4)*1000)}ms') # 봇의 핑을 pong! 이라는 메세지와 함께 전송한다. latency는 일정 시간마다 측정됨에 따라 정확하지 않을 수 있다.

@bot.command(aliases=["ㅂㅂㄱ", "분배금"])
async def qqr(ctx, price):  # ㅂㅂㄱ의 영어 타자
    fair = auctioncalc(int(price))
    embed=discord.Embed(title="경매 입찰 적정가 계산기", description=f"[:coin:`{price}`]")
    embed.add_field(name="손익분기점", value=f"4인: [:coin:`{fair[0]}`]\n8인: [:coin:`{fair[1]}`]", inline=False)
    embed.add_field(name="적정입찰가", value=f"4인: [:coin:`{math.floor(fair[0]/1.1)}`]\n8인: [:coin:`{math.floor(fair[1]/1.1)}`]", inline=False)
    embed.add_field(name="필보입찰가", value=f"[:coin:`{fair[2]}`]", inline=False)
    embed.set_footer(text="Made by 우사니#3136")
    await ctx.send(embed=embed)


bot.run(config.token)