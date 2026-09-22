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

# 마우스 호버 및 레이아웃 설정
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르: %{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 1 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 주요 개봉 영화들 가운데 어떤 장르가 가장 높은 비중을 차지하고 있는지 한눈에 비교해볼 수 있습니다.")

st.markdown("---")

# 2. 장르 및 영화별 총 관객 수 (트리맵)
st.subheader("2. 장르별 영화 분포 및 총 관객 수 트리맵")

# Plotly 트리맵 차트 생성
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'genre_primary', 'movieNm'],
    values='total_audi',
    color='genre_primary',
    title="장르 및 영화별 총 관객 수 분포"
)

# 마우스 호버 커스텀 설정 (영화명과 총 관객 수 표시)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

fig2.update_layout(
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 2 해석 안내 구역
st.info("💡 **이 그래프로 알 수 있는 것:** 각 장르가 차지하는 전체 관객 규모와 그 장르 내에서 어떤 영화가 총 관객 수를 크게 견인했는지 직관적으로 파악할 수 있습니다.")

st.markdown("---")
