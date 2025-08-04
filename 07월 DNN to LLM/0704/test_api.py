from fastapi import FastAPI 
from pydantic import BaseModel 
import base64
class ImageItem(BaseModel):
    image_data : str 
    # filename : str 
    # create_date : int 

app = FastAPI() 

@app.post("/predict/")
async def inference(item: ImageItem):
    img_bytes = base64.b64decode(item.image_data)

    with open("./aa.jpg", "wb") as f:
        f.write(img_bytes)
    
    return {"message" : "잘 받앗다"}


@app.get("/")
async def test():
    return {"message" : "Hi!!"}