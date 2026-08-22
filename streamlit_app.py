import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from app.tools.screenplay_tools import production_breakdown
    from app.tools.production_bible import ProductionBible
except ImportError:
    from tools.screenplay_tools import production_breakdown
    from tools.production_bible import ProductionBible

st.set_page_config(
    page_title="CinePilot AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Cairo", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(124, 58, 237, 0.18),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(34, 211, 238, 0.10),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #05060b 0%,
            #090b14 45%,
            #05060b 100%
        );
    color: #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { background: transparent !important; }

.hero {
    position: relative;
    padding: 55px 30px 40px 30px;
    text-align: center;
    border-radius: 30px;
    margin-bottom: 30px;
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(139, 92, 246, 0.25),
            transparent 45%
        ),
        linear-gradient(
            135deg,
            rgba(18, 20, 35, 0.96),
            rgba(8, 10, 18, 0.96)
        );
    border: 1px solid rgba(139, 92, 246, 0.28);
    box-shadow:
        0 25px 80px rgba(0, 0, 0, 0.45),
        inset 0 1px rgba(255, 255, 255, 0.05);
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 999px;
    color: #c4b5fd;
    background: rgba(139, 92, 246, 0.10);
    border: 1px solid rgba(139, 92, 246, 0.40);
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 18px;
}

.hero-title {
    font-size: clamp(42px, 7vw, 78px);
    line-height: 1;
    font-weight: 800;
    letter-spacing: -3px;
    margin: 10px 0 20px 0;
    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #818cf8,
        #67e8f9
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 760px;
    margin: auto;
    color: #aeb7ca;
    font-size: 19px;
    line-height: 1.9;
}

.feature-card {
    height: 100%;
    padding: 24px;
    border-radius: 22px;
    background:
        linear-gradient(
            145deg,
            rgba(25, 28, 45, 0.95),
            rgba(11, 13, 23, 0.95)
        );
    border: 1px solid rgba(255, 255, 255, 0.07);
    box-shadow:
        0 15px 40px rgba(0, 0, 0, 0.25);
}

