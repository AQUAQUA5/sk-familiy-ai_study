import requests
import pandas as pd
from xml.etree import ElementTree as ET
import pathlib
import multiprocessing

def get_info(code, s_date, e_date, path="./data/"):
    url = f"https://m.stock.naver.com/front-api/external/chart/domestic/notice?symbol={code}&startTime={s_date}&endTime={e_date}&requestType=0"
    root = ET.fromstring(requests.get(url).text)
   
   
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{'date' : i.get('date'), 'information' : x.text} for i in root.iter(tag='item')  for x in i]).to_csv(f"{path}/{code}.csv", index=False, encoding='utf-8-sig')



if __name__=="__main__":
    get_info('005930', '20250101', '20250525')