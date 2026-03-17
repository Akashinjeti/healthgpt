"""
╔══════════════════════════════════════════════════════════════╗
║        HealthGPT ULTRA — Session 4 HYBRID                    ║
║        by Akash Kumar Injeti                                 ║
║        All Session 3 Features + Supabase + OAuth + Scanner   ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import json
import hashlib
import os
from datetime import datetime
import io
import base64
import re

# ─────────────────────────────────────────────
#  SUPABASE SETUP (NEW)
# ─────────────────────────────────────────────
try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except:
    SUPABASE_AVAILABLE = False

def init_supabase():
    """Initialize Supabase - with fallback to JSON if unavailable"""
    if not SUPABASE_AVAILABLE:
        return None
    
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            return create_client(url, key)
    except:
        pass
    return None

# ─────────────────────────────────────────────
#  GOOGLE OAUTH SETUP (NEW)
# ─────────────────────────────────────────────
def get_google_oauth_url():
    """Generate Google OAuth URL"""
    try:
        client_id = st.secrets.get("GOOGLE_CLIENT_ID")
        redirect_uri = "https://healthgptultra.streamlit.app/"
        scope = "openid profile email"
        oauth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}"
        )
        return oauth_url
    except:
        return None

# ─────────────────────────────────────────────
#  GROQ AI SETUP (from Session 3)
# ─────────────────────────────────────────────
def get_groq_response(prompt, system_prompt=None):
    """Get response from GROQ API"""
    try:
        groq_key = st.secrets.get("GROQ_KEY")
        if not groq_key:
            return "⚠️ GROQ_KEY not configured in secrets"
        
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "mixtral-8x7b-32768",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ GROQ API Error: {response.status_code}"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ─────────────────────────────────────────────
#  PERSISTENT USER STORAGE (Session 3 - KEPT)
# ─────────────────────────────────────────────
USERS_FILE = "users_db.json"
HISTORY_FILE = "history_db.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except: 
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except: 
            return []
    return []

def save_history_file(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ─────────────────────────────────────────────
#  SUPABASE FUNCTIONS (NEW)
# ─────────────────────────────────────────────
def save_to_supabase(supabase, user_email, message, role="user"):
    """Save chat message to Supabase"""
    if not supabase:
        return False
    try:
        supabase.table("chat_history").insert({
            "email": user_email,
            "message": message,
            "role": role,
            "timestamp": datetime.now().isoformat()
        }).execute()
        return True
    except:
        return False

def get_supabase_history(supabase, user_email):
    """Get user's chat history from Supabase"""
    if not supabase:
        return []
    try:
        response = supabase.table("chat_history").select("*").eq("email", user_email).order("timestamp", desc=False).execute()
        return response.data if response.data else []
    except:
        return []

