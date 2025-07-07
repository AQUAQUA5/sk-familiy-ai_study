import streamlit as st
import pandas as pd
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
cur = conn.cursor()

def get_sql(sql):
    cur.execute(sql)
    return cur.fetchall()

rt = get_sql(""" select * from st_master where MKT_TP_NM in ('KOSPI') order by list_dd desc """)

st.write(pd.DataFrame(rt))