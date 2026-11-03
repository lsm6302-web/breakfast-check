import hmac
from datetime import datetime, timezone

import streamlit as st
from supabase import create_client, Client

st.set_page_config(
    page_title="관리자 페이지",
    page_icon="🔐",
    layout="centered"
)


# 관리자용 Supabase 연결
@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SECRET_KEY"]
    )


# 현재 수량 불러오기
def load_data():
    supabase = get_supabase()

    response = (
        supabase.table("breakfast")
        .select("quantity, updated_at")
        .eq("id", 1)
        .single()
        .execute()
    )

    return response.data


# 수량 저장하기
def save_data(quantity):
    supabase = get_supabase()

    data = {
        "id": 1,
        "quantity": int(quantity),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    response = (
        supabase.table("breakfast")
        .upsert(data)
        .execute()
    )

    return response.data


# -------------------------
# 관리자 인증
# -------------------------

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


st.title("🔐 관리자 페이지")


# 로그인하지 않은 경우
if not st.session_state.admin_authenticated:

    st.write("수량을 관리하려면 비밀번호를 입력하세요.")

    with st.form("admin_login"):

        password = st.text_input(
            "관리자 비밀번호",
            type="password"
        )

        login_clicked = st.form_submit_button(
            "로그인",
            type="primary",
            use_container_width=True
        )

    if login_clicked:

        try:
            correct_password = st.secrets["ADMIN_PASSWORD"]

            if hmac.compare_digest(
                password,
                correct_password
            ):
                st.session_state.admin_authenticated = True
                st.rerun()

            else:
                st.error("비밀번호가 올바르지 않습니다.")

        except (KeyError, FileNotFoundError):
            st.error(
                "비밀번호 설정을 찾을 수 없습니다. "
                ".streamlit/secrets.toml 파일을 확인하세요."
            )


# 로그인한 경우
else:

    st.success("관리자 인증이 완료되었습니다.")

    if st.button("로그아웃"):
        st.session_state.admin_authenticated = False
        st.rerun()

    st.divider()
    st.subheader("잔여 수량 관리")

    try:
        data = load_data()

        with st.form("quantity_form"):

            quantity = st.number_input(
                "현재 잔여 수량 (식)",
                min_value=0,
                max_value=10000,
                value=int(data["quantity"]),
                step=1
            )

            submitted = st.form_submit_button(
                "수량 저장",
                type="primary",
                use_container_width=True
            )

        if submitted:

            try:
                save_data(quantity)

                st.success("잔여 수량이 저장되었습니다!")
                st.rerun()

            except Exception as e:
                st.error(f"수량 저장에 실패했습니다: {e}")

        st.divider()

        st.metric(
            "현재 저장된 수량",
            f"{data['quantity']}식"
        )

        st.caption(
            f"마지막 업데이트: {data['updated_at']}"
        )

    except Exception as e:

        st.error(
            f"Supabase에서 데이터를 불러오지 못했습니다: {e}"
        )
