import streamlit as st
import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

def encode_file(uploaded_file):
    """Converts any uploaded file into a Base64 string for the AI."""
    if uploaded_file is not None:
        return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
    return None

def call_multimodal_ai(model, system_prompt, user_text, file_b64, file_type):
    """Sends text + media to the AI."""
    # Build the content list
    content = [{"type": "text", "text": user_text}]
    
    if file_b64:
        # OpenRouter supports 'image_url' and 'video_url' types
        media_key = "video_url" if "video" in file_type or "audio" in file_type else "image_url"
        content.append({
            "type": media_key,
            "url": f"data:{file_type};base64,{file_b64}"
        })

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content}
    ]
    
    return client.chat.completions.create(model=model, messages=messages, stream=True)