import streamlit as st
import utils
import base64

st.set_page_config(page_title="Architect AI", layout="wide", page_icon="💻")
st.title("💻 Universal Logic Architect")

utils.init_chat_history()

# --- 1. SYSTEM PROMPT (The Core Intelligence) ---
SYSTEM_PROMPT = """You are a Senior Software Architect. 
For any logic explained, you MUST provide a JSON block at the end of your response 
wrapped in [LOGIC_START] and [LOGIC_END]. 

The JSON must be a list of frames:
[
  {"step": 1, "desc": "Short description", "code": "line_of_code", "vars": {"var_name": "value"}, "visual": "ascii_art_representation"}
]
"""

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Coding Engine", utils.get_free_models())
    uploaded_file = st.file_uploader("📸 Upload UI or Diagram", type=['png', 'jpg', 'jpeg'])

# --- 3. TABS ---
chat_tab, flow_tab = st.tabs(["💬 Chat", "🎬 Step-by-Step Execution"])

with chat_tab:
    utils.display_chat()

with flow_tab:
    if "logic_frames" in st.session_state and st.session_state.logic_frames:
        frames = st.session_state.logic_frames
        
        # The Playback Slider
        current_idx = st.slider("Scrub Execution Steps", 1, len(frames), 1) - 1
        frame = frames[current_idx]
        
        st.subheader(f"Step {frame['step']}: {frame['desc']}")
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("**Active Code/Logic:**")
            st.code(frame['code'], language="javascript")
            st.markdown("**Memory/State:**")
            st.json(frame['vars'])
        
        with c2:
            st.markdown("**Structural Mental Model:**")
            st.info(frame['visual']) # This shows the tree, DOM, or stack
    else:
        st.info("Ask 'How does this work step by step?' to trigger the visualizer.")

# --- 4. INPUT HANDLING ---
if prompt := st.chat_input("Ask about logic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with chat_tab:
        with st.chat_message("user"):
            st.markdown(prompt)

    with st.chat_message("assistant"):
        response_stream = utils.get_ai_response(model, SYSTEM_PROMPT)
        full_response = st.write_stream(response_stream)
        
        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Extract Frames for the Visualizer
        frames = utils.extract_logic_frames(full_response)
        if frames:
            st.session_state.logic_frames = frames
            st.rerun()