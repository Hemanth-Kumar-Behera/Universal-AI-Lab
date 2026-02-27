import streamlit as st
import requests
import random
import os
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
OR_KEY = os.getenv("OPENROUTER_API_KEY")

# 2. Page Setup (STANDALONE - NO UTILS NEEDED)
st.set_page_config(page_title="Creative Studio", layout="wide")
st.title("🎨 AI Creative Studio")

# Manually handle session state so we don't need utils.py
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. Tabs
tab1, tab2 = st.tabs(["✨ AI Image Generator", "🌀 Concept Remix"])

# --- TAB 1: IMAGE GENERATOR ---
with tab1:
    st.subheader("Visualizer")
    img_input = st.text_input("Describe your vision (e.g., 'A knight in blue fire'):", key="visualizer_input")
    
    if st.button("🚀 Render Image"):
        if img_input:
            with st.spinner("Drawing..."):
                seed = random.randint(1, 999999)
                clean_prompt = img_input.replace(" ", "%20")
                # Direct link to the public GPU cluster (Free/No Key)
                gen_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
                
                # Show the image directly
                st.image(gen_url, caption=f"Result for: {img_input}", use_container_width=True)
                st.success("Pixels generated!")
        else:
            st.warning("Enter a prompt first.")

# --- TAB 2: CONCEPT REMIX ---
with tab2:
    st.subheader("Concept Remix")
    remix_input = st.text_area("Paste code or concept here:", height=150, key="remix_area")
    
    if st.button("🌪️ Start Remix"):
        if remix_input and OR_KEY:
            with st.spinner("Remixing..."):
                headers = {
                    "Authorization": f"Bearer {OR_KEY}",
                    "Content-Type": "application/json"
                }
                
                # Using the standard 'messages' format to avoid the 400 Sync Error
                payload = {
                    "model": "google/gemini-2.0-flash-001",
                    "messages": [
                        {"role": "user", "content": f"Remix this into a poetic visual description: {remix_input}"}
                    ]
                }
                
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    result = response.json()
                    
                    if response.status_code == 200:
                        remix_text = result['choices'][0]['message']['content']
                        st.markdown("### 🌀 Your Remixed Concept:")
                        st.write(remix_text)
                    else:
                        st.error(f"API Error: {result.get('error', {}).get('message', 'Check credits')}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        elif not OR_KEY:
            st.error("Missing OPENROUTER_API_KEY in your .env file!")
        else:
            st.warning("Paste something to remix first.")
import streamlit as st

def init_chat_history():
    """Initializes chat memory across all pages."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def get_free_models():
    """Provides a consistent list of available AI models."""
    return [
        "google/gemini-2.0-flash-001",
        "deepseek/deepseek-r1:free",
        "anthropic/claude-3-haiku:free"
    ]

def display_chat():
    """Standardizes the chat UI for Study Buddy and Career Coach."""
    if "chat_history" in st.session_state:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

def clear_chat():
    """Allows users to wipe memory."""
    st.session_state.chat_history = []
    st.rerun()

    import streamlit as st
from docx import Document
import PyPDF2
import io

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def read_document(uploaded_file):
    """Reads text from PDF or DOCX files."""
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text
import os
import streamlit as st
from openai import OpenAI

def get_ai_response(model_name, system_prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # We set stream=True and return the generator directly
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages 
        ],
        stream=True  # This is the key change!
    )
    
    # Create a generator that yields text chunks
    def stream_generator():
        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'content'):
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    
    return stream_generator()

import re
import json

def extract_logic_frames(text):
    """Extracts JSON frames from the assistant's response."""
    try:
        # Look for content between [LOGIC_START] and [LOGIC_END]
        pattern = r"\[LOGIC_START\](.*?)\[LOGIC_END\]"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        return None
    return None