import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown("---")

# 1. 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    # genre: 세로막대 기호(|)로 분리된 여러 장르 중 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    # 수치형 데이터 변환 (혹시 문자열로 들어온 경우 대비)
    numeric_cols = ['first_scrn', 'first_show', 'first_week_audi', 'total_audi', 'days_in_top10']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# ==========================================
# 그래프 1: 장르별 영화 편수 (도넛 차트)
# ==========================================
st.subheader("1. 장르별 영화 편수")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig1 = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 편수 분포",
    labels={'genre': '장르', 'count': '영화 편수'}
)

# 마우스 호버 시 편수와 비율 표시 (label, value, percent)
fig1.update_traces(
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("특정 장르에 영화 개봉 편수가 쏠려 있는지, 전체 시장에서 각 장르가 차지하는 작품 수 비중을 한눈에 확인할 수 있습니다.")

st.markdown("---")

# ==========================================
# 그래프 2: 장르 및 영화별 총 관객 수 (트리맵)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객 수 (트리맵)")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    title="장르 및 영화별 총 관객 수 분포",
    color='genre',
    color_discrete_sequence=px.colors.qualitative.Set3
)

# 마우스 호버 시 영화명과 총 관객 수 표시
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info("각 장르의 전체 흥행 규모와 함께 장르 내에서 어떤 영화가 총 관객 수의 대부분을 차지하고 있는지 계층적으로 비교할 수 있습니다.")

st.markdown("---")

# ==========================================
# 그래프 3: 총 관객 수 분포 (히스토그램)
# ==========================================
st.subheader("3. 총 관객 수 분포 (히스토그램)")

fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=20,
    title="총 관객 수 히스토그램",
    labels={'total_audi': '총 관객 수'},
    color_discrete_sequence=['#1f77b4']
)

fig3.update_traces(
    hovertemplate="<b>관객 수 구간:</b> %{x}<br><b>영화 수:</b> %{y}편<extra></extra>"
)

fig3.update_layout(
    xaxis_title="총 관객 수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1
)

st.plotly_chart(fig3, use_container_width=True)

# 자동 분석 문구 계산
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 대부분의 영화가 몰려있는 구간 (0 ~ 100만 명 미만 등)
under_1M_count = len(df[df['total_audi'] < 1000000])
percent_under_1M = (under_1M_count / len(df)) * 100

st.markdown("##### 💡 이 그래프로 알 수 있는 것")
st.info(
    f"전체 {len(df)}편 중 대다수의 영화({under_1M_count}편, 약 {percent_under_1M:.1f}%)가 **총 관객 수 100만 명 미만 구간**에 몰려 있어 "
    f"흥행 쏠림 현상이 큼을 알 수 있으며, 가장 많은 관객을 동원한 영화는 **'{top_movie_name}'** (총 관객 수: {top_movie_audi:,.0f}명)입니다."
)

st.markdown("---")
