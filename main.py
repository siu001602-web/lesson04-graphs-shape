import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: 세로막대(|) 기호로 나뉜 경우 첫 번째 장르만 선택
    if 'genre' in df.columns:
        df['genre_primary'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    else:
        df['genre_primary'] = '미상'
        
    return df

df = load_data()

# 앱 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 1. 장르별 영화 편수 (도넛 그래프)
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['genre_primary'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# Plotly 도넛 차트 생성
fig1 = px.pie(
    genre_counts,
    names='장르',
    values='편수',
    hole=0.4,
    title="장르별 영화 편수 비율"
)

# 마우스 호버 및 레이아웃 설정 (편수와 비율이 함께 표시됨)
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 주요 개봉 영화들 가운데 어떤 장르가 가장 높은 비중을 차지하고 있는지 한눈에 비교해볼 수 있습니다.")

st.markdown("---")
