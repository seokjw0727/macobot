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
bot = commands.Bot(command_prefix = "매코야 ", intents=discord.Intents.all()) 

bot.remove_command('help') # 기본 help 명령어를 제거함.

@bot.event # 봇이 준비되면, 봇의 상태를 '개발'으로 바꾸고, 봇의 핑을 출력함.
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='개발'))
    os.system('cls')
    if bot.latency * 1000 >= 210:
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



@bot.tree.command(name="상태") # '상태' 명령어
async def status(interaction: discord.Interaction):
    if bot.latency * 1000 >= 210:
        embed_red = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0xff0000)
        await interaction.response.send_message(embed=embed_red)
    else:
        embed_green = discord.Embed(title='상태', description=f'Ping: {bot.latency * 1000}ms', color=0x00ff00)
        await interaction.response.send_message(embed=embed_green)

@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='거부', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='오류', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await ctx.send(embed=embed)



@bot.tree.command(name="청소") # '청소' 명령어
@commands.has_permissions(administrator=True)
@app_commands.describe(amount="청소할 메시지의 개수")
async def clear_chat(interaction: discord.Interaction, amount: int):
    if amount <= 0 or amount is None:
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.channel.purge(limit=amount)
        embed = discord.Embed(title='청소 완료', description=f'{amount}개의 메시지를 삭제했습니다.', color=0x00ff00)
        await interaction.response.send_message(embed=embed)

@clear_chat.error
async def clear_chat_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='거부', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='오류', description='청소할 메시지의 개수를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='오류', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="경고") # '경고' 명령어
@commands.has_permissions(administrator=True)
@app_commands.describe(유저="경고를 줄 유저", 사유="경고 사유")
async def warn(interaction: discord.Interaction, 유저: discord.Member, 사유: str):
    channel = bot.get_channel(1091003605240266875) # 경고 채널 ID
    if channel is None:
        await interaction.response.send_message('경고 채널을 찾을 수 없습니다.')
        return
    warning_message = f"__{유저}__ 님이 관리자에게 경고를 받았습니다.\n> 사유: {사유}"
    await channel.send(warning_message)
    embed = discord.Embed(title='성공', description=f'{유저} 님에게 경고를 부여했습니다.', color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@warn.error
async def warn_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='오류', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='오류', description='경고를 줄 유저와 경고 사유를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='오류', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="차단", description="/차단 @대상 사유") # '차단' 명령어
@app_commands.describe(유저="차단할 유저", 사유="차단 사유")
@commands.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, 유저: discord.Member, 사유: str):
    channel = bot.get_channel(1091003605240266875) # 경고 채널 ID
    await 유저.add_roles(유저.guild.get_role(1105071533161992244))

    
    for i in 유저.roles: # 모든 역할을 제거함.
        try:
            await 유저.remove_roles(i)
        except:
            banned_message = f"__{유저}__ 님이 서버에서 차단되었습니다.\n> 사유: {사유}"
            await channel.send(banned_message)
            embed = discord.Embed(title='성공', description=f'{유저} 님을 차단했습니다.', color=0x00ff00)
            await interaction.response.send_message(embed=embed)
            
        

    




@bot.tree.command(name="공지") # '공지' 명령어
@app_commands.describe(내용="공지 내용")
@commands.has_permissions(administrator=True)
async def notice(interaction: discord.Interaction, 내용: str):
    channel = bot.get_channel(1094255511609802792)
    if channel is None:
        await interaction.response.send_message('공지 채널을 찾을 수 없습니다.')
        return
    embed=discord.Embed(title="공지", description='> ' + 내용 + ' \n \n ||@everyone||', color=0x00ff00)
    await channel.send(embed=embed)
    embed = discord.Embed(title='성공', description='공지를 보냈습니다.', color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@notice.error
async def notice_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='오류', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='오류', description='공지 내용을 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='오류', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)

        
        


































load_dotenv('token.env')
bot.run(os.getenv('bot_token'))