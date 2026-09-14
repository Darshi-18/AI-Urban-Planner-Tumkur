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

# 2. INJECT EXAMINER-GRADE COMMAND CENTER NEON GRAPHICS (V5.0 PRO)
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
    
    /* Neon Data Grid Layout Panels */
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
st.markdown("`[SYSTEM REBOOTED // GENETIC TOPOLOGY ZONING MATRIX ACTIVE - LOCATION: TUMAKURU]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 MATRIX FREQUENCY HUB")

sector_profile = st.sidebar.selectbox("Active Density Profile Preset", ["Suburban Neighborhood Grid", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Index Threshold", 80, 140, 120, 5)
transit_val = st.sidebar.slider("Arterial Network Extraction Sensitivity", 20, 80, 45, 5)

# Resolution variable mapping keys
b_size = 24
b_gap = 10
if sector_profile == "High-Density Core Matrix":
    b_size, b_gap = 16, 6
if sector_profile == "Eco-Fringe Settlement":
    b_size, b_gap = 32, 14

st.sidebar.markdown("---")
st.sidebar.markdown("`[ZONING SPECTRUM INTERPRETATION]`")
st.sidebar.markdown("🟦 **Electric Cyan:** Commercial Core Infrastructure")
st.sidebar.markdown("🟧 **Neon Terracotta:** Planned Dwellings Footprints")
st.sidebar.markdown("🟪 **Neon Fuchsia:** Public Utility Centers")
st.sidebar.markdown("🟩 **Bio-Synthetic Sage:** Protected Eco-Green Belts")
st.sidebar.markdown("⬜ **Pure Platinum:** Primary Highway Transportation Networks")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD TARGET GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(raw_img)
    
    # Scale coordinates dynamically to bypass browser dimension caching limits
    orig_h, orig_w, _ = img_np.shape
    scale_factor = 512 / max(orig_h, orig_w)
    new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)
    
    img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    h, w, c = img_resized.shape
    
    # Core Computer Vision Feature Extraction Execution Pipeline
    gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (13, 13), 0)
    
    # Extract crisp transit corridors cleanly
    edges = cv2.Canny(blurred, transit_val, transit_val * 2.5)
    edge_y, edge_x = np.where(edges == 255)
    
    # Isolate vegetative fields smoothly
    _, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((13, 13), np.uint8), iterations=1)
    smooth_green = cv2.GaussianBlur(green_mask, (29, 29), 0)
    
    # =========================================================================
    # RESPONSIVE HIGH-REALISM V5.0 BLUEPRINT SYNTHESIS ENGINE
    # =========================================================================
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    blueprint[:] = (10, 20, 25) # Premium dark blueprint canvas backing
    
    # 1. Overlay Preserved Eco-Green Landscapes (Matte Sage Green)
    blueprint[smooth_green > 100] = (24, 76, 58)
    
    spacing = b_size + b_gap
    res_count = 0
    comm_count = 0
    utility_count = 0
    
    # 2. Generative Zoning Matrix Calculation Loops
    for y in range(30, h - spacing, spacing):
        for x in range(30, w - spacing, spacing):
            
            # Distance mapping relative to primary extracted highway route
            if len(edge_x) > 0:
                dist_to_road = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
            else:
                dist_to_road = 999.0
                
            # ZONE 1: IMMEDIATE HIGHWAY PERIMETER -> High-Density Commercial Core (Electric Cyan)
            if dist_to_road < 20:
                if x % 2 == 0:
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size - 4), (0, 240, 255), -1) 
                    cv2.rectangle(blueprint, (x, y + b_size - 4), (x + b_size // 2, y + b_size + 2), (0, 240, 255), -1)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size - 4), (255, 255, 255), 1)
                    comm_count += 1
                    
            # ZONE 2: DEVELOPABLE OPEN VALLEYS -> Reallocates Orange Houses and Pink Utilities perfectly
            elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                # Every 6th block is designated as a civic utility station to break grid monotony
                if (x + y) % 6 == 0:
                    # Public Utility Centers (Neon Fuchsia / Pink Circles)
                    cv2.circle(blueprint, (x + b_size//2, y + b_size//2), b_size//2 - 2, (255, 0, 127), -1)
                    cv2.circle(blueprint, (x + b_size//2, y + b_size//2), b_size//2 - 2, (255, 255, 255), 1)
                    utility_count += 1
                else:
                    # Planned Dwellings Footprints (Neon Terracotta / Vibrant Orange Neighborhoods)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (8, 48, 56), 1) # Property plot border
                    h_dim = int(b_size * 0.6)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_dim, y + h_dim), (255, 85, 0), -1) # Terracotta footprint
                    cv2.line(blueprint, (x + h_dim, y + 4), (x + b_size, y + 4), (0, 240, 255), 1) # Local street path link
                    res_count += 1

    # 3. HIGH-CONTRAST NEON TRANSIT NETWORKS OVERLAYS
    for y_line in range(0, h, spacing * 2):
        cv2.line(blueprint, (0, y_line), (w, y_line), (4, 32, 40), 1)
    for x_line in range(0, w, spacing * 2):
        cv2.line(blueprint, (x_line, 0), (x_line, h), (4, 32, 40), 1)
        
    # Draw primary highway corridor cleanly on top
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (240, 244, 248) # Platinum road casing
        blueprint[edges == 255] = (0, 240, 255)         # Neon cyan median split divider
        
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
        st.markdown(f"<div class='dashboard-panel'><div class='panel-value'>{utility_count} Units</div><div class='panel-label'>⚡ PUBLIC UTILITIES</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # MULTI-RESOLUTION SIDE-BY-SIDE PRESENTATION DISPLAY GRID
    # =========================================================================
    ui_col1, ui_col2 = st.columns(2)
    
    with ui_col1:
        st.subheader("📡 SOURCE DATA FOOTPRINT INGESTION")
        st.image(img_resized, use_container_width=True)
        
    with ui_col2:
        st.subheader("⚡ GENERATIVE METROPOLIS MATRIX BLUEPRINT")
        st.image(blueprint, use_container_width=True)
        
    # EXPORT MANAGER LINK CONTROLLER
    final_output_image = Image.fromarray(blueprint)
    final_output_image.save("cyber_metropolis_masterplan.png")
    with open("cyber_metropolis_masterplan.png", "rb") as file:
        st.download_button(
            label="📥 DOWNLOAD CYBER BLUEPRINT CONFIGURATION LOG",
            data=file,
            file_name="cyber_metropolis_masterplan.png",
            mime="image/png"
        )
else:
    st.info("📡 SYSTEM STANDBY // AWAITING SATELLITE TERRAIN INPUT LAYER TO INITIALIZE RADAR PROTOCOLS.")
