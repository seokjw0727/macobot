import asyncio
import json
import discord
import  random
import os
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='매코 ', intents=intents)



@bot.event
async def on_ready():
    os.system('cls')
    if bot.latency * 1000 >= 200:
        print(f'{bot.user} is ready!')
        print(f'{bot.latency * 1000}ms')
        print('Ping is too high!')
    else:
        print(f'{bot.user} is ready!')
        print(f'{bot.latency * 1000}ms')       



@bot.command() # '상태' 라고 하면, 봇의 핑을 embed로 보여줍니다.
async def 상태(ctx):
    # 만약 봇의 핑이 200 이상이라면 embed의 색을 빨강색으로 합니다.
    if bot.latency * 1000 >= 200:
        embed_red = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0xff0000)
        await ctx.send(embed=embed_red)
    # 만약 봇의 핑이 200 미만이라면 embed의 색을 초록색으로 합니다.
    else:
        embed_green = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0x00ff00)
        await ctx.send(embed=embed_green) # embed를 보냅니다.



@bot.command() # '청소' 라고 하면, 봇이 메시지를 입력하는 자연수만큼 삭제하고, 삭제한 메시지의 수를 embed로 보여줍니다.
async def 청소(ctx, amount: int):
    if amount <= 0 or amount is None:
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title='청소 완료', description=f'{amount}개의 메시지를 삭제했습니다.', color=0x00ff00)
        await ctx.send(embed=embed)

        

@bot.event # '매코야' 라는 메시지를 감지하면, 봇이 '왜여?' 라고 답장합니다.
async def on_message(message):
    if message.content == '매코야':
        replies = ['왜 불러여?', '매코!', '왜여?', '온라인!']
        reply = random.choice(replies)
        await message.channel.send(reply)
    elif message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)     





        

































load_dotenv('token.env')
bot.run(os.getenv('bot_token'))