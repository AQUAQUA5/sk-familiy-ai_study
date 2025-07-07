import streamlit as st
import requests
import base64  # Base64




st.title('강아지 품종')
st.header("품종 조회")




upload_file = st.file_uploader(
    "강아지 사진 올려", type=['png', 'jpg']
)
if upload_file is not None:
    url  = "http://127.0.0.1:8000/predict/"
    image_byes = upload_file.getvalue()
    base64_encoded = base64.b64encode(image_byes).decode("utf-8")
    payload = {'image' : base64_encoded}
    r = requests.post(url, data = payload)


    st.markdown(f"# {r.json()['breed']}")