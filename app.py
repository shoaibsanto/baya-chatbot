import streamlit as st
from openai import OpenAI

# --- Load OpenRouter API Key from secrets ---
api_key = st.secrets["OPENROUTER_API_KEY"]
site_url = st.secrets["YOUR_SITE_URL"]
site_name = st.secrets["YOUR_SITE_NAME"]

# --- Initialize OpenRouter Client ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# --- Streamlit Page Config ---
st.set_page_config(page_title="OpenRouter Chat", page_icon="🤖")

st.title("🤖 BAYA Chatbot")

# --- Session State to Store Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Previous Messages ---
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# --- User Input ---
user_prompt = st.chat_input("Say something...")

if user_prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Bot is thinking...
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": site_url,
                    "X-Title": site_name,
                },
                extra_body={},
                model="deepseek/deepseek-r1:free",
                messages=st.session_state.messages  # send entire chat history!
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)

    # Save bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
