import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# ============================================================
# 1. INITIALIZE STREAMLIT APPLICATION
# ============================================================

st.set_page_config(
    page_title="UrbanAI Studio | GIS Engineering Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. CUSTOM DARK ARCHITECTURAL THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b132b;
        color: #edf2f4;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #101936;
    }

    [data-testid="stSidebar"] * {
        color: #edf2f4;
    }

    div.stButton > button {
        background-color: #3a86ff;
        color: white;
        border-radius: 5px;
        border: none;
        width: 100%;
        font-weight: bold;
        padding: 12px;
        box-shadow: 0px 4px 10px rgba(58, 134, 255, 0.3);
    }

    div.stButton > button:hover {
        background-color: #2563d8;
        color: white;
    }

    .metric-panel {
        background-color: #1c2541;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #3a86ff;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #4cc9f0;
    }

    .metric-label {
        font-size: 11px;
        color: #b0c4de;
        text-transform: uppercase;
        margin-top: 5px;
    }

    .section-title {
        background-color: #1c2541;
        padding: 12px 18px;
        border-left: 4px solid #3a86ff;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
        font-weight: bold;
    }

    .system-status {
        background-color: #111827;
        padding: 12px;
        border-radius: 6px;
        border: 1px solid #263454;
        color: #4cc9f0;
        font-family: monospace;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 3. APPLICATION HEADER
# ============================================================

st.title("🏗️ UrbanAI Studio™ — GIS Master Planning Suite")

st.markdown(
    "`[SYSTEM PROTOCOL: MASTER REGIONAL DEVELOPMENT OVERLAY - EXTRACTING FROM TOPOLOGY]`"
)

st.markdown("---")

# ============================================================
# 4. SIDEBAR CONFIGURATION
# ============================================================

st.sidebar.header("📡 GIS CONFIGURATION")

sector_profile = st.sidebar.selectbox(
    "Active Planning Preset",
    [
        "Suburban Neighborhood Matrix",
        "High-Density Core Matrix",
        "Eco-Fringe Settlement"
    ]
)

preservation_val = st.sidebar.slider(
    "Eco Preservation Threshold",
    min_value=80,
    max_value=140,
    value=110,
    step=5
)

transit_val = st.sidebar.slider(
    "Transit Extraction Sensitivity",
    min_value=20,
    max_value=80,
    value=45,
    step=5
)

# Grid configuration
b_size = 28
b_gap = 10

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎨 GEOSPATIAL MAP LEGEND")

st.sidebar.markdown(
    "🟪 **Deep Purple Line Grids:** High-Density Commercial Core"
)

st.sidebar.markdown(
    "🟦 **Slate Blue Matrix:** Medium-Density Residential Sectors"
)

st.sidebar.markdown(
    "🟩 **Lime & Sage Pasture:** Urban Agriculture & Greenbelts"
)

st.sidebar.markdown(
    "⬜ **Slate Casing / White Split:** Primary Arterial Transit Highways"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    <div class="system-status">
    SYSTEM STATUS: ONLINE<br>
    PROFILE: {sector_profile}<br>
    ECO THRESHOLD: {preservation_val}<br>
    TRANSIT SENSITIVITY: {transit_val}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 5. GEOSPATIAL FILE UPLOAD
# ============================================================

st.subheader("🛰️ Geographic Satellite Image Input")

uploaded_file = st.file_uploader(
    "UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is None:

    st.info(
        "ℹ️ System standby. Please upload geographic satellite terrain "
        "imagery to initiate the planning pipeline."
    )

    st.markdown(
        """
        ### 📋 Processing Pipeline

        **Satellite Image → Image Processing → Road Extraction → "
        Green Area Detection → Zoning Generation → Urban Master Plan**
        """
    )

    st.stop()

# ============================================================
# 6. READ INPUT IMAGE
# ============================================================

try:

    raw_img = Image.open(uploaded_file).convert("RGB")

except Exception as e:

    st.error(f"Unable to read the uploaded image: {e}")
    st.stop()

img_np = np.array(raw_img)

# ============================================================
# 7. IMAGE RESIZING
# ============================================================

orig_h, orig_w, _ = img_np.shape

scale_factor = 650 / max(orig_h, orig_w)

new_h = max(1, int(orig_h * scale_factor))
new_w = max(1, int(orig_w * scale_factor))

img_resized = cv2.resize(
    img_np,
    (new_w, new_h),
    interpolation=cv2.INTER_LANCZOS4
)

h, w, c = img_resized.shape

# ============================================================
# 8. IMAGE PROCESSING
# ============================================================

with st.spinner("⚡ Running spatial matrix optimizations..."):

    # --------------------------------------------------------
    # Convert RGB → Grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        img_resized,
        cv2.COLOR_RGB2GRAY
    )

    # --------------------------------------------------------
    # Gaussian Blur
    # --------------------------------------------------------

    blurred = cv2.GaussianBlur(
        gray,
        (11, 11),
        0
    )

    # --------------------------------------------------------
    # Road / Infrastructure Extraction
    # --------------------------------------------------------

    high_threshold = int(
        min(255, transit_val * 2.5)
    )

    edges = cv2.Canny(
        blurred,
        transit_val,
        high_threshold
    )

    edge_y, edge_x = np.where(
        edges == 255
    )

    # --------------------------------------------------------
    # Green / Preservation Area Extraction
    # --------------------------------------------------------

    _, green_mask = cv2.threshold(
        blurred,
        preservation_val,
        255,
        cv2.THRESH_BINARY_INV
    )

    green_mask = cv2.dilate(
        green_mask,
        np.ones((9, 9), np.uint8),
        iterations=1
    )

    smooth_green = cv2.GaussianBlur(
        green_mask,
        (25, 25),
        0
    )

    # ========================================================
    # 9. CREATE BLUEPRINT CANVAS
    # ========================================================

    blueprint = np.zeros(
        (h, w, 3),
        dtype=np.uint8
    )

    # Asphalt / slate background
    blueprint[:] = (45, 52, 54)

    # ========================================================
    # 10. GREENBELT DETECTION
    # ========================================================

    green_pixels = smooth_green > 100

    blueprint[green_pixels] = (
        156,
        204,
        101
    )

    # ========================================================
    # 11. GENERATIVE ZONING PARAMETERS
    # ========================================================

    spacing = b_size + b_gap

    res_count = 0
    comm_count = 0

    commercial_threshold = (
        55 + (45 - transit_val) * 0.5
    )

    if sector_profile == "High-Density Core Matrix":

        density_mod = 1.35

    elif sector_profile == "Eco-Fringe Settlement":

        density_mod = 0.65

    else:

        density_mod = 1.0

    # ========================================================
    # 12. GENERATIVE URBAN ZONING MATRIX
    # ========================================================

    for y in range(
        40,
        max(40, h - spacing),
        spacing
    ):

        for x in range(
            40,
            max(40, w - spacing),
            spacing
        ):

            # ------------------------------------------------
            # Calculate distance to detected road
            # ------------------------------------------------

            if len(edge_x) > 0:

                distances = np.sqrt(
                    (edge_x - x) ** 2 +
                    (edge_y - y) ** 2
                )

                dist_to_transit = np.min(
                    distances
                )

            else:

                dist_to_transit = 999.0

            # ------------------------------------------------
            # Check whether location is green area
            # ------------------------------------------------

            center_y = min(
                y + b_size // 2,
                h - 1
            )

            center_x = min(
                x + b_size // 2,
                w - 1
            )

            is_green = (
                smooth_green[
                    center_y,
                    center_x
                ] > 100
            )

            # =================================================
            # COMMERCIAL ZONE
            # =================================================

            if not is_green:

                if (
                    dist_to_transit
                    < commercial_threshold
                ):

                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x + b_size, y + b_size),
                        (94, 53, 177),
                        -1
                    )

                    # Commercial hatch pattern
                    for offset in range(
                        0,
                        b_size,
                        6
                    ):

                        cv2.line(
                            blueprint,
                            (x + offset, y),
                            (x, y + offset),
                            (255, 255, 255),
                            1
                        )

                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x + b_size, y + b_size),
                        (255, 255, 255),
                        1
                    )

                    comm_count += 1

                # =============================================
                # RESIDENTIAL ZONE
                # =============================================

                else:

                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x + b_size, y + b_size),
                        (58, 125, 160),
                        -1
                    )

                    half = b_size // 2

                    # Four housing plots
                    cv2.rectangle(
                        blueprint,
                        (x + 2, y + 2),
                        (x + half - 1, y + half - 1),
                        (255, 255, 255),
                        1
                    )

                    cv2.rectangle(
                        blueprint,
                        (x + half + 1, y + 2),
                        (x + b_size - 2, y + half - 1),
                        (255, 255, 255),
                        1
                    )

                    cv2.rectangle(
                        blueprint,
                        (x + 2, y + half + 1),
                        (x + half - 1, y + b_size - 2),
                        (255, 255, 255),
                        1
                    )

                    cv2.rectangle(
                        blueprint,
                        (x + half + 1, y + half + 1),
                        (x + b_size - 2, y + b_size - 2),
                        (255, 255, 255),
                        1
                    )

                    res_count += 1

    # ========================================================
    # 13. TRANSIT GRID
    # ========================================================

    for y_line in range(
        0,
        h,
        spacing * 3
    ):

        cv2.line(
            blueprint,
            (0, y_line),
            (w, y_line),
            (236, 240, 241),
            1
        )

    for x_line in range(
        0,
        w,
        spacing * 3
    ):

        cv2.line(
            blueprint,
            (x_line, 0),
            (x_line, h),
            (236, 240, 241),
            1
        )

    # ========================================================
    # 14. ROAD NETWORK OVERLAY
    # ========================================================

    if len(edge_x) > 0:

        road_casing = cv2.dilate(
            edges,
            np.ones((9, 9), np.uint8),
            iterations=1
        )

        blueprint[
            road_casing == 255
        ] = (44, 62, 80)

        road_core = cv2.dilate(
            edges,
            np.ones((3, 3), np.uint8),
            iterations=1
        )

        blueprint[
            road_core == 255
        ] = (255, 255, 255)

        blueprint[
            edges == 255
        ] = (44, 62, 80)

    # ========================================================
    # 15. OUTER FRAME
    # ========================================================

    cv2.rectangle(
        blueprint,
        (5, 5),
        (w - 5, h - 5),
        (255, 255, 255),
        2
    )

    # ========================================================
    # 16. TRANSPARENT TITLE BLOCK + LEGEND
    # ========================================================

    overlay = blueprint.copy()

    # Title block
    tb_w = min(260, w - 10)
    tb_h = min(95, h - 10)

    cv2.rectangle(
        overlay,
        (w - tb_w, h - tb_h),
        (w - 5, h - 5),
        (20, 25, 30),
        -1
    )

    # Legend
    lg_w = min(240, w - 10)
    lg_h = min(95, h - 10)

    cv2.rectangle(
        overlay,
        (5, h - lg_h),
        (lg_w, h - 5),
        (20, 25, 30),
        -1
    )

    # Alpha blend
    alpha = 0.55

    blueprint = cv2.addWeighted(
        overlay,
        alpha,
        blueprint,
        1 - alpha,
        0
    )

    # ========================================================
    # 17. TITLE BLOCK FRAME
    # ========================================================

    cv2.rectangle(
        blueprint,
        (w - tb_w, h - tb_h),
        (w - 5, h - 5),
        (255, 255, 255),
        2
    )

    cv2.rectangle(
        blueprint,
        (5, h - lg_h),
        (lg_w, h - 5),
        (255, 255, 255),
        2
    )

    # ========================================================
    # 18. TITLE BLOCK TEXT
    # ========================================================

    cv2.putText(
        blueprint,
        "URBANAI REGIONAL PLAN",
        (w - tb_w + 12, h - tb_h + 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.40,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "AUTONOMOUS GIS BLUEPRINT PLAN",
        (w - tb_w + 12, h - tb_h + 44),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "SCALE: 1:25,000",
        (w - tb_w + 12, h - tb_h + 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.34,
        (180, 180, 180),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "PROJECT CORE: UrbanAI V5.5",
        (w - tb_w + 12, h - tb_h + 82),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.32,
        (0, 240, 255),
        1,
        cv2.LINE_AA
    )

    # ========================================================
    # 19. LEGEND
    # ========================================================

    # Commercial
    cv2.rectangle(
        blueprint,
        (15, h - lg_h + 12),
        (35, h - lg_h + 27),
        (94, 53, 177),
        -1
    )

    cv2.putText(
        blueprint,
        "Commercial Core Hubs",
        (45, h - lg_h + 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # Residential
    cv2.rectangle(
        blueprint,
        (15, h - lg_h + 37),
        (35, h - lg_h + 52),
        (58, 125, 160),
        -1
    )

    cv2.putText(
        blueprint,
        "Residential Sectors",
        (45, h - lg_h + 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # Greenbelt
    cv2.rectangle(
        blueprint,
        (15, h - lg_h + 62),
        (35, h - lg_h + 77),
        (156, 204, 101),
        -1
    )

    cv2.putText(
        blueprint,
        "Eco Preservation Belts",
        (45, h - lg_h + 73),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # ========================================================
    # 20. NORTH COMPASS
    # ========================================================

    cv2.circle(
        blueprint,
        (35, 35),
        15,
        (255, 255, 255),
        1
    )

    cv2.line(
        blueprint,
        (35, 42),
        (35, 20),
        (255, 255, 255),
        2
    )

    cv2.line(
        blueprint,
        (35, 20),
        (31, 25),
        (255, 255, 255),
        2
    )

    cv2.line(
        blueprint,
        (35, 20),
        (39, 25),
        (255, 255, 255),
        2
    )

    cv2.putText(
        blueprint,
        "N",
        (31, 14),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # ========================================================
    # 21. DYNAMIC MAP LABELS
    # ========================================================

    if comm_count > 0:

        cv2.putText(
            blueprint,
            "HIGH-DENSITY COMMERCIAL CORRIDOR",
            (120, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    if res_count > 0:

        label_y = max(
            100,
            h - 130
        )

        cv2.putText(
            blueprint,
            "PROPOSED RESIDENTIAL URBAN MATRIX",
            (60, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    if np.sum(
        smooth_green > 100
    ) > 0:

        label_y = min(
            h - 20,
            h // 2 + 60
        )

        cv2.putText(
            blueprint,
            "URBAN AGRICULTURE AND GREEN BELT",
            (60, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.36,
            (44, 62, 80),
            1,
            cv2.LINE_AA
        )

# ============================================================
# 22. CALCULATE MASTER PLAN METRICS
# ============================================================

green_ratio = int(
    (
        np.sum(smooth_green > 100)
        /
        (h * w)
    ) * 100
)

infrastructure_km = (
    int(np.sum(edges == 255) / 100)
    if len(edge_x) > 0
    else 0
)

planned_dwellings = int(
    res_count * 4 * density_mod
)

commercial_hubs = int(
    comm_count * density_mod
)

# ============================================================
# 23. METRICS DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 REAL-TIME LIVE DATA ANALYSIS COMMAND CENTER'
    '</div>',
    unsafe_allow_html=True
)

m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:

    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-value">
                {planned_dwellings:,}
            </div>
            <div class="metric-label">
                🏡 Planned Dwellings
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m_col2:

    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-value">
                {commercial_hubs:,}
            </div>
            <div class="metric-label">
                🏢 Commercial Hubs
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m_col3:

    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-value">
                {green_ratio}%
            </div>
            <div class="metric-label">
                🌿 Greenbelt Coverage
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m_col4:

    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-value">
                {infrastructure_km} km
            </div>
            <div class="metric-label">
                🛣️ Primary Highway Route
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 24. IMAGE PRESENTATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🗺️ SIDE-BY-SIDE PRESENTATION VIEW'
    '</div>',
    unsafe_allow_html=True
)

ui_col1, ui_col2 = st.columns(2)

with ui_col1:

    st.subheader("🛰️ Input Satellite Imagery Capture")

    st.image(
        img_resized,
        use_container_width=True
    )

with ui_col2:

    st.subheader(
        "🗺️ Synthesized Regional Development Layout"
    )

    st.image(
        blueprint,
        use_container_width=True
    )

# ============================================================
# 25. ANALYSIS INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🧠 URBANAI GENERATIVE ANALYSIS'
    '</div>',
    unsafe_allow_html=True
)

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:

    st.markdown(
        f"""
        **Planning Profile:**  
        {sector_profile}

        **Residential Grid Blocks:**  
        {res_count:,}

        **Commercial Grid Blocks:**  
        {comm_count:,}

        **Greenbelt Coverage:**  
        {green_ratio}%
        """
    )

with analysis_col2:

    st.markdown(
        f"""
        **Transit Sensitivity:**  
        {transit_val}

        **Eco Preservation Threshold:**  
        {preservation_val}

        **Detected Road Pixels:**  
        {int(np.sum(edges == 255)):,}

        **Image Resolution:**  
        {orig_w} × {orig_h}
        """
    )

# ============================================================
# 26. EXPORT IMAGE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📥 FILE EXPORTER MANAGER'
    '</div>',
    unsafe_allow_html=True
)

final_output_image = Image.fromarray(
    cv2.cvtColor(
        blueprint,
        cv2.COLOR_BGR2RGB
    )
)

# NOTE:
# blueprint is already stored as an OpenCV-style array.
# Convert it correctly to RGB for PIL/export.

export_path = "gis_regional_masterplan.jpg"

final_output_image.save(
    export_path,
    format="JPEG",
    quality=95
)

with open(
    export_path,
    "rb"
) as file:

    st.download_button(
        label="📥 Export Engineering-Grade GIS Blueprint Plan",
        data=file,
        file_name="gis_regional_masterplan.jpg",
        mime="image/jpeg"
    )

# ============================================================
# 27. SYSTEM FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7f8caa;
        font-size:12px;
        padding:15px;
    ">
        UrbanAI Studio™ | Generative AI Urban Planning Prototype |
        GIS Engineering Suite | OpenCV Spatial Processing
    </div>
    """,
    unsafe_allow_html=True
)
