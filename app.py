import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="천원의 아침밥",
    page_icon="🍚",
    layout="centered"
)

# Supabase 연결
@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


def load_data():
    supabase = get_supabase()

    response = (
        supabase.table("breakfast")
        .select("quantity, updated_at")
        .eq("id", 1)
        .single()
        .execute()
    )

    data = response.data

    return {
        "quantity": max(0, int(data["quantity"])),
        "updated_at": str(
            data.get("updated_at", "기록 없음")
        )
    }


# 화면 디자인
st.markdown("""
<style>
    .stApp {
        background-color: #F7F8F3;
    }

    .block-container {
        max-width: 760px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(135deg, #245C43, #43815C);
        padding: 35px 28px;
        border-radius: 24px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(36, 92, 67, 0.14);
    }

    .hero-label {
        font-size: 14px;
        letter-spacing: 2px;
        opacity: 0.85;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        line-height: 1.35;
        margin-bottom: 10px;
    }

    .hero-description {
        font-size: 16px;
        opacity: 0.92;
    }

    .count-card {
        background: white;
        border: 1px solid #E6E9E1;
        border-radius: 24px;
        padding: 30px 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.04);
        margin: 18px 0;
    }

    .count-label {
        color: #66736A;
        font-size: 17px;
        font-weight: 600;
    }

    .count-number {
        font-size: 68px;
        font-weight: 800;
        line-height: 1.4;
        margin: 8px 0;
    }

    .count-unit {
        font-size: 23px;
        font-weight: 600;
    }

    .status {
        display: inline-block;
        border-radius: 30px;
        padding: 9px 17px;
        font-size: 15px;
        font-weight: 700;
        margin-top: 8px;
    }

    .status-good {
        background: #E4F4E8;
        color: #267343;
    }

    .status-low {
        background: #FFF0D5;
        color: #946200;
    }

    .status-none {
        background: #FCE7E7;
        color: #B42318;
    }

    .info-card {
        background: #EEF2E9;
        border-radius: 16px;
        padding: 18px 20px;
        color: #4B5B4F;
        font-size: 14px;
        line-height: 1.8;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #879087;
        font-size: 12px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)


# 상단 소개
st.markdown("""
<div class="hero">
    <div class="hero-label">CAMPUS BREAKFAST</div>
    <div class="hero-title">🍚 천원의 아침밥</div>
    <div class="hero-description">
        든든한 하루의 시작, 잔여 수량을 미리 확인하세요.
    </div>
</div>
""", unsafe_allow_html=True)


# 잔여 수량 표시
@st.fragment(run_every="2s")
def student_page():

    try:
        data = load_data()
        quantity = data["quantity"]

    except Exception:
        st.error(
            "잔여 수량을 불러오지 못했습니다. "
            "잠시 후 다시 확인해 주세요."
        )
        return

    # 수량에 따라 숫자 색상과 안내 문구 설정
    if quantity <= 5:
        number_color = "#DC2626"
        status_class = "status-none"

        if quantity == 0:
            status_text = "현재 잔여 수량이 없습니다"
        else:
            status_text = "잔여 수량이 얼마 남지 않았어요!"

    elif quantity <= 10:
        number_color = "#EA8500"
        status_class = "status-low"
        status_text = "잔여 수량이 얼마 남지 않았어요!"

    else:
        number_color = "#245C43"
        status_class = "status-good"
        status_text = "아직 이용할 수 있어요!"

    # 수량 카드
    st.markdown(f"""
    <div class="count-card">
        <div class="count-label">현재 잔여 수량</div>
        <div class="count-number" style="color: {number_color};">
            {quantity}<span class="count-unit">식</span>
        </div>
        <div class="status {status_class}">
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 마지막 업데이트 정보
    st.markdown(f"""
    <div class="info-card">
        🕒 <b>마지막 업데이트</b><br>
        {data["updated_at"]}<br><br>
        💡 잔여 수량은 실제 현장 상황과 차이가 있을 수 있습니다.
    </div>
    """, unsafe_allow_html=True)


student_page()


# 하단 안내
st.markdown("""
<div class="footer">
    CAMPUS BREAKFAST · 학생용 잔여 수량 안내
</div>
""", unsafe_allow_html=True)

        
