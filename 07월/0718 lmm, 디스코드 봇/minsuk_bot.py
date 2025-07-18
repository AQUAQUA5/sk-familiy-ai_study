import discord
import requests
import re

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

API_KEY = "k"
URL = "https://api.perplexity.ai/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",}

payload = {
    "model": "sonar-pro",           # 사용할 모델
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "민석이에 대해서 설명해줘"}
    ],
    "stream": False,                # 스트리밍 여부
    "max_tokens": 100,              # 최대 토큰 수
    "temperature": 0.5,             # 답변 랜덤성 조절
    # 검색 모드와 추가 옵션
    "search_mode": "academic",      
    "web_search_options": {
        "search_context_size": "medium",
        "search_after_date_filter": "07/01/2025",
        "search_before_date_filter": "07/18/2025"}}

@client.event
async def on_ready():
    print(f'{client.user}로 로그인 완료')

@client.event
async def on_message(message):
    if (message.author == client.user) or (message.author.id != 658951345256136713):  # 봇 자신의 메시지는 무시
        return
    
    content = message.content

    pattern_how = re.compile(r'민석아.*어때\s*\?*$', re.IGNORECASE)
    pattern_check = re.compile(r'^민석아.*(?<!\?)$', re.IGNORECASE)

    if pattern_how.match(content):
        await message.channel.send("좋은데?")
        return
    
    if pattern_check.match(content):
        await message.channel.send("확인했다")
        return


client.run("token")
