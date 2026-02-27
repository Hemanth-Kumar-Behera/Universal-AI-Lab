import streamlit as st
import json
import os
import time
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))
MODEL_STABLE = "google/gemini-2.0-flash-001"

# --- 1. SESSION STATE (Stable Core) ---
states = {
    "source_text": "",
    "chat_history": [],
    "current_tool": "chat",
    "game_active": False,
    "game_step": 0,
    "game_questions": [],
    "full_alphabet": [], 
    "grammar_charts": [],
    "detected_lang": "Language",
    "difficulty": "Basic"
}
for key, val in states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- 2. ENGINE ROOM ---
def safe_extract_json(text, expected_key="data"):
    if not text: return {expected_key: []}
    try:
        clean = re.sub(r"```json|```|json", "", text, flags=re.IGNORECASE).strip()
        data = json.loads(clean)
        return data if isinstance(data, dict) else {expected_key: []}
    except:
        return {expected_key: []}

def call_ai(sys, user, json_mode=True):
    # Forced JSON enforcement
    sys += " Respond ONLY with valid JSON. No prose. No markdown backticks."
    try:
        res = client.chat.completions.create(
            model=MODEL_STABLE,
            messages=[{"role": "system", "content": sys}, {"role": "user", "content": user}],
            response_format={"type": "json_object"} if json_mode else None,
            timeout=120 
        )
        return res.choices[0].message.content
    except Exception:
        return ""

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="Universal AI Lab", layout="wide")

with st.sidebar:
    st.header("📚 Knowledge Base")
    st.session_state.source_text = st.text_area("Lesson Context:", 
                                              placeholder="Paste specific topics here (e.g. Arabic Tenses, French Verbs)...",
                                              value=st.session_state.source_text, height=150)
    
    st.session_state.difficulty = st.select_slider("Learning Level", options=["Basic", "Medium", "Expert"])

    if st.button("🚀 FORCE FULL REBUILD", use_container_width=True):
        if st.session_state.source_text:
            with st.spinner("Executing Triple-Task Reconstruction..."):
                
                # TASK 1: THE ARCHIVIST (Alphabet/Writing System)
                # This prompt is isolated to ensure the alphabet is NEVER skipped.
                a_sys = "You are a Linguistic Archivist. Identify the language. Provide the COMPLETE writing system (e.g. ALL 28 Arabic letters, ALL Hiragana, or ALL Pinyin initials)."
                a_user = f"Context: {st.session_state.source_text}. JSON structure: {{'lang': 'Language Name', 'alpha': [{{'l':'Character','p':'Pronunciation'}}]}}"
                a_res = call_ai(a_sys, a_user)
                data_a = safe_extract_json(a_res, "alpha")
                st.session_state.full_alphabet = data_a.get('alpha', [])
                st.session_state.detected_lang = data_a.get('lang', "Language")
                
                # TASK 2: THE PROFESSOR (Grammar, Tenses, Particles)
                # This prompt is forced to provide structure even if the context is thin.
                g_sys = "You are a Grammar Professor. Create 3 detailed tables: 1. Core Grammar/Tenses, 2. Essential Particles/Articles, 3. Context-Specific Vocabulary."
                g_user = f"Context: {st.session_state.source_text}. JSON structure: {{'charts': [{{'title':'Table Name','rows':[['Header1','Header2'],['Row1','Row2']]}}]}}"
                g_res = call_ai(g_sys, g_user)
                data_g = safe_extract_json(g_res, "charts")
                st.session_state.grammar_charts = data_g.get('charts', [])
                
                st.success("Foundation & Lessons Rebuilt!")
                st.session_state.current_tool = "ref"
                st.rerun()

# --- 4. NAVIGATION ---
st.title("🎙️ Universal AI Lab")
c1, c2, c3, c4 = st.columns(4)
if c1.button("💬 Chat", use_container_width=True): st.session_state.current_tool = "chat"
if c2.button("📖 Reference", use_container_width=True): st.session_state.current_tool = "ref"
if c3.button("🎯 Game", use_container_width=True): st.session_state.current_tool = "game"
if c4.button("🗑️ Reset All", use_container_width=True):
    for k in states: st.session_state[k] = states[k]
    st.rerun()

st.divider()

# --- 5. REFERENCE (The Fortress) ---
if st.session_state.current_tool == "ref":
    st.header(f"📖 {st.session_state.detected_lang} Comprehensive Foundation")
    
    # Grid display for Alphabet
    if st.session_state.full_alphabet:
        st.subheader("🔤 Complete Writing System / Phonetics")
        cols = st.columns(10) 
        for i, item in enumerate(st.session_state.full_alphabet):
            with cols[i % 10]:
                st.markdown(f"""<div style="border:1px solid #444; border-radius:8px; padding:12px; text-align:center; background:#111; margin-bottom:10px;">
                    <h2 style="margin:0; color:#00d4ff;">{item.get('l','?')}</h2>
                    <p style="margin:0; font-size:0.8em; color:#888;">{item.get('p','')}</p></div>""", unsafe_allow_html=True)
    
    # Tables for Lessons
    if st.session_state.grammar_charts:
        st.divider()
        for chart in st.session_state.grammar_charts:
            st.subheader(f"📊 {chart.get('title', 'Reference Table')}")
            st.table(chart.get('rows', []))

# --- 6. ADAPTIVE GAME (The Strict Logic) ---
elif st.session_state.current_tool == "game":
    if not st.session_state.full_alphabet:
        st.warning("Please Sync the Knowledge Base first.")
    elif not st.session_state.game_active:
        if st.button("Start Quiz"):
            with st.spinner("Generating Level-Specific Quiz..."):
                # HARD RULES for Difficulty
                rule_map = {
                    "Basic": "Questions in English. Options in Native Language with (English Translation) in brackets.",
                    "Medium": "Questions in a mix of English and Native language. Options in Native Language only.",
                    "Expert": "Questions and Options MUST be entirely in the Native language. No English allowed."
                }
                curr_rule = rule_map[st.session_state.difficulty]
                
                prompt = f"Topic: {st.session_state.source_text}. Level: {st.session_state.difficulty}. Rule: {curr_rule}. 5 Questions JSON: {{'questions': [{{'q':'...','options':['...'],'a':'...'}}]}}"
                res = call_ai("Quiz Engine", prompt)
                st.session_state.game_questions = safe_extract_json(res, "questions").get('questions', [])
                st.session_state.game_active = True
                st.session_state.game_step = 0
                st.rerun()
    else:
        step = st.session_state.game_step
        qs = st.session_state.game_questions
        if step < len(qs):
            st.write(f"### Question {step+1} ({st.session_state.difficulty} Mode)")
            st.info(qs[step]['q'])
            for opt in qs[step]['options']:
                if st.button(opt, key=f"q_{step}_{opt}", use_container_width=True):
                    if opt == qs[step]['a']: st.success("🎯 Correct!")
                    else: st.error(f"❌ Incorrect. The answer was: {qs[step]['a']}")
                    time.sleep(1.5)
                    st.session_state.game_step += 1
                    st.rerun()
        else:
            st.balloons()
            st.success("Quiz Complete!")
            st.session_state.game_active = False

# --- 7. CHAT (Assistant) ---
elif st.session_state.current_tool == "chat":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if p := st.chat_input("Ask a question about the lesson..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        with st.chat_message("assistant"):
            res = call_ai(f"Tutor for {st.session_state.detected_lang}. Context: {st.session_state.source_text}", p, json_mode=False)
            st.write(res)
            st.session_state.chat_history.append({"role": "assistant", "content": res})