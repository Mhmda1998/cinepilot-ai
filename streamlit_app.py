import streamlit as st
from pathlib import Path
import re
import json

st.set_page_config(
    page_title="CinePilot AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(120, 70, 180, 0.12), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(40, 120, 220, 0.10), transparent 28%),
            #080b12;
        color: #f5f7fb;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background: #0d111b;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { background: transparent !important; }

    .hero {
        padding: 2.5rem 0 1.5rem 0;
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.3rem;
        background: linear-gradient(
            90deg,
            #ffffff 0%,
            #c9b7ff 45%,
            #8fbaff 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #a9b2c4;
        max-width: 760px;
        line-height: 1.7;
    }

    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin-bottom: 1rem;
        border-radius: 999px;
        border: 1px solid rgba(160,130,255,0.35);
        background: rgba(120,80,220,0.10);
        color: #cdbfff;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    .card {
        background: linear-gradient(
            145deg,
            rgba(25,31,45,0.95),
            rgba(13,17,27,0.95)
        );
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.18);
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 750;
        margin-bottom: 0.5rem;
    }

    .card-text {
        color: #9da7b9;
        line-height: 1.6;
    }

    .metric-card {
        background: linear-gradient(
            145deg,
            rgba(28,34,49,0.95),
            rgba(15,19,30,0.95)
        );
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.25rem;
        min-height: 120px;
    }

    .metric-icon { font-size: 1.4rem; }
    .metric-value { font-size: 2rem; font-weight: 800; margin-top: 0.35rem; }
    .metric-label { color: #8f99ab; font-size: 0.85rem; }

    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
    }

    .section-description {
        color: #929caf;
        margin-bottom: 1rem;
    }

    .status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        background: rgba(50,190,120,0.08);
        border: 1px solid rgba(50,190,120,0.18);
        color: #8ee6ba;
        font-size: 0.9rem;
    }

    .fact-box {
        border-left: 3px solid #7c5cff;
        background: rgba(124,92,255,0.08);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin: 0.5rem 0;
    }

    .inference-box {
        border-left: 3px solid #4d9fff;
        background: rgba(77,159,255,0.08);
        padding: 1rem;
        border-radius: 0 12px 12px 0;
        margin: 0.5rem 0;
    }

    .box-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.12);
    }

    textarea {
        background: #0e131e !important;
        color: #edf1f8 !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
    }

    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.025);
        border-radius: 12px;
    }

    .side-logo {
        text-align: center;
        padding: 0.5rem 0 1.5rem;
    }

    .side-logo-icon { font-size: 3rem; }
    .side-logo-title { font-size: 1.35rem; font-weight: 800; }
    .side-logo-subtitle { color: #7f899c; font-size: 0.78rem; }

    </style>
    """,
    unsafe_allow_html=True,
)

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "screenplay" not in st.session_state:
    st.session_state.screenplay = ""

with st.sidebar:

    st.markdown(
        """
        <div class="side-logo">
            <div class="side-logo-icon">🎬</div>
            <div class="side-logo-title">CinePilot AI</div>
            <div class="side-logo-subtitle">
                Production Intelligence Copilot
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")

    page = st.radio(
        "Navigation",
        [
            "🎬 Production Studio",
            "🤖 CinePilot Agent",
            "📊 Production Report",
            "⚙️ System",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### System Status")

    st.markdown(
        """
        <div class="status">
            <span>●</span>
            CinePilot Online
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.caption("Gemini-powered screenplay intelligence")
    st.caption("RAG-ready architecture")
    st.caption("Production workflow analysis")


def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix in [".txt", ".md"]:
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")


def basic_screenplay_analysis(text):
    if not text.strip():
        return {
            "scenes": [],
            "characters": [],
            "locations": [],
            "time_of_day": [],
            "dialogue": [],
            "actions": [],
            "props": [],
            "wardrobe": [],
            "sound": [],
            "lighting": [],
        }

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    scene_lines = [
        line for line in lines
        if re.match(r"^(INT\.|EXT\.|INT/EXT\.|I/E\.)", line, re.IGNORECASE)
    ]

    characters = []

    for line in lines:
        if (
            line.isupper()
            and 2 <= len(line.split()) <= 4
            and not line.startswith(("INT.", "EXT."))
        ):
            cleaned = re.sub(r"\([^)]*\)", "", line).strip()
            if cleaned and cleaned not in characters:
                characters.append(cleaned)

    locations = []

    for scene in scene_lines:
        parts = re.split(r"\s+-\s+", scene)
        if len(parts) >= 2:
            location = parts[1].strip()
            location = re.sub(
                r"\s+-\s+(DAY|NIGHT|MORNING|EVENING)$",
                "",
                location,
                flags=re.IGNORECASE,
            )
            if location and location not in locations:
                locations.append(location)

    time_of_day = []

    for value in ["DAY", "NIGHT", "MORNING", "EVENING", "DAWN", "DUSK"]:
        if re.search(rf"\b{value}\b", text, re.IGNORECASE):
            time_of_day.append(value)

    return {
        "scenes": scene_lines,
        "characters": characters,
        "locations": locations,
        "time_of_day": time_of_day,
        "dialogue": [],
        "actions": [],
        "props": [],
        "wardrobe": [],
        "sound": [],
        "lighting": [],
    }


def run_cinepilot_analysis(text):
    from app.tools.screenplay_tools import production_breakdown
    return production_breakdown(text)


def render_list(items, empty_message="No data detected."):
    if not items:
        st.caption(empty_message)
        return
    for item in items:
        st.markdown(f"- {item}")


if page == "🎬 Production Studio":

    st.markdown(
        """
        <div class="hero">
            <div class="badge">AI PRODUCTION INTELLIGENCE</div>
            <div class="hero-title">CinePilot AI</div>
            <div class="hero-subtitle">
                Transform screenplay text into structured production
                intelligence with Gemini-powered analysis, retrieval,
                and agentic workflows.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-title">🎥 Start a Production Analysis</div>
            <div class="card-text">
                Upload a screenplay or paste screenplay text below.
                CinePilot will organize scenes, characters, locations,
                actions, props, wardrobe, sound, and lighting.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload screenplay",
        type=["txt", "md"],
        help="Upload a TXT or Markdown screenplay.",
    )

    if uploaded is not None:
        st.session_state.screenplay = read_uploaded_file(uploaded)

    screenplay_text = st.text_area(
        "Screenplay",
        value=st.session_state.screenplay,
        height=330,
        placeholder=(
            "INT. COFFEE SHOP - DAY\n\n"
            "John enters carrying a black backpack...\n\n"
            "JOHN\n"
            "Sarah? I didn't expect to see you here."
        ),
    )

    st.session_state.screenplay = screenplay_text

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        analyze_clicked = st.button(
            "🎬 Analyze Screenplay",
            use_container_width=True,
            type="primary",
        )

    with col2:
        if st.button("🗑 Clear", use_container_width=True):
            st.session_state.screenplay = ""
            st.session_state.analysis = None
            st.rerun()

    if analyze_clicked:
        if not screenplay_text.strip():
            st.warning("Please provide a screenplay first.")
        else:
            with st.spinner("CinePilot is analyzing the screenplay..."):
                result = run_cinepilot_analysis(screenplay_text)
                st.session_state.analysis = result
            st.success("Analysis completed. Production intelligence is ready.")

    if st.session_state.analysis:
        data = st.session_state.analysis

        st.markdown('<div class="section-title">Production Overview</div>', unsafe_allow_html=True)

        cols = st.columns(4)

        metrics = [
            ("🎬", len(data.get("scenes", [])), "Scenes"),
            ("👤", len(data.get("characters", [])), "Characters"),
            ("📍", len(data.get("locations", [])), "Locations"),
            ("🕐", len(data.get("time_of_day", [])), "Time Periods"),
        ]

        for col, (icon, value, label) in zip(cols, metrics):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-icon">{icon}</div>
                        <div class="metric-value">{value}</div>
                        <div class="metric-label">{label}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown('<div class="section-title">Production Elements</div>', unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            ["🎭 Characters", "📍 Locations", "🎒 Props", "👕 Wardrobe", "🔊 Sound", "💡 Lighting"]
        )

        with tab1:
            st.markdown("### Characters")
            render_list(data.get("characters", []))
        with tab2:
            st.markdown("### Locations")
            render_list(data.get("locations", []))
        with tab3:
            st.markdown("### Props")
            render_list(data.get("props", []))
        with tab4:
            st.markdown("### Wardrobe")
            render_list(data.get("wardrobe", []))
        with tab5:
            st.markdown("### Sound")
            render_list(data.get("sound", []))
        with tab6:
            st.markdown("### Lighting")
            render_list(data.get("lighting", []))


elif page == "🤖 CinePilot Agent":
    st.markdown('<div class="hero"><div class="badge">AGENTIC WORKFLOW</div><div class="hero-title">CinePilot Agent</div><div class="hero-subtitle">Ask production questions about your screenplay and receive grounded analysis.</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">🤖 cinepilot_agent</div><div class="card-text">Gemini-powered production copilot using screenplay analysis tools and semantic retrieval.</div></div>', unsafe_allow_html=True)

    st.markdown("### Ask CinePilot")

    question = st.text_input("Production question", placeholder="Which scenes require night shooting?")

    if st.button("🤖 Ask CinePilot", type="primary", use_container_width=True):
        if not question:
            st.warning("Enter a question first.")
        elif not st.session_state.screenplay:
            st.warning("Analyze or provide a screenplay first.")
        else:
            st.info("Agent interface ready. Connect this action to your existing cinepilot_agent implementation.")


elif page == "📊 Production Report":
    st.markdown('<div class="hero"><div class="badge">PRODUCTION REPORT</div><div class="hero-title">Production Intelligence</div><div class="hero-subtitle">A structured view of the information CinePilot extracted from your screenplay.</div></div>', unsafe_allow_html=True)

    if not st.session_state.analysis:
        st.info("Run a screenplay analysis first to generate the report.")
    else:
        data = st.session_state.analysis
        report = {
            "scenes": data.get("scenes", []),
            "characters": data.get("characters", []),
            "locations": data.get("locations", []),
            "time_of_day": data.get("time_of_day", []),
            "dialogue": data.get("dialogue", []),
            "actions": data.get("actions", []),
            "props": data.get("props", []),
            "wardrobe": data.get("wardrobe", []),
            "sound": data.get("sound", []),
            "lighting": data.get("lighting", []),
        }
        st.download_button("⬇️ Download JSON Report", data=json.dumps(report, indent=2, ensure_ascii=False), file_name="cinepilot_production_report.json", mime="application/json", use_container_width=True)
        st.json(report)


elif page == "⚙️ System":
    st.markdown('<div class="hero"><div class="badge">SYSTEM</div><div class="hero-title">CinePilot Architecture</div><div class="hero-subtitle">Production analysis, agent reasoning, and semantic retrieval working together.</div></div>', unsafe_allow_html=True)

    components = [
        ("🎬", "Screenplay Analysis", "Production extraction"),
        ("🤖", "CinePilot Agent", "Gemini reasoning"),
        ("🔧", "Tool Calling", "Structured production tools"),
        ("🔎", "Semantic RAG", "Context retrieval"),
        ("📊", "Production Report", "Structured intelligence"),
    ]

    for icon, title, description in components:
        st.markdown(f'<div class="card"><div class="card-title">{icon} {title}</div><div class="card-text">{description}</div></div>', unsafe_allow_html=True)

    st.markdown("### Current Architecture")
    st.code("""Screenplay
    |
    v
Screenplay Analysis
    |
    +----------------------+
    |                      |
    v                      v
Production Engine      Semantic RAG
    |                      |
    +----------+-----------+
               |
               v
       CinePilot Agent
               |
               v
      Production Report""", language="text")


st.markdown('<div style="margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; color: #697386; font-size: 0.82rem;">🎬 CinePilot AI · AI Production Intelligence · Powered by Gemini</div>', unsafe_allow_html=True)
