import streamlit as st
import requests

API_URL = "https://friskily-spiriferous-irene.ngrok-free.dev"

st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🏥",
    layout="centered"
)

# --- UI Styling ---
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stApp { max-width: 800px; margin: auto; }

    .chat-bubble-user {
        background: #2563eb;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    .chat-bubble-bot {
        background: white;
        color: #1e293b;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        border: 1px solid #e2e8f0;
    }
    .header-box {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="header-box">
    <h1>🏥 Medical Chatbot</h1>
    <p>Powered by LLaMA 3 · Running on Colab</p>
</div>
""", unsafe_allow_html=True)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- Display Messages ---
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# --- Input ---
question = st.chat_input("Ask a medical question...")

if question:
    st.session_state["messages"].append({"role": "user", "content": question})

    with st.spinner("🤔 Thinking..."):
        try:
            res = requests.post(
                f"{API_URL}/chat",
                json={"question": question},
                timeout=60
            )

            if res.status_code == 200:
                answer = res.json().get("answer", "No answer received.")
            else:
                answer = f"❌ Server error: {res.status_code}"

        except Exception as e:
            answer = f"❌ Error: {str(e)}"

    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.rerun()

# --- Clear button ---
if st.button("🗑️ Clear Chat"):
    st.session_state["messages"] = []
    st.rerun()