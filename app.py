"""
╔══════════════════════════════════════════════════════════════╗
║        HealthGPT PRO — Full AI Health Assistant              ║
║        Session 2 | by Akash Kumar Injeti                     ║
║        PDF Analyzer + BMI + Chat + History Tracker           ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import json
import base64
from datetime import datetime

# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="HealthGPT — AI Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  FULL DARK CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

  html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
  }

  .stApp { background: #0d1117; }

  [data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
  }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

  .main .block-container { padding: 1.5rem 2rem; max-width: 960px; }

  /* ── Hero ── */
  .hero {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px; padding: 2rem;
    text-align: center; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #0ea5e9, #7c3aed, #22c55e, #0ea5e9, transparent);
  }
  .hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem; font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0 0%, #0ea5e9 50%, #7c3aed 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem;
  }
  .hero p { font-size: 0.92rem; color: #8b949e; margin: 0 0 1rem; }
  .badge-row { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
  .badge { font-size: 0.7rem; font-weight: 600; padding: 3px 12px; border-radius: 20px; border: 1px solid; }
  .badge-blue   { background: rgba(14,165,233,0.1); color: #38bdf8; border-color: rgba(14,165,233,0.3); }
  .badge-purple { background: rgba(124,58,237,0.1); color: #a78bfa; border-color: rgba(124,58,237,0.3); }
  .badge-green  { background: rgba(34,197,94,0.1);  color: #4ade80; border-color: rgba(34,197,94,0.3); }
  .badge-red    { background: rgba(239,68,68,0.1);  color: #f87171; border-color: rgba(239,68,68,0.3); }
  .badge-amber  { background: rgba(251,191,36,0.1); color: #fbbf24; border-color: rgba(251,191,36,0.3); }

  /* ── Section Labels ── */
  .section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #0ea5e9; margin-bottom: 0.3rem;
  }

  /* ── Inputs ── */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stSelectbox > div > div,
  .stNumberInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.9rem !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.1) !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #7c3aed) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.9rem !important; transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.85 !important; }

  /* ── AI Message Cards ── */
  .ai-message {
    background: #161b22; border: 1px solid #30363d;
    border-left: 3px solid #0ea5e9; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #e2e8f0;
    white-space: pre-wrap;
  }
  .ai-message::before {
    content: '🤖 HealthGPT'; display: block;
    font-size: 0.68rem; color: #0ea5e9; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem;
  }

  .emergency-message {
    background: #1a0a0a; border: 1px solid #7f1d1d;
    border-left: 3px solid #ef4444; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #fca5a5; white-space: pre-wrap;
  }
  .emergency-message::before {
    content: '🚨 Emergency Guide'; display: block;
    font-size: 0.68rem; color: #ef4444; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem;
  }

  .diet-message {
    background: #0a1a0f; border: 1px solid #14532d;
    border-left: 3px solid #22c55e; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #86efac; white-space: pre-wrap;
  }
  .diet-message::before {
    content: '🥗 Diet Plan'; display: block;
    font-size: 0.68rem; color: #22c55e; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem;
  }

  .medicine-message {
    background: #0f0a1a; border: 1px solid #4c1d95;
    border-left: 3px solid #7c3aed; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #c4b5fd; white-space: pre-wrap;
  }
  .medicine-message::before {
    content: '💊 Medicine Info'; display: block;
    font-size: 0.68rem; color: #7c3aed; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem;
  }

  .pdf-message {
    background: #1a1400; border: 1px solid #78350f;
    border-left: 3px solid #f59e0b; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #fde68a; white-space: pre-wrap;
  }
  .pdf-message::before {
    content: '📄 Report Analysis'; display: block;
    font-size: 0.68rem; color: #f59e0b; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.75rem;
  }

  /* ── Chat bubbles ── */
  .chat-user {
    background: linear-gradient(135deg, rgba(14,165,233,0.15), rgba(124,58,237,0.15));
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 12px 12px 2px 12px;
    padding: 0.85rem 1.1rem; margin: 0.5rem 0 0.5rem 3rem;
    font-size: 0.92rem; color: #e2e8f0; line-height: 1.6;
  }
  .chat-user::before {
    content: '👤 You'; display: block;
    font-size: 0.65rem; color: #0ea5e9; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.4rem;
  }

  .chat-ai {
    background: #161b22; border: 1px solid #30363d;
    border-left: 3px solid #0ea5e9;
    border-radius: 12px 12px 12px 2px;
    padding: 0.85rem 1.1rem; margin: 0.5rem 3rem 0.5rem 0;
    font-size: 0.92rem; color: #e2e8f0; line-height: 1.7;
    white-space: pre-wrap;
  }
  .chat-ai::before {
    content: '🤖 HealthGPT'; display: block;
    font-size: 0.65rem; color: #0ea5e9; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.4rem;
  }

  /* ── BMI Cards ── */
  .bmi-card {
    border-radius: 14px; padding: 1.5rem;
    text-align: center; margin: 0.5rem 0;
  }
  .bmi-score {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem; font-weight: 700; line-height: 1;
  }
  .bmi-label { font-size: 0.85rem; margin-top: 0.4rem; font-weight: 600; }

  /* ── History cards ── */
  .history-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 1rem 1.25rem;
    margin: 0.5rem 0; font-size: 0.85rem; color: #8b949e;
  }
  .history-card .h-date { color: #0ea5e9; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em; }
  .history-card .h-type { color: #e2e8f0; font-weight: 600; font-size: 0.9rem; margin: 2px 0; }

  /* ── Metric boxes ── */
  .metric-box {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 1.1rem; text-align: center;
  }
  .metric-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem; font-weight: 700; color: #0ea5e9;
  }
  .metric-label { font-size: 0.72rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 3px; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #161b22; border-radius: 10px;
    padding: 4px; gap: 4px; border: 1px solid #30363d;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #8b949e !important;
    border-radius: 8px !important; font-size: 0.82rem !important;
    font-weight: 500 !important; padding: 0.45rem 0.9rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(14,165,233,0.2), rgba(124,58,237,0.2)) !important;
    color: #e2e8f0 !important; border: 1px solid #30363d !important;
  }

  /* ── File uploader ── */
  [data-testid="stFileUploader"] {
    background: #161b22 !important;
    border: 2px dashed #30363d !important;
    border-radius: 12px !important;
  }

  /* ── Download btn ── */
  .stDownloadButton > button {
    background: transparent !important; border: 1px solid #30363d !important;
    color: #8b949e !important; border-radius: 8px !important;
    font-size: 0.8rem !important;
  }
  .stDownloadButton > button:hover {
    border-color: #0ea5e9 !important; color: #0ea5e9 !important;
    background: rgba(14,165,233,0.05) !important;
  }

  /* ── Progress bar ── */
  .stProgress > div > div > div { background: linear-gradient(90deg, #0ea5e9, #7c3aed) !important; }

  /* ── Emergency numbers ── */
  .emergency-numbers {
    background: #1a0a0a; border: 1px solid #7f1d1d;
    border-radius: 12px; padding: 1.25rem;
    font-size: 0.88rem; color: #fca5a5; line-height: 2;
  }

  /* ── Footer ── */
  .footer {
    margin-top: 3rem; padding: 1.5rem;
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; text-align: center;
    position: relative; overflow: hidden;
  }
  .footer::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #0ea5e9, #7c3aed, #22c55e, #f59e0b);
  }
  .footer .powered { color: #8b949e; font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 5px; }
  .footer .name    { color: #e2e8f0; font-size: 1.25rem; font-weight: 700; font-family: 'Space Grotesk', sans-serif; }
  .footer .name span {
    background: linear-gradient(135deg, rgba(14,165,233,0.15), rgba(124,58,237,0.15));
    border: 1px solid #30363d; padding: 2px 16px; border-radius: 20px;
  }
  .footer .tagline { color: #8b949e; font-size: 0.75rem; margin-top: 6px; }

  hr { border-color: #30363d !important; }
  #MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Session State Init
# ─────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "health_history" not in st.session_state:
    st.session_state.health_history = []


# ─────────────────────────────────────────────
#  Groq API
# ─────────────────────────────────────────────
def call_groq(api_key, prompt, temperature=0.5, max_tokens=1500):
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        },
        timeout=40
    )
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"].strip()
    elif resp.status_code == 401:
        raise ValueError("Invalid API key.")
    elif resp.status_code == 429:
        raise ValueError("Rate limit hit. Please wait a few seconds.")
    else:
        raise ValueError(f"API error {resp.status_code}: {resp.text}")


def call_groq_chat(api_key, messages, temperature=0.7):
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "max_tokens": 800,
            "temperature": temperature
        },
        timeout=40
    )
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"].strip()
    raise ValueError(f"API error {resp.status_code}")


def save_to_history(entry_type, summary):
    st.session_state.health_history.append({
        "type": entry_type,
        "summary": summary,
        "time": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:700;
        background:linear-gradient(135deg,#0ea5e9,#7c3aed);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        🏥 HealthGPT
      </div>
      <div style="font-size:0.72rem; color:#8b949e; margin-top:4px; letter-spacing:0.05em;">
        AI Health Assistant PRO
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">🔑 Groq API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="gsk_...",
                             label_visibility="collapsed")
    st.markdown("<div style='font-size:0.75rem;color:#8b949e'>Free at <a href='https://console.groq.com' target='_blank' style='color:#0ea5e9'>console.groq.com</a></div>", unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-label">🌍 Language / భాష</div>', unsafe_allow_html=True)
    lang = st.selectbox("Language", ["English", "Telugu (తెలుగు)"], label_visibility="collapsed")
    is_telugu = lang == "Telugu (తెలుగు)"

    st.divider()

    st.markdown("""
    <div class="section-label">🚨 Emergency Numbers</div>
    <div style="font-size:0.82rem;color:#8b949e;line-height:2">
      🚑 Ambulance: <strong style="color:#f87171">108</strong><br>
      🚔 Police: <strong style="color:#f87171">100</strong><br>
      🚒 Fire: <strong style="color:#f87171">101</strong><br>
      🆘 National: <strong style="color:#f87171">112</strong>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    history_count = len(st.session_state.health_history)
    chat_count    = len(st.session_state.chat_history)
    st.markdown(f"""
    <div style="font-size:0.78rem;color:#8b949e;line-height:2">
      📋 History entries: <strong style="color:#0ea5e9">{history_count}</strong><br>
      💬 Chat messages: <strong style="color:#7c3aed">{chat_count}</strong>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-size:0.78rem;color:#8b949e">
      ⚠️ <strong style="color:#fbbf24">Disclaimer:</strong> Educational purposes only.
      Not a substitute for professional medical advice.
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="font-size:0.78rem;color:#8b949e">
      Built by <strong style="color:#e2e8f0">Akash Kumar Injeti</strong><br>
      Data Science & AI 🚀
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🏥 HealthGPT</h1>
  <p>Your personal AI Health Assistant — free for everyone in India 🇮🇳</p>
  <div class="badge-row">
    <span class="badge badge-green">✅ 100% Free</span>
    <span class="badge badge-blue">🤖 LLaMA 3.3 70B</span>
    <span class="badge badge-purple">🌍 English + Telugu</span>
    <span class="badge badge-amber">📄 PDF Analyzer</span>
    <span class="badge badge-blue">💬 Chat Mode</span>
    <span class="badge badge-green">🧮 BMI Calculator</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ALL 7 TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🩺 Symptoms",
    "💊 Medicine",
    "🥗 Diet",
    "🚨 Emergency",
    "📄 PDF Report",
    "💬 Chat",
    "📊 My Health"
])


# ══════════════════════════════════
#  TAB 1 — Symptom Checker
# ══════════════════════════════════
with tab1:
    st.markdown("#### 🩺 " + ("లక్షణ పరీక్షకుడు" if is_telugu else "Symptom Checker"))
    st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Describe your symptoms — AI suggests possible causes and what to do next.</span>", unsafe_allow_html=True)
    st.markdown("")

    symptoms = st.text_area("Symptoms",
        placeholder="e.g. headache, fever, cough for 3 days, feeling tired...",
        label_visibility="collapsed", height=100)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="section-label">Age</div>', unsafe_allow_html=True)
        age = st.number_input("Age", 1, 100, 25, label_visibility="collapsed")
    with c2:
        st.markdown('<div class="section-label">Gender</div>', unsafe_allow_html=True)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], label_visibility="collapsed")
    with c3:
        st.markdown('<div class="section-label">Duration</div>', unsafe_allow_html=True)
        duration = st.selectbox("Duration", ["Today", "2-3 Days", "1 Week", "1+ Month"], label_visibility="collapsed")

    if st.button("🩺  Analyze My Symptoms", use_container_width=True, type="primary", key="sym_btn"):
        if not api_key:
            st.error("⚠️  Enter your Groq API key in the sidebar.")
        elif not symptoms:
            st.error("⚠️  Please describe your symptoms.")
        else:
            lang_inst = "Respond in Telugu" if is_telugu else "Respond in simple English"
            prompt = f"""You are a helpful medical information assistant. {lang_inst}.
Patient: Age {age}, {gender}, symptoms for {duration}
Symptoms: {symptoms}
Provide:
1. 🔍 Possible Conditions (3-4 likely causes)
2. 📋 What These Symptoms May Mean
3. 🏠 Home Care Tips
4. ⚠️ Warning Signs — when to see a doctor immediately
5. 👨‍⚕️ Which type of doctor to visit
End with: This is AI information only, not a substitute for professional medical advice."""
            with st.spinner("🤖 Analyzing symptoms..."):
                try:
                    result = call_groq(api_key, prompt)
                    st.markdown(f'<div class="ai-message">{result}</div>', unsafe_allow_html=True)
                    save_to_history("🩺 Symptom Check", f"Symptoms: {symptoms[:60]}...")
                    st.download_button("⬇️ Download Report", data=result.encode(), file_name="symptom_report.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"❌ {e}")


# ══════════════════════════════════
#  TAB 2 — Medicine Info
# ══════════════════════════════════
with tab2:
    st.markdown("#### 💊 Medicine Information")
    st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Type any medicine name — AI explains it in plain simple language.</span>", unsafe_allow_html=True)
    st.markdown("")

    medicine_name = st.text_input("Medicine",
        placeholder="e.g. Paracetamol, Dolo 650, Metformin...",
        label_visibility="collapsed")

    if st.button("💊  Get Medicine Info", use_container_width=True, type="primary", key="med_btn"):
        if not api_key:
            st.error("⚠️  Enter your Groq API key in the sidebar.")
        elif not medicine_name:
            st.error("⚠️  Please enter a medicine name.")
        else:
            lang_inst = "Respond in Telugu" if is_telugu else "Respond in simple English"
            prompt = f"""You are a helpful pharmacist assistant. {lang_inst}.
Explain the medicine: {medicine_name}
Include:
1. 💊 What is this medicine?
2. 🎯 What is it used for?
3. 📏 Common Dosage
4. ⚠️ Common Side Effects
5. 🚫 Who should NOT take this?
6. 🍽️ With or without food?
7. 💡 Important Tips
Always remind: Follow doctor's prescription. Do not self-medicate."""
            with st.spinner("🤖 Fetching medicine info..."):
                try:
                    result = call_groq(api_key, prompt)
                    st.markdown(f'<div class="medicine-message">{result}</div>', unsafe_allow_html=True)
                    save_to_history("💊 Medicine Info", f"Medicine: {medicine_name}")
                    st.download_button("⬇️ Download", data=result.encode(), file_name=f"{medicine_name}_info.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"❌ {e}")


# ══════════════════════════════════
#  TAB 3 — Diet Planner
# ══════════════════════════════════
with tab3:
    st.markdown("#### 🥗 Personalized Diet Planner")
    st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Enter your details — AI creates a personalized Indian diet plan for you.</span>", unsafe_allow_html=True)
    st.markdown("")

    cd1, cd2 = st.columns(2)
    with cd1:
        st.markdown('<div class="section-label">Age</div>', unsafe_allow_html=True)
        d_age = st.number_input("DAge", 1, 100, 25, label_visibility="collapsed", key="d_age")
        st.markdown('<div class="section-label">Weight (kg)</div>', unsafe_allow_html=True)
        weight = st.number_input("Weight", 20, 200, 70, label_visibility="collapsed")
    with cd2:
        st.markdown('<div class="section-label">Gender</div>', unsafe_allow_html=True)
        d_gender = st.selectbox("DGender", ["Male", "Female"], label_visibility="collapsed", key="d_gen")
        st.markdown('<div class="section-label">Height (cm)</div>', unsafe_allow_html=True)
        height = st.number_input("Height", 100, 250, 165, label_visibility="collapsed")

    st.markdown('<div class="section-label">Health Condition</div>', unsafe_allow_html=True)
    condition = st.selectbox("Condition", ["Healthy", "Diabetes", "High Blood Pressure",
        "Weight Loss", "Weight Gain", "Thyroid", "Heart Disease", "Anemia", "PCOD/PCOS"],
        label_visibility="collapsed")

    st.markdown('<div class="section-label">Food Preference</div>', unsafe_allow_html=True)
    food_pref = st.selectbox("Food", ["Vegetarian", "Non-Vegetarian", "Eggetarian"], label_visibility="collapsed")

    if st.button("🥗  Generate My Diet Plan", use_container_width=True, type="primary", key="diet_btn"):
        if not api_key:
            st.error("⚠️  Enter your Groq API key in the sidebar.")
        else:
            lang_inst = "Respond in Telugu" if is_telugu else "Respond in simple English"
            prompt = f"""You are a certified Indian nutritionist. {lang_inst}.
1-day Indian diet plan for: Age {d_age}, {d_gender}, {weight}kg, {height}cm, {condition}, {food_pref}
Include:
🌅 Early Morning | 🍳 Breakfast | 🥤 Mid Morning | 🍱 Lunch | ☕ Evening | 🌙 Dinner
💧 Water intake | ❌ Foods to avoid | ✅ Super foods | 💡 3 Tips
Use only common Indian foods."""
            with st.spinner("🤖 Creating your diet plan..."):
                try:
                    result = call_groq(api_key, prompt)
                    st.markdown(f'<div class="diet-message">{result}</div>', unsafe_allow_html=True)
                    save_to_history("🥗 Diet Plan", f"Condition: {condition} | {food_pref}")
                    st.download_button("⬇️ Download Diet Plan", data=result.encode(), file_name="diet_plan.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"❌ {e}")


# ══════════════════════════════════
#  TAB 4 — Emergency
# ══════════════════════════════════
with tab4:
    st.markdown("#### 🚨 Emergency First Aid Guide")
    st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Instant step-by-step first aid before the doctor arrives.</span>", unsafe_allow_html=True)
    st.markdown("")

    st.markdown('<div class="section-label">Select Emergency</div>', unsafe_allow_html=True)
    emergency_type = st.selectbox("Emergency", [
        "Heart Attack / గుండెపోటు", "Stroke / పక్షవాతం",
        "Choking / గొంతు అడ్డుపడటం", "Severe Burns",
        "Fracture / ఎముక విరుగుట", "Fainting / మూర్ఛపోవడం",
        "Severe Bleeding", "Seizure / మూర్ఛ",
        "Allergic Reaction", "Snake Bite / పాము కాటు",
        "Drowning", "Electric Shock",
    ], label_visibility="collapsed")

    if st.button("🚨  Get Emergency Guide", use_container_width=True, type="primary", key="emg_btn"):
        if not api_key:
            st.error("⚠️  Enter your Groq API key in the sidebar.")
        else:
            lang_inst = "Respond in Telugu" if is_telugu else "Respond in simple English"
            prompt = f"""You are an emergency first aid expert. {lang_inst}.
Step-by-step emergency guide for: {emergency_type}
🚨 CALL 108 IMMEDIATELY
⚡ FIRST 60 SECONDS — What to do RIGHT NOW (3-4 actions)
📋 STEP BY STEP FIRST AID (numbered)
❌ DO NOT DO THESE (dangerous mistakes)
✅ WHILE WAITING FOR AMBULANCE
Simple language — no medical training required."""
            with st.spinner("🚨 Loading emergency guidance..."):
                try:
                    result = call_groq(api_key, prompt)
                    st.markdown(f'<div class="emergency-message">{result}</div>', unsafe_allow_html=True)
                    save_to_history("🚨 Emergency Guide", f"Emergency: {emergency_type[:40]}")
                    st.download_button("⬇️ Download Guide", data=result.encode(), file_name="emergency_guide.txt", mime="text/plain")
                except Exception as e:
                    st.error(f"❌ {e}")

    st.markdown("""
    <div class="emergency-numbers">
      <strong>🇮🇳 India Emergency — Save these now!</strong><br><br>
      🚑 <strong>108</strong> — Ambulance &nbsp;|&nbsp;
      🚔 <strong>100</strong> — Police &nbsp;|&nbsp;
      🚒 <strong>101</strong> — Fire &nbsp;|&nbsp;
      🆘 <strong>112</strong> — National &nbsp;|&nbsp;
      💊 <strong>1800-116-117</strong> — Poison
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════
#  TAB 5 — PDF Report Analyzer
# ══════════════════════════════════
with tab5:
    st.markdown("#### 📄 Medical Report Analyzer")
    st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Upload your blood test / medical report — AI explains it in simple language.</span>", unsafe_allow_html=True)
    st.markdown("")

    uploaded_file = st.file_uploader(
        "Upload Report",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        help="Upload PDF or TXT medical report"
    )

    if uploaded_file:
        st.success(f"✅  File uploaded: **{uploaded_file.name}** ({round(uploaded_file.size/1024, 1)} KB)")

        report_type = st.selectbox("What type of report is this?", [
            "Blood Test / CBC Report",
            "Liver Function Test (LFT)",
            "Kidney Function Test (KFT)",
            "Thyroid Test",
            "Diabetes / HbA1c Report",
            "Lipid Profile / Cholesterol",
            "Urine Test",
            "X-Ray / Scan Report",
            "General Medical Report",
        ])

        patient_age = st.number_input("Patient Age", 1, 100, 25, key="pdf_age")

        if st.button("📄  Analyze My Report", use_container_width=True, type="primary", key="pdf_btn"):
            if not api_key:
                st.error("⚠️  Enter your Groq API key in the sidebar.")
            else:
                try:
                    file_content = ""
                    if uploaded_file.type == "text/plain":
                        file_content = uploaded_file.read().decode("utf-8", errors="ignore")
                    else:
                        # For PDF — read raw bytes and extract text best-effort
                        raw = uploaded_file.read()
                        # Try to extract readable text from PDF bytes
                        text_parts = []
                        i = 0
                        while i < len(raw):
                            try:
                                chunk = raw[i:i+1000].decode("latin-1", errors="ignore")
                                readable = ''.join(c if c.isprintable() else ' ' for c in chunk)
                                if len(readable.strip()) > 20:
                                    text_parts.append(readable)
                            except:
                                pass
                            i += 1000
                        file_content = ' '.join(text_parts)[:4000]

                    if not file_content.strip():
                        file_content = f"[{report_type} uploaded — analyze based on report type]"

                    lang_inst = "Respond in Telugu" if is_telugu else "Respond in simple English"
                    prompt = f"""You are a medical report interpreter assistant. {lang_inst}.

Report Type: {report_type}
Patient Age: {patient_age}
Report Content: {file_content[:3000]}

Analyze this medical report and provide:
1. 📋 Summary — What this report is about (simple explanation)
2. ✅ Normal Values — What's within normal range
3. ⚠️ Abnormal Values — What's outside normal range and what it means
4. 🎯 What This Means For The Patient — Plain language explanation
5. 💊 General Recommendations — Lifestyle or diet changes suggested
6. 👨‍⚕️ Should they see a doctor? Which specialist?

Use very simple language. Avoid medical jargon.
Always end with: Please consult a doctor for proper diagnosis and treatment."""

                    with st.spinner("📄 Analyzing your medical report..."):
                        result = call_groq(api_key, prompt, max_tokens=2000)
                        st.markdown(f'<div class="pdf-message">{result}</div>', unsafe_allow_html=True)
                        save_to_history("📄 Report Analysis", f"Report: {report_type}")
                        st.download_button("⬇️ Download Analysis", data=result.encode(),
                                           file_name="report_analysis.txt", mime="text/plain")

                except Exception as e:
                    st.error(f"❌ {e}")
    else:
        st.markdown("""
        <div style="background:#161b22;border:2px dashed #30363d;border-radius:12px;
          padding:2.5rem;text-align:center;color:#8b949e;margin-top:1rem">
          <div style="font-size:2rem;margin-bottom:0.5rem">📄</div>
          <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.3rem">Upload your medical report</div>
          <div style="font-size:0.82rem">Supports PDF and TXT files — Blood tests, scan reports, lab results</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════
#  TAB 6 — Chat Mode
# ══════════════════════════════════
with tab6:
    st.markdown("#### 💬 Chat with HealthGPT")
    st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Ask any health question — like talking to a doctor friend.</span>", unsafe_allow_html=True)
    st.markdown("")

    # Show chat history
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-radius:12px;
          padding:1.5rem;text-align:center;color:#8b949e;margin:1rem 0">
          <div style="font-size:1.5rem;margin-bottom:0.5rem">💬</div>
          <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.3rem">Start a health conversation</div>
          <div style="font-size:0.82rem">Ask anything — symptoms, medicines, diet, general health tips...</div>
        </div>
        """, unsafe_allow_html=True)

    # Suggested questions
    st.markdown("<div style='font-size:0.72rem;color:#8b949e;margin-top:1rem;letter-spacing:0.08em;text-transform:uppercase'>💡 Try asking</div>", unsafe_allow_html=True)
    suggestion_cols = st.columns(3)
    suggestions = [
        "What foods help with diabetes?",
        "How to reduce stress naturally?",
        "What are signs of dehydration?",
    ]
    for i, sug in enumerate(suggestions):
        with suggestion_cols[i]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state["chat_prefill"] = sug

    # Chat input
    prefill = st.session_state.get("chat_prefill", "")
    user_input = st.text_input(
        "Chat Input",
        value=prefill,
        placeholder="Ask any health question...",
        label_visibility="collapsed",
        key="chat_input_field"
    )
    if "chat_prefill" in st.session_state:
        del st.session_state["chat_prefill"]

    c_send, c_clear = st.columns([4, 1])
    with c_send:
        send = st.button("💬  Send Message", use_container_width=True, type="primary", key="chat_send")
    with c_clear:
        if st.button("🗑️ Clear", use_container_width=True, key="chat_clear"):
            st.session_state.chat_history = []
            st.rerun()

    if send and user_input:
        if not api_key:
            st.error("⚠️  Enter your Groq API key in the sidebar.")
        else:
            lang_inst = "Always respond in Telugu language" if is_telugu else "Always respond in simple English"
            system_msg = {
                "role": "system",
                "content": f"""You are HealthGPT, a friendly and knowledgeable AI health assistant built for India.
{lang_inst}. Be warm, caring, and helpful like a doctor friend.
Give practical, easy-to-understand health advice.
Always remind users to consult a real doctor for serious concerns.
Keep responses concise and easy to read."""
            }
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            messages = [system_msg] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history
            ]
            with st.spinner("🤖 HealthGPT is thinking..."):
                try:
                    reply = call_groq_chat(api_key, messages)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")


# ══════════════════════════════════
#  TAB 7 — BMI + Health History
# ══════════════════════════════════
with tab7:
    st.markdown("#### 📊 My Health Dashboard")
    st.markdown("")

    # ── BMI Calculator ──
    st.markdown("##### 🧮 BMI Calculator & Health Score")
    bmi_c1, bmi_c2, bmi_c3 = st.columns(3)
    with bmi_c1:
        st.markdown('<div class="section-label">Weight (kg)</div>', unsafe_allow_html=True)
        bmi_weight = st.number_input("BMI Weight", 20, 200, 70, label_visibility="collapsed", key="bmi_w")
    with bmi_c2:
        st.markdown('<div class="section-label">Height (cm)</div>', unsafe_allow_html=True)
        bmi_height = st.number_input("BMI Height", 100, 250, 170, label_visibility="collapsed", key="bmi_h")
    with bmi_c3:
        st.markdown('<div class="section-label">Age</div>', unsafe_allow_html=True)
        bmi_age = st.number_input("BMI Age", 1, 100, 25, label_visibility="collapsed", key="bmi_a")

    if st.button("🧮  Calculate My BMI", use_container_width=True, type="primary", key="bmi_btn"):
        bmi = round(bmi_weight / ((bmi_height / 100) ** 2), 1)
        if bmi < 18.5:
            category, color, emoji, bg = "Underweight", "#38bdf8", "⚠️", "rgba(14,165,233,0.1)"
        elif bmi < 25:
            category, color, emoji, bg = "Normal Weight", "#4ade80", "✅", "rgba(34,197,94,0.1)"
        elif bmi < 30:
            category, color, emoji, bg = "Overweight", "#fbbf24", "⚠️", "rgba(251,191,36,0.1)"
        else:
            category, color, emoji, bg = "Obese", "#f87171", "❌", "rgba(239,68,68,0.1)"

        ideal_min = round(18.5 * (bmi_height / 100) ** 2, 1)
        ideal_max = round(24.9 * (bmi_height / 100) ** 2, 1)

        st.markdown(f"""
        <div style="background:{bg};border:1px solid {color}33;border-radius:14px;
          padding:1.5rem;text-align:center;margin:1rem 0">
          <div style="font-family:'Space Grotesk',sans-serif;font-size:3.5rem;
            font-weight:700;color:{color};line-height:1">{bmi}</div>
          <div style="font-size:1rem;font-weight:700;color:{color};margin-top:0.3rem">{emoji} {category}</div>
          <div style="font-size:0.82rem;color:#8b949e;margin-top:0.5rem">
            Ideal weight for your height: <strong style="color:#e2e8f0">{ideal_min} – {ideal_max} kg</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Metrics row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{bmi}</div><div class="metric-label">BMI Score</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{bmi_weight}kg</div><div class="metric-label">Your Weight</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{bmi_height}cm</div><div class="metric-label">Your Height</div></div>', unsafe_allow_html=True)
        with m4:
            diff = round(bmi_weight - ideal_min, 1)
            diff_label = f"+{diff}kg" if diff > 0 else f"{diff}kg"
            st.markdown(f'<div class="metric-box"><div class="metric-val">{diff_label}</div><div class="metric-label">From Ideal</div></div>', unsafe_allow_html=True)

        # AI Tips
        if api_key:
            with st.spinner("🤖 Getting personalized health tips..."):
                try:
                    prompt = f"""Give 5 specific, practical health tips for a {bmi_age}-year-old with BMI {bmi} ({category}).
Include diet tips, exercise suggestions, and lifestyle changes.
Be specific and actionable. Keep each tip to 1-2 lines.
{"Respond in Telugu" if is_telugu else "Respond in simple English"}"""
                    tips = call_groq(api_key, prompt, max_tokens=500)
                    st.markdown(f'<div class="ai-message">{tips}</div>', unsafe_allow_html=True)
                    save_to_history("🧮 BMI Check", f"BMI: {bmi} — {category}")
                except Exception as e:
                    st.warning(f"Could not load AI tips: {e}")

    st.divider()

    # ── Health History ──
    st.markdown("##### 📋 Health Activity History")

    if st.session_state.health_history:
        # Clear button
        if st.button("🗑️  Clear History", key="clear_hist"):
            st.session_state.health_history = []
            st.rerun()

        for entry in reversed(st.session_state.health_history):
            st.markdown(f"""
            <div class="history-card">
              <div class="h-date">🕐 {entry['time']}</div>
              <div class="h-type">{entry['type']}</div>
              <div style="color:#8b949e;font-size:0.82rem;margin-top:3px">{entry['summary']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-radius:12px;
          padding:2rem;text-align:center;color:#8b949e">
          <div style="font-size:1.5rem;margin-bottom:0.5rem">📋</div>
          <div style="font-weight:600;color:#e2e8f0">No activity yet</div>
          <div style="font-size:0.82rem;margin-top:0.3rem">Use any feature above and it will appear here</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="powered">✦ Powered by</div>
  <div class="name"><span>Akash Kumar Injeti</span></div>
  <div class="tagline">Data Science & AI · HealthGPT PRO · Python · Streamlit · Groq LLaMA 3.3 70B</div>
</div>
""", unsafe_allow_html=True)