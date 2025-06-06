import requests
import pymysql
from bs4 import BeautifulSoup as bs

#contents > div.sub-content > div.player_info > div.player_basic > ul
conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
cur = conn.cursor()
cur.execute("select kbo_id from kbo_players")
rows = cur.fetchall()

insert_q = "INSERT IGNORE INTO player_detail VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
create_q = """CREATE TABLE player_detail  (
    kbo_id varchar(10)  not null,
    name varchar(30) not null,
    player_number int default null,
    birthday varchar(15)  default null default null,
    position varchar(20) default null,
    height int default null,
    weight int default null,
    career varchar(50) default null,
    입단계약금 varchar(10)  default null,
    연봉 varchar(10)  default null,
    지명순위 varchar(30)  default null,
    입단년도 varchar(20)  default null
)"""

cur.execute('show tables')
tables = [row[0] for row in cur.fetchall()]
if 'player_detail' in tables:
    cur.execute('drop table player_detail')
cur.execute(create_q)



for id in rows:
    url = f"https://www.koreabaseball.com/Record/Player/HitterDetail/Basic.aspx?playerId={id[0]}"
    soup = bs(requests.get(url).text, 'lxml').find('div', class_='player_basic').find_all('span')
    row_list = []
    for i in soup:
        row_list.append(i.text)

    h, w = row_list[4].split('cm/')
    h = int(h)
    w = int(w[0:-2])
    row_list.insert(0, id[0])
    row_list.insert(5, h)
    row_list.insert(6, w)
    row_list.pop(7)
    cur.execute(insert_q, row_list)

conn.commit()






