import streamlit as st
import folium
from streamlit_folium import st_folium
import pickle

st.title("스타벅스 지도 시각화")

seoul = folium.Map(location=[37.55, 126.98], zoom_start=12)

with open("./starbucks.pkl", 'rb') as f:
    result = pickle.load(f)


for store in result['list']:
    folium.Marker([store['lat'], store['lot']], popup=store['s_name'], tooltip=store['s_name'], icon=folium.Icon(color='blue', icon='info-sign')).add_to(seoul)

map_data = st_folium(seoul, width=1000, height=1000)

#streamlit run starbuck_map.py