import discord
import  random
import os
from discord.ext import commands
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='매코 ', intents=intents) # 호출 명령어를 '매코 ' 로 설정함.



@bot.event # 봇이 준비되면, 봇의 상태를 '개발'으로 바꾸고, 봇의 핑을 출력함.
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='개발'))
    os.system('cls')
    if bot.latency * 1000 >= 200:
        print(f'{bot.user} is ready!')
        print(f'{bot.latency * 1000}ms')
        print('Ping is too high!')
    else:
        print(f'{bot.user} is ready!')
        print(f'{bot.latency * 1000}ms')       



@bot.event # '매코야' 라는 메시지를 감지하면, 랜덤으로 메시지를 보냄.
async def on_message(message):
    if message.author.bot:
        return None
    if message.content == '매코야':
        replies = ['왜 불러여?', '매코!', '왜여?', '온라인!']
        reply = random.choice(replies)
        await message.channel.send(reply)
    elif message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)



@bot.command() # '상태' 명령어, 봇의 상태를 embed로 보여줌.
async def 상태(ctx):
    # 만약 봇의 핑이 200 이상이라면 embed의 색을 빨강색으로 합니다.
    if bot.latency * 1000 >= 200:
        embed_red = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0xff0000)
        await ctx.send(embed=embed_red)
    # 만약 봇의 핑이 200 미만이라면 embed의 색을 초록색으로 합니다.
    else:
        embed_green = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0x00ff00)
        await ctx.send(embed=embed_green) # embed를 보냅니다.



@bot.command() # '청소' 명령어, 메시지를 청소함.
@commands.has_permissions(administrator=True)
async def 청소(ctx, amount: int):
    if amount <= 0 or amount is None:
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title='청소 완료', description=f'{amount}개의 메시지를 삭제했습니다.', color=0x00ff00)
        await ctx.send(embed=embed)
@청소.error
async def 청소_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='오류', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await ctx.send(embed=embed)



@bot.command() # '경고' 명령어, 유저에게 경고를 줌. (추가 기능 필요)
@commands.has_permissions(administrator=True)
async def 경고(ctx, member: discord.Member, *, reason=None):
    channel = bot.get_channel(1091003605240266875)
    if channel is None:
        await ctx.send('경고 채널을 찾을 수 없습니다.')
        return
    warning_message = f"__{member}__ 님이 관리자에게 경고를 받았습니다.\n> 사유: {reason}"
    await channel.send(warning_message)
@경고.error
async def 경고_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='오류', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await ctx.send(embed=embed)



@bot.command() # '공지' 명령어, 특정 채널에 공지 embed를 전송함.
@commands.has_permissions(administrator=True)
async def 공지(ctx, *, content):
    channel = bot.get_channel(1094255511609802792)
    if channel is None:
        await ctx.send('공지 채널을 찾을 수 없습니다.')
        return
    embed=discord.Embed(title="공지", description='> ' + content + ' \n \n ||@everyone||', color=0x00ff00)
    await channel.send(embed=embed)
@공지.error
async def 공지_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='오류', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await ctx.send(embed=embed)
        
        

































load_dotenv('token.env')
bot.run(os.getenv('bot_token'))