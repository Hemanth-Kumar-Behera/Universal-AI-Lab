import streamlit as st
import utils

st.title("📖 Study Buddy (with Memory)")

# 1. Initialize Memory
utils.init_chat_history()

# 2. Sidebar Setup
with st.sidebar:
    # Get models from utils - handles potential API errors internally
    model_list = utils.get_free_models()
    model = st.selectbox("Select Engine", model_list)
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# 3. Define Personality
SYSTEM_PROMPT = """You are an elite Academic Tutor. 
Instead of just giving answers, ask clarifying questions to see what the student knows.
Maintain a supportive, encouraging, yet intellectually rigorous tone."""

# 4. Show History
utils.display_chat()

# 5. Handle New Input
if prompt := st.chat_input("Ask your tutor anything..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        # This calls the updated utils.get_ai_response that merges prompts
        response_stream = utils.get_ai_response(model, SYSTEM_PROMPT)
        
        if response_stream:
            # Word-by-word streaming
            full_response = st.write_stream(response_stream)
            st.session_state.messages.append({"role": "assistant", "content": full_response})