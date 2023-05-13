import discord
import random
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import datetime
import pytz
import asyncio
from webdriver import keep_alive
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix = "매코 ", intents=discord.Intents.all()) 

bot.remove_command('help') # 기본 help 명령어를 제거함.

@bot.event # 봇이 준비되면, 봇의 상태를 '개발'으로 바꾸고, 봇의 핑을 출력함.
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="매코야"))
    os.system('cls')
    print('-------------------------')
    print(f'현재 네트워크 상태 : {round(round(bot.latency, 4)*1000)}ms')
    print(f'봇의 ID : {bot.user.id}')
    print(f'봇의 이름 : {bot.user.name}#{bot.user.discriminator}')
    print('-------------------------')
    print("　")
    print("　")
    print("　")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}개의 커맨드가 성공적으로 로드되었습니다.")
    except Exception as e:
        print(f"에러: {e}")
    print("　")
    print("　")
    print(" --- 콘솔 로그 ---")




@bot.event # '매코야' 이벤트, 봇이 랜덤으로 메시지를 답함.
async def on_message(message):
    if message.author.bot:
        return None
    if message.content == '매코야':
        replies = ['왜 불러여?', '매코!', '왜여?', '온라인!', '히히', '반가워요!', '매코봇은 매코#0663 에 의해 개발되었습니다.']
        reply = random.choice(replies)
        await message.channel.send(reply)
    elif message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)



