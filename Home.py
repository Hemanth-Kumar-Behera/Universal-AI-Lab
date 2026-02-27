import streamlit as st
import utils

# 1. Page Configuration
st.set_page_config(
    page_title="Universal AI Lab | Capstone",
    page_icon="🎓",
    layout="wide"
)

# 2. Main Title and Intro
st.title("🎓 Universal AI Lab")
st.subheader("A Multi-Modal Suite for Empowered Student Learning")
st.markdown("---")

# 3. Project Identity (As per your PPT Template)
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📌 Project Overview")
    st.write("""
    The **Universal AI Lab** is designed to bridge the gap between passive AI usage and deep 
    comprehension. While most students use AI to 'mug up' answers, this platform focuses 
    on **Stateful Memory** and **Visual Logic** to ensure students truly understand 
    complex subjects like Data Structures, React, and New Languages.
    """)

with col2:
    st.info(f"""
    **Student Name:** Hemanth Kumar Behera  
    **College:** Raghu Institute of Technology  
    **Department:** CSM  
    **Batch:** 2022 - 2026
    """)

# 4. Problem vs Solution (As per your PPT)
st.header("🚀 The Capstone Focus")
tab1, tab2 = st.tabs(["Problem Statement", "The Solution"])

with tab1:
    st.error("**The Problem:** Many students face difficulty in learning languages or complex code. Existing AI applications often lead to rote memorization because they lack visualization and session-based progress.")

with tab2:
    st.success("**The Solution:** A unified platform offering everything from resume preparation to real-time code visualizers, helping students visualize the 'Why' behind the logic.")

# 5. Application Outline
st.header("📂 Lab Modules")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="Module 1", value="Language Hub")
    st.caption("Adaptive characters and grammar games.")
with m2:
    st.metric(label="Module 2", value="Study Buddy")
    st.caption("Stateful memory for academic support.")
with m3:
    st.metric(label="Module 3", value="Career Coach")
    st.caption("Resume parsing and interview prep.")
with m4:
    st.metric(label="Module 4", value="Architect AI")
    st.caption("Visualizing code logic step-by-step.")

st.markdown("---")

st.write("👈 **Use the sidebar to explore the different lab modules.**")
