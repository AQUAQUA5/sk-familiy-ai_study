import streamlit as st 
from langchain_openai import ChatOpenAI 
from langchain_core.messages import SystemMessage, HumanMessage 
from langchain_core.prompts import ChatPromptTemplate 
from openai import OpenAI


load_dotenv(dotenv_path="../../.env")
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)
model = ChatOpenAI(
    model = 'gpt-4.1-2025-04-14',
    temperature=0.5,
)

system_prompt = """
당신은 취업 준비생입니다. 아래 입력값을 참고하여 500자 자기소개서를 작성해주세요. 
"""

user_promt = """ 
대학교: {univ}
동아리: {circle}
봉사활동: {helper}
성격: {type}
"""

prompt = ChatPromptTemplate.from_messages(
    [
       ("system", system_prompt),
       ("human", user_promt)
    ]
)
# print(prompt)

col1, col2 = st.columns(2)
with col1:
    univ = st.text_input("대학교명", placeholder= ' ')
    circle = st.text_input("동아리", placeholder= ' ')
with col2:
    helper = st.text_input("봉사활동", placeholder= ' ')
    type_ = st.text_input("성격", placeholder= ' ')    
print("-----------")
print(univ, circle, helper, type_)

if st.button("자소서 생성"):
    msgs = prompt.format_messages(
        univ = univ,
        circle = circle, 
        helper = helper, 
        type = type_
    )
    print(msgs)

    with st.spinner("자소서 생성중..."):
        response = model.invoke(msgs)
    
    st.success("생성 완료")

    st.text_area(label='결과', value=response.content, height=300)
    audio = client.audio.speech.create(
        model='tts-1',
        voice= 'fable',
        input = response.content,
        speed = 1
    )
    audio_content = audio.content

    with open("tmp.mp3", 'wb') as f:
        f.write(audio_content)
    st.audio("tmp.mp3", format='audio/mp3')