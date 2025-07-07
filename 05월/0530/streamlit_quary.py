import streamlit as st
import pandas as pd
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='play', passwd='123', database='sk17', port=3306)
cur = conn.cursor()

def get_sql(sql):
    cur.execute(sql)
    return cur.fetchall()

input_sql = st.text_input(label='SQL 입력력')

if input_sql:
    rt = get_sql(input_sql)
    st.write(pd.DataFrame(rt))