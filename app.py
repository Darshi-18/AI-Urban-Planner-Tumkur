import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# Set professional layout configurations
st.set_page_config(page_title="AI Urban Planner", layout="wide", initial_sidebar_state="expanded")

# =========================================================================
# UI HEADER & BRANDING
# =========================================================================
st.title("🏗️ Generative AI Greenfield Urban City Planner")
st.markdown("""
This interactive interface acts as an automated tool for rapid master planning in expanding smart cities like **Tumakuru, Karnataka**. 
Upload any raw satellite terrain snapshot to generate a structured 2D architectural zoning layout instantly.
""")

# =========================================================================
# SIDEBAR CONFIGURATIONS (User Interaction Panel)
# =========================================================================
st.sidebar.header("🎨 Planning Parameters")
st.sidebar.markdown("Fine-tune the AI zoning thresholds below:")

# Interactive sliders for the user
sector_size = st.sidebar.slider("Residential Block Grid Size", min_value=40, max_value=120, value=70, step=10)
green_threshold = st.sidebar.slider("Eco-Park Sensitivity", min_value=80, max_value=140, value=105, step=5)
road_sensitivity = st.sidebar.slider("Highway Extraction Sensitivity", min_value=20, max_value=80, value=40, step=5)

st.sidebar.markdown("---")
st.sidebar.markdown("**Zoning Legend:**")
st.sidebar.markdown("🟠 **Orange:** Residential Footprints")
st.sidebar.markdown("🔵 **Blue:** Commercial Core Complexes")
st.sidebar.markdown("🟢 **Green:** Eco-Park Buffer Zones")
st.sidebar.markdown("⚫ **Grey/White:** Primary Highway Artery")

# =========================================================================
# FILE CONTROLLER UPLOAD HANDLER
# =========================================================================
uploaded_file = st.file_uploader("Choose a square satellite land image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read the uploaded file into a usable image format
    raw_img = Image.open(uploaded_file).convert("RGB")
    raw_img = raw_img.resize((600, 600), Image.Resampling.LANCZOS)
    img_np = np.array(raw_img)
    h, w, c = img_np.shape
    
    # Create the side-by-side display columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input: Raw Satellite Terrain")
        st.image(img_np, use_container_width=True)
        
    # =========================================================================
    # CORE PROCESSING ENGINE (Our Realistic Architecture Renderer)
    # =========================================================================
    with st.spinner("🧠 AI Engine is analyzing topography maps..."):
        # Initialize Canvas
        blueprint = np.zeros((h, w, 3), dtype=np.uint8)
        blueprint[:] = (235, 237, 240) # Linen grey blueprint base
        
        # Computer Vision Structural Pipeline
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(blurred, road_sensitivity, road_sensitivity * 3)
        
        # 1. Eco-Green recreational zones
        _, green_mask = cv2.threshold(blurred, green_threshold, 255, cv2.THRESH_BINARY_INV)
        green_mask = cv2.dilate(green_mask, np.ones((21, 21), np.uint8), iterations=1)
        green_mask = cv2.GaussianBlur(green_mask, (15, 15), 0)
        blueprint[green_mask > 127] = (200, 230, 201)
        
        # 2. Commercial Hub strip
        comm_start_x = int(w * 0.70)
        cv2.rectangle(blueprint, (comm_start_x, 0), (w, h), (207, 226, 243), -1)
        for y in range(30, h, 80):
            cv2.rectangle(blueprint, (comm_start_x + 30, y), (w - 30, y + 45), (41, 128, 185), -1)

        # 3. Residential Neighborhood Footprints
        for y in range(10, h, sector_size):
            for x in range(10, comm_start_x - 20, sector_size):
                if (x // sector_size) % 2 == 0 or (y // sector_size) % 2 == 0:
                    cv2.rectangle(blueprint, (x, y), (x + sector_size - 15, y + sector_size - 15), (254, 237, 222), -1)
                    
                    # Nest houses inside the community boxes
                    for row_y in range(y + 8, y + sector_size - 25, 24):
                        for col_x in range(x + 8, x + sector_size - 25, 24):
                            if row_y < h and col_x < w and green_mask[row_y, col_x] <= 127:
                                cv2.rectangle(blueprint, (col_x, row_y), (col_x + 14, row_y + 14), (211, 84, 0), -1)

        # 4. Transportation Network Grid Infrastructure
        for y in range(0, h, sector_size):
            cv2.line(blueprint, (0, y), (comm_start_x, y), (255, 255, 255), 3)
        for x in range(0, comm_start_x, sector_size):
            cv2.line(blueprint, (x, 0), (x, h), (255, 255, 255), 3)
            
        road_dilation = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
        blueprint[road_dilation == 255] = (100, 110, 120) 
        blueprint[edges == 255] = (255, 255, 255)         

    with col2:
        st.subheader("Output: AI Master Plan Render")
        st.image(blueprint, use_container_width=True)
        
    # Download Button to let users export their generated blueprint maps
    # Convert back to standard image bytes to save
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
