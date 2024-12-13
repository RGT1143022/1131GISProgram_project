
import folium
from streamlit_folium import st_folium
import streamlit as st

# 創建第一個地圖 m1，用 OpenStreetMap
m1 = folium.Map(location=[0, 0], zoom_start=5, control_scale=True)  # 使用控制縮放和比例尺
folium.TileLayer('OpenStreetMap', attr='OpenStreetMap').add_to(m1)  # OSM 基底圖

# 創建第二個地圖 m2，用暗色基底
m2 = folium.Map(location=[0, 0], zoom_start=5, control_scale=True)  # 使用控制縮放和比例尺
folium.TileLayer('Stamen Toner', attr='Stamen Toner Tiles').add_to(m2)  # 暗色基底圖

# 使用 Streamlit 展示地圖
row1, row2 = st.columns(2)

with row1:
    output1 = st_folium(m1, width=400, height=300, key="map1")

with row2:
    output2 = st_folium(m2, width=400, height=300, key="map2")

    # 設定同步移動和縮放
    if "map_center" not in st.session_state:
        st.session_state.map_center = output1["center"]
        st.session_state.map_zoom = output1["zoom"]

    # 更新 m2 的中心和縮放級別
    def sync_map(event):
        st.session_state.map_center = event["center"]
        st.session_state.map_zoom = event["zoom"]

    m1.on('moveend', sync_map)  # 正確的事件名稱與回調函數參數