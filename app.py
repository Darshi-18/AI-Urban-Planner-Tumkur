import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

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
        background-color: #01080a; border: 1px solid #00f0ff; padding: 12px;
        font-family: 'Courier New', monospace; color: #00f0ff; margin-bottom: 20px;
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

# Setup layout spacing variables directly without function restrictions
b_size, b_gap = 26, 12
if sector_density == "High-Density Core Matrix":
    b_size, b_gap = 20, 8
if sector_density == "Eco-Fringe Modular Settlement":
    b_size, b_gap = 36, 18

st.sidebar.markdown("---")
st.sidebar.markdown("`[MATRIX SPECTRUM INTERPRETATION]`")
st.sidebar.markdown("🟦 **Electric Cyan:** Commercial Core Complexes")
st.sidebar.markdown("🟧 **Neon Terracotta:** Residential House Footprints")
st.sidebar.markdown("🟪 **Neon Fuchsia:** Public Utility Centers")
st.sidebar.markdown("🟩 **Bio-Synthetic Sage:** Protected Eco-Green Belts")
st.sidebar.markdown("⬜ **Pure Platinum:** Primary Highway Transport Arteries")

# =========================================================================
# GEOSPATIAL FILE INGESTION UTILITY
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Scale coordinates dynamically to fix smaller container bounds
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    st.markdown("<div class='console-box'>⚡ CACHE DEACTIVATED: PROCESSING ARCHITECTURAL bluePRINT NEIGHBORHOODS INSTANTLY...</div>", unsafe_allow_html=True)
    
    # Core Image Filtering Pipeline
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred_heavy = cv2.GaussianBlur(gray, (13, 13), 0)
    edges = cv2.Canny(blurred_heavy, transit_hierarchy, transit_hierarchy * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    _, green_mask = cv2.threshold(blurred_heavy, preservation_idx, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((13, 13), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (29, 29), 0)
    
    # =========================================================================
    # HIGH-REALISM BLUEPRINT GENERATION SUITE
    # =========================================================================
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    blueprint[:] = (2, 16, 20) # Premium dark teal city grid backing
    
    # 1. Paint Smooth Preserved Natural Buffers (Matte Green)
    blueprint[smooth_green > 100] = (20, 68, 52)
    
    spacing = b_size + b_gap
    res_count, comm_count, utility_count = 0, 0, 0
    
    # 2. Advanced Multi-Tier Spatial Partitioning Loop
    for y in range(30, h - spacing, spacing):
        for x in range(30, w - spacing, spacing):
            
            # Distance mapping relative to primary extracted road coordinates
            if len(edge_x) > 0:
                dist_to_road = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
            else:
                dist_to_transit = 999.0
                
            # ZONE A: HIGHWAY ACCESS (Distance < 24) -> High-density Commercial Core Skyscrapers
            if dist_to_road < 24:
                if x % 2 == 0:
                    # Draw futuristic, distinct L-shaped compound commercial properties
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size - 4), (0, 240, 255), -1) # Cyan
                    cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (0, 240, 255), -1)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size - 4), (255, 255, 255), 1) # White grid accent line
                    comm_count += 1
                    
            # ZONE B: SUBDIVISION VALLEYS -> Open buildable land away from highways
            elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                # Randomly allocate a public civic utility sector to break monotony
                if (x + y) % 7 == 0:
                    # Draw Public Utilities (Fuchsia/Pink Centers)
                    cv2.circle(blueprint, (x + b_size//2, y + b_size//2), b_size//2 - 2, (255, 0, 127), -1)
                    cv2.circle(blueprint, (x + b_size//2, y + b_size//2), b_size//2 - 2, (255, 255, 255), 1)
                    utility_count += 1
                else:
                    # Draw Structured Residential Parcels (Terracotta Orange Houses with Access Roads)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (6, 54, 64), 1) # Fine property border
                    h_dim = int(b_size * 0.55)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (255, 100, 34), -1) # Orange house footprint
                    cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (0, 240, 255), 1) # Cyan access street link
                    res_count += 1

    # 3. HIGH-CONTRAST VECTOR STREET Dividers
    for y_line in range(0, h, spacing * 2):
        cv2.line(blueprint, (0, y_line), (w, y_line), (3, 26, 32), 1)
    for x_line in range(0, w, spacing * 2):
        cv2.line(blueprint, (x_line, 0), (x_line, h), (3, 26, 32), 1)
        
    # Draw primary highway corridor cleanly on top
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (240, 244, 248) # Platinum road casing
        blueprint[edges == 255] = (0, 240, 255)         # Neon cyan divider
        
    # =========================================================================
    # REAL-TIME LIVE DATA ANALYSIS COMMAND CENTER METRICS
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    total_infrastructure_nodes = comm_count + utility_count
    
    with m_col1:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{res_count:,}</div><div class='metric-label'>⚡ RESIDENTIAL DWELLINGS</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{total_infrastructure_nodes}</div><div class='metric-label'>⚡ CIVIC & COMMERCIAL NODES</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{green_ratio}%</div><div class='metric-label'>⚡ ECO-PRESERVATION INDEX</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='metric-panel'><div class='metric-value'>{utility_count} Units</div><div class='metric-label'>⚡ PUBLIC UTILITIES</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # SIDE-BY-SIDE PRESENTATION COLUMNS (RESPONSIVE VIEW)
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("📡 SOURCE DATA FOOTPRINT INGESTION")
        st.image(img_resized, use_container_width=True)
        
    with ui_col2:
        st.subheader("⚡ GENERATIVE METROPOLIS MATRIX BLUEPRINT")
        st.image(blueprint, use_container_width=True)
        
    # EXPORT MANAGER LINK
