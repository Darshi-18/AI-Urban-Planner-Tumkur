import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import time

# 1. INITIALIZE MASTER COMMAND PORTAL CORE
st.set_page_config(
    page_title="NEURAL METROPOLIS V4.0 | Command Core", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT CYBER HYPER-GLOW THEME INTERFACE LAYOUT STYLES
st.markdown("""
    <style>
    .main { background-color: #020d0f; color: #e2f1f5; font-family: 'Courier New', Courier, monospace; }
    div.stButton > button:first-child {
        background-color: #00f0ff; color: #020d0f; border-radius: 0px;
        border: 2px solid #00f0ff; width: 100%; font-weight: bold; font-size: 16px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4); text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stSlider > div > div > div > div { background-color: #00f0ff; }
    .stSelectbox div[data-baseweb="select"] { background-color: #041d22; color: #00f0ff; border: 1px solid #00f0ff; border-radius: 0px; }
    .metric-panel {
        background-color: #031a1e; padding: 20px; border-radius: 0px;
        border: 1px solid #00f0ff; border-left: 5px solid #00f0ff; text-align: center;
        box-shadow: 0 0 10px rgba(0,240,255,0.1);
    }
    .metric-value { font-size: 30px; font-weight: 800; color: #00f0ff; text-shadow: 0 0 5px rgba(0,240,255,0.5); }
    .metric-label { font-size: 10px; color: #78a5ad; text-transform: uppercase; letter-spacing: 1px; margin-top: 6px; }
    .console-box {
        background-color: #01080a; border: 1px solid #ff0055; padding: 12px;
        font-family: 'Courier New', monospace; color: #ff0055; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NEURAL METROPOLIS V4.0 — Autonomous Command Core")
st.markdown("`[SYSTEM PROTOCOL: GREENFIELD TARGET CORRIDOR MASTER PLANNING OVERLAY - SITE: TUMAKURU]`")
st.markdown("---")

# =========================================================================
# INTERACTIVE SYSTEM MAPPING CONTROL CONTROLLERS (SIDEBAR)
# =========================================================================
st.sidebar.header("📡 RADAR CORE MATRIX")
st.sidebar.markdown("`// ADJUST MATRIX FREQUENCIES`")

sector_density = st.sidebar.selectbox("Zoning Profile Preset", ["High-Density Core Matrix", "Suburban Neighborhood Matrix", "Eco-Fringe Modular Settlement"])
preservation_idx = st.sidebar.slider("Eco-Preservation Index Threshold", 80, 140, 115, 5)
transit_hierarchy = st.sidebar.slider("Arterial Network Extraction Sensitivity", 20, 80, 50, 5)

# Resolution tuning parameters
b_size, b_gap = 24, 10
if sector_density == "High-Density Core Matrix":
    b_size, b_gap = 18, 6
if sector_density == "Eco-Fringe Modular Settlement":
    b_size, b_gap = 34, 16

st.sidebar.markdown("---")
st.sidebar.markdown("`[MATRIX SPECTRUM INTERPRETATION]`")
st.sidebar.markdown("🟦 **Electric Cyan:** Commercial Core Infrastructure")
st.sidebar.markdown("🟧 **Neon Terracotta:** Planned Dwellings Footprints")
st.sidebar.markdown("🟩 **Bio-Synthetic Sage:** Protected Eco-Green Belts")
st.sidebar.markdown("⬜ **Pure Platinum:** Primary Highway Transportation Networks")

# =========================================================================
# GEOSPATIAL FILE INGESTION UTILITY
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Scale coordinates to protect UI container bounds
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # -------------------------------------------------------------------------
    # 🎬 AUTOMATED LAYOUT SEQUENCING STATUS ANIMATION BLOCK
    # -------------------------------------------------------------------------
    st.markdown("<div class='console-box'>⚠️ INITIALIZING AUTONOMOUS MODEL SCANNING MATRICES... PIPELINE STAGE: ACTIVE</div>", unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("⚙️ STAGE 1/3: Analyzing terrain pixel profiles and computing spatial cost metrics...")
    time.sleep(0.4)
    progress_bar.progress(35)
    
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred_heavy = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred_heavy, transit_hierarchy, transit_hierarchy * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    status_text.text("🛰️ STAGE 2/3: Segmenting high-contrast transit corridors and mapping natural greenbelts...")
    time.sleep(0.4)
    progress_bar.progress(70)
    
    _, green_mask = cv2.threshold(blurred_heavy, preservation_idx, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((11, 11), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)
    
    status_text.text("🧠 STAGE 3/3: Running sector grid generation and compiling vector blueprint layouts...")
    time.sleep(0.3)
    progress_bar.progress(100)
    
    status_text.empty()
    progress_bar.empty()
    
    # =========================================================================
    # RESPONSIVE HIGH-REALISM BLUEPRINT SYNTHESIS ENGINE
    # =========================================================================
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    blueprint[:] = (1, 14, 18) # Neon Cyber Backdrop Tones
    
    # 1. Plot Preserved Landscape Buffers (Soft emerald geometry blocks)
    blueprint[smooth_green > 100] = (16, 61, 46)
    
    spacing = b_size + b_gap
    res_count = 0
    comm_count = 0
    
    # 2. Generative Zoning Matrix Optimization Pass Loops
    for y in range(20, h - spacing, spacing):
        for x in range(20, w - spacing, spacing):
            
            if len(edge_x) > 0:
                dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
            else:
                dist_to_transit = 999.0
                
            # FIXED LOGIC HIERARCHY: Restrict Commercial nodes to the immediate narrow highway path (distance < 20)
            if dist_to_transit < 20:
                if x % 2 == 0 and y % 2 == 0:
                    # Draw futuristic neon high-density commercial centers (Electric Cyan)
                    cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (0, 240, 255), -1) 
                    cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (0, 240, 255), -1)
                    cv2.rectangle(blueprint, (x, y), (x + b_size + 2, y + b_size - 4), (255, 255, 255), 1)
                    comm_count += 1
            # Allocate Residential Dwellings in flat buildable plots away from heavy transit lines
            elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                # Draw property boundaries and individual terracotta dwellings (Neon Terracotta/Orange)
                cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (4, 45, 54), 1)
                h_dim = int(b_size * 0.6)
                cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (255, 110, 0), -1) 
                cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (0, 240, 255), 1)
                res_count += 1

    # 3. OVERLAY HIGH-DENSITY TRANSIT VECTOR OVERLAYS
    for y_line in range(0, h, spacing * 3):
        cv2.line(blueprint, (0, y_line), (w, y_line), (3, 30, 36), 1)
    for x_line in range(0, w, spacing * 3):
        cv2.line(blueprint, (x_line, 0), (x_line, h), (3, 30, 36), 1)
        
    # Superimpose high-visibility primary infrastructure routes cleanly
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (255, 255, 255) 
        blueprint[edges == 255] = (0, 240, 255)         
        
    # =========================================================================
    # COMPUTATIONAL DATA METRICS MONITOR CONTROL BOARD
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    infrastructure_km = int(np.sum(edges == 255) / 100) if len(edge_x) > 0 else 0
    
    with m_col1:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{res_count:,}</div><div class='metric-label'>⚡ ALLOCATED DWELLINGS</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{comm_count}</div><div class='metric-label'>⚡ COMMERCIAL NODES</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{green_ratio}%</div><div class='metric-label'>⚡ ECO-PRESERVATION INDEX</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{infrastructure_km} KM</div><div class='metric-label'>⚡ TRANSIT NETWORK INTEGRATION</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # SIDE-BY-SIDE PRESENTATION COLUMNS (RESPONSIVE VIEW ENABLED)
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("📡 SOURCE DATA FOOTPRINT INGESTION")
        st.image(img_resized, use_container_width=True)
        
    with ui_col2:
        st.subheader("⚡ GENERATIVE METROPOLIS MATRIX BLUEPRINT")
