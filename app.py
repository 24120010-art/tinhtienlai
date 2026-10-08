import streamlit as st
from openai import OpenAI

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Chatbot AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 CHATBOT AI")
st.write("Xin chào! Tôi là trợ lý AI. Bạn có thể hỏi tôi bất cứ điều gì.")

# ==============================
# KẾT NỐI OPENAI
# ==============================
try:
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )
except Exception:
    st.error("⚠️ Chưa cấu hình OPENAI_API_KEY trong Secrets.")
    st.stop()

# ==============================
# KHỞI TẠO LỊCH SỬ CHAT
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào 👋 Mình có thể giúp gì cho bạn?"
        }
    ]

# ==============================
# HIỂN THỊ LỊCH SỬ
# ==============================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================
# Ô NHẬP CÂU HỎI
# ==============================
prompt = st.chat_input("Nhập câu hỏi của bạn...")

if prompt:

    # Hiển thị câu hỏi của người dùng
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi câu hỏi đến AI
    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):

            try:
                response = client.responses.create(
                    model="gpt-5.4-mini",
                    input=st.session_state.messages
                )

                answer = response.output_text

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"❌ Có lỗi xảy ra: {e}")

# ==============================
# NÚT XÓA LỊCH SỬ
# ==============================
if st.button("🗑️ Xóa cuộc trò chuyện"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào 👋 Mình có thể giúp gì cho bạn?"
        }
    ]
    st.rerun()
