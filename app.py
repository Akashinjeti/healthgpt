"""
╔══════════════════════════════════════════════════════════════╗
║        HealthGPT ULTRA — Full Product                        ║
║        Session 3 | by Akash Kumar Injeti                     ║
║        Login + Voice + News + 4 Languages + Landing Page     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import json
import hashlib
from datetime import datetime
import io

# ─────────────────────────────────────────────
#  PDF Generator (pure Python, no library)
# ─────────────────────────────────────────────
def generate_pdf_bytes(title, content, author="Akash Kumar Injeti"):
    """Generate a simple PDF as bytes using pure Python."""
    lines = []
    lines.append(f"HealthGPT ULTRA — {title}")
    lines.append(f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    lines.append(f"Powered by Akash Kumar Injeti | healthgptultra.streamlit.app")
    lines.append("=" * 60)
    lines.append("")
    # Clean content
    clean = content.replace("**", "").replace("*", "").replace("#", "")
    for line in clean.split("\n"):
        lines.append(line)
    lines.append("")
    lines.append("=" * 60)
    lines.append("DISCLAIMER: This is AI-generated health information for")
    lines.append("educational purposes only. Not a substitute for medical advice.")
    lines.append("Always consult a qualified doctor.")
    lines.append("=" * 60)
    lines.append(f"© HealthGPT ULTRA by Akash Kumar Injeti")

    full_text = "\n".join(lines)

    # Build minimal valid PDF
    objects = []

    # Object 1: Catalog
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")

    # Object 3: Font
    objects.append(b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n")

    # Object 4: Page content
    content_lines = []
    content_lines.append("BT")
    content_lines.append("/F1 10 Tf")
    content_lines.append("40 780 Td")
    content_lines.append("14 TL")
    for line in lines:
        safe = line.replace("\\","\\\\").replace("(","\\(").replace(")","\\)")
        safe = ''.join(c if ord(c) < 128 else '?' for c in safe)
        if len(safe) > 100:
            safe = safe[:100] + "..."
        content_lines.append(f"({safe}) Tj T*")
    content_lines.append("ET")
    content_str = "\n".join(content_lines).encode("latin-1", errors="replace")

    obj4 = b"4 0 obj\n<< /Length " + str(len(content_str)).encode() + b" >>\nstream\n"
    obj4 += content_str + b"\nendstream\nendobj\n"
    objects.append(obj4)

    # Object 2: Pages
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [5 0 R] /Count 1 >>\nendobj\n")

    # Object 5: Page
    objects.append(b"5 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Contents 4 0 R /Resources << /Font << /F1 3 0 R >> >> >>\nendobj\n")

    # Build PDF
    pdf = b"%PDF-1.4\n"
    offsets = []
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj

    xref_offset = len(pdf)
    pdf += b"xref\n"
    pdf += f"0 {len(objects)+1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for off in offsets:
        pdf += f"{off:010d} 00000 n \n".encode()

    pdf += b"trailer\n"
    pdf += f"<< /Size {len(objects)+1} /Root 1 0 R >>\n".encode()
    pdf += b"startxref\n"
    pdf += f"{xref_offset}\n".encode()
    pdf += b"%%EOF"

    return pdf

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
#  ULTRA CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

  html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', sans-serif; color: #e2e8f0;
  }
  .stApp { background: #0d1117; }
  [data-testid="stSidebar"] { background: #161b22 !important; border-right: 1px solid #30363d; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  .main .block-container { padding: 1.5rem 2rem; max-width: 980px; }

  /* ── Landing Page ── */
  .landing-hero {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 20px; padding: 4rem 2rem;
    text-align: center; margin-bottom: 2rem;
    position: relative; overflow: hidden;
  }
  .landing-hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #0ea5e9, #7c3aed, #22c55e, #f59e0b, #ef4444, #0ea5e9);
  }
  .landing-hero::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(14,165,233,0.08) 0%, transparent 70%);
    pointer-events: none;
  }
  .landing-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 700; line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #0ea5e9 50%, #7c3aed 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 1rem;
  }
  .landing-sub {
    font-size: 1.1rem; color: #8b949e;
    max-width: 560px; margin: 0 auto 2rem; line-height: 1.7;
  }
  .feature-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px; margin: 2rem 0;
  }
  .feature-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 1.25rem;
    text-align: center; transition: border-color 0.2s;
  }
  .feature-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
  .feature-title { font-weight: 600; font-size: 0.9rem; color: #e2e8f0; margin-bottom: 0.3rem; }
  .feature-desc  { font-size: 0.78rem; color: #8b949e; line-height: 1.5; }

  .stat-row {
    display: flex; gap: 16px; justify-content: center;
    flex-wrap: wrap; margin: 1.5rem 0;
  }
  .stat-item { text-align: center; }
  .stat-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem; font-weight: 700;
    background: linear-gradient(135deg, #0ea5e9, #7c3aed);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .stat-lbl { font-size: 0.75rem; color: #8b949e; }

  /* ── Auth Forms ── */
  .auth-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 16px; padding: 2rem;
    max-width: 420px; margin: 0 auto;
  }
  .auth-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem; font-weight: 700;
    color: #e2e8f0; margin-bottom: 0.3rem; text-align: center;
  }
  .auth-sub { font-size: 0.82rem; color: #8b949e; text-align: center; margin-bottom: 1.5rem; }

  /* ── App Header ── */
  .app-hero {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 16px; padding: 1.25rem 1.75rem;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 1rem;
  }
  .app-hero::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #0ea5e9, #7c3aed, #22c55e);
  }
  .app-title {
    font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0, #0ea5e9);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }

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
    background: #161b22 !important; border: 1px solid #30363d !important;
    border-radius: 10px !important; color: #e2e8f0 !important; font-size: 0.9rem !important;
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

  /* ── Message Cards ── */
  .ai-message {
    background: #161b22; border: 1px solid #30363d;
    border-left: 3px solid #0ea5e9; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #e2e8f0; white-space: pre-wrap;
  }
  .ai-message::before {
    content: '🤖 HealthGPT'; display: block; font-size: 0.68rem;
    color: #0ea5e9; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.75rem;
  }
  .emergency-message {
    background: #1a0a0a; border: 1px solid #7f1d1d;
    border-left: 3px solid #ef4444; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #fca5a5; white-space: pre-wrap;
  }
  .emergency-message::before {
    content: '🚨 Emergency Guide'; display: block; font-size: 0.68rem;
    color: #ef4444; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.75rem;
  }
  .diet-message {
    background: #0a1a0f; border: 1px solid #14532d;
    border-left: 3px solid #22c55e; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #86efac; white-space: pre-wrap;
  }
  .diet-message::before {
    content: '🥗 Diet Plan'; display: block; font-size: 0.68rem;
    color: #22c55e; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.75rem;
  }
  .medicine-message {
    background: #0f0a1a; border: 1px solid #4c1d95;
    border-left: 3px solid #7c3aed; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #c4b5fd; white-space: pre-wrap;
  }
  .medicine-message::before {
    content: '💊 Medicine Info'; display: block; font-size: 0.68rem;
    color: #7c3aed; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.75rem;
  }
  .pdf-message {
    background: #1a1400; border: 1px solid #78350f;
    border-left: 3px solid #f59e0b; border-radius: 12px;
    padding: 1.25rem 1.5rem; margin: 1rem 0;
    line-height: 1.85; font-size: 0.92rem; color: #fde68a; white-space: pre-wrap;
  }
  .pdf-message::before {
    content: '📄 Report Analysis'; display: block; font-size: 0.68rem;
    color: #f59e0b; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.75rem;
  }

  /* ── Chat ── */
  .chat-user {
    background: linear-gradient(135deg, rgba(14,165,233,0.12), rgba(124,58,237,0.12));
    border: 1px solid rgba(14,165,233,0.2); border-radius: 12px 12px 2px 12px;
    padding: 0.85rem 1.1rem; margin: 0.5rem 0 0.5rem 3rem;
    font-size: 0.92rem; color: #e2e8f0; line-height: 1.6;
  }
  .chat-user::before {
    content: '👤 You'; display: block; font-size: 0.65rem;
    color: #0ea5e9; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.4rem;
  }
  .chat-ai {
    background: #161b22; border: 1px solid #30363d;
    border-left: 3px solid #0ea5e9; border-radius: 12px 12px 12px 2px;
    padding: 0.85rem 1.1rem; margin: 0.5rem 3rem 0.5rem 0;
    font-size: 0.92rem; color: #e2e8f0; line-height: 1.7; white-space: pre-wrap;
  }
  .chat-ai::before {
    content: '🤖 HealthGPT'; display: block; font-size: 0.65rem;
    color: #0ea5e9; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.4rem;
  }

  /* ── News Card ── */
  .news-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 1.1rem 1.3rem;
    margin: 0.6rem 0; transition: border-color 0.2s;
  }
  .news-card:hover { border-color: #0ea5e9; }
  .news-title { font-weight: 600; font-size: 0.92rem; color: #e2e8f0; margin-bottom: 0.4rem; line-height: 1.4; }
  .news-meta  { font-size: 0.72rem; color: #8b949e; }
  .news-summary { font-size: 0.82rem; color: #8b949e; line-height: 1.6; margin-top: 0.4rem; }

  /* ── History ── */
  .history-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 1rem 1.25rem; margin: 0.5rem 0;
  }
  .h-date  { color: #0ea5e9; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em; }
  .h-type  { color: #e2e8f0; font-weight: 600; font-size: 0.9rem; margin: 2px 0; }
  .h-sum   { color: #8b949e; font-size: 0.82rem; margin-top: 3px; }

  /* ── Metric ── */
  .metric-box {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 1.1rem; text-align: center;
  }
  .metric-val   { font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; color:#0ea5e9; }
  .metric-label { font-size:0.72rem; color:#8b949e; text-transform:uppercase; letter-spacing:0.08em; margin-top:3px; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #161b22; border-radius: 10px;
    padding: 4px; gap: 4px; border: 1px solid #30363d;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #8b949e !important;
    border-radius: 8px !important; font-size: 0.8rem !important;
    font-weight: 500 !important; padding: 0.4rem 0.8rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(14,165,233,0.2), rgba(124,58,237,0.2)) !important;
    color: #e2e8f0 !important; border: 1px solid #30363d !important;
  }

  /* ── Voice box ── */
  .voice-box {
    background: #161b22; border: 2px dashed #30363d;
    border-radius: 14px; padding: 2rem; text-align: center;
    margin: 1rem 0;
  }

  /* ── Badge ── */
  .badge { font-size:0.7rem; font-weight:600; padding:3px 12px; border-radius:20px; border:1px solid; }
  .badge-blue   { background:rgba(14,165,233,0.1); color:#38bdf8; border-color:rgba(14,165,233,0.3); }
  .badge-purple { background:rgba(124,58,237,0.1); color:#a78bfa; border-color:rgba(124,58,237,0.3); }
  .badge-green  { background:rgba(34,197,94,0.1);  color:#4ade80; border-color:rgba(34,197,94,0.3); }
  .badge-red    { background:rgba(239,68,68,0.1);  color:#f87171; border-color:rgba(239,68,68,0.3); }
  .badge-amber  { background:rgba(251,191,36,0.1); color:#fbbf24; border-color:rgba(251,191,36,0.3); }
  .badge-row { display:flex; gap:8px; justify-content:center; flex-wrap:wrap; }

  /* ── Footer ── */
  .footer {
    margin-top:3rem; padding:1.5rem; background:#161b22;
    border:1px solid #30363d; border-radius:12px; text-align:center;
    position:relative; overflow:hidden;
  }
  .footer::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,#0ea5e9,#7c3aed,#22c55e,#f59e0b);
  }
  .footer .powered { color:#8b949e; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:5px; }
  .footer .name    { color:#e2e8f0; font-size:1.25rem; font-weight:700; font-family:'Space Grotesk',sans-serif; }
  .footer .name span { background:linear-gradient(135deg,rgba(14,165,233,0.15),rgba(124,58,237,0.15)); border:1px solid #30363d; padding:2px 16px; border-radius:20px; }
  .footer .tagline { color:#8b949e; font-size:0.75rem; margin-top:6px; }

  /* ── Download btn ── */
  .stDownloadButton > button {
    background:transparent !important; border:1px solid #30363d !important;
    color:#8b949e !important; border-radius:8px !important; font-size:0.8rem !important;
  }
  .stDownloadButton > button:hover { border-color:#0ea5e9 !important; color:#0ea5e9 !important; }

  /* ── File uploader ── */
  [data-testid="stFileUploader"] { background:#161b22 !important; border:2px dashed #30363d !important; border-radius:12px !important; }

  hr { border-color:#30363d !important; }
  #MainMenu { visibility:hidden; } footer { visibility:hidden; } header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Session State Init
# ─────────────────────────────────────────────
for key, default in {
    "page": "landing",
    "logged_in": False,
    "username": "",
    "users": {},
    "chat_history": [],
    "health_history": [],
    "voice_text": "",
    "api_key": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def save_history(entry_type, summary):
    st.session_state.health_history.append({
        "type": entry_type, "summary": summary,
        "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "user": st.session_state.username
    })

def call_groq(api_key, prompt, temperature=0.5, max_tokens=1500):
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile",
              "messages": [{"role": "user", "content": prompt}],
              "max_tokens": max_tokens, "temperature": temperature},
        timeout=40
    )
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"].strip()
    elif resp.status_code == 401: raise ValueError("Invalid API key.")
    elif resp.status_code == 429: raise ValueError("Rate limit hit. Please wait a few seconds.")
    else: raise ValueError(f"API error {resp.status_code}")

def call_groq_chat(api_key, messages):
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "messages": messages,
              "max_tokens": 800, "temperature": 0.7},
        timeout=40
    )
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"].strip()
    raise ValueError(f"API error {resp.status_code}")

LANG_OPTIONS = {
    "English": "Respond in simple English",
    "Telugu (తెలుగు)": "Respond in Telugu language",
    "Hindi (हिंदी)": "Respond in Hindi language",
    "Tamil (தமிழ்)": "Respond in Tamil language",
}


# ════════════════════════════════════════════
#  PAGE 1 — LANDING PAGE
# ════════════════════════════════════════════
if st.session_state.page == "landing":

    st.markdown("""
    <div class="landing-hero">
      <div style="font-size:3.5rem;margin-bottom:0.5rem">🏥</div>
      <div class="landing-title">HealthGPT</div>
      <div class="landing-sub">
        Your personal AI Health Assistant — built for India 🇮🇳<br>
        Free for everyone. Works in English, Telugu, Hindi & Tamil.
      </div>
      <div class="badge-row" style="margin-bottom:2rem">
        <span class="badge badge-green">✅ 100% Free</span>
        <span class="badge badge-blue">🤖 LLaMA 3.3 70B</span>
        <span class="badge badge-purple">🌍 4 Languages</span>
        <span class="badge badge-amber">📄 PDF Analyzer</span>
        <span class="badge badge-blue">💬 AI Chat</span>
        <span class="badge badge-red">⚠️ Not a doctor replacement</span>
      </div>
      <div class="stat-row">
        <div class="stat-item"><div class="stat-num">7+</div><div class="stat-lbl">AI Features</div></div>
        <div class="stat-item"><div class="stat-num">4</div><div class="stat-lbl">Languages</div></div>
        <div class="stat-item"><div class="stat-num">12</div><div class="stat-lbl">Emergency Guides</div></div>
        <div class="stat-item"><div class="stat-num">₹0</div><div class="stat-lbl">Cost</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature grid
    st.markdown("""
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon">🩺</div>
        <div class="feature-title">Symptom Checker</div>
        <div class="feature-desc">Describe symptoms — AI suggests possible causes & what to do</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">💊</div>
        <div class="feature-title">Medicine Info</div>
        <div class="feature-desc">Search any medicine — plain language explanation instantly</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🥗</div>
        <div class="feature-title">Diet Planner</div>
        <div class="feature-desc">Personalized Indian diet plans for 9 health conditions</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">PDF Analyzer</div>
        <div class="feature-desc">Upload blood test report — AI explains it simply</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">AI Chat Mode</div>
        <div class="feature-desc">Talk to HealthGPT like ChatGPT — ask anything</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🚨</div>
        <div class="feature-title">Emergency Guide</div>
        <div class="feature-desc">Step-by-step first aid for 12 medical emergencies</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🧮</div>
        <div class="feature-title">BMI Calculator</div>
        <div class="feature-desc">Calculate BMI + get personalized AI health tips</div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📰</div>
        <div class="feature-title">Health News</div>
        <div class="feature-desc">Latest AI-curated health news and medical updates</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀  Get Started — It's Free", use_container_width=True, type="primary"):
            st.session_state.page = "auth"
            st.rerun()
        st.markdown("<div style='text-align:center;font-size:0.78rem;color:#8b949e;margin-top:0.5rem'>No credit card • No signup fees • Open source</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      <div class="powered">✦ Powered by</div>
      <div class="name"><span>Akash Kumar Injeti</span></div>
      <div class="tagline">Data Science & AI · HealthGPT ULTRA · Python · Streamlit · Groq LLaMA 3.3 70B</div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════
#  PAGE 2 — AUTH (Login / Signup)
# ════════════════════════════════════════════
elif st.session_state.page == "auth":

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div style="text-align:center;margin-bottom:1.5rem">
          <div style="font-size:2rem">🏥</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:700;
            background:linear-gradient(135deg,#e2e8f0,#0ea5e9);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent">HealthGPT</div>
        </div>
        """, unsafe_allow_html=True)

        auth_tab1, auth_tab2 = st.tabs(["🔑  Login", "✨  Sign Up"])

        with auth_tab1:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Username</div>', unsafe_allow_html=True)
            login_user = st.text_input("LUser", placeholder="Enter your username", label_visibility="collapsed", key="lu")
            st.markdown('<div class="section-label">Password</div>', unsafe_allow_html=True)
            login_pass = st.text_input("LPass", type="password", placeholder="Enter your password", label_visibility="collapsed", key="lp")
            st.markdown('<div class="section-label">🔑 Groq API Key</div>', unsafe_allow_html=True)
            login_api = st.text_input("LApi", type="password", placeholder="gsk_... (get free at console.groq.com)", label_visibility="collapsed", key="la")
            st.markdown("<div style='font-size:0.72rem;color:#8b949e'>Free API key at <a href='https://console.groq.com' target='_blank' style='color:#0ea5e9'>console.groq.com</a> — no credit card needed</div>", unsafe_allow_html=True)

            if st.button("🔑  Login", use_container_width=True, type="primary", key="login_btn"):
                if not login_api:
                    st.error("⚠️  Please enter your Groq API key.")
                else:
                    users = st.session_state.users
                    if login_user in users and users[login_user]["password"] == hash_pw(login_pass):
                        st.session_state.logged_in = True
                        st.session_state.username = login_user
                        st.session_state.api_key = login_api
                        st.session_state.page = "app"
                        st.rerun()
                    elif login_user == "demo" and login_pass == "demo123":
                        st.session_state.logged_in = True
                        st.session_state.username = "Demo User"
                        st.session_state.api_key = login_api
                        st.session_state.page = "app"
                        st.rerun()
                    else:
                        st.error("❌  Invalid username or password.")

            st.markdown("<div style='font-size:0.78rem;color:#8b949e;text-align:center;margin-top:0.5rem'>Demo: username <b style='color:#0ea5e9'>demo</b> / password <b style='color:#0ea5e9'>demo123</b></div>", unsafe_allow_html=True)

        with auth_tab2:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Full Name</div>', unsafe_allow_html=True)
            reg_name = st.text_input("RName", placeholder="e.g. Akash Kumar", label_visibility="collapsed", key="rn")
            st.markdown('<div class="section-label">Username</div>', unsafe_allow_html=True)
            reg_user = st.text_input("RUser", placeholder="Choose a username", label_visibility="collapsed", key="ru")
            st.markdown('<div class="section-label">Password</div>', unsafe_allow_html=True)
            reg_pass = st.text_input("RPass", type="password", placeholder="Choose a password", label_visibility="collapsed", key="rp")
            st.markdown('<div class="section-label">🔑 Groq API Key</div>', unsafe_allow_html=True)
            reg_api = st.text_input("RApi", type="password", placeholder="gsk_... (get free at console.groq.com)", label_visibility="collapsed", key="ra")
            st.markdown("<div style='font-size:0.72rem;color:#8b949e'>Free at <a href='https://console.groq.com' target='_blank' style='color:#0ea5e9'>console.groq.com</a></div>", unsafe_allow_html=True)

            if st.button("✨  Create Account", use_container_width=True, type="primary", key="reg_btn"):
                if not reg_name or not reg_user or not reg_pass:
                    st.error("⚠️  Please fill in all fields.")
                elif not reg_api:
                    st.error("⚠️  Please enter your Groq API key.")
                elif reg_user in st.session_state.users:
                    st.error("❌  Username already taken.")
                elif len(reg_pass) < 4:
                    st.error("⚠️  Password must be at least 4 characters.")
                else:
                    st.session_state.users[reg_user] = {
                        "name": reg_name, "password": hash_pw(reg_pass)
                    }
                    st.session_state.logged_in = True
                    st.session_state.username = reg_user
                    st.session_state.api_key = reg_api
                    st.session_state.page = "app"
                    st.success(f"🎉 Welcome {reg_name}!")
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", use_container_width=True, key="back_btn"):
            st.session_state.page = "landing"
            st.rerun()


