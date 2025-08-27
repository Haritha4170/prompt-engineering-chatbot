import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError, RateLimitError

# Load environment variables from local .env
load_dotenv()

api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Page config
st.set_page_config(page_title="Prompt Engineering Chatbot", layout="wide")
st.title("🤖 Prompt Engineering Learning Chatbot")
st.write("Explore lessons: Summarize • Transform • Expand • Infer • Chat")

# Sidebar for settings
st.sidebar.header("⚙️ Settings")
model = st.sidebar.text_input("OpenAI model", value="gpt-4o-mini")

# Retry function for OpenAI requests
def safe_openai_request(model, messages, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            with st.spinner("🤖 Thinking... please wait"):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    request_timeout=60
                )
            return response
        except RateLimitError:
            st.warning("⚠️ Rate limit reached. Retrying in 20 seconds...")
            time.sleep(20)
            retries += 1
        except OpenAIError as e:
            st.warning(f"⚠️ OpenAI Error: {e}. Retrying in 10 seconds...")
            time.sleep(10)
            retries += 1

    st.error("❌ Failed after multiple retries. Please try again later.")
    return None

# Tabs for lessons
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Summarize", "Transform", "Expand", "Infer", "Chat"]
)

# --- Summarize ---
with tab1:
    st.subheader("📄 Summarize Text")
    text = st.text_area("Paste text here:", key="summarize")
    style = st.selectbox("Summary style", ["Bullet points", "One line", "Detailed"], key="summarize_style")
    if st.button("Summarize", key="summarize_btn") and text.strip():
        prompt = f"Summarize this text in {style.lower()}:\n{text}"
        response = safe_openai_request(model, [{"role": "user", "content": prompt}])
        if response:
            st.write(response.choices[0].message.content)

# --- Transform ---
with tab2:
    st.subheader("🔄 Transform Text")
    text = st.text_area("Paste text here:", key="transform")
    tone = st.selectbox(
        "Transform to",
        ["Formal", "Casual", "Funny", "Professional", "Translate to Telugu"],
        key="transform_tone"
    )
    if st.button("Transform", key="transform_btn") and text.strip():
        if tone.startswith("Translate"):
            prompt = f"Translate this text into Telugu:\n{text}"
        else:
            prompt = f"Transform this text into a {tone} style:\n{text}"
        response = safe_openai_request(model, [{"role": "user", "content": prompt}])
        if response:
            st.write(response.choices[0].message.content)

# --- Expand ---
with tab3:
    st.subheader("✍️ Expand Text")
    text = st.text_area("Paste text here:", key="expand")
    if st.button("Expand", key="expand_btn") and text.strip():
        prompt = f"Expand this text with more details / make it professional:\n{text}"
        response = safe_openai_request(model, [{"role": "user", "content": prompt}])
        if response:
            st.write(response.choices[0].message.content)

# --- Infer ---
with tab4:
    st.subheader("🔍 Infer Sentiment / Intent")
    text = st.text_area("Paste text here:", key="infer")
    if st.button("Infer", key="infer_btn") and text.strip():
        prompt = f"Analyze this text. Give:\n- Sentiment\n- Topics Mentioned\n- Possible Intent\n\nText: {text}"
        response = safe_openai_request(model, [{"role": "user", "content": prompt}])
        if response:
            st.write(response.choices[0].message.content)

# --- Chat ---
with tab5:
    st.subheader("💬 Chat")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get assistant reply
        response = safe_openai_request(model, st.session_state["messages"])
        if response:
            bot_reply = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(bot_reply)
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
