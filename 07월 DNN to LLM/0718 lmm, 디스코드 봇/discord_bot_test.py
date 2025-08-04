import discord
import requests

intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 읽기 권한

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}로 로그인 완료')

@client.event
async def on_message(message):
    if (message.author == client.user) or (message.author == client.user):  # 봇 자신의 메시지는 무시
        return
    print(f"메시지 보낸 사람 ID: {message.author.id}")
    
    if message.content == "민석아 저거 어때?":    # "테스트" 입력 감지
        await message.channel.send("좋은데?")



# 토큰은 실제 봇 토큰으로 교체
client.run("token")
