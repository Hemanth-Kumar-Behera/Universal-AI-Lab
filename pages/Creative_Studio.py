import streamlit as st
import requests
import io
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
OR_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="Creative Studio", layout="wide")
st.title("🎨 AI Creative Studio (Router Config)")

tab1, tab2 = st.tabs(["✨ AI Image Generator", "🌀 Concept Remix"])

# --- TAB 1: NEW HUGGING FACE ROUTER ---
with tab1:
    st.subheader("Visualizer (SDXL via HF Router)")
    
    # NEW 2026 ENDPOINT
    MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
    ROUTER_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
    
    img_input = st.text_input("Describe your vision:", placeholder="e.g. A digital brain in a jar...", key="img_prompt")

    if st.button("🚀 Render High-Def"):
        if img_input and HF_TOKEN:
            with st.spinner("🛰️ Routing through Hugging Face Cluster..."):
                # Standard headers but with the new Router requirements
                headers = {
                    "Authorization": f"Bearer {HF_TOKEN}",
                    "Content-Type": "application/json",
                    "x-use-cache": "false" # Forces a fresh generation
                }
                
                payload = {
                    "inputs": img_input,
                    "parameters": {"target_size": {"width": 1024, "height": 1024}}
                }
                
                try:
                    response = requests.post(ROUTER_URL, headers=headers, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        image = Image.open(io.BytesIO(response.content))
                        st.image(image, use_container_width=True)
                        st.success("Pixels Rendered via Router.")
                    elif response.status_code == 503:
                        st.warning("Model is currently cold-starting. Try again in 15 seconds.")
                    else:
                        st.error(f"Router Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Request Failed: {e}")
        else:
            st.error("Missing Prompt or HF Token.")

# --- TAB 2: REMIX ---
with tab2:
    st.subheader("Concept Remix")
    remix_input = st.text_area("Paste code or text:", height=200, key="remix_txt")
    
    if st.button("🌪️ Start Remix"):
        if remix_input and OR_KEY:
            with st.spinner("Remixing..."):
                headers = {"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"}
                payload = {
                    "model": "google/gemini-2.0-flash-001",
                    "messages": [{"role": "user", "content": f"Turn this into a prompt for SDXL: {remix_input}"}]
                }
                try:
                    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                    st.markdown(f"### 🌀 Visual Prompt:\n{res.json()['choices'][0]['message']['content']}")
                except Exception as e:
                    st.error(f"Remix Failed: {e}")