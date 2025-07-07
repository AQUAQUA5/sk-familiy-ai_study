import requests
import pymysql

def naver_stock(code, sdate, edate):
    url = f"https://m.stock.naver.com/front-api/external/chart/domestic/info?symbol={code}&requestType=1&startTime={sdate}&endTime={edate}&timeframe=day"
    data = eval(requests.get(url).text.strip())
    return data, code

def store_data(data, code):
    data.pop(0)
    conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
    cur = conn.cursor()
    sql = "INSERT IGNORE INTO naver_day_stock VALUE (%s, %s, %s, %s, %s, %s, %s)"
    
    trow= [None]*7
    
    trow[0] = code
    for rows in data:
        for i in range(1,7):
            trow[i] = rows[i-1]
        cur.execute(sql, trow)
    conn.commit()
    conn.close()


data, code =naver_stock('005930', '20250401', '20250510')
store_data(data, code)

# conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
# cur = conn.cursor()
# sql = "INSERT INTO stock_day VALUE (%s, %s, %s, %s, %s, %s, %s)"
# ls = ['005930', '20250103', 52800, 55100, 52800, 54400, 19318046]
# cur.execute(sql, ls)
# conn.commit()