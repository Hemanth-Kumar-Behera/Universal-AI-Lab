import streamlit as st
import requests
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Clients ---
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def transcribe_audio(file_obj):
    """
    Handles both MP3 and WAV by detecting the file's Mime-Type 
    and sending raw bytes to the HF Router.
    """
    API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
    
    # 1. Get the bytes and the specific type (audio/mpeg or audio/wav)
    audio_data = file_obj.getvalue()
    mime_type = file_obj.type 
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": mime_type 
    }
    
    for attempt in range(3):
        try:
            response = requests.post(API_URL, headers=headers, data=audio_data)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("text", "Transcription empty.")
            
            elif response.status_code == 503:
                st.warning(f"🕒 Engine warming up... attempt {attempt+1}/3")
                time.sleep(15)
                continue
            else:
                return f"❌ Router Error {response.status_code}: {response.text[:100]}"
                
        except Exception as e:
            return f"❌ Connection Error: {str(e)}"
            
    return "❌ Failed after multiple attempts."

st.title("🎙️ Lecture Note Architect")

# --- Session State ---
if "lecture_chat" not in st.session_state:
    st.session_state.lecture_chat = []
if "transcription" not in st.session_state:
    st.session_state.transcription = ""

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("AI Brain", ["google/gemini-2.0-flash-exp:free", "deepseek/deepseek-r1:free"])
    if st.button("🗑️ Reset Session"):
        st.session_state.lecture_chat = []
        st.session_state.transcription = ""
        st.rerun()

# --- File Upload ---
uploaded_file = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"])

# Check if we have a file and it hasn't been processed yet
if uploaded_file and not st.session_state.transcription:
    with st.spinner("👂 Hearing your lecture..."):
        # We pass the WHOLE object so the function can grab .type and .getvalue()
        result = transcribe_audio(uploaded_file)
        
        if "❌" not in str(result):
            st.session_state.transcription = result
            st.success("Lecture Processed!")
        else:
            st.error(result)

# --- Display & Interaction ---
if st.session_state.transcription:
    with st.expander("📝 View Transcription"):
        st.write(st.session_state.transcription)

    for msg in st.session_state.lecture_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me about the lecture..."):
        st.session_state.lecture_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_context = f"TRANSCRIPTION: {st.session_state.transcription}\n\nUSER: {prompt}"
            stream = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "system", "content": "You are a university scribe."},
                          {"role": "user", "content": full_context}],
                stream=True
            )
            response = st.write_stream(stream)
            st.session_state.lecture_chat.append({"role": "assistant", "content": response})