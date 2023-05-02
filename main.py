import discord
import random
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix='매코 ', intents=discord.Intents.all()) # 호출 명령어를 '매코 ' 로 설정함.


bot.remove_command('help') # 기본 help 명령어를 제거함.

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
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}개의 슬래시 커맨드가 성공적으로 동기화되었습니다.")
    except Exception as e:
        print(f"에러: {e}")


@bot.tree.command(name="안녕")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("반가워요!")  

@bot.tree.command(name="말해")
@app_commands.describe(말씀="말할 내용")
async def say(interaction: discord.Interaction, 말씀: str):
    await interaction.response.send_message(f"{interaction.user.mention} 님의 말씀: {말씀}!")



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



@bot.tree.command(name="상태")
async def status(interaction: discord.Interaction):
    if bot.latency * 1000 >= 210:
        embed_red = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0xff0000)
        await interaction.response.send_message(embed=embed_red)
    else:
        embed_green = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0x00ff00)
        await interaction.response.send_message(embed=embed_green)


# @bot.command() # '상태' 명령어, 봇의 상태를 embed로 보여줌.
# async def 상태(ctx):
#     # 만약 봇의 핑이 200 이상이라면 embed의 색을 빨강색으로 합니다.
#     if bot.latency * 1000 >= 200:
#         embed_red = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0xff0000)
#         await ctx.send(embed=embed_red)
#     # 만약 봇의 핑이 200 미만이라면 embed의 색을 초록색으로 합니다.
#     else:
#         embed_green = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0x00ff00)
#         await ctx.send(embed=embed_green) # embed를 보냅니다.





@bot.tree.command(name="청소")
@commands.has_permissions(administrator=True)
@app_commands.describe(개수="청소할 메시지의 개수")
async def clear_chat(interaction: discord.Interaction, amount: int):
    if amount <= 0 or amount is None:
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await interaction.send(embed=embed)
    else:
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(title='청소 완료', description=f'{amount}개의 메시지를 삭제했습니다.', color=0x00ff00)
        await interaction.send(embed=embed)

@clear_chat.error
async def clear_chat_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='거부', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='오류', description='청소할 메시지의 개수를 입력해주세요.', color=0xff0000)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='오류', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await ctx.send(embed=embed)



# @bot.command() # '청소' 명령어, 메시지를 청소함.
# @commands.has_permissions(administrator=True)
# async def 청소(ctx, amount: int):
#     if amount <= 0 or amount is None:
#         embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
#         await ctx.send(embed=embed)
#     else:
#         await ctx.channel.purge(limit=amount)
#         embed = discord.Embed(title='청소 완료', description=f'{amount}개의 메시지를 삭제했습니다.', color=0x00ff00)
#         await ctx.send(embed=embed)
# @청소.error
# async def 청소_error(ctx, error):
#     if isinstance(error, commands.MissingPermissions):
#         embed = discord.Embed(title='오류', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
#         await ctx.send(embed=embed)



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