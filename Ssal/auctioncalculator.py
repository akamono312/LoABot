import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import discord
import discord.ext
import math

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