.feature-icon { font-size: 30px; margin-bottom: 10px; }
.feature-title { font-size: 18px; font-weight: 700; color: #f8fafc; }
.feature-text { color: #9ca8bd; font-size: 14px; line-height: 1.7; }

.section-title {
    font-size: 27px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 18px;
    color: #f8fafc;
}

.section-subtitle {
    color: #8e9ab0;
    margin-bottom: 20px;
}

.metric-card {
    padding: 22px 16px;
    text-align: center;
    border-radius: 20px;
    background:
        linear-gradient(
            145deg,
            rgba(23, 27, 43, 0.98),
            rgba(11, 13, 23, 0.98)
        );
    border: 1px solid rgba(139, 92, 246, 0.18);
    box-shadow: 0 12px 35px rgba(0,0,0,.20);
}

.metric-value { font-size: 34px; font-weight: 800; color: #c4b5fd; }
.metric-label { color: #8995aa; font-size: 13px; }

.result-card {
    padding: 22px;
    border-radius: 20px;
    background: rgba(15, 18, 30, 0.92);
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 14px;
}

.result-header {
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 12px;
}

.result-item {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px;
    border-radius: 10px;
    color: #dbeafe;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.20);
    font-size: 13px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 12px;
    border-radius: 999px;
    color: #86efac;
    background: rgba(34,197,94,.08);
    border: 1px solid rgba(34,197,94,.18);
    font-size: 13px;
    font-weight: 700;
}

.stButton > button {
    border-radius: 14px !important;
    border: 1px solid rgba(139,92,246,.35) !important;
    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #6366f1
        ) !important;
    color: white !important;
    font-weight: 800 !important;
    min-height: 48px;
    box-shadow:
        0 12px 30px rgba(99,102,241,.20) !important;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: #a78bfa !important;
    transform: translateY(-1px);
    box-shadow:
        0 16px 35px rgba(124,58,237,.30) !important;
}

textarea {
    background: #0d101a !important;
    color: #e5e7eb !important;
    border-radius: 18px !important;
    border: 1px solid rgba(139,92,246,.20) !important;
}

[data-testid="stFileUploader"] {
    background: rgba(16,19,31,.85);
    border-radius: 20px;
    border: 1px dashed rgba(139,92,246,.35);
    padding: 12px;
}

[data-testid="stExpander"] {
    background: rgba(13,16,27,.85);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 18px;
}

.footer {
    margin-top: 60px;
    padding: 25px;
    text-align: center;
    color: #69758a;
    border-top: 1px solid rgba(255,255,255,.06);
}

.footer strong {
    color: #a78bfa;
}

</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero" dir="rtl">

<div class="hero-badge">
🎬 AI-POWERED FILM PRODUCTION
</div>

<div class="hero-title">
CinePilot AI
</div>

<div class="hero-subtitle">
حوّل السيناريو إلى معلومات إنتاجية منظمة
باستخدام تحليل السيناريو، الذكاء الاصطناعي،
الاسترجاع الدلالي، وسير عمل الوكيل الذكي المدعوم بـ Gemini.
</div>

</div>
""",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
<div class="feature-card" dir="rtl">
<div class="feature-icon">🎬</div>
<div class="feature-title">تحليل السيناريو</div>
<div class="feature-text">
استخراج المشاهد والشخصيات والمواقع والوقت والحوار والأحداث.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
<div class="feature-card" dir="rtl">
<div class="feature-icon">🎭</div>
<div class="feature-title">Production Breakdown</div>
<div class="feature-text">
استخراج الدعائم والملابس والأصوات والإضاءة وعناصر الإنتاج.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
<div class="feature-card" dir="rtl">
<div class="feature-icon">🧠</div>
<div class="feature-title">AI Agent</div>
<div class="feature-text">
وكيل CinePilot مدعوم بـ Gemini لاتخاذ خطوات تحليلية منظمة.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        """
<div class="feature-card" dir="rtl">
<div class="feature-icon">🔎</div>
<div class="feature-title">Semantic RAG</div>
<div class="feature-text">
استرجاع سياق السيناريو عند الحاجة للتحليل الدلالي.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="section-title" dir="rtl">🎬 ابدأ تحليل الإنتاج</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle" dir="rtl">ارفع سيناريو أو الصق النص مباشرة لتحويله إلى Production Intelligence.</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "تحميل السيناريو",
    type=["txt", "md"],
    help="الحد الأقصى الموصى به 200KB للملف.",
)

screenplay = ""

if uploaded_file is not None:
    try:
        screenplay = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        screenplay = uploaded_file.read().decode(
            "utf-8",
            errors="replace",
        )

if screenplay:
    st.success(
        f"تم تحميل السيناريو: {uploaded_file.name}"
    )

screenplay_input = st.text_area(
    "أو الصق السيناريو هنا",
    value=screenplay,
    height=300,
    placeholder=(
        "INT. COFFEE SHOP - DAY\n\n"
        "JOHN enters carrying a black backpack.\n\n"
        "JOHN\n"
        "I didn't expect to see you here."
    ),
)

col_a, col_b = st.columns(2)

with col_a:
    analyze_clicked = st.button(
        "🎬 Analyze Screenplay",
        use_container_width=True,
    )

with col_b:
    report_clicked = st.button(
        "📘 Generate Production Bible",
        use_container_width=True,
    )

if analyze_clicked:

    if not screenplay_input.strip():
        st.warning(
            "يرجى رفع سيناريو أو إدخال نص السيناريو أولاً."
        )
        st.stop()

    with st.spinner("CinePilot يحلل السيناريو..."):

        try:
            data = production_breakdown(
                screenplay_input
            )
        except Exception as exc:
            st.error(
                f"حدث خطأ أثناء التحليل: {exc}"
            )
            st.stop()

    if not data.get("success"):
        st.error(
            data.get(
                "error",
                "فشل تحليل السيناريو.",
            )
        )
        st.stop()

    st.session_state["production_data"] = data
    st.session_state["screenplay"] = screenplay_input

    st.markdown(
        '<div class="section-title" dir="rtl">📊 Production Overview</div>',
        unsafe_allow_html=True,
    )

    metrics = [
        (
            "🎬",
            data.get("scene_count", 0),
            "Scenes",
        ),
        (
            "👤",
            data.get("character_count", 0),
            "Characters",
        ),
        (
            "📍",
            data.get("location_count", 0),
            "Locations",
        ),
        (
            "🎒",
            len(data.get("props", [])),
            "Props",
        ),
        (
            "👕",
            len(data.get("wardrobe", [])),
            "Wardrobe",
        ),
        (
            "🔊",
            len(data.get("sounds", [])),
            "Sound",
        ),
        (
            "💡",
            len(data.get("lighting", [])),
            "Lighting",
        ),
        (
            "⚡",
            len(data.get("actions", [])),
            "Actions",
        ),
    ]

    cols = st.columns(4)

    for index, (icon, value, label) in enumerate(metrics):

        with cols[index % 4]:

            st.markdown(
                f"""
<div class="metric-card" dir="rtl">

<div style="font-size:22px;">
{icon}
</div>

<div class="metric-value">
{value}
</div>

<div class="metric-label">
{label}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title" dir="rtl">🔎 Production Intelligence</div>',
        unsafe_allow_html=True,
    )

    categories = [
        (
            "👤 Characters",
            data.get("characters", []),
        ),
        (
            "📍 Locations",
            data.get("locations", []),
        ),
        (
            "🕐 Time of Day",
            data.get("time_of_day", []),
        ),
        (
            "⚡ Actions",
            data.get("actions", []),
        ),
        (
            "🎒 Props",
            data.get("props", []),
        ),
        (
            "👕 Wardrobe",
            data.get("wardrobe", []),
        ),
        (
            "🔊 Sound",
            data.get("sounds", []),
        ),
        (
            "💡 Lighting",
            data.get("lighting", []),
        ),
    ]

    for title, items in categories:

        if not items:
            continue

        with st.expander(
            f"{title}  •  {len(items)}",
            expanded=False,
        ):

            for item in items:

                if isinstance(item, dict):

                    value = item.get(
                        "text",
                        item.get(
                            "heading",
                            json.dumps(
                                item,
                                ensure_ascii=False,
                            ),
                        ),
                    )

                else:
                    value = str(item)

                st.markdown(
                    f"""
<div class="result-item">
{value}
</div>
""",
                    unsafe_allow_html=True,
                )

    dialogue = data.get("dialogue", [])

    if dialogue:

        st.markdown(
            '<div class="section-title" dir="rtl">💬 Dialogue</div>',
            unsafe_allow_html=True,
        )

        for entry in dialogue:

            character = entry.get(
                "character",
                "Unknown",
            )

            text = entry.get(
                "text",
                "",
            )

            st.markdown(
                f"""
<div class="result-card" dir="rtl">

<div class="result-header">
🎭 {character}
</div>

<div style="color:#b8c2d6; line-height:1.8;">
{text}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
<div class="status-pill">
● Screenplay analysis completed
</div>
""",
        unsafe_allow_html=True,
    )

if report_clicked:

    if not screenplay_input.strip():

        st.warning(
            "يرجى إدخال السيناريو أولاً."
        )

        st.stop()

    with st.spinner(
        "CinePilot يبني Production Bible..."
    ):

        try:

            bible = ProductionBible()

            report = bible.generate_full_report(
                screenplay_input
            )

        except Exception as exc:

            st.error(
                f"حدث خطأ أثناء إنشاء التقرير: {exc}"
            )

            st.stop()

    st.markdown(
        '<div class="section-title" dir="rtl">📘 CinePilot Production Bible</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="status-pill">
● Production report generated
</div>
""",
        unsafe_allow_html=True,
    )

    st.text_area(
        "Production Report",
        value=report,
        height=650,
    )

    st.download_button(
        label="⬇️ Download Production Bible",
        data=report,
        file_name="cinepilot_production_bible.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.markdown(
    '<div class="section-title" dir="rtl">⚙️ CinePilot Technology</div>',
    unsafe_allow_html=True,
)

t1, t2, t3, t4 = st.columns(4)

tech = [
    (
        "🧠",
        "Gemini",
        "AI reasoning and production intelligence",
    ),
    (
        "🤖",
        "Agentic Workflow",
        "Tool calling and structured workflows",
    ),
    (
        "🔎",
        "Semantic RAG",
        "Context-aware screenplay retrieval",
    ),
    (
        "📊",
        "ClickHouse",
        "Production data storage and analytics",
    ),
]

for column, item in zip(
    [t1, t2, t3, t4],
    tech,
):

    icon, title, text = item

    with column:

        st.markdown(
            f"""
<div class="feature-card" dir="rtl">

<div class="feature-icon">
{icon}
</div>

<div class="feature-title">
{title}
</div>

<div class="feature-text">
{text}
</div>

</div>
""",
            unsafe_allow_html=True,
        )

st.markdown(
    """
<div class="footer" dir="rtl">

<strong>CinePilot AI</strong>

<br>

AI-powered production intelligence for filmmakers.

<br><br>

Built with Gemini • Agentic AI • Semantic RAG • Google Cloud

</div>
""",
    unsafe_allow_html=True,
)
