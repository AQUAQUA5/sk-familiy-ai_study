from fastapi import FastAPI
from pydantic import BaseModel
import base64

app =FastAPI()


class Imageitem(BaseModel):
    image_data : str

@app.post("/predict/")
async def inference(item: Imageitem):
    img_bytes - base64.b64decode(item.image_data)
    with open("./aa,jpg", "wb") as f:
        f.write(img_bytes)

    return {"message" : "잘 받았다."}

@app.get("/")
async def test():
    return {"message":"HI!"}