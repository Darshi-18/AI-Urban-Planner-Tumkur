import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE WEB DASHBOARD LAYER
st.set_page_config(
    page_title="UrbanAI Nexus | Smart City Generative Engine", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INJECT CUSTOM CYBERPUNK CSS ARCHITECTURE
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stSlider > div > div > div > div { background-color: #58a6ff; }
    div.stButton > button:first-child {
        background-color: #238636; color: white; border-radius: 6px;
        border: 1px solid rgba(240,240,240,0.2); width: 100%; font-weight: bold;
    }
    .metric-box {
        background-color: #161b22; padding: 15px; border-radius: 8px;
        border: 1px solid #30363d; text-align: center;
    }
    .metric-val { font-size: 24px; font-weight: bold; color: #58a6ff; }
    .metric-lbl { font-size: 12px; color: #8b949e; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# =========================================================================
# APPLICATION CORE BRANDING
# =========================================================================
st.title("⚡ UrbanAI Nexus™ — Generative Smart City Engine")
st.markdown("---")

# =========================================================================
# INTERACTIVE CONTROL PANEL (SIDEBAR)
# =========================================================================
st.sidebar.header("🎛️ GENERATIVE CONFIGURATIONS")
st.sidebar.markdown("Modify structural topology constraints:")

# High-fidelity parameter controls
density_preset = st.sidebar.selectbox("Urban Density Blueprint", ["High-Density Core", "Suburban Modular Grid", "Low-Density Eco-Fringe"])
green_factor = st.sidebar.slider("Environmental Preservation Index", 80, 140, 110, 5)
road_hierarchy = st.sidebar.slider("Transit Arterial Extraction Threshold", 20, 80, 45, 5)

# Mapping grid internal adjustments based on preset values
if density_preset == "High-Density Core":
    b_size, b_gap = 14, 4
elif density_preset == "Suburban Modular Grid":
    b_size, b_gap = 20, 8
else:
    b_size, b_gap = 28, 14

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 LAYOUT MATRIX LEGEND:**")
st.sidebar.markdown("🟠 **Terracotta Red:** Residential House Footprints")
st.sidebar.markdown("🔵 **Deep Cobalt:** High-Density Commercial Hubs")
st.sidebar.markdown("🟢 **Emerald Pasture:** Preserved Eco-Buffer Zones")
st.sidebar.markdown("⚪ **Asphalt / Platinum:** Primary Transit Grids")

# =========================================================================
# SATELLITE IMAGE FILE CONTROLLER
# =========================================================================
uploaded_file = st.file_uploader("Upload target geographic aerial imagery (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    raw_img = Image.open(uploaded_file).convert("RGB")
    raw_img = raw_img.resize((700, 700), Image.Resampling.LANCZOS)
    img_np = np.array(raw_img)
    h, w, c = img_np.shape
    
    # Run Computer Vision Data Decomposition
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, road_hierarchy, road_hierarchy * 3)
    edge_y, edge_x = np.where(edges == 255)
    
    # Calculate natural vegetation topology mask
    _, green_mask = cv2.threshold(blurred, green_factor, 255, cv2.THRESH_BINARY_INV)
    green_mask = cv2.dilate(green_mask, np.ones((11, 11), np.uint8), iterations=1)
    
    # =========================================================================
    # HIGH-REALISM BLUEPRINT RENDER ENGINE
    # =========================================================================
    with st.spinner("⚡ Running layout matrix computations..."):
        # Create professional blueprints blueprint linen canvas
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (240, 242, 245) 
        
        # 1. Render Eco-Park Boundaries smoothly
        smooth_green = cv2.GaussianBlur(green_mask, (25, 25), 0)
        blueprint[smooth_green > 100] = (208, 240, 212) # Soft architectural sage green
        
        # 2. Generative Block Layout Iteration Loops
        spacing = b_size + b_gap
        res_count, comm_count = 0, 0
        
        for y in range(20, h - spacing, spacing):
            for x in range(20, w - spacing, spacing):
                
                # Check proximity to actual infrastructure lines extracted from this image
                if len(edge_x) > 0:
                    dist_to_road = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    dist_to_road = 999.0
                    
                # A. HIGHWAY ACCESS CORRIDORS: Plot high-density commercial complexes
                if dist_to_road < 50:
                    if x % 3 == 0 and y % 2 == 0:
                        # Draw complex L-shaped commercial footprints instead of flat squares
                        cv2.rectangle(blueprint, (x, y), (x + b_size + 4, y + b_size - 2), (41, 128, 185), -1)
                        cv2.rectangle(blueprint, (x, y + b_size - 2), (x + b_size // 2, y + b_size + 4), (41, 128, 185), -1)
                        comm_count += 1
                        
                # B. SETTLEMENT VALLEYS: Plot rows of residential houses with driveways
                elif smooth_green[y + b_size // 2, x + b_size // 2] <= 100:
                    # Draw a crisp residential land parcel plot border
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (243, 244, 246), -1)
                    cv2.rectangle(blueprint, (x, y), (x + b_size, y + b_size), (209, 213, 219), 1)
                    
                    # Draw individual house footprint structure inside the parcel boundary
                    h_w, h_h = int(b_size * 0.6), int(b_size * 0.6)
                    cv2.rectangle(blueprint, (x + 2, y + 2), (x + h_w, y + h_h), (211, 84, 0), -1) # Terracotta footprint
                    
                    # Add tiny detail: Private access driveway lines
                    cv2.line(blueprint, (x + h_w, y + 4), (x + b_size, y + 4), (180, 180, 180), 1)
                    res_count += 1

        # 3. OVERLAY TRANSPORTATION NETWORKS
        # Draw clean white local collector street lines separating structural zones
        for y in range(0, h, spacing * 2):
            cv2.line(blueprint, (0, y), (w, y), (255, 255, 255), 2)
        for x in range(0, w, spacing * 2):
            cv2.line(blueprint, (x, 0), (x, h), (255, 255, 255), 2)
            
        # Overlay the primary asphalt highway line extracted from the image
        road_bed = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=1)
        blueprint[road_bed == 255] = (74, 85, 104)   # Slate-grey infrastructure layer
        blueprint[edges == 255] = (255, 255, 255)     # Crispy white center road dividers
        
    # =========================================================================
    # REAL-TIME LIVE STATISTICAL ANALYTICS METRICS DISPLAY
    # =========================================================================
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    # Calculate green space coverage percentage
    green_pct = int((np.sum(smooth_green > 100) / (h * w)) * 100)
    # Calculate road length index approximation
    road_idx = int(np.sum(edges == 255) / 100)
    
    with col_m1:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{res_count:,}</div><div class='metric-lbl'>🏡 Residential Units</div></div>", unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{comm_count}</div><div class='metric-lbl'>🏢 Commercial Blocks</div></div>", unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{green_pct}%</div><div class='metric-lbl'>🌳 Eco-Preservation Ratio</div></div>", unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"<div class='metric-box'><div class='metric-val'>{road_idx} km</div><div class='metric-lbl'>🛣️ Total Planned Roads</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # =========================================================================
    # RENDER SIDE-BY-SIDE PLATFORM COLUMNS
    # =========================================================================
    layout_col1, layout_col2 = st.columns(2)
    
    with layout_col1:
        st.subheader("🛰️ Input Terrain Capture")
        st.image(img_np, use_container_width=True)
        
    with layout_col2:
        st.subheader("🗺️ Synthesized Generative Blueprint Layout")
        st.image(blueprint, use_container_width=True)
        
    # RENDER DATA EXPORT CONTROLLER
    result_img = Image.fromarray(blueprint)
    result_img.save("temp_blueprint.png")
    with open("temp_blueprint.png", "rb") as file:
        st.download_button(
            label="📥 Export High-Resolution Structural Layout Blueprint",
            data=file,
            file_name="urban_nexus_masterplan.png",
            mime="image/png"
        )
else:
    st.info("ℹ️ System standing by. Upload high-resolution aerial terrain imagery to initiate the planning pipeline.")
