import requests
import pymysql

headers1 = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '88',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '__smVisitorID=jMYvcn8H966; _ga=GA1.1.7639877.1748567776; _ga_Z6N0DBVT2W=GS2.1.s1748567775$o1$g1$t1748567823$j12$l0$h0; JSESSIONID=g8b2nahgZKunheR73JiFUWtqaaPK9Fmw5b41wPRhG396lt7SlJErT5itRiUjyDuC.bWRjX2RvbWFpbi9tZGNvd2FwMi1tZGNhcHAxMQ==; _ga_808R2EHLL3=GS2.1.s1748567823$o1$g0$t1748567836$j47$l0$h0',
    'Host': 'data.krx.co.kr',
    'Origin': 'http://data.krx.co.kr',
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
payload = {
    'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
    'locale': 'ko_KR',
    'mktId': 'ALL',
    'share': '1',
    'csvxls_isNo': 'false'
}


url = f"http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
r = requests.post(url, data = payload, headers = headers1)
data= r.json()['OutBlock_1']
numb = 100
conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
cur = conn.cursor()
sql = "INSERT IGNORE INTO st_master2 VALUE (%s, %s)"

for i in range(100):
    cur.execute(sql, [ data[i]['ISU_CD'],  data[i]['ISU_SRT_CD']])

conn.commit()