# 🎓 Universal AI Lab
**A Multi-Modal Suite for Empowered Student Learning**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://universal-ai-lab-abmawveebxmibf4qbfydgq.streamlit.app/)

## 👤 Author Information
- **Name:** HEMANTH KUMAR BEHERA
- **College:** Raghu Institute of Technology
- **Department:** CSM (Computer Science and Machine Learning)
- **Batch:** 2022 - 2026

## 📌 Project Overview
The **Universal AI Lab** is a centralized platform designed to bridge the gap between passive AI usage and deep comprehension. This platform focuses on **Stateful Memory** and **Visual Logic Breakdown** to ensure students truly understand complex technical and linguistic subjects.

---

## 🛠️ Required Libraries (`requirements.txt`)
Before running the application, ensure your environment has the following dependencies installed. These are listed in the `requirements.txt` file in this repository:

```text
streamlit
openai
python-dotenv
PyPDF2
python-docx
python-pptx

```
🚀 Installation & Local Setup
Follow these steps to run the lab on your local machine:

1. Prerequisites
Python 3.9 or higher installed.
An API Key from OpenRouter.

2. Clone the Repository
git clone [https://github.com/Hemanth-Kumar-Behera/Universal-AI-Lab.git](https://github.com/Hemanth-Kumar-Behera/Universal-AI-Lab.git)
cd Universal-AI-Lab

3. Install Required Libraries
Run the following command to automatically install all dependencies:
pip install -r requirements.txt

4. Configure Environment
Create a file named .env in the root directory and add your key:

Code snippet
OPENROUTER_API_KEY=your_actual_key_here

5. Launch the Application
Start the Streamlit server:
streamlit run home.py

🏗️ System Architecture 
State Management: Utilizes st.session_state to maintain academic context across different modules.

Logic Visualization: Custom-built "Architect AI" engine that parses AI responses into interactive execution frames.

Multi-Modal Processing: Handles PDF transcripts, Word documents, and Image-to-Code conversions using Gemini 2.0 Flash.
