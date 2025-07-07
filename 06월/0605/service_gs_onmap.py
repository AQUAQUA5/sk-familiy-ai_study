import streamlit as st
import pandas as pd
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
cur = conn.cursor()

num_rows = 4
num_cols = 5

st.title("GS25 서비스 검색")
services = ['cafe25',
 'instant',
 'drug',
 'post',
 'parcel_service',
 'potatoes',
 'cardiac_defi',
 'spirit_wine',
 'musinsa',
 'posa',
 'fish_shaped_bun',
 'withdrawal',
 'atm',
 'smart_atm',
 'delivery_service',
 'fresh_ganghw',
 'self_cook',
 'toto',
 'gopizza',
 'tax']
services_names = [ '카페25', '인스턴트', '약', '우편', '택배' '서비스', '감자', '심장 제세동기', '주류', '무신사', 'POSA GC' , '붕어빵', '출금', 'ATM', '스마트 ATM', '배달 서비스', '신선 식품', '셀프 요리', '토토', '고피자', '세금' ]

id =0
for row in range(num_rows):
    columns = st.columns(num_cols)
    for col in range(num_cols):
        columns[id%5].checkbox(services_names[id], key = services_names[id])
        id +=1
place1 = st.empty() 
place2 = st.empty() 
chk_list = []

selec_q = '''SELECT *
FROM 
gs25_service a
LEFT JOIN gs25 b
ON a.shopCode = b.shopCode
WHERE '''

def get_sql(sql):
    cur.execute(sql)
    return cur.fetchall()

def chk_update():
    if len(chk_list) == 0:
        return
    new_q = selec_q
    new_q = new_q + "a.offeringService = " + "'" + chk_list[0] + "'"
    for i in range(1, len(chk_list)):
        new_q = new_q + " and a.offeringService = " + "'" + chk_list[i] + "'"
    
    place1.write(new_q)

    rt = get_sql(new_q)
    place2.write(pd.DataFrame(rt))
    


for i in range(20):
    if st.session_state[services_names[i]] :
        chk_list.append(services[i])
        chk_update()



