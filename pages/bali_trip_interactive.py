import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 페이지 설정 ---
st.set_page_config(
    page_title="발리 인터랙티브 여행 코스",
    page_icon="🗺️",
    layout="wide",
)

# --- 제목 및 설명 ---
st.title('7월 말, 발리 인터랙티브 여행 코스')
st.write("""
지도 위의 마커를 클릭할 수 있도록 개선했습니다.
지도 위의  관광지(파란색)와 맛집(빨간색) 아이콘을 클릭하여 상세 정보를 확인해 보세요!
""")

# --- 여행지 및 맛집 데이터 ---
# 관광지 데이터 (위도, 경도)
locations = {
    '스미냑 비치': [-8.6917, 115.1583], '짱구 비치': [-8.6593, 115.1385],
    '우붓 왕궁': [-8.5069, 115.2624], '우붓 시장': [-8.5076, 115.2622],
    '몽키 포레스트': [-8.5193, 115.2592], '렘푸양 사원': [-8.3902, 115.6321],
    '띠르따 강가': [-8.4120, 115.5902], '뜨갈랄랑': [-8.4312, 115.2779],
    '울루와뚜 사원': [-8.8291, 115.0849], '짐바란 베이': [-8.7844, 115.1637],
    '꾸따 비치': [-8.7186, 115.1685]
}
df_locations = pd.DataFrame.from_dict(locations, orient='index', columns=['lat', 'lon'])

# 맛집 데이터 (위도, 경도, 설명)
restaurants = {
    'The Shady Shack (짱구)': {'lat': -8.6635, 'lon': 115.1363, 'desc': '건강한 채식/비건 메뉴'},
    'La Favela (스미냑)': {'lat': -8.6800, 'lon': 115.1561, 'desc': '독특한 인테리어의 바 & 레스토랑'},
    "Naughty Nuri's Warung (우붓)": {'lat': -8.4975, 'lon': 115.2559, 'desc': '인생 폭립을 맛볼 수 있는 곳'},
    'Warung Babi Guling Ibu Oka (우붓)': {'lat': -8.5064, 'lon': 115.2621, 'desc': '발리 전통 새끼돼지 통구이'},
    'Sari Organik (우붓)': {'lat': -8.4950, 'lon': 115.2592, 'desc': '논밭 뷰의 유기농 레스토랑'},
    'Jimbaran Bay Seafood (짐바란)': {'lat': -8.7779, 'lon': 115.1676, 'desc': '해변에서의 로맨틱한 해산물 BBQ'},
    'Bumbu Bali 1 (누사두아)': {'lat': -8.7958, 'lon': 115.2229, 'desc': '정통 발리 요리 전문점'},
    'Fat Chow (꾸따)': {'lat': -8.7159, 'lon': 115.1712, 'desc': '맛있는 아시안 퓨전 요리'}
}
df_restaurants = pd.DataFrame.from_dict(restaurants, orient='index', columns=['lat', 'lon', 'desc'])


# --- 화면 구성 ---
tab1, tab2, tab3 = st.tabs(["🗺️ 인터랙티브 지도", "🗓️ 세부 추천 일정", "🍽️ 추천 맛집 리스트"])

with tab1:
    st.header("📍 한눈에 보는 발리 추천 코스")

    # 1. Folium 지도 생성 (발리 중심 좌표)
    m = folium.Map(location=[-8.65, 115.20], zoom_start=10)

    # 2. 관광지 마커 추가 (파란색)
    for index, row in df_locations.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<strong>{index}</strong>",  # 클릭 시 나타나는 팝업 (굵은 글씨)
            tooltip=index,  # 마우스 올렸을 때 보이는 툴팁
            icon=folium.Icon(color='blue', icon='camera-retro', prefix='fa')
        ).add_to(m)

    # 3. 맛집 마커 추가 (빨간색)
    for index, row in df_restaurants.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"<strong>{index}</strong><br>{row['desc']}",
            tooltip=index,
            icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
        ).add_to(m)

    # 4. Streamlit에 Folium 지도 출력
    st_folium(m, width= '100%', height=500)


