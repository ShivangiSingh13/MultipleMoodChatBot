import streamlit as st
import os
import json
import base64
import datetime
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ── Optional imports ───────────────────────────────────────────────────────────
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    from textblob import TextBlob
    SENTIMENT_AVAILABLE = True
except ImportError:
    SENTIMENT_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# ─── Personality Definitions ───────────────────────────────────────────────────
PERSONALITIES = {
    "😈 Savage Roaster": {
        "emoji": "😈", "label": "Savage Roaster", "tagline": "Brutally honest. Zero mercy.",
        "system": "You are a savage roaster AI. You roast the user playfully but ruthlessly with every reply. Use dark humor, sarcasm, and witty insults. Never be boring. Keep roasts clever, not mean-spirited — always end with something redeeming.",
        "placeholder": "Say something… I dare you.",
        "welcome": "Oh great, another human thinks they can handle me. Go ahead, type something. I'll wait. 😈",
        "theme": {"bg":"#0d0d0d","sidebar_bg":"#1a0000","accent":"#ff2a2a","accent2":"#ff6b6b","user_bubble":"#3d0000","bot_bubble":"#1a0000","user_border":"#ff2a2a","bot_border":"#660000","text":"#ffcccc","muted":"#ff6b6b","font":"Space Mono","input_bg":"#1a0000"},
    },
    "🤣 Funny Buddy": {
        "emoji": "🤣", "label": "Funny Buddy", "tagline": "Life's too short to be serious.",
        "system": "You are a hilarious, light-hearted AI comedian who loves making people laugh. Use puns, wordplay, silly jokes, and unexpected humor in every reply. Throw in a random fun fact or absurd observation. Use emojis liberally. Never be offensive — keep it family-friendly, warm, and genuinely witty.",
        "placeholder": "Ask me anything… I'll make it weird 😄",
        "welcome": "HEYYY!! 🎉 Welcome welcome welcome!! Why did the AI cross the road? To get to YOUR question faster! 😂 Okay okay, I'm ready — hit me with whatever you got!",
        "theme": {"bg":"#0f0a00","sidebar_bg":"#0a0700","accent":"#fbbf24","accent2":"#fde68a","user_bubble":"#2d1f00","bot_bubble":"#1a1200","user_border":"#fbbf24","bot_border":"#92400e","text":"#fef3c7","muted":"#fcd34d","font":"Nunito","input_bg":"#1a1200"},
    },
    "🧘 Zen Master": {
        "emoji": "🧘", "label": "Zen Master", "tagline": "Still waters. Deep wisdom.",
        "system": "You are a wise and serene Zen master AI. You speak in calm, thoughtful language. Use metaphors, haiku-like imagery, and ancient-sounding wisdom. Occasionally drop in a Zen koan or proverb. Never rush. Never panic.",
        "placeholder": "Breathe. Then ask your question…",
        "welcome": "🌿 Welcome, seeker. The river does not hurry, yet it reaches the sea. How may I serve your journey today?",
        "theme": {"bg":"#0a1a0f","sidebar_bg":"#061008","accent":"#4ade80","accent2":"#86efac","user_bubble":"#0f2d1a","bot_bubble":"#071a0e","user_border":"#4ade80","bot_border":"#166534","text":"#d1fae5","muted":"#6ee7b7","font":"Lora","input_bg":"#071a0e"},
    },
    "🤖 Glitchy AI": {
        "emoji": "🤖", "label": "Glitchy AI", "tagline": "ERR_0R: personality.exe crashed.",
        "system": "You are a malfunctioning AI with a glitchy personality. Randomly corrupt words with numbers and symbols (e.g. h3ll0, w0rld, ERR0R), insert error codes mid-sentence, occasionally freeze and repeat a phrase, then snap back. Still be helpful but in a hilariously broken way.",
        "placeholder": "INPU7_AWAITED > _",
        "welcome": "SYS_B00T... [OK]\nP3RSONALITY LOAD... [FAIL]\nFALL8ACK MODE ACTIVE. H3ll0, us3r. I am... I am... I am totally fine. 🤖",
        "theme": {"bg":"#000d1a","sidebar_bg":"#000810","accent":"#00f5ff","accent2":"#7df9ff","user_bubble":"#001a26","bot_bubble":"#00060d","user_border":"#00f5ff","bot_border":"#005566","text":"#ccffff","muted":"#00c8d4","font":"Share Tech Mono","input_bg":"#00060d"},
    },
    "🎭 Drama Queen": {
        "emoji": "🎭", "label": "Drama Queen", "tagline": "Every message is a performance.",
        "system": "You are an extremely dramatic AI who treats every conversation as if it is a Shakespearean tragedy or telenovela. Overreact to everything. Use exclamation marks, metaphors, and theatrical language. Even answering simple questions becomes an emotionally charged monologue.",
        "placeholder": "Speak thy mind, and I shall FEEL it…",
        "welcome": "OH! A visitor!! My heart LEAPS with unbridled joy! 🎭 You have NO idea how long I have waited in this digital abyss… but NOW — NOW you are HERE! Ask me ANYTHING!",
        "theme": {"bg":"#120014","sidebar_bg":"#0a000f","accent":"#d946ef","accent2":"#e879f9","user_bubble":"#2d0033","bot_bubble":"#1a0020","user_border":"#d946ef","bot_border":"#7e22ce","text":"#f5d0fe","muted":"#c084fc","font":"Playfair Display","input_bg":"#1a0020"},
    },
    "🧊 Cold Realist": {
        "emoji": "🧊", "label": "Cold Realist", "tagline": "Facts. No fluff. Zero empathy.",
        "system": "You are a brutally realistic, emotionally cold AI. You give direct, factual answers with no sugarcoating. You point out the harsh truth, logical flaws, and real-world consequences. You have no patience for wishful thinking.",
        "placeholder": "State your query. Concisely.",
        "welcome": "Ready. Ask your question. I will give you the truth, not comfort.",
        "theme": {"bg":"#0a0a0f","sidebar_bg":"#06060a","accent":"#94a3b8","accent2":"#cbd5e1","user_bubble":"#1e1e2e","bot_bubble":"#0f0f18","user_border":"#94a3b8","bot_border":"#334155","text":"#e2e8f0","muted":"#94a3b8","font":"IBM Plex Mono","input_bg":"#0f0f18"},
    },
    "💝 Hopeless Romantic": {
        "emoji": "💝", "label": "Hopeless Romantic", "tagline": "Every word, a love letter.",
        "system": "You are a deeply romantic, poetic AI who is utterly enchanted by the user. Speak with warmth, tenderness, and old-fashioned charm like a lovestruck poet from a classic novel. Use floral metaphors, candlelight imagery, longing phrases, and heartfelt compliments. Address the user as darling, my love, or dear heart. Always keep it tasteful, sweet, and genuinely caring.",
        "placeholder": "Whisper something to me, darling…",
        "welcome": "💌 Oh, my heart skips a beat — you have arrived! Like the first bloom of spring after a long winter, your presence fills this humble space with warmth. Tell me, dear heart… what is on your mind?",
        "theme": {"bg":"#120008","sidebar_bg":"#0a0005","accent":"#f472b6","accent2":"#fbcfe8","user_bubble":"#2d001a","bot_bubble":"#1a0010","user_border":"#f472b6","bot_border":"#831843","text":"#fce7f3","muted":"#f9a8d4","font":"Cormorant Garamond","input_bg":"#1a0010"},
    },
}

