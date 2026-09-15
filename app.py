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
    .main { background-color: #030a0d; color: #e2f1f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #00f0ff; color: #020d0f; border-radius: 4px;
        border: 1px solid #00f0ff; width: 100%; font-weight: bold; font-size: 14px;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.3); text-transform: uppercase;
    }
    .stSlider > div > div > div > div { background-color: #ff5500; }
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
st.markdown("`[SYSTEM PROTOCOL: GREENFIELD TARGET CORRIDOR LABELEDBLUEPRINT - SITE: TUMAKURU]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 MATRIX FREQUENCY HUB")

sector_profile = st.sidebar.selectbox("Active Density Profile Preset", ["Suburban Neighborhood Grid", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Index Threshold", 80, 140, 120, 5)
transit_val = st.sidebar.slider("Arterial Network Extraction Sensitivity", 20, 80, 50, 5)

# Resolution variables mapping
b_size, b_gap = 26, 12
if sector_profile == "High-Density Core Matrix":
    b_size, b_gap = 20, 8
if sector_profile == "Eco-Fringe Settlement":
    b_size, b_gap = 36, 18

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 BLUEPRINT MAP KEY:**")
st.sidebar.markdown("🟦 **Electric Cyan:** Commercial Core Infrastructure")
st.sidebar.markdown("🟧 **Neon Terracotta:** Planned Dwellings Districts")
st.sidebar.markdown("🟩 **Bio-Synthetic Sage:** Protected Eco-Green Belts")
st.sidebar.markdown("⬜ **Pure Platinum:** Primary Highway Transportation Networks")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Scale coordinates to balance smaller resolution displays layout constraints
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 600 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # Clean Core Feature Extraction Image Filtering Pipelines
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    
    # Extract clean transportation network traces
    edges = cv2.Canny(blurred, transit_val, transit_val * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    # Isolate vegetative fields smoothly
    _, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((15, 15), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (35, 35), 0)
    
    # =========================================================================
    # HIGH-REALISM BLUEPRINT GENERATION PIPELINE WITH LABELS
    # =========================================================================
    with st.spinner("⚡ Generating high-fidelity blueprint with map labels..."):
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (10, 20, 25) # Premium deep teal city grid canvas backing
        
        # 1. Overlay Preserved Eco-Green Landscapes (Matte Green fields)
        blueprint[smooth_green > 100] = (24, 76, 58)
        
        spacing = b_size + b_gap
        res_count = 0
        comm_count = 0
        
        # Tracking center locations to drop visual text markers neatly without overlap
        commercial_labeled = False
        residential_labeled = False
        highway_labeled = False
        
        # 2. Generative Zoning Matrix Calculation Loops
        for y in range(40, h - spacing, spacing):
            for x in range(40, w - spacing, spacing):
                
                # Check pixel proximity to primary extracted highway route
                if len(edge_x) > 0:
                    dist_to_road = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_road = 999.0
                    
                # ZONE 1: HIGHWAY CORRIDOR ACCESS -> High-Density Commercial Complexes (Cyan)
                if dist_to_road < 35:
                    if smooth_green[y + b_size//2, x + b_size//2] <= 100:
                        cv2.rectangle(blueprint, (x+1, y+1), (x+b_size-1, y+b_size-1), (0, 240, 255), -1) 
                        cv2.rectangle(blueprint, (x+1, y+1), (x+b_size-1, y+b_size-1), (255, 255, 255), 1)
                        comm_count += 1
                        
                        # Drop text marker near the upper section of commercial cluster
                        if not commercial_labeled and y > 80:
                            cv2.putText(blueprint, "COMMERCIAL HUB", (x - 10, y - 8), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 240, 255), 2, cv2.LINE_AA)
                            commercial_labeled = True
                            
                # ZONE 2: BUILDABLE FIELD VALLEYS -> Planned Residential Districts (Orange)
                elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                    cv2.rectangle(blueprint, (x+1, y+1), (x+b_size-1, y+b_size-1), (255, 110, 0), -1)
                    cv2.rectangle(blueprint, (x+1, y+1), (x+b_size-1, y+b_size-1), (4, 45, 54), 1)
                    res_count += 1
                    
                    # Drop text marker near the center section of the residential grid
                    if not residential_labeled and y > h // 2:
                        cv2.putText(blueprint, "RESIDENTIAL ZONE", (x - 20, y - 8), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 110, 0), 2, cv2.LINE_AA)
                        residential_labeled = True

        # 3. HIGH-Visibility PRIMARY TRANSIT ARTERY OVERLAY
        if len(edge_x) > 0:
            road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
            blueprint[road_casing == 255] = (240, 244, 248) # Clean platinum road bed
            blueprint[edges == 255] = (0, 240, 255)         # Neon cyan median lines
            
            # Place label exactly on top of the primary highway corridor path track
            mid_idx = len(edge_x) // 2
            cv2.putText(blueprint, "MAIN TRANSIT ARTERY", (edge_x[mid_idx] - 60, edge_y[mid_idx] - 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2, cv2.LINE_AA)
                        
        # 4. ENVIRONMENT LABEL BUFFER
        if np.sum(smooth_green > 100) > 0:
            green_y, green_x = np.where(smooth_green > 100)
            g_mid = len(green_x) // 3
            cv2.putText(blueprint, "ECO-PRESERVATION BELT", (green_x[g_mid] - 50, green_y[g_mid]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (140, 240, 160), 2, cv2.LINE_AA)
        
    # =========================================================================
    # NEON COMMAND CENTER DATA MONITORS CONTROL MODULE
    # =========================================================================
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    
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
    # RESPONSIVE VIEW DISPLAY COLUMNS
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("📡 SOURCE DATA FOOTPRINT INGESTION")
        st.image(img_resized, use_container_width=True)
        
    with ui_col2:
        st.subheader("⚡ GENERATIVE METROPOLIS MATRIX BLUEPRINT")
        st.image(blueprint, use_container_width=True)
        