with tab2:
    st.header("🗓️ 4박 5일 세부 추천 일정")
    # (이전 코드와 동일한 내용)
    with st.expander("**Day 1: 스미냑/짱구 - 활기찬 해변과 트렌디한 감성**", expanded=True):
        st.markdown("- **오후**: 공항 도착 후, 스미냑/짱구 숙소로 이동\n- **저녁**: 해변 레스토랑이나 비치 클럽에서 서핑과 함께 활기찬 분위기 만끽\n- **주요 스팟**: 스미냑 비치, 짱구 비치, 포테이토 헤드 비치 클럽")
    with st.expander("**Day 2: 우붓 - 발리의 예술과 영혼을 만나다**"):
        st.markdown("- **오전**: 문화 중심지 우붓으로 이동\n- **오후**: 우붓 왕궁, 우붓 시장, 몽키 포레스트 방문\n- **주요 스팟**: 우붓 왕궁, 우붓 시장, 몽키 포레스트")
    with st.expander("**Day 3: 우붓 근교 - 인생 사진과 함께하는 자연 탐험**"):
        st.markdown("- **오전**: '천국의 문' 렘푸양 사원 방문 (일찍 출발 추천)\n- **오후**: '물의 궁전' 띠르따 강가 산책 후 뜨갈랄랑 계단식 논 방문\n- **주요 스팟**: 렘푸양 사원, 띠르따 강가, 뜨갈랄랑")
    with st.expander("**Day 4: 울루와뚜/짐바란 - 장엄한 절벽과 로맨틱한 일몰**"):
        st.markdown("- **오후**: 울루와뚜 절벽 사원에서 인도양 절경 감상\n- **저녁**: 케착 파이어 댄스 관람 후 짐바란 해변에서 해산물 디너\n- **주요 스팟**: 울루와뚜 사원, 짐바란 베이")
    with st.expander("**Day 5: 출국 - 마지막 여운 즐기기**"):
        st.markdown("- **오전**: 꾸따 비치 또는 스미냑에서 마지막 쇼핑\n- **오후**: 공항으로 이동하여 출국\n- **주요 스팟**: 꾸따 비치, 비치워크 쇼핑센터")


with tab3:
    st.header("🍽️ 지역별 추천 맛집")
    st.write("여행 코스에 맞춰 방문하기 좋은 검증된 맛집 리스트입니다.")
    st.subheader("🌴 스미냑 / 짱구")
    st.text("La Favela: 신비로운 정글 컨셉의 인테리어가 인상적인 곳")
    st.text("The Shady Shack: 건강하고 맛있는 채식 요리를 즐길 수 있는 곳")
    st.subheader("🌳 우붓")
    st.text("Naughty Nuri's Warung: 부드러운 폭립과 특제 소스의 환상적인 조화")
    st.text("Warung Babi Guling Ibu Oka: 발리 전통 음식 '바비굴링'의 정석")
    st.text("Sari Organik: 아름다운 논밭을 바라보며 즐기는 힐링 푸드")
    st.subheader("🌊 짐바란 / 울루와뚜")
    st.text("Jimbaran Bay Seafood: 해변의 노을을 보며 즐기는 낭만적인 해산물 BBQ")
    st.text("Bumbu Bali 1: 인도네시아의 다양한 향신료를 경험할 수 있는 정통 발리 요리")
    st.subheader("☀️ 꾸따")
    st.text("Fat Chow: 다양한 아시안 퓨전 음식을 맛볼 수 있는 트렌디한 맛집")

st.info("💡 **여행 Tip**: 발리 내에서 지역 간 이동은 '그랩(Grab)'이나 '고젝(Gojek)' 같은 차량 호출 앱을 이용하면 편리합니다. 또는 전일 차량을 대절하여 원하는 코스대로 자유롭게 여행하는 것도 좋은 방법입니다.")
