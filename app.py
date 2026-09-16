import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER PORTAL CONSOLE
st.set_page_config(
    page_title="UrbanAI Studio | GIS Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT SLEEK MODERN DARK ARCHITECTURAL CORE THEME
st.markdown("""
    <style>
    .main { background-color: #0b132b; color: #edf2f4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    div.stButton > button:first-child {
        background-color: #3a86ff; color: white; border-radius: 4px;
        border: none; width: 100%; font-weight: bold; padding: 12px;
        box-shadow: 0px 4px 10px rgba(58, 134, 255, 0.3);
    }
    .stSlider > div > div > div > div { background-color: #3a86ff; }
    .stSelectbox div[data-baseweb="select"] { background-color: #1c2541; color: #edf2f4; border: 1px solid #3a86ff; }
    .metric-panel {
        background-color: #1c2541; padding: 20px; border-radius: 6px;
        border-top: 4px solid #3a86ff; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #4cc9f0; }
    .metric-label { font-size: 11px; color: #b0c4de; text-transform: uppercase; margin-top: 4px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ UrbanAI Studio™ — Engineering Layout Suite")
st.markdown("`[SYSTEM PROTOCOL: DYNAMIC TECHNICAL RECONSTRUCTION CORE]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 LAYOUT FREQUENCY CONFIGURATION")

sector_profile = st.sidebar.selectbox("Active Density Target", ["High-Density Commercial Core", "Suburban Neighborhood Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Eco Preservation Threshold", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Transit Extraction Sensitivity", 20, 80, 45, 5)

b_size = 28
b_gap = 10

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 GEOSPATIAL MAP LEGEND:**")
st.sidebar.markdown("🟥🟪 **Angled Hatch Lines:** High-Density Commercial Core")
st.sidebar.markdown("🟦⬜ **Horizontal Subdivisions:** Medium-Density Residential")
st.sidebar.markdown("🟩🟢 **Dotted Pasture:** Urban Agriculture & Greenbelts")
st.sidebar.markdown("⬜🛣️ **Double Slate Lines:** Primary Arterial Transit Highways")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is None:
    st.info("ℹ️ System standby. Please upload geographic satellite terrain imagery to initiate the planning pipeline.")
    st.stop()

# =========================================================================
# HIGH-FIDELITY TECHNICAL VECTOR RECONSTRUCTION ENGINE
# =========================================================================
raw_img = Image.open(uploaded_file).convert("RGB")
img_np = np.array(raw_img)

# Scale canvas dimensions dynamically to guarantee fluid loading speeds
orig_h, orig_w, _ = img_np.shape
scale_factor = 650 / max(orig_h, orig_w)
new_h, new_w = int(orig_h * scale_factor), int(orig_w * scale_factor)

img_resized = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
h, w, c = img_resized.shape

# Core Image Signal Filtering Processing Pipeline
gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# Extract real-time highway corridors and green clusters matching the input image
edges = cv2.Canny(blurred, transit_val, transit_val * 2.5)
edge_y, edge_x = np.where(edges == 255)

_, green_mask = cv2.threshold(blurred, preservation_val, 255, cv2.THRESH_BINARY_INV)
green_mask = cv2.dilate(green_mask, np.ones((9, 9), np.uint8), iterations=1)
smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)

with st.spinner("⚡ Simulating engineering blueprint drawing..."):
    # Create the base slate grey structural engineering backdrop canvas
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    blueprint[:] = (53, 59, 72) # Slate Grey
    
    # 1. GENERATE DOTTED GREENBELT FIELDS (Matches your actual terrain foliage)
    blueprint[smooth_green > 100] = (76, 154, 42) # Base Green Fill
    # Inject fine technical stipple dots into the greenbelt fields
    for y_dot in range(0, h, 8):
        for x_dot in range(0, w, 8):
            if smooth_green[y_dot, x_dot] > 100:
                cv2.circle(blueprint, (x_dot, y_dot), 1, (139, 195, 74), -1)
                
    spacing = b_size + b_gap
    res_count = 0
    comm_count = 0
    
    commercial_cushion = int(55 + (45 - transit_val) * 0.5)
    density_mod = 1.35 if sector_profile == "High-Density Commercial Core" else (0.65 if sector_profile == "Eco-Fringe Settlement" else 1.0)
    
    # 2. GENERATE DETAILED HATCH & SUBDIVISION BLOCKS
    for y in range(40, h - spacing, spacing):
        for x in range(40, w - spacing, spacing):
            
            # Map distance to the real extracted highway lines dynamically
            if len(edge_x) > 0:
                dist_to_transit = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
            else:
                dist_to_transit = 999.0
                
            if smooth_green[y + b_size//2, x + b_size//2] <= 100:
                
                # ZONE A: HIGHWAY ACCESS -> High-Density Commercial Core (Angled Hatch Patterns)
                if dist_to_transit < commercial_cushion:
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (41, 128, 185), -1) # Dark Blue background
                    # Draw elegant technical cross-hatch vector line strokes inside the block
                    for offset in range(0, b_size, 5):
                        cv2.line(blueprint, (x + offset, y), (x, y + offset), (231, 76, 60), 1) # Red hatch lines
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (255, 255, 255), 1)
                    comm_count += 1
                    
                # ZONE B: OPEN TERRAIN -> Medium-Density Residential (Horizontal Wireframe Subdivisions)
                else:
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (47, 54, 114), -1) # Dark Indigo base
                    # Draw thin white interior lot subdivision street lines
                    for y_offset in range(4, b_size, 6):
                        cv2.line(blueprint, (x + 2, y + y_offset), (x + b_size - 2, y + y_offset), (255, 255, 255), 1)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (120, 120, 120), 1)
                    res_count += 1

    # 3. SUPERIMPOSE PROFESSIONAL HIGH-CONTRAST TRANSIT NETWORK CORRIDORS
    # Minor local street grid guides
    for y_line in range(0, h, spacing * 3):
        cv2.line(blueprint, (0, y_line), (w, y_line), (87, 101, 116), 1)
    for x_line in range(0, w, spacing * 3):
        cv2.line(blueprint, (x_line, 0), (x_line, h), (87, 101, 116), 1)
        
    # Major primary double-lined highways tracing your actual photo roads
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((9, 9), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (44, 62, 80)    # Deep slate outer road pad
        road_core = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        blueprint[road_core == 255] = (255, 255, 255)   # White center lane markings
        blueprint[edges == 255] = (44, 62, 80)          # Median split divider gap
        
    # =========================================================================
    # 4. INJECT STRUCTURAL MAP TITLE BLOCK, LEGAL LEGEND TABLE & COMPASS
    # =========================================================================
    # Draw technical white outer box margin frame
    cv2.rectangle(blueprint, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
    
    # Generate the standard engineering Title Block box card in the lower right corner
    tb_w, tb_h = 250, 95
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (30, 39, 46), -1)
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (255, 255, 255), 2)
    
    cv2.putText(blueprint, "TUMKUR MASTER REGION", (w - tb_w + 12, h - tb_h + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "REGIONAL DEVELOPMENT PLAN", (w - tb_w + 12, h - tb_h + 44), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "SCALE: 1:25,000", (w - tb_w + 12, h - tb_h + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.34, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "PROJECT CORE: UrbanAI v5.5", (w - tb_w + 12, h - tb_h + 82), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 240, 255), 1, cv2.LINE_AA)
    
    # Generate a professional, clean Legend Table card in the lower left corner
    lg_w, lg_h = 240, 95
    cv2.rectangle(blueprint, (5, h - lg_h), (lg_w, h - 5), (30, 39, 46), -1)
    cv2.rectangle(blueprint, (5, h - lg_h), (lg_w, h - 5), (255, 255, 255), 2)
    
    # Legend Row 1: Commercial (Red/Purple Hatch swatch box)
    cv2.rectangle(blueprint, (15, h - lg_h + 12), (35, h - lg_h + 27), (41, 128, 185), -1)
    cv2.line(blueprint, (15, h - lg_h + 12), (35, h - lg_h + 27), (231, 76, 60), 1)
    cv2.putText(blueprint, "Commercial Core Hubs", (45, h - lg_h + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Legend Row 2: Residential (Horizontal layout swatch box)
    cv2.rectangle(blueprint, (15, h - lg_h + 37), (35, h - lg_h + 52), (47, 54, 114), -1)
    cv2.line(blueprint, (15, h - lg_h + 44), (35, h - lg_h + 44), (255, 255, 255), 1)
