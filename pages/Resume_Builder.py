import streamlit as st
import utils
from openai import OpenAI
import os

# Setup
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
utils.init_chat_history()

st.title("📄 Career Coach & Resume Expert")

# --- FILE UPLOAD SECTION ---
with st.sidebar:
    st.header("📤 Upload Resume/JD")
    uploaded_file = st.file_uploader("Upload PDF or Word Doc", type=["pdf", "docx"])
    
    if uploaded_file:
        with st.spinner("Reading document..."):
            doc_text = utils.read_document(uploaded_file)
            st.session_state.current_resume_text = doc_text
            st.success("Document Analyzed!")

# --- CHAT INTERFACE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask for advice or to rewrite a section..."):
    # Add context from uploaded file if it exists
    context = st.session_state.get("current_resume_text", "No resume uploaded yet.")
    full_prompt = f"Resume Content:\n{context}\n\nUser Request: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are an expert Career Coach. Use the provided resume context to give specific, high-impact advice."},
                {"role": "user", "content": full_prompt}
            ]
        )
        answer = response.choices[0].message.content
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})