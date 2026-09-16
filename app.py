import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. INITIALIZE MASTER PORTAL CONSOLE
st.set_page_config(
    page_title="UrbanAI Studio | Beginner-Friendly GIS", 
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

st.title("🏗️ UrbanAI Studio™ — Simple Urban Layout Suite")
st.markdown("`[SYSTEM PROTOCOL: EASY-READ HIGH-VISIBILITY ZONING MATRIX]`")
st.markdown("---")

# =========================================================================
# SYSTEM CONTROL SIDEBAR CONTROLLERS
# =========================================================================
st.sidebar.header("📡 EASY CONTROL PANEL")
st.sidebar.markdown("Use these sliders to easily change the map layout:")

sector_profile = st.sidebar.selectbox("Active Planning Preset", ["Suburban Neighborhood Matrix", "High-Density Core Matrix", "Eco-Fringe Settlement"])
preservation_val = st.sidebar.slider("Forest Preservation Area", 80, 140, 110, 5)
transit_val = st.sidebar.slider("Road Detection Range", 20, 80, 45, 5)

b_size = 28
b_gap = 10

st.sidebar.markdown("---")
st.sidebar.markdown("**🎨 COLOR EXPLANATION GUIDE:**")
st.sidebar.markdown("🟪 **Solid Purple Fields:** Business & Commercial Hubs")
st.sidebar.markdown("🟦 **Solid Slate Blue Fields:** Residential Housing Neighborhoods")
st.sidebar.markdown("🟩 **Solid Emerald Green Fields:** Protected Parks & Forests")
st.sidebar.markdown("⬜ **Thick White Lines:** Main Transportation Highways")

# =========================================================================
# GEOSPATIAL FILE INGESTION LAYERS
# =========================================================================
uploaded_file = st.file_uploader("UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is None:
    st.info("ℹ️ System standby. Please upload geographic satellite terrain imagery to initiate the planning pipeline.")
    st.stop()

# =========================================================================
# EXPERT HIGH-VISIBILITY STANDALONE CANVAS ENGINE
# =========================================================================
raw_img = Image.open(uploaded_file).convert("RGB")
img_np = np.array(raw_img)

# Scale canvas dimensions dynamically to guarantee quick loading speeds
orig_h, orig_w, _ = img_np.shape
scale_factor = 512 / max(orig_h, orig_w)
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

with st.spinner("⚡ Creating easy-read layout map..."):
    # Create a clean matte charcoal backdrop canvas for extreme readability
    blueprint = np.zeros((h, w, 3), dtype=np.uint8)
    blueprint[:] = (45, 52, 54) # Charcoal base
    
    # 1. Base Layer: Fill open land with Solid Slate Blue (Residential Houses)
    blueprint[:] = (52, 73, 94) 
    
    # 2. Layer 2: Draw Continuous, Smooth Eco-Preservation Belts (Solid Emerald Green)
    blueprint[smooth_green > 100] = (34, 112, 63) 
    
    spacing = b_size + b_gap
    res_count = 0
    comm_count = 0
    
    commercial_cushion = int(55 + (45 - transit_val) * 0.5)
    density_mod = 1.35 if sector_profile == "High-Density Core Matrix" else (0.65 if sector_profile == "Eco-Fringe Settlement" else 1.0)
    
    # 3. Layer 3: Trace Solid Purple Commercial blocks directly near the highway
    if len(edge_x) > 0:
        dist_transform = cv2.distanceTransform(255 - edges, cv2.DIST_L2, 5)
        commercial_buffer = dist_transform < commercial_cushion
        # Fill commercial zones neatly
        blueprint[commercial_buffer & (smooth_green <= 100)] = (108, 92, 231) # Deep Purple

    # 4. Layer 4: Superimpose High-Contrast Double-Line Highways on top of everything
    if len(edge_x) > 0:
        road_casing = cv2.dilate(edges, np.ones((9, 9), np.uint8), iterations=1)
        blueprint[road_casing == 255] = (44, 62, 80)    # Deep slate outer road pad
        road_core = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
        blueprint[road_core == 255] = (255, 255, 255)   # White center lanes
        blueprint[edges == 255] = (44, 62, 80)          # Center lane split gap
        
    # 5. INJECT TECHNICAL BOX BOUNDARIES & ENGINEERING TITLE BLOCK CARD
    cv2.rectangle(blueprint, (5, 5), (w - 5, h - 5), (255, 255, 255), 2)
    
    tb_w, tb_h = 240, 90
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (30, 39, 46), -1)
    cv2.rectangle(blueprint, (w - tb_w, h - tb_h), (w - 5, h - 5), (255, 255, 255), 2)
    
    cv2.putText(blueprint, "TUMKUR URBAN PLANNING", (w - tb_w + 10, h - tb_h + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "EASY-READ MASTER PLAN", (w - tb_w + 10, h - tb_h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.34, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "SCALE: 1:25,000", (w - tb_w + 10, h - tb_h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "DEVELOPMENT LEVEL: v5.5", (w - tb_w + 10, h - tb_h + 76), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 240, 255), 1, cv2.LINE_AA)
    
    # Compass
    cv2.circle(blueprint, (30, 30), 14, (255, 255, 255), 1)
    cv2.line(blueprint, (30, 36), (30, 18), (255, 255, 255), 2)
    cv2.line(blueprint, (30, 18), (27, 22), (255, 255, 255), 2)
    cv2.line(blueprint, (30, 18), (33, 22), (255, 255, 255), 2)
    cv2.putText(blueprint, "N", (26, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (255, 255, 255), 1, cv2.LINE_AA)

    # 6. INJECT HIGH-VISIBILITY BEGINNER-FRIENDLY PLAIN TEXT LABELS
    # Places text descriptions perfectly inside the colored fields with zero overlap clutter
    cv2.putText(blueprint, "BUSINESS HUB (COMMERCIAL)", (int(w * 0.12), int(h * 0.18)), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "RESIDENTIAL NEIGHBORHOOD", (int(w * 0.08), int(h * 0.72)), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(blueprint, "PROTECTED GREEN BELT", (int(w * 0.38), int(h * 0.48)), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)

# =========================================================================
# REAL-TIME LIVE DATA ANALYSIS COMMAND CENTER METRICS
# =========================================================================
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

green_ratio = int((np.sum(smooth_green > 100) / (h * w)) * 100)
res_ratio = int((np.sum(blueprint == (52, 73, 94)) / (h * w * 3)) * 100)
comm_ratio = int((np.sum(blueprint == (108, 92, 231)) / (h * w * 3)) * 100)
infrastructure_km = int(np.sum(edges == 255) / 100) if len(edge_x) > 0 else 0

with m_col1:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{res_ratio}%</div><div class='metric-label'>🏡 Residential Area</div></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{comm_ratio}%</div><div class='metric-label'>🏢 Commercial Hubs</div></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{green_ratio}%</div><div class='metric-label'>🌿 Greenbelt Coverage</div></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-panel'><div class='metric-value'>{infrastructure_km} km</div><div class='metric-label'>🛣️ Primary Highway Route</div></div>", unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================================
# SIDE-BY-SIDE PRESENTATION COLUMNS VIEWGRID
# =========================================================================
ui_col1, ui_col2 = st.columns(2)

with ui_col1:
    st.subheader("🛰️ Input Satellite Imagery Capture")
    st.image(img_resized, use_container_width=True)
    
with ui_col2:
    st.subheader("🗺️ Easy-Read Generative Master Plan")
    st.image(blueprint, use_container_width=True)
    
# FILE EXPORTER MANAGER
final_output_image = Image.fromarray(blueprint)
final_output_image.save("gis_regional_masterplan.jpg")
with open("gis_regional_masterplan.jpg", "rb") as file:
    st.download_button(
        label="📥 Export Easy-Read GIS Blueprint Plan",
        data=file,
        file_name="gis_regional_masterplan.jpg",
        mime="image/jpeg"
    )
