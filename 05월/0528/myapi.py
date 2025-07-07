#RESTful API
#인터넷을 통해서 가져옴

from fastapi import FastAPI

app = FastAPI()

# @app.get("./encore/")
# def myfunc():
#     return {"message" : "ㅋㅋㅋㅋ"}

# #시간이 오래걸릴땐 비동기로 생성해야함

@app.get("/encore/")
async def myfunc():     #async 비동기함수
    return {"message" : "ㅋㅋㅋㅋ"}