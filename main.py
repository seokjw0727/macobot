import discord
import random
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import datetime
import pytz
from mcstatus import JavaServer
from webdriver import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix = "매코 ", intents=discord.Intents.all()) 

bot.remove_command('help') # 봇에 기본적으로 탑재된 help 명령어를 제거함.

@bot.event # 'on_ready' 이벤트 || 봇이 준비되면 콘솔에 봇 관련 정보를 출력함.
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




@bot.event # '매코야' 이벤트 || 유저가 "매코야" 를 입력하면 랜덤한 메시지를 보냄.
async def on_message(message):
    if message.author.bot:
        return None
    if message.content == '매코야':
        replies = ['왜 불러여?', '매코!', '왜여?', '온라인!', '히히', '반가워요!', '매코봇은 매코#0663 에 의해 개발되었습니다.']
        reply = random.choice(replies)
        await message.channel.send(reply)
    elif message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)



@bot.tree.command(name="상태", description="봇의 네트워크 상태를 확인합니다.") # '상태' 명령어 || 봇의 네트워크 상태를 embed 함.
async def status(interaction: discord.Interaction):
    logging_channel = bot.get_channel(1114564440092835990)
    if bot.latency * 1000 >= 100:
        embed_green = discord.Embed(title= "**🔴 상태 나쁨 🔴**", description= f"봇의 네트워크 상태는 **{round(round(bot.latency, 4)*1000)}ms** 입니다.", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0xff0000)
        await interaction.response.send_message(embed=embed_green)
    else:
        embed_red = discord.Embed(title= "**🟢 상태 좋음 🟢**", description= f"봇의 네트워크 상태는 **{round(round(bot.latency, 4)*1000)}ms** 입니다.", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
        await interaction.response.send_message(embed=embed_red)
    await logging_channel.send(f"{interaction.user} 님이 '/상태' 명령어를 사용했습니다.")



@bot.tree.command(name="청소", description="/청소 [1 이상의 자연수] | ⚙️") # '청소' 명령어 || 원하는 수 만큼의 메시지를 삭제함.
@commands.has_permissions(administrator=True)
@app_commands.describe(amount="청소할 메시지의 개수")
async def clear_chat(interaction: discord.Interaction, amount: int):
    logging_channel = bot.get_channel(1114564440092835990)
    if amount < 1 :
        embed = discord.Embed(title='오류', description='1 이상의 자연수를 입력해주세요.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("청소를 시작합니다...")
        await interaction.channel.purge(limit=amount + 1)
        embed = discord.Embed(title= "🧹 **채팅 청소** 🧹", description= f"__{amount}__ 개의 메시지를 청소했습니다. \n 　", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0x99ffff)
        embed.add_field(name= "처리자", value= f"<@{interaction.user.id}>", inline= False)
        await interaction.channel.send(embed=embed)
    await logging_channel.send(f"{interaction.user} 님이 '/청소' 명령어를 사용했습니다.")

@clear_chat.error
async def clear_chat_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="경고", description="/경고 @대상 [사유] | ⚙️") # '경고' 명령어 || 유저에 대한 경고 embed 를 처벌 채널에 보내고, 유저에게 dm 으로 관련 안내를 함.
@commands.has_permissions(administrator=True)
@app_commands.describe(유저="경고를 줄 유저", 사유="경고 사유")
async def warn(interaction: discord.Interaction, 유저: discord.Member, 사유: str):
    logging_channel = bot.get_channel(1114564440092835990)
    channel = bot.get_channel(878886065321160745) # 처벌 채널 
    if channel is None:
        await interaction.response.send_message('경고 채널을 찾을 수 없습니다.')
        return
    
    # 경고 embed 를 처벌 채널에 보냄.
    embed = discord.Embed(title= "❗ **경고** ❗", description= f"관리자가 *{유저}* 에게 경고를 부여했습니다!", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
    embed.add_field(name= "사유", value= f"{사유}")
    embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
    await channel.send(embed=embed)
    await interaction.response.send_message(f'*{유저.mention}* 을(를) 경고했습니다.')

    # 경고 embed 를 경고 대상에게 dm 으로 보냄.
    embed = discord.Embed(title= "❗ **경고** ❗", description= "관리자가 당신에게 경고를 부여했습니다.", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
    embed.add_field(name= "사유", value= f"{사유}")
    embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
    await 유저.send(embed=embed)
    await 유저.send("**안내드립니다.** \n\n 경고가 누적될 경우, 서버에서 불이익을 받을 수 있습니다. \n 경고 처리자에게 반성문을 작성하시면, 정도에 따라 경고를 철회할 수 있습니다.")
    await logging_channel.send(f"{interaction.user} 님이 '/경고' 명령어를 사용했습니다.")

@warn.error
async def warn_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



@bot.tree.command(name="차단", description="/차단 @대상 [사유] | ⚙️") # '차단' 명령어 || 유저의 모든 역할을 박탈하고 '차단' 역할을 부여하고, 처벌 채널에 embed 를 보내며, 유저에게 dm 으로 관련 안내를 함.
@app_commands.describe(유저="차단할 유저", 사유="차단 사유")
@commands.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, 유저: discord.Member, 사유: str):
    logging_channel = bot.get_channel(1114564440092835990)
    
    for i in 유저.roles: # 차단 대상의 모든 역할을 박탈함.
        try:
            await 유저.remove_roles(i)  
        except:
            channel = bot.get_channel(878886065321160745) # 처벌 채널 
            await 유저.add_roles(유저.guild.get_role(878966349701971999))
            if channel is None:
                await interaction.response.send_message('처벌 채널을 찾을 수 없습니다.')
                return
    
            # 차단 embed 를 처벌 채널에 보냄.
            embed = discord.Embed(title= "⛔ **차단** ⛔", description= f"관리자가 *{유저}* 을(를) 차단했습니다!", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
            embed.add_field(name= "사유", value= f"{사유}")
            embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
            await channel.send(embed=embed)
            await interaction.response.send_message(f'*{유저.mention}* 을(를) 차단했습니다.')

            # 차단 embed 를 경고 대상에게 dm 으로 보냄.
            embed = discord.Embed(title= "❗ **경고** ❗", description= "관리자가 당신을 서버에서 차단했습니다.", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xff0000)
            embed.add_field(name= "사유", value= f"{사유}")
            embed.add_field(name= "처리자", value= interaction.user.mention, inline= False)
            await 유저.send(embed=embed)
            await 유저.send("**안내드립니다.** \n\n 차단 처리자에게 반성문을 작성하시면 차단을 해제할 수 있습니다.")
    await logging_channel.send(f"{interaction.user} 님이 '/차단' 명령어를 사용했습니다.")

@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
        


@bot.tree.command(name="공지", description="/공지 [내용] | ⚙️") # '공지' 명령어 || 공지 채널에 embed 를 보냄.
@app_commands.describe(내용="공지 내용")
@commands.has_permissions(administrator=True)
async def notice(interaction: discord.Interaction, 내용: str, 멘션: bool = False):
    logging_channel = bot.get_channel(1114564440092835990)
    channel = bot.get_channel(878870335863287818)
    if channel is None:
        await interaction.response.send_message('공지 채널을 찾을 수 없습니다.')
        return
    if 멘션 == True:
        embed=discord.Embed(title="🔔 **공지사항** 🔔", description=f"\n\n{내용} ||@everyone||", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xFF6633)
        await channel.send(embed=embed)
        await interaction.response.send_message('공지를 보냈습니다.', ephemeral=True)
    else:
        embed=discord.Embed(title="🔔 **공지사항** 🔔", description=f"\n\n{내용}\n\n", timestamp= datetime.datetime.now(pytz.timezone('UTC')), color= 0xFF6633)
        await channel.send(embed=embed)
        await interaction.response.send_message('공지를 보냈습니다.', ephemeral=True)
    await logging_channel.send(f"{interaction.user} 님이 '/공지' 명령어를 사용했습니다.")

@notice.error
async def notice_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)

        
        
@bot.tree.command(name="초대", description="서버 초대링크를 확인합니다.") # '초대' 명령어 || 관련 정보를 embed로 dm 으로 보냄.
async def invite_link(interaction: discord.Interaction):
    logging_channel = bot.get_channel(1114564440092835990)
    invite_link = "https://discord.gg/gakU7vUP5H"

    embed = discord.Embed(title='초대링크', description= f'{invite_link}', color=0xffffff)
    await interaction.user.send(embed=embed) 
    await interaction.response.send_message('DM으로 초대링크를 보냈습니다.', ephemeral=True)
    await logging_channel.send(f"{interaction.user} 님이 '/초대' 명령어를 사용했습니다.")



@bot.tree.command(name="크레딧", description="봇의 크레딧을 확인합니다.") # '크레딧' 명령어 || 크레딧을 embed 로 보냄.
async def credit(interaction: discord.Interaction):
    logging_channel = bot.get_channel(1114564440092835990)
    embed = discord.Embed(title='🎖️ **크레딧** 🎖️', description='오래된 겜펜봇을 대체하고자 만들어진 매코봇입니다.', color=0xffffff)
    embed.add_field(name='개발자', value='`매코#0663`', inline=False)
    embed.add_field(name='개발 시작일', value='`2023년 3월 25일`', inline=False)
    embed.add_field(name='개발 종료일', value='`2023년 5월 13일`', inline=False)
    embed.add_field(name='개발 언어', value='`Python`', inline=False)
    embed.add_field(name='개발 라이브러리', value='`discord.py`', inline=False)
    embed.set_footer(text='*All rights reserved. © 2023. 매코*')
    await interaction.response.send_message(embed=embed, ephemeral=True)
    await logging_channel.send(f"{interaction.user} 님이 '/크레딧' 명령어를 사용했습니다.")



@bot.event # '관종' 이벤트 || SUPER, ULTRA, 넘치는 존재감 역할이 있는 유저가 음성 채널에 접속하면, 채팅 채널에 접속하였음을 알림.
async def on_voice_state_update(member, before, after):
    
    
    # 채널
    chat_channel = bot.get_channel(1008066418127937586) # 채팅 채널
    voice_channel_1 = bot.get_channel(878881493806633010) # '비' 채널
    voice_channel_2 = bot.get_channel(878881956111204373) # '맑음' 채널
    voice_channel_3 = bot.get_channel(972503073224273981) # '흐림' 채널
    voice_channel_4 = bot.get_channel(878882702835712021) # '번개' 채널

    # 역할
    roles_super = member.guild.get_role(878975480412381214) # SUPER 역할
    roles_ultra = member.guild.get_role(931000785477730365) # ULTRA 역할
    roles_identity = member.guild.get_role(879589070718771250) # 넘치는 존재감 역할

    if before.channel is None and after.channel is not None:
        if after.channel is voice_channel_1 and roles_identity in member.roles: # '넘치는 존재감'이 '비' 채널에 접속한 경우임.
            await chat_channel.send(f"✨ 👑**{member.nick}** __**ㄷㄷㄷㅈ!**__ 바로 __🌧비__ 채널에 합류하세요! ✨")
        elif after.channel is voice_channel_1 and roles_ultra in member.roles: # 'ULTRA'가 '비' 채널에 접속한 경우임.
            await chat_channel.send(f"💎방금, __🌧비__ 채널에 **{member.nick}** 님이 강림했어요! 💎")
        elif after.channel is voice_channel_1 and roles_super in member.roles: # 'SUPER'가 '비' 채널에 접속한 경우임.
            await chat_channel.send(f"**{member.nick}** 님이 __🌧비__ 채널에 나타났어요!")

        elif after.channel is voice_channel_2 and roles_identity in member.roles: # '넘치는 존재감'이 '맑음' 채널에 접속한 경우임.
            await chat_channel.send(f"✨ 👑**{member.nick}** __**ㄷㄷㄷㅈ!**__ 바로 __🌞맑음__ 채널에 합류하세요! ✨ ")
        elif after.channel is voice_channel_2 and roles_ultra in member.roles: # 'ULTRA'가 '맑음' 채널에 접속한 경우임.
            await chat_channel.send(f"💎 방금, __🌞맑음__ 채널에 **{member.nick}** 님이 강림했어요! 💎")
        elif after.channel is voice_channel_2 and roles_super in member.roles: # 'SUPER'가 '맑음' 채널에 접속한 경우임.
            await chat_channel.send(f"**{member.nick}** 님이 __🌞맑음__ 채널에 나타났어요!")

        elif after.channel is voice_channel_3 and roles_identity in member.roles: # '넘치는 존재감'이 '흐림' 채널에 접속한 경우임.
            await chat_channel.send(f"✨ 👑**{member.nick}** __**ㄷㄷㄷㅈ!**__ 바로 __⛅흐림__ 채널에 합류하세요! ✨ ")
        elif after.channel is voice_channel_3 and roles_ultra in member.roles: # 'ULTRA'가 '흐림' 채널에 접속한 경우임.
            await chat_channel.send(f"💎 방금, __⛅흐림__ 채널에 **{member.nick}** 님이 강림했어요! 💎")
        elif after.channel is voice_channel_3 and roles_super in member.roles: # 'SUPER'가 '흐림' 채널에 접속한 경우임.
            await chat_channel.send(f"**{member.nick}** 님이 __⛅흐림__ 채널에 나타났어요!")

        elif after.channel is voice_channel_4 and roles_identity in member.roles: # '넘치는 존재감'이 '번개' 채널에 접속한 경우임.
            await chat_channel.send(f"✨ 👑**{member.nick}** __**ㄷㄷㄷㅈ!**__ 바로 __⚡번개__ 채널에 합류하세요! ✨ ")
        elif after.channel is voice_channel_4 and roles_ultra in member.roles: # 'ULTRA'가 '번개' 채널에 접속한 경우임.
            await chat_channel.send(f"💎 방금, __⚡번개__ 채널에 **{member.nick}** 님이 강림했어요! 💎")
        elif after.channel is voice_channel_4 and roles_super in member.roles: # 'SUPER'가 '번개' 채널에 접속한 경우임.
            await chat_channel.send(f"**{member.nick}** 님이 __⚡번개__ 채널에 나타났어요!")
        


@bot.tree.command(name= "마크", description="🛠️ 수리중 🛠️") # '마크' 명령어 || 수리중인 명령어를 임시로 막음.
async def minecraft_server_check(interaction: discord.Interaction):
    await interaction.response.send_message("해당 명령어는 수리중입니다.", ephemeral=True)



@bot.tree.command(name= "minecraft_server_check", description= "매코 서버의 상태를 확인합니다.") # 'minecraft_server_check' 명령어 || '마크' 명령어를 수리하기 위해 만든 임시 명령어.
@commands.has_permissions(administrator=True)
async def minecraft_server_check_test_version(interaction: discord.Interaction):
    logging_channel = bot.get_channel(1114564440092835990)
    await logging_channel.send(f"{interaction.user} 님이 '/minecraft_server_check' 명령어를 사용했습니다.")
    server = JavaServer.lookup("124.60.247.163:25565")
    status = server.status()

    if status.latency == None:
        embed = discord.Embed(title='🔴오프라인🔴', description='서버가 오프라인이거나 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='🟢온라인🟢', description='서버에 접속할 수 있습니다.', color=0x00ff00)
        embed.add_field(name='서버 상태', value=f'{status.latency}ms', inline=False)
        embed.add_field(name='현재 플레이어 수', value=f'{status.players.online}명', inline=False)
        await interaction.response.send_message(embed=embed)
        
@minecraft_server_check_test_version.error
async def minecraft_server_check_test_version_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title='❌거부❌', description='당신은 관리자 권한이 없습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title='⛔오류⛔', description='알 수 없는 오류가 발생했습니다.', color=0xff0000)
        await interaction.response.send_message(embed=embed)



keep_alive()
load_dotenv('secret.json')
bot.run(os.getenv('token'))