@bot.tree.command(name="상태", description="봇의 상태를 알려줍니다.") # '상태' 명령어, 봇의 네트워크 상태를 embed 에 담아서 보냄.
async def status(interaction: discord.Interaction):
    if bot.latency * 1000 >= 100:
        embed_green = discord.Embed(title= "**🔴 상태 나쁨 🔴**", description= f"봇의 네트워크 상태는 **{round(round(bot.latency, 4)*1000)}ms** 입니다.", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        embed_green.set_footer(text= "개발자 | 매코#0663", icon_url="https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
        await interaction.response.send_message(embed=embed_green)
    else:
        embed_red = discord.Embed(title= "**🟢 상태 좋음 🟢**", description= f"봇의 네트워크 상태는 **{round(round(bot.latency, 4)*1000)}ms** 입니다.", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
        embed_red.set_footer(text= "개발자 | 매코#0663", icon_url="https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
        await interaction.response.send_message(embed=embed_red)

@status.error
async def status_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title='🛑오류🛑', description='명령어를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='🛑오류🛑', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="청소", description="/청소 [1 이상의 자연수] (관리자 권한이 필요합니다.)") # '청소' 명령어, 메시지를 청소함.
@commands.has_permissions(administrator=True)
@app_commands.describe(amount="청소할 메시지의 개수")
async def clear_chat(interaction: discord.Interaction, amount: int):
    if amount < 1 :
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("청소를 시작합니다...")
        await interaction.channel.purge(limit=amount + 1)
        embed = discord.Embed(title= "🧹 **채팅 청소** 🧹", description= f"__{amount}__ 개의 메시지를 청소했습니다. \n 　", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0x99ffff)
        embed.add_field(name= "처리자", value= f"<@{interaction.user.id}>", inline= False)
        embed.set_footer(text= "개발자 | 매코#0663", icon_url= "https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
        await interaction.channel.send(embed=embed)

@clear_chat.error
async def clear_chat_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="경고", description="/경고 @대상 [사유] (관리자 권한이 필요합니다.)") # '경고' 명령어, 경고 embed 를 처벌 채널에 보내고, 유저에게 dm을 보냄.
@commands.has_permissions(administrator=True)
@app_commands.describe(유저="경고를 줄 유저", 사유="경고 사유")
async def warn(interaction: discord.Interaction, 유저: discord.Member, 사유: str):
    channel = bot.get_channel(1091003605240266875) # 처벌 채널 ID
    if channel is None:
        await interaction.response.send_message('경고 채널을 찾을 수 없습니다.')
        return
    
    # 경고 embed 를 처벌 채널에 보냄.
    embed = discord.Embed(title= "❗ **경고** ❗", description= f"관리자가 *{유저}* 에게 경고를 부여했습니다!", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
    embed.add_field(name= "사유", value= f"{사유}")
    embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
    embed.set_footer(text = "개발자 | 매코#0663", icon_url="https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
    await channel.send(embed=embed)
    await interaction.response.send_message(f'*{유저.mention}* 을(를) 경고했습니다.')

    # 경고 embed 를 경고 대상에게 보냄.
    embed = discord.Embed(title= "❗ **경고** ❗", description= "관리자가 당신에게 경고를 부여했습니다.", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
    embed.add_field(name= "사유", value= f"{사유}")
    embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
    await 유저.send(embed=embed)
    await 유저.send("**안내드립니다.** \n\n 경고가 누적될 경우, 서버에서 불이익을 받을 수 있습니다. \n 경고 처리자에게 반성문을 작성하시면, 정도에 따라 경고를 철회할 수 있습니다.")

@warn.error
async def warn_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
        embed = discord.Embed(title='🛑오류🛑', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="차단", description="/차단 @대상 [사유] (관리자 권한이 필요합니다.)") # '차단' 명령어, 차단 embed 를 처벌 채널에 보내고, 유저에게 dm을 보냄.
@app_commands.describe(유저="차단할 유저", 사유="차단 사유")
@commands.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, 유저: discord.Member, 사유: str):
    
    for i in 유저.roles: # 모든 역할을 제거함.
        try:
            await 유저.remove_roles(i)
        except:
            channel = bot.get_channel(1091003605240266875) # 처벌 채널 ID
            await 유저.add_roles(유저.guild.get_role(1105071533161992244))
            if channel is None:
                await interaction.response.send_message('처벌 채널을 찾을 수 없습니다.')
                return
    
            # 차단 embed 를 처벌 채널에 보냄.
            embed = discord.Embed(title= "⛔ **차단** ⛔", description= f"관리자가 *{유저}* 을(를) 차단했습니다!", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
            embed.add_field(name= "사유", value= f"{사유}")
            embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
            embed.set_footer(text = "개발자 | 매코#0663", icon_url="https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
            await channel.send(embed=embed)
            await interaction.response.send_message(f'*{유저.mention}* 을(를) 차단했습니다.')

            # 경고 embed 를 경고 대상에게 보냄.
            embed = discord.Embed(title= "❗ **경고** ❗", description= "관리자가 당신을 서버에서 차단했습니다.", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
            embed.add_field(name= "사유", value= f"{사유}")
            embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
            await 유저.send(embed=embed)
            await 유저.send("**안내드립니다.** \n\n 차단 처리자에게 반성문을 작성하시면 차단을 해제할 수 있습니다.")



@bot.tree.command(name="공지", description="/공지 [내용] (관리자 권한이 필요합니다.)") # '공지' 명령어, 공지 embed 를 공지 채널에 보냄.
@app_commands.describe(내용="공지 내용")
@commands.has_permissions(administrator=True)
async def notice(interaction: discord.Interaction, 내용: str, 멘션: bool = False):
    channel = bot.get_channel(1094255511609802792)
    if channel is None:
        await interaction.response.send_message('공지 채널을 찾을 수 없습니다.')
        return
    if 멘션 == True:
        embed=discord.Embed(title="🔔 **공지사항** 🔔", description=f"\n\n{내용} ||@everyone||", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xFF6633)
        embed.set_footer(text = "개발자 | 매코#0663", icon_url= "https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
        await channel.send(embed=embed)
        await interaction.response.send_message('공지를 보냈습니다.', ephemeral=True)
    else:
        embed=discord.Embed(title="🔔 **공지사항** 🔔", description=f"\n\n{내용}\n\n", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xFF6633)
        embed.set_footer(text = "개발자 | 매코#0663", icon_url= "https://cdn.discordapp.com/attachments/878968805760565288/941033278146752542/a896d7f6ec22b5cd.png")
        await channel.send(embed=embed)
        await interaction.response.send_message('공지를 보냈습니다.', ephemeral=True)

@notice.error
async def notice_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='🛑오류🛑', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)

        
        
@bot.tree.command(name="초대", description="서버 초대링크를 확인합니다.") # '초대' 명령어, 서버의 초대 코드를 유저에게 dm으로 보냄.
async def invite_link(interaction: discord.Interaction):
    invite_link = "https://discord.gg/gakU7vUP5H"

    embed = discord.Embed(title='초대링크', description= f'{invite_link}', color=0xffffff)
    await interaction.user.send(embed=embed) # 유저에게 DM으로 보냄.
    await interaction.response.send_message('DM으로 초대링크를 보냈습니다.', ephemeral=True) # 응답으로 보냄.

@invite_link.error
async def invite_link_error(interaction: discord.Interaction, error):
    embed = discord.Embed(title='🛑오류🛑', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
    await interaction.response.send_message(embed=embed)





keep_alive()
load_dotenv('secret.json')
bot.run(os.getenv('token'))