# ─────────────────────────────────────────────
#  PDF GENERATOR (Session 3 - KEPT)
# ─────────────────────────────────────────────
def generate_pdf_bytes(title, content, author="Akash Kumar Injeti"):
    """Generate a simple PDF as bytes using pure Python."""
    lines = []
    lines.append(f"HealthGPT ULTRA — {title}")
    lines.append(f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    lines.append(f"Powered by Akash Kumar Injeti | healthgptultra.streamlit.app")
    lines.append("=" * 60)
    lines.append("")
    
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
    objects = []
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n")

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

    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [5 0 R] /Count 1 >>\nendobj\n")
    objects.append(b"5 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Contents 4 0 R /Resources << /Font << /F1 3 0 R >> >> >>\nendobj\n")

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
#  PAGE CONFIG (Session 3 - KEPT)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="HealthGPT ULTRA — AI Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  ULTRA CSS (Session 3 - KEPT)
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

  .landing-hero {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 20px; padding: 4rem 2rem;
    text-align: center; margin-bottom: 2rem;
  }
  .landing-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff 0%, #0ea5e9 50%, #7c3aed 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 1rem;
  }
  .landing-sub {
    font-size: 1.1rem; color: #8b949e;
    max-width: 560px; margin: 0 auto 2rem;
  }
  .feature-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px; margin: 2rem 0;
  }
  .feature-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 12px; padding: 1.25rem;
    text-align: center;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "supabase" not in st.session_state:
    st.session_state.supabase = init_supabase()
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "current_language" not in st.session_state:
    st.session_state.current_language = "English"
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
#  TRANSLATIONS (Session 3 - KEPT & EXPANDED)
# ─────────────────────────────────────────────
TRANSLATIONS = {
    "English": {
        "title": "🏥 HealthGPT ULTRA",
        "subtitle": "AI Health Assistant for India",
        "chat": "💬 AI Chat",
        "symptoms": "🔍 Symptom Checker",
        "medicine": "💊 Medicine Info",
        "diet": "🥗 Diet Planner",
        "pdf": "📄 PDF Analyzer",
        "news": "📰 Health News",
        "emergency": "🚨 Emergency Guide",
        "bmi": "🧮 BMI Calculator",
        "scanner": "📸 Prescription Scanner",
        "history": "📊 History",
        "login": "🔐 Login",
        "logout": "🚪 Logout",
        "language": "🌍 Language"
    },
    "Telugu": {
        "title": "🏥 HealthGPT ULTRA",
        "subtitle": "AI ఆరోగ్య సహాయక",
        "chat": "💬 AI చాట్",
        "symptoms": "🔍 లక్షణ పరిశీలన",
        "medicine": "💊 ఔషధ సమాచారం",
        "diet": "🥗 ఆహార ప్రణాళిక",
        "scanner": "📸 ప్రిస్క్రిప్షన్ స్కానర్",
    },
    "Hindi": {
        "title": "🏥 HealthGPT ULTRA",
        "subtitle": "AI स्वास्थ्य सहायक",
        "chat": "💬 AI चैट",
        "symptoms": "🔍 लक्षण जांच",
        "medicine": "💊 दवा की जानकारी",
        "diet": "🥗 आहार योजना",
        "scanner": "📸 प्रिस्क्रिप्शन स्कैनर",
    },
    "Tamil": {
        "title": "🏥 HealthGPT ULTRA",
        "subtitle": "AI சுகாதார உதவி",
        "chat": "💬 AI சேட்",
        "symptoms": "🔍 அறிகுறி சரிபார்ப்பு",
        "medicine": "💊 மருந்து தகவல்",
        "diet": "🥗 உணவு திட்டம்",
        "scanner": "📸 பரிந்துரை ஸ்கேனர்",
    }
}

def t(key):
    """Translate text based on current language"""
    lang = st.session_state.current_language
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)

# ─────────────────────────────────────────────
#  SIDEBAR (Session 3 - KEPT & ENHANCED)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Language selector
    lang_col = st.columns([1, 2])
    with lang_col[0]:
        st.write(t("language"))
    with lang_col[1]:
        st.session_state.current_language = st.selectbox(
            "Language",
            ["English", "Telugu", "Hindi", "Tamil"],
            index=["English", "Telugu", "Hindi", "Tamil"].index(st.session_state.current_language),
            label_visibility="collapsed"
        )
    
    st.divider()
    
    # Authentication section (ENHANCED with Google OAuth)
    st.markdown("### 🔐 Authentication")
    
    if not st.session_state.authenticated:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📧 Demo Login"):
                # Demo login (keep Session 3 functionality)
                username = st.text_input("Username", key="demo_user")
                password = st.text_input("Password", type="password", key="demo_pass")
                if st.button("Login"):
                    if username and password:
                        st.session_state.authenticated = True
                        st.session_state.user = {"name": username, "email": f"{username}@demo.com"}
                        st.success(f"✅ Logged in as {username}")
                        st.rerun()
        
        with col2:
            oauth_url = get_google_oauth_url()
            if oauth_url:
                st.markdown(f"[🔵 Google OAuth]('{oauth_url}')")
            st.info("👆 Or use demo login")
    else:
        st.success(f"✅ {st.session_state.user.get('name', 'User')} logged in")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()

# ─────────────────────────────────────────────
#  MAIN APP (Session 3 - KEPT + NEW FEATURES)
# ─────────────────────────────────────────────
st.markdown(f"# {t('title')}")
st.markdown(f"_{t('subtitle')}_")

# Show login requirement if not authenticated
if not st.session_state.authenticated:
    st.warning("👆 Please login via sidebar to access features")
    st.markdown("""
    ### ✨ Features Available After Login:
    - 💬 AI Chat with medical advice
    - 🔍 Symptom Checker
    - 💊 Medicine Information
    - 🥗 Diet Plans for India
    - 📄 Blood Test PDF Analysis
    - 📰 AI Health News
    - 🚨 Emergency First Aid
    - 🧮 BMI Calculator
    - 📸 **NEW:** Prescription Scanner
    - 📊 Chat History
    """)
