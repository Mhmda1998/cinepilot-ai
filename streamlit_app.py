"""CinePilot AI - Streamlit Web Interface."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from app.tools.screenplay_tools import production_breakdown
from app.tools.gemini_analyzer import analyze_with_gemini

st.set_page_config(
    page_title="CinePilot AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CinePilot AI")
st.subheader("AI-Powered Screenplay Analysis & Production Copilot")

with st.sidebar:
    st.header("About")
    st.write("CinePilot AI analyzes screenplays and extracts production data.")
    st.write("Built with:")
    st.write("- Gemini 3.6 Flash")
    st.write("- Google ADK")
    st.write("- ClickHouse MCP")
    
    st.divider()
    st.header("Analysis Mode")
    mode = st.radio(
        "Choose mode:",
        ["Regex Analysis", "Gemini AI Analysis"]
    )

screenplay = st.text_area(
    "Paste your screenplay:",
    height=250,
    placeholder="INT. COFFEE SHOP - DAY\nJohn enters carrying a backpack..."
)

if st.button("🔍 Analyze", type="primary"):
    if screenplay.strip():
        with st.spinner("Analyzing..."):
            if mode == "Gemini AI Analysis":
                result = analyze_with_gemini(screenplay)
            else:
                result = production_breakdown(screenplay)
            
            if result.get("success"):
                st.success("✅ Analysis Complete!")
                
                st.subheader("📍 Scenes")
                scenes = result.get("scenes", [])
                st.write(f"Scene count: {len(scenes)}")
                
                st.subheader("👤 Characters")
                characters = result.get("characters", [])
                st.write(characters if characters else "None found")
                
                st.subheader("🎯 Props")
                props = result.get("props", [])
                st.write(props if props else "None found")
                
                st.subheader("👕 Wardrobe")
                wardrobe = result.get("wardrobe", [])
                st.write(wardrobe if wardrobe else "None found")
                
                st.subheader("🔊 Sounds")
                sounds = result.get("sounds", [])
                st.write(sounds if sounds else "None found")
                
                st.subheader("💡 Lighting")
                lighting = result.get("lighting", [])
                st.write(lighting if lighting else "None found")
            else:
                st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
    else:
        st.warning("Please enter screenplay text")
