import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="발리 인터랙티브 여행 가이드",
    page_icon="🌴",
    layout="wide"
)

st.title("7월 말, 발리 인터랙티브 여행 가이드")
st.write("아래 일정별 지도를 클릭해서 세부 위치를 확인하고, 병원/응급상황 대비 정보도 참고하세요!")

# 관광지 데이터
locations = {
    '스미냑 비치': [-8.6917, 115.1583], '짱구 비치': [-8.6593, 115.1385],
    '우붓 왕궁': [-8.5069, 115.2624], '우붓 시장': [-8.5076, 115.2622],
    '몽키 포레스트': [-8.5193, 115.2592], '렘푸양 사원': [-8.3902, 115.6321],
    '띠르따 강가': [-8.4120, 115.5902], '뜨갈랄랑': [-8.4312, 115.2779],
    '울루와뚜 사원': [-8.8291, 115.0849], '짐바란 베이': [-8.7844, 115.1637],
    '꾸따 비치': [-8.7186, 115.1685]
}
df_locations = pd.DataFrame.from_dict(locations, orient='index', columns=['lat', 'lon'])

# 맛집 데이터
restaurants = {
    'The Shady Shack (짱구)': {'lat': -8.6635, 'lon': 115.1363, 'desc': '건강한 채식/비건 메뉴'},
    'La Favela (스미냑)': {'lat': -8.6800, 'lon': 115.1561, 'desc': '독특한 인테리어의 바 & 레스토랑'},
    "Naughty Nuri's Warung (우붓)": {'lat': -8.4975, 'lon': 115.2559, 'desc': '인생 폭립'},
    'Warung Babi Guling Ibu Oka (우붓)': {'lat': -8.5064, 'lon': 115.2621, 'desc': '바비굴링의 정석'},
    'Sari Organik (우붓)': {'lat': -8.4950, 'lon': 115.2592, 'desc': '논밭 뷰의 유기농 식당'},
    'Jimbaran Bay Seafood (짐바란)': {'lat': -8.7779, 'lon': 115.1676, 'desc': '해변 해산물 BBQ'},
    'Bumbu Bali 1 (누사두아)': {'lat': -8.7958, 'lon': 115.2229, 'desc': '정통 발리 요리'},
    'Fat Chow (꾸따)': {'lat': -8.7159, 'lon': 115.1712, 'desc': '아시안 퓨전 요리'}
}
df_restaurants = pd.DataFrame.from_dict(restaurants, orient='index')

# 병원/응급시설/대사관 정보
safety_locations = {
    '상갈라 병원 (Sanglah Hospital)': {'lat': -8.6695, 'lon': 115.2156, 'desc': '발리 최대의 종합병원'},
    'BIMC 병원 누사두아': {'lat': -8.7932, 'lon': 115.2263, 'desc': '외국인 대상 프리미엄 병원'},
    '대한민국 대사관 (주인도네시아)': {'lat': -6.2287, 'lon': 106.8286, 'desc': '자카르타 소재, 비상시 연락처 확보'}
}
df_safety = pd.DataFrame.from_dict(safety_locations, orient='index')

# 일정별 관광지 매핑
itinerary = {
    "Day 1: 스미냑/짱구": ['스미냑 비치', '짱구 비치'],
    "Day 2: 우붓 중심": ['우붓 왕궁', '우붓 시장', '몽키 포레스트'],
    "Day 3: 우붓 근교": ['렘푸양 사원', '띠르따 강가', '뜨갈랄랑'],
    "Day 4: 울루와뚜/짐바란": ['울루와뚜 사원', '짐바란 베이'],
    "Day 5: 꾸따/귀국": ['꾸따 비치']
}

# 지도 그리기 함수
def create_map(day_key):
    m = folium.Map(location=[-8.65, 115.2], zoom_start=10)

    # 해당 일정 관광지
    for loc in itinerary[day_key]:
        lat, lon = locations[loc]
        folium.Marker(
            location=[lat, lon],
            popup=f"<strong>{loc}</strong>",
            tooltip=loc,
            icon=folium.Icon(color='blue', icon='camera-retro', prefix='fa')
        ).add_to(m)

    # 해당 지역 맛집 (근처만 필터링 없이 전체 표시)
    for index, row in df_restaurants.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<strong>{index}</strong><br>{row['desc']}",
            tooltip=index,
            icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
        ).add_to(m)

    # 병원 및 대사관
    for index, row in df_safety.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<strong>{index}</strong><br>{row['desc']}",
            tooltip=index,
            icon=folium.Icon(color='green', icon='plus-square', prefix='fa')
        ).add_to(m)

    return m

# 각 Day 별 탭 구성
tabs = st.tabs(list(itinerary.keys()) + ["🏥 병원/대사관 위치"])

for i, day in enumerate(itinerary.keys()):
    with tabs[i]:
        st.subheader(f"📍 {day} 추천 코스")
        map_obj = create_map(day)
        st_folium(map_obj, width='100%', height=500)

# 병원/대사관만 별도 탭에 표시
with tabs[-1]:
    st.subheader("🏥 주요 병원 및 대사관 위치")
    m_safety = folium.Map(location=[-8.69, 115.2], zoom_start=9)

    for index, row in df_safety.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<strong>{index}</strong><br>{row['desc']}",
            tooltip=index,
            icon=folium.Icon(color='green', icon='plus-square', prefix='fa')
        ).add_to(m_safety)

    st_folium(m_safety, width='100%', height=500)

# 여행 팁
st.info("💡 **여행 Tip**: '그랩(Grab)' 또는 '고젝(Gojek)' 앱을 활용해 편리하게 지역 간 이동하세요. 병원/대사관 정보는 만일의 경우를 대비해 미리 저장해두면 좋습니다.")