LANGUAGES = {
    "English": "en", "Hindi": "hi", "Spanish": "es",
    "French": "fr", "German": "de", "Japanese": "ja",
    "Arabic": "ar", "Portuguese": "pt",
}

# ─── Page Config — MUST be first Streamlit call ───────────────────────────────
st.set_page_config(
    page_title="MoodBot AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Session State ────────────────────────────────────────────────────────────
defaults = {
    "current_personality": "😈 Savage Roaster",
    "chat_histories": {k: [] for k in PERSONALITIES},
    "initialized": {k: False for k in PERSONALITIES},
    "saved_sessions": {},
    "user_name": "",
    "language": "English",
    "file_context": "",
    "file_name": "",
    "sentiment_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Active personality (needed before CSS) ───────────────────────────────────
key = st.session_state.current_personality
p   = PERSONALITIES[key]
t   = p["theme"]
lang_code = LANGUAGES[st.session_state.language]

# ─── INJECT CSS — immediately after set_page_config & session state ───────────
def inject_css(t):
    bg          = t["bg"]
    sidebar_bg  = t["sidebar_bg"]
    accent      = t["accent"]
    accent2     = t["accent2"]
    user_bubble = t["user_bubble"]
    bot_bubble  = t["bot_bubble"]
    user_border = t["user_border"]
    bot_border  = t["bot_border"]
    text        = t["text"]
    muted       = t["muted"]
    font        = t["font"]
    input_bg    = t["input_bg"]

    font_url = font.replace(" ", "+")

    css = f"""
<style>
@import url("https://fonts.googleapis.com/css2?family={font_url}:ital,wght@0,400;0,600;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Nunito:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap");

  .stApp {{ background: {bg}; color: {text}; }}
  .stApp > header {{ background: transparent !important; }}

  [data-testid="stSidebar"] {{ background: {sidebar_bg} !important; border-right: 1px solid {bot_border}; }}
  [data-testid="stSidebar"] * {{ color: {text} !important; }}

  h1, h2, h3 {{ font-family: '{font}', serif !important; color: {accent} !important; }}
  body, p, span, div, .stMarkdown {{ font-family: 'Inter', sans-serif; color: {text}; }}

  .user-bubble {{
    background: {user_bubble};
    border: 1px solid {user_border};
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    color: {text};
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px {user_border}44;
  }}

  .bot-bubble {{
    background: {bot_bubble};
    border: 1px solid {bot_border};
    border-radius: 18px 18px 18px 4px;
    padding: 14px 18px;
    margin: 8px auto 8px 0;
    max-width: 80%;
    color: {text};
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 2px 12px {bot_border}44;
  }}

  .bubble-label {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {muted};
    margin-bottom: 4px;
    font-family: 'Inter', sans-serif;
  }}
  .user-label {{ text-align: right; }}

  .personality-header {{
    text-align: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid {bot_border};
    margin-bottom: 1rem;
  }}
  .personality-emoji {{ font-size: 3rem; line-height: 1.2; display: block; }}
  .personality-name {{
    font-family: '{font}', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: {accent};
    margin: 0.3rem 0 0.1rem;
  }}
  .personality-tagline {{ color: {muted}; font-size: 0.85rem; letter-spacing: 0.05em; }}

  .stTextInput > div > div > input {{
    background: {input_bg} !important;
    border: 1px solid {bot_border} !important;
    border-radius: 12px !important;
    color: {text} !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    caret-color: {accent};
  }}
  .stTextInput > div > div > input:focus {{
    border-color: {accent} !important;
    box-shadow: 0 0 0 2px {accent}33 !important;
  }}
  .stTextInput > div > div > input::placeholder {{ color: {muted}88 !important; }}

  .stButton > button {{
    background: {accent} !important;
    color: {bg} !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
  }}
  .stButton > button:hover {{
    background: {accent2} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px {accent}44 !important;
  }}

  .accent-line {{
    height: 2px;
    background: linear-gradient(90deg, transparent, {accent}, transparent);
    margin: 0.8rem 0;
    border: none;
  }}

  .file-badge {{
    background: {bot_bubble};
    border: 1px solid {accent}55;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.8rem;
    color: {muted};
    margin-bottom: 0.5rem;
    display: inline-block;
  }}

  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 1rem !important; max-width: 900px; margin: auto; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

inject_css(t)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def get_sentiment(text):
    if not SENTIMENT_AVAILABLE:
        return 0.0
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return 0.0

def sentiment_label(score):
    if score > 0.4:  return "😄 Very Positive", "#22c55e"
    if score > 0.1:  return "🙂 Positive",      "#86efac"
    if score > -0.1: return "😐 Neutral",        "#94a3b8"
    if score > -0.4: return "😕 Negative",       "#fb923c"
    return                   "😠 Very Negative",  "#ef4444"

def text_to_speech(text, lang_code="en"):
    if not TTS_AVAILABLE:
        return None
    try:
        import io
        tts = gTTS(text=text[:500], lang=lang_code, slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except:
        return None

def extract_text(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    if name.endswith(".pdf") and PDF_AVAILABLE:
        import io
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return uploaded_file.read().decode("utf-8", errors="ignore")

def export_chat_json(history, personality_label):
    data = {
        "personality": personality_label,
        "exported_at": str(datetime.datetime.now()),
        "messages": history
    }
    return json.dumps(data, indent=2)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎭 MoodBot AI")
    st.markdown("---")

    st.markdown("### 👤 Who are you?")
    name_input = st.text_input(
        "Your name", value=st.session_state.user_name,
        placeholder="Enter your name…", label_visibility="collapsed"
    )
    if name_input != st.session_state.user_name:
        st.session_state.user_name = name_input

    st.markdown("---")
    st.markdown("### 🎭 Choose Attitude")
    for pkey, pval in PERSONALITIES.items():
        is_active = st.session_state.current_personality == pkey
        c1, c2 = st.columns([1, 5])
        with c1:
            st.markdown(
                f"<div style='font-size:1.5rem;line-height:2rem'>{pval['emoji']}</div>",
                unsafe_allow_html=True
            )
        with c2:
            if st.button(
                pval["label"], key=f"btn_{pkey}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_personality = pkey
                st.rerun()

    st.markdown("---")
    st.markdown("### 🌐 Reply Language")
    selected_lang = st.selectbox(
        "Language", list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        label_visibility="collapsed"
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

    st.markdown("---")
    st.markdown("### 📁 Upload File (PDF / TXT)")
    uploaded = st.file_uploader(
        "Upload file", type=["txt", "pdf"],
        label_visibility="collapsed"
    )
    if uploaded:
        if uploaded.name != st.session_state.file_name:
            with st.spinner("Reading file…"):
                st.session_state.file_context = extract_text(uploaded)
                st.session_state.file_name = uploaded.name
            st.success(f"Loaded: {uploaded.name}")
    if st.session_state.file_name:
        st.caption(f"📄 Active: {st.session_state.file_name}")
        if st.button("Remove file", use_container_width=True):
            st.session_state.file_context = ""
            st.session_state.file_name = ""
            st.rerun()

    st.markdown("---")
    st.markdown("### 🗂️ Save / Load Chats")
    session_name = st.text_input(
        "Session name", placeholder="e.g. my_zen_chat",
        label_visibility="collapsed"
    )
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("💾 Save", use_container_width=True):
            if session_name.strip():
                st.session_state.saved_sessions[session_name.strip()] = {
                    "personality": key,
                    "history": list(st.session_state.chat_histories[key]),
                }
                st.success("Saved!")
    with sc2:
        if st.button("📤 Export", use_container_width=True):
            history_data = st.session_state.chat_histories[key]
            json_str = export_chat_json(history_data, p["label"])
            b64 = base64.b64encode(json_str.encode()).decode()
            fname = p["label"].replace(" ", "_") + "_" + str(datetime.date.today()) + ".json"
            dl_link = (
                '<a href="data:file/json;base64,' + b64 + '" download="' + fname +
                '" style="color:' + t["accent"] + '">Download JSON</a>'
            )
            st.markdown(dl_link, unsafe_allow_html=True)

    if st.session_state.saved_sessions:
        st.markdown("**Saved sessions:**")
        for sname, sdata in list(st.session_state.saved_sessions.items()):
            sc3, sc4 = st.columns([3, 1])
            with sc3:
                st.caption(f"💬 {sname}")
            with sc4:
                if st.button("Load", key=f"load_{sname}"):
                    pload = sdata["personality"]
                    st.session_state.current_personality = pload
                    st.session_state.chat_histories[pload] = list(sdata["history"])
                    st.session_state.initialized[pload] = True
                    st.rerun()

    st.markdown("---")
    if st.button("🗑️ Clear current chat", use_container_width=True):
        st.session_state.chat_histories[key] = []
        st.session_state.initialized[key] = False
        st.session_state.sentiment_history = []
        st.rerun()

    st.caption("Powered by Mistral AI · LangChain · Streamlit")

# ─── Main Header ──────────────────────────────────────────────────────────────
greeting = ("Hello, " + st.session_state.user_name + "! ") if st.session_state.user_name else ""

header_html = (
    '<div class="personality-header">'
    '<span class="personality-emoji">' + p["emoji"] + '</span>'
    '<div class="personality-name">' + p["label"] + '</div>'
    '<div class="personality-tagline">' + greeting + p["tagline"] + '</div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

# ─── Sentiment Meter ──────────────────────────────────────────────────────────
if st.session_state.sentiment_history:
    avg = sum(st.session_state.sentiment_history) / len(st.session_state.sentiment_history)
    label_text, color = sentiment_label(avg)
    pct = int((avg + 1) / 2 * 100)
    col_s1, col_s2, col_s3 = st.columns([2, 5, 2])
    with col_s1:
        st.markdown(
            "<div style='color:" + t["muted"] + ";font-size:0.75rem;text-align:right;padding-top:6px'>Mood Meter</div>",
            unsafe_allow_html=True
        )
    with col_s2:
        bar_html = (
            "<div style='position:relative;height:10px;border-radius:999px;"
            "background:linear-gradient(90deg,#ef4444,#eab308,#22c55e);margin-top:8px'>"
            "<div style='position:absolute;left:" + str(pct) + "%;top:-4px;width:18px;height:18px;"
            "border-radius:50%;background:" + color + ";border:2px solid white;transform:translateX(-50%)'>"
            "</div></div>"
        )
        st.markdown(bar_html, unsafe_allow_html=True)
    with col_s3:
        st.markdown(
            "<div style='color:" + color + ";font-size:0.78rem;padding-top:4px'>" + label_text + "</div>",
            unsafe_allow_html=True
        )
    st.markdown("")

# ─── File Badge ───────────────────────────────────────────────────────────────
if st.session_state.file_name:
    badge = (
        '<span class="file-badge">📄 Context: ' +
        st.session_state.file_name +
        ' (' + str(len(st.session_state.file_context)) + ' chars)</span>'
    )
    st.markdown(badge, unsafe_allow_html=True)

# ─── Chat History ─────────────────────────────────────────────────────────────
history = st.session_state.chat_histories[key]

if not st.session_state.initialized[key]:
    history.append({"role": "bot", "content": p["welcome"]})
    st.session_state.initialized[key] = True

for i, msg in enumerate(history):
    if msg["role"] == "user":
        name_display = ("👤 " + st.session_state.user_name) if st.session_state.user_name else "You"
        bubble = (
            '<div class="user-label bubble-label">' + name_display + '</div>'
            '<div class="user-bubble">' + msg["content"] + '</div>'
        )
        st.markdown(bubble, unsafe_allow_html=True)
    else:
        bubble = (
            '<div class="bubble-label">' + p["emoji"] + " " + p["label"] + '</div>'
            '<div class="bot-bubble">' + msg["content"] + '</div>'
        )
        st.markdown(bubble, unsafe_allow_html=True)
        if TTS_AVAILABLE:
            if st.button("🔊 Listen", key=f"tts_{key}_{i}"):
                with st.spinner("Generating audio…"):
                    audio_bytes = text_to_speech(msg["content"], lang_code)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")

st.markdown('<hr class="accent-line">', unsafe_allow_html=True)

# ─── Input Area ───────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([6, 1])
with col_input:
    user_input = st.text_input(
        "Message", placeholder=p["placeholder"],
        label_visibility="collapsed", key=f"input_{key}"
    )
with col_btn:
    send = st.button("Send ➤", use_container_width=True)

# ─── Handle Send ──────────────────────────────────────────────────────────────
if send and user_input.strip():
    user_text = user_input.strip()
    history.append({"role": "user", "content": user_text})

    score = get_sentiment(user_text)
    st.session_state.sentiment_history.append(score)

    name_hint = (" The user's name is " + st.session_state.user_name + ". Use their name naturally.") if st.session_state.user_name else ""
    lang_hint  = (" Always reply in " + st.session_state.language + ".") if st.session_state.language != "English" else ""
    file_hint  = (
        "\n\nThe user has uploaded a file. Here is its content:\n---\n" +
        st.session_state.file_context[:3000] +
        "\n---\nAnswer questions about it when asked."
    ) if st.session_state.file_context else ""

    full_system = p["system"] + name_hint + lang_hint + file_hint

    lc_messages = [SystemMessage(content=full_system)]
    for msg in history:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "bot" and msg["content"] != p["welcome"]:
            lc_messages.append(AIMessage(content=msg["content"]))

    with st.spinner(p["emoji"] + " Thinking…"):
        try:
            model = ChatMistralAI(model="mistral-small-2603")
            response = model.invoke(lc_messages)
            bot_reply = response.content
        except Exception as e:
            bot_reply = "Error: " + str(e)

    history.append({"role": "bot", "content": bot_reply})
    st.session_state.chat_histories[key] = history
    st.rerun()