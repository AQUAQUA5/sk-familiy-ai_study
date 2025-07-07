import streamlit as st
from get_info_rt import get_name_to_code, get_info
import logging, os
from datetime import datetime

if os.path.isdir('./logs') == False:
    os.mkdir('./logs')

#file_name = "service_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
file_name = 'service' + datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
log_datefmt = '%Y-%m-%d %H:%M:%S' # 예: 2025-04-22 10:07:49

logging.basicConfig(filename="./logs/" + file_name,  level=logging.INFO, # INFO 레벨 이상만 기록
                    format=log_format,
                    datefmt=log_datefmt)

st.title('공시정보 보여주기')
st.header("공시정보 조회")

col1, col2, col3 = st.columns(3)
input_sdate = '20250101'
input_edate = '20250525'

with col1:
    input_code = st.text_input(
    label = '종목이름 입력해주세요',
    placeholder="예) 삼성전자"
    )  

with col2:
    input_sdate = st.text_input(
    label = '시작 날짜입력',
    placeholder="예) 20250101"
    )   

with col3:
    input_edate = st.text_input(
    label = '종료료 날짜입력',
    placeholder="예) 20250525"
    )   

if st.button("조회"):
    logging.info(f"{input_code} - {input_sdate} - {input_edate}")
    print(f"{input_code} - {input_sdate} - {input_edate}")
    rt = get_info(get_name_to_code(input_code), input_sdate, input_edate)
    st.write(rt)