"""CinePilot AI - Streamlit Web Interface."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from app.tools.screenplay_tools import production_breakdown
from app.tools.gemini_analyzer import analyze_with_gemini
from app.tools.production_bible import ProductionBible

st.set_page_config(
    page_title="CinePilot AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CinePilot AI")
st.subheader("AI-Powered Screenplay Analysis & Production Copilot")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("CinePilot AI analyzes screenplays and extracts production data.")
    st.write("Built with:")
    st.write("- Gemini 3.6 Flash")
    st.write("- Google ADK")
    st.write("- ClickHouse Cloud")
    st.write("- 11+ Production Tools")
    
    st.divider()
    st.header("Analysis Mode")
    mode = st.radio(
        "Choose mode:",
        ["Full Production Bible", "Quick Analysis"]
    )

# Main area
screenplay = st.text_area(
    "Paste your screenplay:",
    height=250,
    placeholder="INT. COFFEE SHOP - DAY\nJohn enters carrying a backpack..."
)

if st.button("🚀 Analyze", type="primary", use_container_width=True):
    if screenplay.strip():
        with st.spinner("Analyzing... Please wait"):
            if mode == "Full Production Bible":
                bible = ProductionBible()
                report = bible.generate_full_report(screenplay)
                st.success("✅ Production Bible Generated!")
                st.code(report, language="text")
            else:
                result = production_breakdown(screenplay)
                st.success("✅ Analysis Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📍 Scenes")
                    st.write(result.get("scene_count", 0))
                    st.subheader("👤 Characters")
                    st.write(result.get("characters", []))
                with col2:
                    st.subheader("🎯 Props")
                    st.write(result.get("props", []))
                    st.subheader("👕 Wardrobe")
                    st.write(result.get("wardrobe", []))
    else:
        st.warning("Please enter screenplay text")
