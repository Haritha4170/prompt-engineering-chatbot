import streamlit as st
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# -----------------------------
# Initialize Hugging Face model
# -----------------------------
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-small"  # smaller, fast, CPU-friendly
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)

generator = load_model()

# Helper function for generation
def generate_text(prompt, max_tokens=150):
    result = generator(prompt, max_length=max_tokens, do_sample=True, temperature=0.7)
    return result[0]["generated_text"]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Prompt Engineering Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Prompt Engineering Chatbot (Hugging Face)")
st.caption("Summarize • Transform • Expand • Chat — Fully Local, No API keys required")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": "You are a helpful, concise assistant."}]

tabs = st.tabs(["📝 Summarize", "🎨 Transform", "✉️ Expand Email", "💬 Chat"])

# ---------------- Summarize ----------------
with tabs[0]:
    st.subheader("📝 Summarize Text")
    text = st.text_area("Paste the text to summarize:", height=220)
    style = st.selectbox("Summary style", ["3 bullet points", "Short paragraph", "Key insights + action items"])
    if st.button("Summarize"):
        if not text.strip():
            st.warning("Please paste some text to summarize.")
        else:
            style_prompt = {
                "3 bullet points": "Return exactly 3 concise bullet points.",
                "Short paragraph": "Return a concise paragraph (3–5 sentences).",
                "Key insights + action items": "Return two sections: 'Key Insights' and 'Action Items' in short bullets."
            }
            prompt = f"summarize: {text} \nStyle: {style_prompt[style]}"
            summary = generate_text(prompt, max_tokens=150)
            st.success("Summary")
            st.write(summary)

# ---------------- Transform ----------------
with tabs[1]:
    st.subheader("🎨 Transform Text (Grammar, Tone, Formatting)")
    t_text = st.text_area("Paste text to transform:", height=220)
    tone = st.selectbox("Tone", ["neutral", "formal", "friendly", "polite", "confident", "enthusiastic"])
    formatting = st.selectbox("Formatting", ["plain text", "bulleted list", "numbered steps", "email-ready"])
    grammar_fix = st.checkbox("Fix grammar & clarity", value=True)
    if st.button("Transform"):
        if not t_text.strip():
            st.warning("Please paste some text to transform.")
        else:
            rules = []
            if grammar_fix: rules.append("Fix grammar, punctuation, and clarity.")
            rules.append(f"Use a {tone} tone.")
            if formatting == "bulleted list":
                rules.append("Return as concise bullets.")
            elif formatting == "numbered steps":
                rules.append("Return as numbered steps.")
            elif formatting == "email-ready":
                rules.append("Return as a complete email with greeting and sign-off.")
            else:
                rules.append("Return as plain text.")

            prompt = f"Transform the following text:\n{text}\nRules:\n- " + "\n- ".join(rules)
            transformed = generate_text(prompt, max_tokens=200)
            st.success("Transformed Output")
            st.write(transformed)

# ---------------- Expand Email ----------------
with tabs[2]:
    st.subheader("✉️ Expand Short Email into Detailed, Professional Email")
    brief = st.text_area("Short email / points:", height=180)
    audience = st.text_input("Recipient", value="")
    objective = st.text_input("Goal", value="")
    extras = st.text_area("Optional extras", height=100, value="")
    if st.button("Expand Email"):
        if not brief.strip():
            st.warning("Please add at least a brief or bullet points.")
        else:
            prompt = (
                f"Expand into a professional email:\nRecipient: {audience or 'N/A'}\n"
                f"Goal: {objective or 'N/A'}\nExtras: {extras or 'N/A'}\nNotes:\n{brief}\n"
                "Requirements: Add a subject line, use polite tone, include clear call-to-action."
            )
            expanded = generate_text(prompt, max_tokens=250)
            st.success("Expanded Email")
            st.write(expanded)

# ---------------- Chat ----------------
with tabs[3]:
    st.subheader("💬 General Chat (with Memory)")
    chat_input = st.chat_input("Type your message and press Enter")

    # Display history
    for msg in st.session_state.chat_history:
        if msg["role"] != "system":
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.write(msg["content"])

    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        reply = generate_text(chat_input, max_tokens=150)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

    if st.button("Clear Chat History"):
        st.session_state.chat_history = [{"role": "system", "content": "You are a helpful, concise assistant."}]
        st.success("Chat history cleared.")