# ════════════════════════════════════════════
#  PAGE 3 — MAIN APP
# ════════════════════════════════════════════
elif st.session_state.page == "app":

    # ── Sidebar ──
    with st.sidebar:
        user_display = st.session_state.users.get(
            st.session_state.username, {}
        ).get("name", st.session_state.username)

        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 1.5rem">
          <div style="font-size:2.5rem">🏥</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;
            background:linear-gradient(135deg,#0ea5e9,#7c3aed);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent">HealthGPT</div>
          <div style="font-size:0.72rem;color:#8b949e;margin-top:2px">AI Health Assistant</div>
        </div>
        <div style="background:#0d1117;border:1px solid #30363d;border-radius:10px;
          padding:0.75rem 1rem;margin-bottom:1rem;text-align:center">
          <div style="font-size:1.2rem">👤</div>
          <div style="font-size:0.88rem;font-weight:600;color:#e2e8f0">{user_display}</div>
          <div style="font-size:0.72rem;color:#0ea5e9">@{st.session_state.username}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">🔑 API Key</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:8px 12px;font-size:0.78rem;color:#4ade80'>✅ API Key connected</div>", unsafe_allow_html=True)
        if st.button("🔄 Change API Key", key="change_api", use_container_width=True):
            st.session_state.page = "auth"
            st.session_state.logged_in = False
            st.rerun()
        api_key = st.session_state.api_key

        st.divider()

        st.markdown('<div class="section-label">🌍 Language / भाषा / భాష</div>', unsafe_allow_html=True)
        lang = st.selectbox("Lang", list(LANG_OPTIONS.keys()), label_visibility="collapsed")
        lang_inst = LANG_OPTIONS[lang]

        st.divider()

        st.markdown("""
        <div style="font-size:0.78rem;color:#8b949e;line-height:2.2">
          <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#ef4444;margin-bottom:4px">🚨 Emergency</div>
          🚑 <strong style="color:#f87171">108</strong> Ambulance<br>
          🚔 <strong style="color:#f87171">100</strong> Police<br>
          🆘 <strong style="color:#f87171">112</strong> National
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        hist_count = len([h for h in st.session_state.health_history if h.get("user") == st.session_state.username])
        st.markdown(f"<div style='font-size:0.78rem;color:#8b949e'>📋 Your history: <strong style='color:#0ea5e9'>{hist_count}</strong> entries<br>💬 Chat: <strong style='color:#7c3aed'>{len(st.session_state.chat_history)}</strong> messages</div>", unsafe_allow_html=True)

        st.divider()

        if st.button("🚪  Logout", use_container_width=True, key="logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.chat_history = []
            st.session_state.page = "landing"
            st.rerun()

    # ── App Header ──
    st.markdown(f"""
    <div class="app-hero">
      <div>
        <div class="app-title">🏥 HealthGPT ULTRA</div>
        <div style="font-size:0.78rem;color:#8b949e">Welcome back, <strong style="color:#0ea5e9">{user_display}</strong></div>
      </div>
      <div class="badge-row">
        <span class="badge badge-green">✅ Free</span>
        <span class="badge badge-blue">🤖 LLaMA 3.3</span>
        <span class="badge badge-purple">{lang.split()[0]}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 8 Tabs ──
    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([
        "🩺 Symptoms","💊 Medicine","🥗 Diet",
        "🚨 Emergency","📄 PDF","💬 Chat",
        "📰 News","📊 Dashboard"
    ])

    # ── TAB 1 Symptoms ──
    with tab1:
        st.markdown("#### 🩺 Symptom Checker")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Describe your symptoms — AI suggests possible causes and next steps.</span>", unsafe_allow_html=True)
        st.markdown("")
        symptoms = st.text_area("Sym", placeholder="e.g. headache, fever, cough for 3 days...", label_visibility="collapsed", height=100)
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown('<div class="section-label">Age</div>', unsafe_allow_html=True)
            age = st.number_input("Age",1,100,25,label_visibility="collapsed")
        with c2:
            st.markdown('<div class="section-label">Gender</div>', unsafe_allow_html=True)
            gender = st.selectbox("Gen",["Male","Female","Other"],label_visibility="collapsed")
        with c3:
            st.markdown('<div class="section-label">Duration</div>', unsafe_allow_html=True)
            dur = st.selectbox("Dur",["Today","2-3 Days","1 Week","1+ Month"],label_visibility="collapsed")
        if st.button("🩺  Analyze Symptoms", use_container_width=True, type="primary", key="sym_b"):
            if not api_key: st.error("⚠️  Enter API key in sidebar.")
            elif not symptoms: st.error("⚠️  Describe your symptoms.")
            else:
                prompt = f"""{lang_inst}. You are a helpful medical information assistant.
Patient: Age {age}, {gender}, symptoms for {dur}. Symptoms: {symptoms}
Provide:
1. 🔍 Possible Conditions (3-4 likely causes)
2. 📋 What These Symptoms May Mean
3. 🏠 Home Care Tips
4. ⚠️ Warning Signs — when to see a doctor immediately
5. 👨‍⚕️ Which specialist to visit
End with: This is AI information only — not a substitute for professional medical advice."""
                with st.spinner("🤖 Analyzing..."):
                    try:
                        r = call_groq(api_key, prompt)
                        st.markdown(f'<div class="ai-message">{r}</div>', unsafe_allow_html=True)
                        save_history("🩺 Symptom Check", f"{symptoms[:60]}...")
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button("⬇️ Download TXT", data=r.encode(), file_name="symptom_report.txt", mime="text/plain", key="sym_txt")
                        with col_dl2:
                            pdf_bytes = generate_pdf_bytes("Symptom Report", r)
                            st.download_button("📄 Download PDF", data=pdf_bytes, file_name="symptom_report.pdf", mime="application/pdf", key="sym_pdf")
                    except Exception as e: st.error(f"❌ {e}")

    # ── TAB 2 Medicine ──
    with tab2:
        st.markdown("#### 💊 Medicine Information")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Type any medicine — AI explains it in plain language.</span>", unsafe_allow_html=True)
        st.markdown("")
        med = st.text_input("Med", placeholder="e.g. Paracetamol, Dolo 650, Metformin...", label_visibility="collapsed")
        if st.button("💊  Get Medicine Info", use_container_width=True, type="primary", key="med_b"):
            if not api_key: st.error("⚠️  Enter API key in sidebar.")
            elif not med: st.error("⚠️  Enter a medicine name.")
            else:
                prompt = f"""{lang_inst}. You are a helpful pharmacist assistant.
Explain the medicine: {med}
1. 💊 What is it? 2. 🎯 Uses 3. 📏 Dosage 4. ⚠️ Side Effects
5. 🚫 Who should avoid it 6. 🍽️ With/without food 7. 💡 Tips
Always: Follow doctor's prescription."""
                with st.spinner("🤖 Fetching info..."):
                    try:
                        r = call_groq(api_key, prompt)
                        st.markdown(f'<div class="medicine-message">{r}</div>', unsafe_allow_html=True)
                        save_history("💊 Medicine Info", f"Medicine: {med}")
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button("⬇️ Download TXT", data=r.encode(), file_name=f"{med}_info.txt", mime="text/plain", key="med_txt")
                        with col_dl2:
                            pdf_bytes = generate_pdf_bytes(f"Medicine Info — {med}", r)
                            st.download_button("📄 Download PDF", data=pdf_bytes, file_name=f"{med}_info.pdf", mime="application/pdf", key="med_pdf")
                    except Exception as e: st.error(f"❌ {e}")

    # ── TAB 3 Diet ──
    with tab3:
        st.markdown("#### 🥗 Personalized Diet Planner")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Get a personalized Indian diet plan based on your health condition.</span>", unsafe_allow_html=True)
        st.markdown("")
        cd1,cd2 = st.columns(2)
        with cd1:
            st.markdown('<div class="section-label">Age</div>', unsafe_allow_html=True)
            da = st.number_input("DA",1,100,25,label_visibility="collapsed",key="da")
            st.markdown('<div class="section-label">Weight (kg)</div>', unsafe_allow_html=True)
            wt = st.number_input("Wt",20,200,70,label_visibility="collapsed")
        with cd2:
            st.markdown('<div class="section-label">Gender</div>', unsafe_allow_html=True)
            dg = st.selectbox("DG",["Male","Female"],label_visibility="collapsed",key="dg")
            st.markdown('<div class="section-label">Height (cm)</div>', unsafe_allow_html=True)
            ht = st.number_input("Ht",100,250,165,label_visibility="collapsed")
        st.markdown('<div class="section-label">Health Condition</div>', unsafe_allow_html=True)
        cond = st.selectbox("Cond",["Healthy","Diabetes","High Blood Pressure","Weight Loss","Weight Gain","Thyroid","Heart Disease","Anemia","PCOD/PCOS"],label_visibility="collapsed")
        st.markdown('<div class="section-label">Food Preference</div>', unsafe_allow_html=True)
        fp = st.selectbox("FP",["Vegetarian","Non-Vegetarian","Eggetarian"],label_visibility="collapsed")
        if st.button("🥗  Generate Diet Plan", use_container_width=True, type="primary", key="diet_b"):
            if not api_key: st.error("⚠️  Enter API key in sidebar.")
            else:
                prompt = f"""{lang_inst}. You are a certified Indian nutritionist.
1-day Indian diet plan: Age {da}, {dg}, {wt}kg, {ht}cm, {cond}, {fp}
🌅 Early Morning | 🍳 Breakfast | 🥤 Mid Morning | 🍱 Lunch | ☕ Evening | 🌙 Dinner
💧 Water intake | ❌ Avoid | ✅ Superfoods | 💡 3 Tips. Use common Indian foods only."""
                with st.spinner("🤖 Creating plan..."):
                    try:
                        r = call_groq(api_key, prompt)
                        st.markdown(f'<div class="diet-message">{r}</div>', unsafe_allow_html=True)
                        save_history("🥗 Diet Plan", f"{cond} | {fp}")
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button("⬇️ Download TXT", data=r.encode(), file_name="diet_plan.txt", mime="text/plain", key="diet_txt")
                        with col_dl2:
                            pdf_bytes = generate_pdf_bytes("My Personalized Diet Plan", r)
                            st.download_button("📄 Download PDF", data=pdf_bytes, file_name="diet_plan.pdf", mime="application/pdf", key="diet_pdf")
                    except Exception as e: st.error(f"❌ {e}")

    # ── TAB 4 Emergency ──
    with tab4:
        st.markdown("#### 🚨 Emergency First Aid Guide")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Instant step-by-step first aid before the doctor arrives.</span>", unsafe_allow_html=True)
        st.markdown("")
        etype = st.selectbox("Etype",["Heart Attack","Stroke","Choking","Severe Burns","Fracture","Fainting","Severe Bleeding","Seizure","Allergic Reaction","Snake Bite","Drowning","Electric Shock"],label_visibility="collapsed")
        if st.button("🚨  Get Emergency Guide", use_container_width=True, type="primary", key="emg_b"):
            if not api_key: st.error("⚠️  Enter API key in sidebar.")
            else:
                prompt = f"""{lang_inst}. Emergency first aid for: {etype}
🚨 CALL 108 IMMEDIATELY
⚡ FIRST 60 SECONDS (3-4 actions)
📋 STEP BY STEP FIRST AID (numbered)
❌ DO NOT DO THESE
✅ WHILE WAITING FOR AMBULANCE
Simple language — no medical training required."""
                with st.spinner("🚨 Loading..."):
                    try:
                        r = call_groq(api_key, prompt)
                        st.markdown(f'<div class="emergency-message">{r}</div>', unsafe_allow_html=True)
                        save_history("🚨 Emergency", f"{etype}")
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button("⬇️ Download TXT", data=r.encode(), file_name="emergency_guide.txt", mime="text/plain", key="emg_txt")
                        with col_dl2:
                            pdf_bytes = generate_pdf_bytes(f"Emergency Guide — {etype}", r)
                            st.download_button("📄 Download PDF", data=pdf_bytes, file_name="emergency_guide.pdf", mime="application/pdf", key="emg_pdf")
                    except Exception as e: st.error(f"❌ {e}")
        st.markdown("""<div style="background:#1a0a0a;border:1px solid #7f1d1d;border-radius:12px;padding:1rem;margin-top:1rem;font-size:0.88rem;color:#fca5a5;line-height:2">
        🚑 <strong>108</strong> Ambulance &nbsp;|&nbsp; 🚔 <strong>100</strong> Police &nbsp;|&nbsp; 🚒 <strong>101</strong> Fire &nbsp;|&nbsp; 🆘 <strong>112</strong> National</div>""", unsafe_allow_html=True)

    # ── TAB 5 PDF ──
    with tab5:
        st.markdown("#### 📄 Medical Report Analyzer")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Upload blood test / medical report — AI explains it in simple language.</span>", unsafe_allow_html=True)
        st.markdown("")
        uploaded = st.file_uploader("Upload", type=["pdf","txt"], label_visibility="collapsed")
        if uploaded:
            st.success(f"✅  Uploaded: **{uploaded.name}**")
            rtype = st.selectbox("Report Type",["Blood Test / CBC","Liver Function (LFT)","Kidney Function (KFT)","Thyroid Test","Diabetes / HbA1c","Lipid Profile","Urine Test","General Report"])
            page_age = st.number_input("Patient Age",1,100,25,key="page_age")
            if st.button("📄  Analyze Report", use_container_width=True, type="primary", key="pdf_b"):
                if not api_key: st.error("⚠️  Enter API key in sidebar.")
                else:
                    try:
                        raw = uploaded.read()
                        content = raw.decode("utf-8", errors="ignore") if uploaded.type=="text/plain" else \
                            ' '.join(''.join(c if c.isprintable() else ' ' for c in raw[i:i+1000].decode("latin-1",errors="ignore")) for i in range(0,len(raw),1000))[:4000]
                        prompt = f"""{lang_inst}. You are a medical report interpreter.
Report: {rtype}, Patient Age: {page_age}
Content: {content[:3000]}
1. 📋 Summary 2. ✅ Normal Values 3. ⚠️ Abnormal Values & meaning
4. 🎯 What this means for patient 5. 💊 Recommendations 6. 👨‍⚕️ See a doctor?
Simple language. End with: Please consult a doctor for proper diagnosis."""
                        with st.spinner("📄 Analyzing..."):
                            r = call_groq(api_key, prompt, max_tokens=2000)
                            st.markdown(f'<div class="pdf-message">{r}</div>', unsafe_allow_html=True)
                            save_history("📄 Report Analysis", f"{rtype}")
                            col_dl1, col_dl2 = st.columns(2)
                            with col_dl1:
                                st.download_button("⬇️ Download TXT", data=r.encode(), file_name="report_analysis.txt", mime="text/plain", key="pdf_txt")
                            with col_dl2:
                                pdf_bytes = generate_pdf_bytes(f"Medical Report Analysis — {rtype}", r)
                                st.download_button("📄 Download PDF", data=pdf_bytes, file_name="report_analysis.pdf", mime="application/pdf", key="pdf_pdf")
                    except Exception as e: st.error(f"❌ {e}")

    # ── TAB 6 Chat ──
    with tab6:
        st.markdown("#### 💬 Chat with HealthGPT")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>Ask any health question — like talking to a knowledgeable doctor friend.</span>", unsafe_allow_html=True)
        st.markdown("")

        # Voice Input Section
        st.markdown("""
        <div class="voice-box">
          <div style="font-size:1.5rem;margin-bottom:0.5rem">🎤</div>
          <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.3rem">Voice Input</div>
          <div style="font-size:0.82rem;color:#8b949e">Click the mic button below → speak your question → it appears in the text box</div>
        </div>
        """, unsafe_allow_html=True)

        # HTML5 voice recognition
        st.components.v1.html("""
        <div style="text-align:center;padding:0.5rem">
          <button id="micBtn" onclick="startListening()" style="
            background:linear-gradient(135deg,#0ea5e9,#7c3aed);
            color:white;border:none;border-radius:50px;
            padding:12px 28px;font-size:14px;font-weight:600;
            cursor:pointer;font-family:Inter,sans-serif">
            🎤 Start Speaking
          </button>
          <div id="status" style="margin-top:10px;font-size:13px;color:#8b949e;font-family:Inter,sans-serif"></div>
          <div id="result" style="margin-top:8px;background:#161b22;border:1px solid #30363d;
            border-radius:8px;padding:10px;font-size:13px;color:#e2e8f0;
            font-family:Inter,sans-serif;display:none;min-height:40px"></div>
          <button id="copyBtn" onclick="copyToClipboard()" style="
            display:none;margin-top:8px;
            background:transparent;color:#0ea5e9;
            border:1px solid #0ea5e9;border-radius:8px;
            padding:6px 16px;font-size:12px;cursor:pointer;
            font-family:Inter,sans-serif">
            📋 Copy to input below
          </button>
        </div>
        <script>
        let recognition;
        let finalText = '';
        function startListening() {
          if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            document.getElementById('status').innerText = '❌ Voice not supported. Use Chrome browser.';
            return;
          }
          recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
          recognition.lang = 'en-IN';
          recognition.continuous = false;
          recognition.interimResults = true;
          document.getElementById('status').innerText = '🔴 Listening... speak now';
          document.getElementById('micBtn').innerText = '⏹ Stop';
          document.getElementById('result').style.display = 'block';
          recognition.onresult = function(e) {
            let interim = '';
            for (let i = e.resultIndex; i < e.results.length; i++) {
              if (e.results[i].isFinal) finalText += e.results[i][0].transcript;
              else interim += e.results[i][0].transcript;
            }
            document.getElementById('result').innerText = finalText || interim;
          };
          recognition.onend = function() {
            document.getElementById('status').innerText = '✅ Done! Copy text below to chat input.';
            document.getElementById('micBtn').innerText = '🎤 Start Speaking';
            if (finalText) document.getElementById('copyBtn').style.display = 'inline-block';
          };
          recognition.onerror = function(e) {
            document.getElementById('status').innerText = '❌ Error: ' + e.error + '. Try again.';
            document.getElementById('micBtn').innerText = '🎤 Start Speaking';
          };
          recognition.start();
        }
        function copyToClipboard() {
          navigator.clipboard.writeText(finalText).then(() => {
            document.getElementById('status').innerText = '✅ Copied! Now paste it in the chat box below (Ctrl+V)';
          });
        }
        </script>
        """, height=200)

        st.divider()

        # Chat history display
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                css = "chat-user" if msg["role"] == "user" else "chat-ai"
                st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

        # Suggestions
        st.markdown("<div style='font-size:0.72rem;color:#8b949e;margin-top:1rem;letter-spacing:0.08em;text-transform:uppercase'>💡 Quick Questions</div>", unsafe_allow_html=True)
        sug_cols = st.columns(3)
        for i, sug in enumerate(["What foods help diabetes?","How to sleep better?","Signs of vitamin deficiency?"]):
            with sug_cols[i]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state["chat_pre"] = sug

        prefill = st.session_state.pop("chat_pre", "")
        user_in = st.text_input("ChatIn", value=prefill, placeholder="Type or paste your health question here...", label_visibility="collapsed", key="chat_in")

        cs1, cs2 = st.columns([4,1])
        with cs1:
            send = st.button("💬  Send", use_container_width=True, type="primary", key="chat_s")
        with cs2:
            if st.button("🗑️", use_container_width=True, key="chat_clr"):
                st.session_state.chat_history = []
                st.rerun()

        if send and user_in:
            if not api_key: st.error("⚠️  Enter API key in sidebar.")
            else:
                system = {"role":"system","content":f"""You are HealthGPT, a friendly AI health assistant for India.
{lang_inst}. Be warm and caring. Give practical easy-to-understand advice.
Always remind users to consult a real doctor for serious concerns.
Keep responses concise and easy to read."""}
                st.session_state.chat_history.append({"role":"user","content":user_in})
                msgs = [system] + st.session_state.chat_history
                with st.spinner("🤖 Thinking..."):
                    try:
                        reply = call_groq_chat(api_key, msgs)
                        st.session_state.chat_history.append({"role":"assistant","content":reply})
                        st.rerun()
                    except Exception as e: st.error(f"❌ {e}")

    # ── TAB 7 Health News ──
    with tab7:
        st.markdown("#### 📰 Health News & Updates")
        st.markdown("<span style='color:#8b949e;font-size:0.88rem'>AI-generated latest health news, tips, and medical updates for India.</span>", unsafe_allow_html=True)
        st.markdown("")

        news_cat = st.selectbox("Category", [
            "General Health News", "Diabetes & Lifestyle",
            "Heart Health", "Mental Health & Stress",
            "Women's Health", "Child Health",
            "COVID & Infectious Diseases", "Nutrition & Diet",
            "Cancer Awareness", "Ayurveda & Natural Remedies"
        ])

        if st.button("📰  Load Health News", use_container_width=True, type="primary", key="news_b"):
            if not api_key: st.error("⚠️  Enter API key in sidebar.")
            else:
                prompt = f"""{lang_inst}. You are a health journalist writing for India.

Generate 5 realistic, informative health news items about: {news_cat}

For each news item use this exact format:
TITLE: [Catchy news headline]
DATE: [Recent date in 2025]
SOURCE: [Realistic source like AIIMS, WHO India, ICMR, Ministry of Health]
SUMMARY: [2-3 sentence summary of the news]
TIP: [One practical tip for readers]
---

Make the news educational, factual, and helpful for common Indians.
Focus on actionable health information."""

                with st.spinner("📰 Loading health news..."):
                    try:
                        raw = call_groq(api_key, prompt, temperature=0.8, max_tokens=2000)
                        items = raw.split("---")
                        for item in items:
                            if not item.strip(): continue
                            lines = {k.strip():v.strip() for line in item.strip().split("\n") if ":" in line for k,v in [line.split(":",1)]}
                            title   = lines.get("TITLE","Health Update")
                            date    = lines.get("DATE","2025")
                            source  = lines.get("SOURCE","Health Ministry")
                            summary = lines.get("SUMMARY","")
                            tip     = lines.get("TIP","")
                            st.markdown(f"""
                            <div class="news-card">
                              <div class="news-title">{title}</div>
                              <div class="news-meta">📅 {date} &nbsp;·&nbsp; 🏥 {source}</div>
                              <div class="news-summary">{summary}</div>
                              {"<div style='margin-top:0.5rem;font-size:0.8rem;color:#4ade80'>💡 " + tip + "</div>" if tip else ""}
                            </div>
                            """, unsafe_allow_html=True)
                        save_history("📰 Health News", f"Category: {news_cat}")
                    except Exception as e: st.error(f"❌ {e}")

    # ── TAB 8 Dashboard ──
    with tab8:
        st.markdown("#### 📊 My Health Dashboard")
        st.markdown("")

        # BMI
        st.markdown("##### 🧮 BMI Calculator")
        b1,b2,b3 = st.columns(3)
        with b1:
            st.markdown('<div class="section-label">Weight kg</div>', unsafe_allow_html=True)
            bw = st.number_input("BW",20,200,70,label_visibility="collapsed",key="bw")
        with b2:
            st.markdown('<div class="section-label">Height cm</div>', unsafe_allow_html=True)
            bh = st.number_input("BH",100,250,170,label_visibility="collapsed",key="bh")
        with b3:
            st.markdown('<div class="section-label">Age</div>', unsafe_allow_html=True)
            ba = st.number_input("BA",1,100,25,label_visibility="collapsed",key="ba")

        if st.button("🧮  Calculate BMI", use_container_width=True, type="primary", key="bmi_b"):
            bmi = round(bw / ((bh/100)**2), 1)
            if bmi < 18.5:   cat,col,emoji = "Underweight","#38bdf8","⚠️"
            elif bmi < 25:   cat,col,emoji = "Normal Weight","#4ade80","✅"
            elif bmi < 30:   cat,col,emoji = "Overweight","#fbbf24","⚠️"
            else:            cat,col,emoji = "Obese","#f87171","❌"
            ideal_min = round(18.5*(bh/100)**2,1)
            ideal_max = round(24.9*(bh/100)**2,1)
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.3);border:1px solid {col}44;border-radius:14px;
              padding:1.5rem;text-align:center;margin:1rem 0">
              <div style="font-family:'Space Grotesk',sans-serif;font-size:3.5rem;
                font-weight:700;color:{col};line-height:1">{bmi}</div>
              <div style="font-size:1rem;font-weight:700;color:{col};margin-top:0.3rem">{emoji} {cat}</div>
              <div style="font-size:0.82rem;color:#8b949e;margin-top:0.5rem">
                Ideal weight: <strong style="color:#e2e8f0">{ideal_min}–{ideal_max} kg</strong>
              </div>
            </div>
            """, unsafe_allow_html=True)
            m1,m2,m3,m4 = st.columns(4)
            diff = round(bw-ideal_min,1)
            for col_w, val, lbl in [(m1,str(bmi),"BMI"),(m2,f"{bw}kg","Weight"),(m3,f"{bh}cm","Height"),(m4,f"{'+' if diff>0 else ''}{diff}kg","From Ideal")]:
                with col_w:
                    st.markdown(f'<div class="metric-box"><div class="metric-val">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)
            if api_key:
                with st.spinner("🤖 Getting tips..."):
                    try:
                        tips = call_groq(api_key, f"{lang_inst}. Give 5 specific health tips for age {ba}, BMI {bmi} ({cat}). Be practical.", max_tokens=500)
                        st.markdown(f'<div class="ai-message">{tips}</div>', unsafe_allow_html=True)
                        save_history("🧮 BMI Check", f"BMI: {bmi} — {cat}")
                        bmi_report = f"BMI Score: {bmi}\nCategory: {cat}\nWeight: {bw}kg | Height: {bh}cm | Age: {ba}\nIdeal Weight Range: {ideal_min}–{ideal_max}kg\n\nAI Health Tips:\n{tips}"
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button("⬇️ Download TXT", data=bmi_report.encode(), file_name="bmi_report.txt", mime="text/plain", key="bmi_txt")
                        with col_dl2:
                            pdf_bytes = generate_pdf_bytes("BMI Report & Health Tips", bmi_report)
                            st.download_button("📄 Download PDF", data=pdf_bytes, file_name="bmi_report.pdf", mime="application/pdf", key="bmi_pdf")
                    except: pass

        st.divider()

        # History
        st.markdown("##### 📋 Your Health History")
        my_history = [h for h in st.session_state.health_history if h.get("user") == st.session_state.username]

        if my_history:
            if st.button("🗑️  Clear History", key="clr_hist"):
                st.session_state.health_history = [h for h in st.session_state.health_history if h.get("user") != st.session_state.username]
                st.rerun()
            # Export all history
            export_text = "\n\n".join([f"{h['time']}\n{h['type']}\n{h['summary']}" for h in reversed(my_history)])
            st.download_button("⬇️ Export All History", data=export_text.encode(), file_name="health_history.txt", mime="text/plain")
            for h in reversed(my_history):
                st.markdown(f"""
                <div class="history-card">
                  <div class="h-date">🕐 {h['time']}</div>
                  <div class="h-type">{h['type']}</div>
                  <div class="h-sum">{h['summary']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#161b22;border:1px solid #30363d;border-radius:12px;
              padding:2rem;text-align:center;color:#8b949e">
              <div style="font-size:1.5rem;margin-bottom:0.5rem">📋</div>
              <div style="font-weight:600;color:#e2e8f0">No activity yet</div>
              <div style="font-size:0.82rem;margin-top:0.3rem">Use any feature and it appears here</div>
            </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
      <div class="powered">✦ Powered by</div>
      <div class="name"><span>Akash Kumar Injeti</span></div>
      <div class="tagline">Data Science & AI · HealthGPT ULTRA · Python · Streamlit · Groq LLaMA 3.3 70B</div>
    </div>
    """, unsafe_allow_html=True)