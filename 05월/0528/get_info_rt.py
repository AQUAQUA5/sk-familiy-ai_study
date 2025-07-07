import requests
import pandas as pd

from xml.etree import ElementTree as ET
import pathlib
import multiprocessing

def get_name_to_code(target):

    #http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

    payload={
        "bld":"dbms/MDC/STAT/standard/MDCSTAT01901",
        "locale":"ko_KR",
        "mktId":"ALL",
        "share":"1",
        "csvxls_isNo":"false",
        }

    request_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "88",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "data.krx.co.kr",
        "Origin": "http://data.krx.co.kr",
        "Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    r= requests.post(url, data=payload, headers=request_headers)
    data= r.json()['OutBlock_1']


    rt = [y['ISU_SRT_CD'] for y in [ x for x in data if x['ISU_ABBRV'].find(f"{target}") > -1] if y['ISU_ABBRV'].find(target + '우') == -1]

    if len(rt) > 0:
        return rt[0]
    else:
        return '종목 코드가 존재하지 않음'
    

def get_info(code, s_date='20250101', e_date='20250525', path="./data/"):
    url = f"https://m.stock.naver.com/front-api/external/chart/domestic/notice?symbol={code}&startTime={s_date}&endTime={e_date}&requestType=0"
    root = ET.fromstring(requests.get(url).text)
   
   
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([{'date' : i.get('date'), 'information' : x.text} for i in root.iter(tag='item')  for x in i])

    return df

if __name__=="__main__":
    get_info('005930', '20250101', '20250525')