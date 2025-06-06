from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import pymysql
import time

def start():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # 메인페이지 접속
    driver.get("https://www.koreabaseball.com/Default.aspx?vote=true")

    # 선수 조회 창 접속
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#lnb > li:nth-child(3) > a"))
    ).click()
    return driver

def select_team(n, driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_ddlTeam > option:nth-child({n})"))
    ).click()

    return

def select_page(n, driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"#cphContents_cphContents_cphContents_ucPager_btnNo{n}"))
    ).click()
    return
def html_2_df(html):
    col = ['등번호', '선수명', 'kbo_id', '팀', '포지션', '생년월일', '키', '몸무게', '출신']
    soup = bs(table_html, 'html.parser')
    data = []
    for row in soup.find_all('tr'):
        row_list = []
        for i in row.find_all('td'):
            row_list.append(i.text)
        row_list.insert(2, row.find('a')['href'].split("=")[-1])
        h, w = row_list[6].split(', ')
        row_list[6] = h
        row_list.insert(7, w)
        data.append(row_list)
    df = pd.DataFrame(data, columns=col)
    return df


cr_table_quary = """CREATE TABLE kbo_players (
    player_number int default null,
    name varchar(30) not null,
    kbo_id varchar(10)  not null,
    team varchar(10)  not null,
    position varchar(20) default null,
    birthday date default null,
    height int default null,
    weight int default null,
    career varchar(50) default null
)"""

query = "INSERT IGNORE INTO kbo_players VALUE ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"

conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
cur = conn.cursor()

cur.execute("show tables")
if 'kbo_players' in cur.fetchall():
    cur.execute("drop table kbo_players")
cur.execute(cr_table_quary)

driver = start()
for i in range(2, 12):
    select_team(i, driver)
    time.sleep(1)
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > div.inquiry > div"))
    )
    maxPage = element.text.split()[-1]
    for j in range(1, int(maxPage)+1):
        select_page(j, driver)
        time.sleep(1)
        table_html = driver.find_element(By.CSS_SELECTOR, "#cphContents_cphContents_cphContents_udpRecord > div.inquiry > table > tbody").get_attribute('innerHTML')
        df = html_2_df(table_html)
        for row in df.itertuples(index=False):
            cur.execute(query, [x if x != '' else None for x in row] )
            conn.commit()

#table = driver.find_element(By.CSS_SELECTOR,"#cphContents_cphContents_cphContents_udpRecord > div.inquiry > table > tbody").text






