import os
import json
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env 로드
load_dotenv()

# 환경 변수 불러오기
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ROBLOX_API_KEY = os.getenv("ROBLOX_API_KEY")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
UNIVERSE_ID = os.getenv("UNIVERSE_ID")

print(DISCORD_BOT_TOKEN)
print(ROBLOX_API_KEY)
print(GUILD_ID)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# 🔐 Roblox Ban 함수
def ban(userid, reason, time, banalts=False):
    
    url = f"https://apis.roblox.com/cloud/v2/universes/" + UNIVERSE_ID +"/user-restrictions/{userid}"
    
    headers = {
    "x-api-key": ROBLOX_API_KEY,  # ✅ API 키는 여기에!
    "Content-Type": "application/json"
    }
    
    body = {
        "user": f"/users/{userid}",
        "gameJoinRestriction": {
            "active": True,
            "duration": f"{time}s",
            "displayReason": reason,
            "excludeAltAccounts": banalts
        }
    }
    response = requests.patch(url, headers=headers, data=json.dumps(body))
    return response

# 🔐 Roblox Unban 함수
def unban(userid):
    url = f"https://apis.roblox.com/cloud/v2/universes/" + UNIVERSE_ID +"/user-restrictions/{userid}"
    
    headers = {
    "x-api-key": ROBLOX_API_KEY,  # ✅ API 키는 여기에!
    "Content-Type": "application/json"
    }
    
    body = {
        "user": f"/users/{userid}",
        "gameJoinRestriction": {
            "active": False,
        }
    }
    response = requests.patch(url, headers=headers, data=json.dumps(body))
    return response

# 봇 준비 완료 이벤트
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f'{bot.user} 로 로그인됨')
# 명령어 정의
@bot.hybrid_command()
async def banrbx(ctx, userid: str, reason: str, time: int):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("잘못된 채널입니다 (관리자 전용).")
        return
    response = ban(userid, reason, time)
    await ctx.send(f"Roblox 응답: {response.status_code} - {response.text}")

@bot.hybrid_command()
async def unbanrbx(ctx, userid: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("잘못된 채널입니다 (관리자 전용).")
        return
    response = unban(userid)
    await ctx.send(f"Roblox 응답: {response.status_code} - {response.text}")

# 봇 실행
bot.run(DISCORD_BOT_TOKEN)