else:
    # Create tabs for all features
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        t("chat"),
        t("symptoms"),
        t("medicine"),
        t("diet"),
        t("pdf"),
        t("scanner"),
        t("news"),
        t("emergency"),
        t("bmi")
    ])
    
    # TAB 1: AI CHAT (Session 3 - KEPT + Supabase persistence)
    with tab1:
        st.markdown(f"### {t('chat')}")
        
        # Load chat history from Supabase or local
        if st.session_state.supabase and st.session_state.user:
            history = get_supabase_history(st.session_state.supabase, st.session_state.user['email'])
            st.session_state.messages = [{"role": h["role"], "content": h["message"]} for h in history]
        
        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about your health..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get AI response
            system_prompt = """You are a helpful health information assistant. 
            Provide accurate health information from reliable sources. 
            Always recommend consulting healthcare professionals for serious conditions."""
            
            response = get_groq_response(prompt, system_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save to Supabase if available
            if st.session_state.supabase and st.session_state.user:
                save_to_supabase(st.session_state.supabase, st.session_state.user['email'], prompt, "user")
                save_to_supabase(st.session_state.supabase, st.session_state.user['email'], response, "assistant")
            
            with st.chat_message("assistant"):
                st.write(response)
    
    # TAB 2: SYMPTOM CHECKER (Session 3 - KEPT)
    with tab2:
        st.markdown(f"### {t('symptoms')}")
        symptoms_text = st.text_area("Describe your symptoms:")
        
        if st.button("🔍 Analyze"):
            prompt = f"""Patient reports: {symptoms_text}
            
Please provide:
1. Possible conditions (most likely first)
2. Warning signs to watch for
3. When to see a doctor
4. Safe home care suggestions"""
            
            response = get_groq_response(prompt)
            st.write(response)
            
            # Download as PDF
            if st.button("📥 Download as PDF"):
                pdf = generate_pdf_bytes("Symptom Analysis", response)
                st.download_button("Download", data=pdf, file_name="symptom_analysis.pdf", mime="application/pdf")
    
    # TAB 3: MEDICINE INFO (Session 3 - KEPT)
    with tab3:
        st.markdown(f"### {t('medicine')}")
        medicine_name = st.text_input("Enter medicine name:")
        
        if st.button("💊 Search"):
            prompt = f"""Provide detailed information about {medicine_name}:
1. What is it used for?
2. Typical dosage (general info only)
3. Common side effects
4. Important warnings
5. When to avoid it"""
            
            response = get_groq_response(prompt)
            st.write(response)
            
            if st.button("📥 Download as PDF", key="med_pdf"):
                pdf = generate_pdf_bytes(f"Medicine: {medicine_name}", response)
                st.download_button("Download", data=pdf, file_name=f"{medicine_name}.pdf", mime="application/pdf", key="med_down")
    
    # TAB 4: DIET PLANNER (Session 3 - KEPT)
    with tab4:
        st.markdown(f"### {t('diet')}")
        condition = st.selectbox("Select health condition:", [
            "Diabetes",
            "High Blood Pressure",
            "Heart Disease",
            "Weight Loss",
            "PCOD",
            "Anemia",
            "Digestion Issues",
            "High Cholesterol",
            "Kidney Disease"
        ])
        
        if st.button("🥗 Generate Diet Plan"):
            prompt = f"""Create a 7-day Indian diet plan for someone with {condition}.
Include:
1. Breakfast ideas
2. Lunch ideas
3. Dinner ideas
4. Healthy snacks
5. Foods to avoid
Include Indian spices and local ingredients."""
            
            response = get_groq_response(prompt)
            st.write(response)
            
            if st.button("📥 Download Diet Plan", key="diet_pdf"):
                pdf = generate_pdf_bytes(f"Diet Plan: {condition}", response)
                st.download_button("Download", data=pdf, file_name=f"diet_{condition}.pdf", mime="application/pdf", key="diet_down")
    
    # TAB 5: PDF ANALYZER (Session 3 - KEPT)
    with tab5:
        st.markdown(f"### {t('pdf')}")
        st.info("Upload a blood test report or medical PDF")
        
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf", "jpg", "png"])
        if uploaded_file:
            st.success("✅ File uploaded")
            
            if st.button("🔍 Analyze Report"):
                prompt = f"""Analyze a medical report and explain:
1. What does this test measure?
2. Are the values normal or abnormal?
3. What do the values mean for health?
4. What should the patient do?
Keep explanation simple and actionable."""
                
                response = get_groq_response(prompt)
                st.write(response)
    
    # TAB 6: PRESCRIPTION SCANNER (NEW - Session 4)
    with tab6:
        st.markdown(f"### {t('scanner')}")
        st.info("📸 Upload a prescription image to extract medicine info")
        
        uploaded_image = st.file_uploader("Upload prescription image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            st.image(uploaded_image, width=300)
            
            if st.button("🔍 Scan Prescription"):
                prompt = """Analyze this prescription image and extract:
1. Patient Name
2. Doctor Name
3. Medicines (name, dosage, frequency)
4. Duration
5. Any allergies or warnings mentioned

Format as a clear list."""
                
                response = get_groq_response(prompt)
                st.write(response)
                
                if st.button("📥 Download Prescription Info", key="script_pdf"):
                    pdf = generate_pdf_bytes("Prescription Scan", response)
                    st.download_button("Download", data=pdf, file_name="prescription_scan.pdf", mime="application/pdf", key="script_down")
    
    # TAB 7: HEALTH NEWS (Session 3 - KEPT)
    with tab7:
        st.markdown(f"### {t('news')}")
        
        if st.button("📰 Generate Health News"):
            prompt = """Generate 3 interesting health/medical news items relevant to India:
For each:
1. Headline
2. Summary (2-3 sentences)
3. Relevance to Indian health
Make it informative and accurate."""
            
            response = get_groq_response(prompt)
            st.write(response)
    
    # TAB 8: EMERGENCY GUIDE (Session 3 - KEPT)
    with tab8:
        st.markdown(f"### {t('emergency')}")
        
        emergency_type = st.selectbox("Select emergency:", [
            "Heart Attack",
            "Stroke",
            "Severe Choking",
            "Severe Bleeding",
            "Poisoning",
            "Severe Burns",
            "Allergic Reaction",
            "Bone Fracture",
            "Unconsciousness",
            "Electrocution",
            "Drowning",
            "Snakebite"
        ])
        
        if st.button("🚨 Get First Aid"):
            prompt = f"""Provide step-by-step FIRST AID for {emergency_type}:
1. Immediate actions (first 2 minutes)
2. What NOT to do
3. When to call emergency (112 in India)
4. Positioning and monitoring
Keep it clear and actionable."""
            
            response = get_groq_response(prompt)
            st.write(response)
    
    # TAB 9: BMI CALCULATOR (Session 3 - KEPT)
    with tab9:
        st.markdown(f"### {t('bmi')}")
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (kg):", min_value=1, max_value=200)
        with col2:
            height = st.number_input("Height (cm):", min_value=50, max_value=250)
        
        if st.button("🧮 Calculate"):
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            
            if bmi < 18.5:
                category = "Underweight"
                color = "blue"
            elif bmi < 25:
                category = "Normal Weight"
                color = "green"
            elif bmi < 30:
                category = "Overweight"
                color = "orange"
            else:
                category = "Obese"
                color = "red"
            
            st.markdown(f"### BMI: {bmi:.1f} - {category}")
            
            # Get AI tips
            prompt = f"""Person has BMI of {bmi:.1f} ({category}).
Provide 5 personalized health tips considering:
1. Their BMI category
2. Indian dietary context
3. Practical exercise suggestions
4. Mental health aspects
5. When to see a doctor"""
            
            response = get_groq_response(prompt)
            st.write(response)

# ─────────────────────────────────────────────
#  FOOTER (Session 3 - KEPT)
# ─────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align: center; color: #8b949e; font-size: 0.9rem; margin-top: 2rem;">
    <p>🏥 <strong>HealthGPT ULTRA</strong> — AI Health Assistant for India 🇮🇳</p>
    <p>Created by <strong>Akash Kumar Injeti</strong> | Data Science & AI</p>
    <p style="font-size: 0.8rem; color: #6e7681;">
    ⚠️ <strong>Disclaimer:</strong> Educational purposes only. Not a substitute for professional medical advice.<br>
    Always consult a qualified healthcare professional.
    </p>
    <p style="font-size: 0.85rem;">
    🔒 <strong>Session 4 with Supabase + Google OAuth + Prescription Scanner</strong>
    </p>
</div>
""", unsafe_allow_html=True)