import os
import streamlit as st
from openai import OpenAI
import openai

from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)


st.title("문장을 mp3 파일 생성")


user_prompt = st.text_area("스크립트 작성", height=300)


if st.button("음성생성"):
    audio = client.audio.speech.create(
        model='tts-1',
        voice='alloy',
        input = user_prompt
    )


    audio_content = audio.content


    with open("tmp.mp3", 'wb') as f:
        f.write(audio_content)
    st.audio("tmp.mp3", format='audio/mp3')
