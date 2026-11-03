
import json
import hmac
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="관리자 페이지",
    page_icon="🔐",
    layout="centered"
)

DATA_FILE = Path(__file__).resolve().parent.parent / "breakfast.json"


def load_data():
    if not DATA_FILE.exists():
        return {
            "quantity": 100,
            "updated_at": "아직 업데이트되지 않음"
        }

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    except (json.JSONDecodeError, OSError, KeyError):
        return {
            "quantity": 0,
            "updated_at": "데이터를 읽을 수 없음"
        }


def save_data(quantity):
    data = {
        "quantity": int(quantity),
        "updated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -------------------------
# 관리자 인증
# -------------------------

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


st.title("🔐 관리자 페이지")

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

else:

    st.success("관리자 인증이 완료되었습니다.")

    if st.button("로그아웃"):
        st.session_state.admin_authenticated = False
        st.rerun()

    st.divider()
    st.subheader("잔여 수량 관리")

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
        save_data(quantity)
        st.success("잔여 수량이 저장되었습니다!")
        st.rerun()

    st.divider()
    st.metric("현재 저장된 수량", f"{data['quantity']}식")
    st.caption(f"마지막 업데이트: {data['updated_at']}")
