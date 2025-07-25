# streamlit_app.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
from fpdf import FPDF
import io

# --------------------- 설정 ---------------------
st.set_page_config(page_title="Bali Travel Guide", page_icon="🌴", layout="wide")

# ------------------- 언어 선택 -------------------
language = st.radio("🌐 언어 / Language", ["한국어", "English"])

TEXT = {
    "한국어": {
        "title": "7월 말, 발리 인터랙티브 여행 가이드",
        "subtitle": "일정별 관광지, 맛집, 병원/대사관 정보를 확인하고 다운로드해보세요!",
        "restaurant": "🍽️ 맛집 정보",
        "attractions": "📍 관광지",
        "safety": "🏥 병원 및 대사관",
        "download_csv": "📥 맛집 리스트 다운로드 (CSV)",
        "download_pdf": "📄 추천 일정 다운로드 (PDF)",
        "distance": "현재 위치에서 거리 (km)"
    },
    "English": {
        "title": "Late July: Interactive Bali Travel Guide",
        "subtitle": "Explore attractions, restaurants, and embassy info by day and download your plan!",
        "restaurant": "🍽️ Restaurant Info",
        "attractions": "📍 Attractions",
        "safety": "🏥 Hospitals & Embassy",
        "download_csv": "📥 Download Restaurant List (CSV)",
        "download_pdf": "📄 Download Itinerary (PDF)",
        "distance": "Distance from current location (km)"
    }
}

T = TEXT[language]

st.title(T["title"])
st.write(T["subtitle"])

# ------------------- 데이터 -------------------
locations = {
    '스미냑 비치': [-8.6917, 115.1583], '짱구 비치': [-8.6593, 115.1385],
    '우붓 왕궁': [-8.5069, 115.2624], '우붓 시장': [-8.5076, 115.2622],
    '몽키 포레스트': [-8.5193, 115.2592], '렘푸양 사원': [-8.3902, 115.6321],
    '띠르따 강가': [-8.4120, 115.5902], '뜨갈랄랑': [-8.4312, 115.2779],
    '울루와뚜 사원': [-8.8291, 115.0849], '짐바란 베이': [-8.7844, 115.1637],
    '꾸따 비치': [-8.7186, 115.1685]
}

restaurants = {
    'The Shady Shack (짱구)': {'lat': -8.6635, 'lon': 115.1363, 'desc': '채식/비건'},
    'La Favela (스미냑)': {'lat': -8.6800, 'lon': 115.1561, 'desc': '바 & 레스토랑'},
    "Naughty Nuri's Warung (우붓)": {'lat': -8.4975, 'lon': 115.2559, 'desc': '폭립'},
    'Warung Babi Guling Ibu Oka (우붓)': {'lat': -8.5064, 'lon': 115.2621, 'desc': '바비굴링'},
    'Sari Organik (우붓)': {'lat': -8.4950, 'lon': 115.2592, 'desc': '유기농'},
    'Jimbaran Bay Seafood (짐바란)': {'lat': -8.7779, 'lon': 115.1676, 'desc': 'BBQ'},
    'Bumbu Bali 1 (누사두아)': {'lat': -8.7958, 'lon': 115.2229, 'desc': '정통요리'},
    'Fat Chow (꾸따)': {'lat': -8.7159, 'lon': 115.1712, 'desc': '퓨전'}
}

safety_locations = {
    '상갈라 병원': {'lat': -8.6695, 'lon': 115.2156, 'desc': '발리 최대 병원'},
    'BIMC 병원 누사두아': {'lat': -8.7932, 'lon': 115.2263, 'desc': '외국인 대상'},
    '주인도네시아 한국대사관': {'lat': -6.2287, 'lon': 106.8286, 'desc': '자카르타 위치'}
}

itinerary = {
    "Day 1": ['스미냑 비치', '짱구 비치'],
    "Day 2": ['우붓 왕궁', '우붓 시장', '몽키 포레스트'],
    "Day 3": ['렘푸양 사원', '띠르따 강가', '뜨갈랄랑'],
    "Day 4": ['울루와뚜 사원', '짐바란 베이'],
    "Day 5": ['꾸따 비치']
}

# ------------------- 사용자 위치 -------------------
user_location = (-8.65, 115.2)

# ------------------- 거리 계산 -------------------
df_restaurants = pd.DataFrame.from_dict(restaurants, orient='index')
df_restaurants['distance_km'] = df_restaurants.apply(
    lambda row: round(geodesic(user_location, (row['lat'], row['lon'])).km, 2), axis=1
)

# ------------------- 탭 구성 -------------------
tabs = st.tabs(list(itinerary.keys()) + [T['restaurant'], T['safety']])

# 지도 생성 함수
def create_map(spots):
    m = folium.Map(location=[-8.65, 115.2], zoom_start=10)

    for spot in spots:
        folium.Marker(
            location=locations[spot],
            tooltip=spot,
            icon=folium.Icon(color='blue', icon='camera-retro', prefix='fa')
        ).add_to(m)

    for name, row in df_restaurants.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"{name}<br>{row['desc']}",
            icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
        ).add_to(m)

    for name, row in safety_locations.items():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"{name}<br>{row['desc']}",
            icon=folium.Icon(color='green', icon='plus-square', prefix='fa')
        ).add_to(m)

    return m

# 일정별 탭
for i, (day, places) in enumerate(itinerary.items()):
    with tabs[i]:
        st.subheader(f"{day} - {T['attractions']}")
        st_folium(create_map(places), width='100%', height=500)

# 맛집 정보 탭
with tabs[-2]:
    st.subheader(T['restaurant'])
    st.dataframe(df_restaurants.sort_values('distance_km')[['desc', 'distance_km']].rename(columns={'desc': '소개', 'distance_km': T['distance']}))

    # 다운로드 버튼 - CSV
    csv = df_restaurants.reset_index().rename(columns={'index': 'Restaurant'}).to_csv(index=False).encode('utf-8')
    st.download_button(T['download_csv'], data=csv, file_name="restaurants.csv", mime='text/csv')

# 병원/대사관 정보 탭
with tabs[-1]:
    st.subheader(T['safety'])
    safety_map = folium.Map(location=[-8.65, 115.2], zoom_start=9)
    for name, info in safety_locations.items():
        folium.Marker(
            location=[info['lat'], info['lon']],
            popup=f"{name}<br>{info['desc']}",
            icon=folium.Icon(color='green', icon='plus-square', prefix='fa')
        ).add_to(safety_map)
    st_folium(safety_map, width='100%', height=500)

# PDF 일정 다운로드
@st.cache_data
def create_pdf(lines):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in lines:
        pdf.cell(200, 10, txt=line, ln=True)
    buffer = io.BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

itinerary_text = []
for day, places in itinerary.items():
    itinerary_text.append(f"{day}:")
    for place in places:
        itinerary_text.append(f" - {place}")

pdf = create_pdf(itinerary_text)
st.download_button(T['download_pdf'], data=pdf, file_name="itinerary.pdf", mime="application/pdf")
