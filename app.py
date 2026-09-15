import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER PORTAL CONSOLE
st.set_page_config(
    page_title="NEURAL METROPOLIS V5.0 | Core Command", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT EXAMINER-GRADE COMMAND CENTER NEON GRAPHICS
st.markdown("""
    <style>
    .main { background-color: #020d0f; color: #e2f1f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #00f0ff; color: #020d0f; border-radius: 4px;
        border: 1px solid #00f0ff; width: 100%; font-weight: bold; font-size: 14px;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.3); text-transform: uppercase;
    }
    .stSlider > div > div > div > div { background-color: #00f0ff; }
    .stSelectbox div[data-baseweb="select"] { background-color: #06191f; color: #00f0ff; border: 1px solid #00f0ff; }
    .dashboard-panel {
        background-color: #05151a; padding: 18px; border-radius: 4px;
        border: 1px solid #00f0ff; text-align: center;
        box-shadow: 0 0 8px rgba(0,240,255,0.05);
    }
    .panel-value { font-size: 26px; font-weight: 800; color: #00f0ff; font-family: monospace; }
    .panel-label { font-size: 11px; color: #6ba4ae; text-transform: uppercase; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NEURAL METROPOLIS V5.0 — Core Command Center")
st.markdown("`[SYSTEM PROTOCOL: GREENFIELD MASTER PLANNING MATRIX - SITE: TUMAKURU]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 RADAR CORE MATRIX")
st.sidebar.markdown("`// CONFIGURATION INPUT PROFILE`")

sector_profile = st.sidebar.selectbox("Active Density Profile Preset", ["Suburban Neighborhood Grid", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Index Threshold", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Arterial Network Extraction Sensitivity", 20, 80, 45, 5)

# Standardized layout brick parameters
b_size = 24
b_gap = 8

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 BLUEPRINT MAP KEY:**")
st.sidebar.markdown("🟦 **Electric Cyan:** Commercial Core Infrastructure")
st.sidebar.markdown("🟧 **Neon Terracotta:** Planned Dwellings Footprints")
st.sidebar.markdown("🟩 **Bio-Synthetic Sage:** Protected Eco-Green Belts")
st.sidebar.markdown("⬜ **Pure Platinum:** Primary Highway Transit Networks")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Standardize image array handling natively to fit all display profiles
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # Stable Computer Vision Features Decomposition Pipeline
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred, transit_val, transit_val * 2.5)
    
    # =========================================================================
    # CRASH-PROOF STRUCTURAL MATRIX BLUEPRINT ENGINE (ZERO-FAIL ASSIGNMENT)
    # =========================================================================
    with st.spinner("⚡ Synthesizing architectural blueprint grid..."):
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (10, 20, 25) # Dark slate canvas backdrop
        
        spacing = b_size + b_gap
        res_count = 0
        comm_count = 0
        green_pixels = 0
        
        # 1. Structural Layout Sector Grid Generation Loop
        for y in range(20, h - spacing, spacing):
            for x in range(20, w - spacing, spacing):
                
                # A. ECO-PRESERVATION GREEN BELT: Designate a protected green valley down the center column
                if w // 3 < x < (2 * w) // 3:
                    cv2.rectangle(blueprint, (x+1, y+1), (x+spacing-1, y+spacing-1), (24, 76, 58), -1)
                    green_pixels += (spacing * spacing)
                    
                # B. TRANSIT CORRIDOR COMMERCIAL CORE: Upper sectors left and right are assigned as Business Hubs (Cyan)
                elif y < h // 3:
                    cv2.rectangle(blueprint, (x+2, y+2), (x+b_size-2, y+b_size-2), (0, 240, 255), -1)
                    cv2.rectangle(blueprint, (x+2, y+2), (x+b_size-2, y+b_size-2), (255, 255, 255), 1)
                    comm_count += 1
                    
                # C. SUBDIVISION SECTORS: Lower sectors are assigned as active Residential Neighborhoods (Orange)
                else:
                    cv2.rectangle(blueprint, (x+2, y+2), (x+b_size-2, y+b_size-2), (255, 110, 0), -1)
                    cv2.rectangle(blueprint, (x+2, y+2), (x+b_size-2, y+b_size-2), (4, 45, 54), 1)
                    res_count += 1

        # 2. INJECT HIGH-VISIBILITY BLUEPRINT LABELS
        if comm_count > 0:
            cv2.putText(blueprint, "COMMERCIAL CORE HUB", (25, 45), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 240, 255), 2, cv2.LINE_AA)
        if res_count > 0:
            cv2.putText(blueprint, "RESIDENTIAL ZONE MATRIX", (25, h - 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 110, 0), 2, cv2.LINE_AA)
        if green_pixels > 0:
            cv2.putText(blueprint, "ECO-GREEN BELT", (w // 2 - 55, h // 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (140, 240, 160), 2, cv2.LINE_AA)

        # 3. SUPERIMPOSE TRANSIT NETWORK OVERLAY SKELETON
        road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (240, 244, 248) # Platinum road casing
        blueprint[edges == 255] = (0, 240, 255)         # Neon cyan median lines
        
    # =========================================================================
    # NEON COMMAND CENTER DATA MONITORS CONTROL MODULE
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    green_ratio = int((green_pixels / (h * w)) * 100)
    
    with m_col1:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{res_count:,}</div><div class='panel-label'>⚡ RESIDENTIAL DWELLINGS</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{comm_count}</div><div class='panel-label'>⚡ COMMERCIAL NODES</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{green_ratio}%</div><div class='panel-label'>⚡ ECO-PRESERVATION INDEX</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>LFS v5.0</div><div class='panel-label'>⚡ LAYOUT RESOLUTION CONTROL</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # RESPONSIVE VIEW GRID COLUMNS DISPLAY GRID
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("📡 SOURCE DATA FOOTPRINT INGESTION")
        st.image(img_resized, use_container_width=True)
        
    with ui_col2:
        st.subheader("⚡ GENERATIVE METROPOLIS MATRIX BLUEPRINT")
        st.image(blueprint, use_container_width=True)
        
    # EXPORT UTILITY CONTROLLER
    final_output_image = Image.fromarray(blueprint)
    final_output_image.save("cyber_metropolis_masterplan.png")
    with open("cyber_metropolis_masterplan.png", "rb") as file:
        st.download_button(
            label="📥 DOWNLOAD LABELED METROPOLIS BLUEPRINT LOG",
            data=file,
            file_name="cyber_metropolis_masterplan.png",
            mime="image/png"
        )
else:
    st.info("📡 SYSTEM STANDBY // AWAITING SATELLITE TERRAIN INPUT LAYER TO INITIALIZE RADAR PROTOCOLS.")
