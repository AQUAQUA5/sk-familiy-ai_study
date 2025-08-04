from openai import OpenAI
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableMap
from langchain_ollama import ChatOllama
import os
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_core.prompts import loading
from langchain_core.prompts import ChatPromptTemplate
import base64
from PIL import Image
import io
from langchain_experimental.text_splitter import SemanticChunker

client = OpenAI()
if os.path.isdir("./mycache") == False:
    os.mkdir("./mycache")
if os.path.isdir("./mycache/files") == False:
    os.mkdir("./mycache/files")
if os.path.isdir("./mycache/embedding") == False:
    os.mkdir("./mycache/embedding")
store = LocalFileStore("./mycache/embedding")

if 'chain' not in st.session_state:
    st.session_state['chain'] = None

st.title("RAG 기반 챗봇")

with st.sidebar:
    uploaded_file = st.file_uploader("파일 업로드", type=['pdf', 'txt'])

@st.cache_resource(show_spinner="업로드 파일 처리중 기다리세요")
def processing(file):
    if file.name.split(".")[-1] == "pdf":
        file_contents = file.read()
        #파일 저장
        with open(f"./mycache/files/{file.name}", "wb") as f:
            f.write(file_contents)
        #파일 임베딩
        # insert your code
        loader = PDFPlumberLoader(f"./mycache/files/{file.name}")
        docs = loader.load()
        text_spliter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        split_documents = text_spliter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
       
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
                            underlying_embeddings=embeddings, # 기본 임베딩 모델 지정
                            document_embedding_cache=store # 로컬 저장소 지정
                        )
        vectorstore = FAISS.from_documents(documents=split_documents, embedding=cached_embedder)
        retriever = vectorstore.as_retriever()
           
    elif file.name.split(".")[-1] == "txt":
        file_contents = file.read()
        #파일 저장
        with open(f"./mycache/files/{file.name}", "w", encoding='utf-8') as f:
            f.write(file_contents.decode())
        text = file_contents.decode()
        text_splitter = SemanticChunker(
                OpenAIEmbeddings(),
                breakpoint_threshold_type="percentile", # 백분위수 기준
                breakpoint_threshold_amount=70, # 임계값 70%
            )
        split_documents = text_splitter.create_documents([text])
        embeddings = OpenAIEmbeddings()
       
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
                            underlying_embeddings=embeddings, # 기본 임베딩 모델 지정
                            document_embedding_cache=store # 로컬 저장소 지정
                        )
        vectorstore = FAISS.from_documents(documents=split_documents, embedding=cached_embedder)
        retriever = vectorstore.as_retriever()
   
    #######
    return retriever


join_docs = RunnableLambda(
    lambda docs: "\n".join(doc.page_content for doc in docs)
)


def create_chain(retriever):
    prompt_text = {'_type': 'prompt',
                'template': "You are an assistant for question-answering tasks. \nUse the following pieces of retrieved `information` to answer the question. \nIf you don't know the answer, just say that you don't know. \nAnswer in Korean.\n\n<information>\n{context} \n</information>\n\n#Question: \n{question}\n\n#Answer:\n",
                'input_variables': ['question', 'context']}
    prompt = loading.load_prompt_from_config(prompt_text)
    # llm = ChatOllama(model='gemma:7b', temperature=0)
    llm = ChatOpenAI( model='gpt-4.1-2025-04-14', temperature=0)

    chain = (RunnableMap({"context" : retriever  | join_docs, "question" : RunnablePassthrough() })
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


if uploaded_file:
    retriever = processing(uploaded_file)
    chain = create_chain(retriever)
    st.session_state['chain'] = chain

options = ("질문하기", "이미지 생성")
selected_radio = st.radio(
    '다음 중 하나 선택하세요',
    options
)

if selected_radio == "질문하기":

    user_input = st.chat_input("질문을 하세요")

    if user_input:
        chain = st.session_state['chain']


        if chain is not None:
            st.chat_message("user").write(user_input)
            response = chain.stream(user_input)

            with st.chat_message('assistant'):
                container = st.empty()

                ai_answer = ""
                for token in response:
                    ai_answer += token
                    container.markdown(ai_answer)
elif selected_radio == "이미지 생성":
    generate_input = st.chat_input("생성하고 싶은 이미지를 설명해주세요")

    if generate_input:

        response = client.images.generate(
                    model='dall-e-3',
                    prompt=generate_input,
                    size="1024x1024",
                    quality = 'standard',
                    response_format='b64_json',
                    n=1
                )
        result = response.model_dump()
        img = response.data[0]
        img_data = base64.b64decode(img.b64_json)
        img = Image.open(io.BytesIO(img_data))
        st.image(img)


