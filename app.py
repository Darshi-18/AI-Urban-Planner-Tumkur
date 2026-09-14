import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# 1. SET HIERARCHICAL PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Adaptive Urban Planner", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Disable potential Windows multithreading collisions safely
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# =========================================================================
# UI HEADER & APPLICATION BRANDING
# =========================================================================
st.title("🏗️ Generative AI Greenfield Urban City Planner")
st.markdown("""
This interactive system provides an automated framework for rapid master planning in expanding smart cities like **Tumakuru, Karnataka**. 
Upload any raw satellite terrain snapshot to watch the generative logic dynamically trace topography and render custom-tailored architectural blueprints.
""")

# =========================================================================
# SIDEBAR DYNAMIC PARAMETERS CONFIGURATION
# =========================================================================
st.sidebar.header("🎨 Planning Parameters")
st.sidebar.markdown("Fine-tune layout allocation metrics live:")

# Interactive hyperparameter controls
sector_size = st.sidebar.slider("Residential Block Grid Size", min_value=40, max_value=120, value=60, step=10)
green_threshold = st.sidebar.slider("Eco-Park Sensitivity", min_value=80, max_value=140, value=105, step=5)
road_sensitivity = st.sidebar.slider("Highway Extraction Sensitivity", min_value=20, max_value=80, value=40, step=5)

st.sidebar.markdown("---")
st.sidebar.markdown("**Master Zoning Legend:**")
st.sidebar.markdown("🟠 **Orange:** Residential Footprints")
st.sidebar.markdown("🔵 **Blue:** Commercial Core Complexes")
st.sidebar.markdown("🟢 **Green:** Eco-Park Buffer Zones")
st.sidebar.markdown("⚫ **Grey/White:** Primary Highway Artery")

# =========================================================================
# CORE UPLOAD HANDLER INTERFACE
# =========================================================================
uploaded_file = st.file_uploader("Choose an un-developed square satellite terrain image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Safely convert data bytes into a standardized matrix canvas
    raw_img = Image.open(uploaded_file).convert("RGB")
    raw_img = raw_img.resize((600, 600), Image.Resampling.LANCZOS)
    img_np = np.array(raw_img)
    h, w, c = img_np.shape
    
    # Establish layout matrix grids columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input: Raw Satellite Terrain")
        st.image(img_np, use_container_width=True)
        
    # =========================================================================
    # DYNAMIC TOPOGRAPHY-AWARE URBAN ENGINE
    # =========================================================================
    with st.spinner("🧠 Analyzing topological features and road corridors..."):
        # Create a clean architectural linen-grey base layout blueprint
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (235, 237, 240) 
        
        # Computer Vision Image Signal Decomposition Pipeline
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Dynamically extract high-contrast transportation highway skeletons
        edges = cv2.Canny(blurred, road_sensitivity, road_sensitivity * 3)
        edge_y, edge_x = np.where(edges == 255)
        
        # LAYER 1: ECO-GREEN BUFFER ZONES (Extracts vegetation shapes natively)
        _, green_mask = cv2.threshold(blurred, green_threshold, 255, cv2.THRESH_BINARY_INV)
        green_mask = cv2.dilate(green_mask, np.ones((15, 15), np.uint8), iterations=1)
        green_mask = cv2.GaussianBlur(green_mask, (15, 15), 0)
        blueprint[green_mask > 127] = (200, 230, 201) # Soft eco-green fill
        
        # LAYERS 2 & 3: ADAPTIVE COMMERCIAL HUBS & RESIDENTIAL NEIGHBORHOODS
        grid_size = sector_size
        
        for y in range(10, h - grid_size, grid_size):
            for x in range(10, w - grid_size, grid_size):
                
                # Check proximity to actual infrastructure lines extracted from this image
                if len(edge_x) > 0:
                    distance_to_road = np.min(np.sqrt((edge_x - x)**2 + (edge_y - y)**2))
                else:
                    distance_to_road = 999.0 # Fallback if no lines are found

                # DYNAMIC ZONING CONDITION CONTROLLERS
                if distance_to_road < 45:
                    # Allocate Commercial Core Centers (Blue) adjacent to transport pathways
                    cv2.rectangle(blueprint, (x+4, y+4), (x+grid_size-4, y+grid_size-4), (254, 254, 254), -1) # Plot frame
                    cv2.rectangle(blueprint, (x+6, y+6), (x+grid_size-6, y+grid_size-6), (207, 226, 243), -1) # Soft blue base
                    cv2.rectangle(blueprint, (x+14, y+16), (x+grid_size-14, y+grid_size-16), (41, 128, 185), -1) # Commercial complex
                    
                elif green_mask[y + grid_size//2, x + grid_size//2] <= 127:
                    # Allocate Grid Housing Communities (Orange) inside secure flat fields
                    cv2.rectangle(blueprint, (x+4, y+4), (x+grid_size-4, y+grid_size-4), (254, 237, 222), -1)
                    
                    # Draw sub-grid individual building footprints
                    for sub_y in range(y + 8, y + grid_size - 12, 22):
                        for sub_x in range(x + 8, x + grid_size - 12, 22):
                            if sub_y < h and sub_x < w and green_mask[sub_y, sub_x] <= 127:
                                cv2.rectangle(blueprint, (sub_x, sub_y), (sub_x + 12, sub_y + 12), (211, 84, 0), -1)

        # LAYER 4: TRANSPORTATION OVERLAYS (Traces the unique geometry of the target file)
        road_dilation = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_dilation == 255] = (100, 110, 120) # Asphalt primary beds
        blueprint[edges == 255] = (255, 255, 255)         # White center medians

    with col2:
        st.subheader("Output: AI Master Plan Render")
        st.image(blueprint, use_container_width=True)
        
    # =========================================================================
    # COMPILATION EXPORT UTILITY
    # =========================================================================
    result_img = Image.fromarray(blueprint)
    result_img.save("temp_blueprint.png")
    with open("temp_blueprint.png", "rb") as file:
        st.download_button(
            label="📥 Download Master Plan Blueprint",
            data=file,
            file_name="ai_urban_blueprint.png",
            mime="image/png"
        )
else:
    st.info("ℹ️ Awaiting satellite land footprint upload. Drop your map image into the handler window above.")
