from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import discord

tokenizer2 = AutoTokenizer.from_pretrained("nlp04/korean_sentiment_analysis_kcelectra")
model2 = AutoModelForSequenceClassification.from_pretrained("nlp04/korean_sentiment_analysis_kcelectra")

pipe2 = pipeline("text-classification", model="nlp04/korean_sentiment_analysis_kcelectra")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

CHANNEL_ID = 1353622927995572254

@client.event
async def on_ready():
    print("Ready!!!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    result = pipe2(message.content)[0]['label']

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f" {result }")

client.run('토큰')