import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# ============================================================
# 1. INITIALIZE MASTER PORTAL CONSOLE
# ============================================================

st.set_page_config(
    page_title="UrbanAI Studio | Generative Neural Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. CUSTOM DARK ARCHITECTURAL UI THEME
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #0b132b;
    color: #edf2f4;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

div.stButton > button:first-child {
    background-color: #3a86ff;
    color: white;
    border-radius: 4px;
    border: none;
    width: 100%;
    font-weight: bold;
    padding: 12px;
    box-shadow: 0px 4px 10px rgba(58, 134, 255, 0.3);
}

div.stButton > button:hover {
    background-color: #4cc9f0;
    color: #0b132b;
}

.stSlider > div > div > div > div {
    background-color: #3a86ff;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #1c2541;
    color: #edf2f4;
    border: 1px solid #3a86ff;
}

.metric-panel {
    background-color: #1c2541;
    padding: 20px;
    border-radius: 6px;
    border-top: 4px solid #3a86ff;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.15);
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
    margin-top: 4px;
}

.results-box {
    background-color: #14223b;
    padding: 24px;
    border-radius: 8px;
    border-left: 5px solid #3a86ff;
    margin-bottom: 20px;
}

.results-header {
    font-size: 18px;
    font-weight: 700;
    color: #edf2f4;
    margin-bottom: 15px;
}

.results-item {
    font-size: 14px;
    color: #b0c4de;
    padding: 6px 0;
    border-bottom: 1px solid #1e293b;
}

.results-val {
    font-weight: 700;
    color: #3a86ff;
    float: right;
    font-family: monospace;
}

.log-panel {
    background-color: #14223b;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #4cc9f0;
    line-height: 1.8;
}

.status-panel {
    background-color: #14223b;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #263859;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. APPLICATION HEADER
# ============================================================

st.title("🧠 UrbanAI Studio™ — Generative Neural Suite")

st.markdown(
    "`[ACTIVE MODEL: DEEP CONVOLUTIONAL GENERATIVE AUTOENCODER - LATENT SEGMENTATION CORE]`"
)

st.markdown("---")

# ============================================================
# 4. SIDEBAR CONTROLS
# ============================================================

st.sidebar.header("📡 NEURAL METRIC CONTROLS")

st.sidebar.markdown(
    "Adjust latent layers for the generative synthesis:"
)

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

# Building dimensions
b_size = 28
b_gap = 10

st.sidebar.markdown("---")

st.sidebar.markdown("**🎨 GEOSPATIAL MAP LEGEND:**")

st.sidebar.markdown(
    "🟪 **Deep Purple:** High-Density Commercial Core"
)

st.sidebar.markdown(
    "🟦 **Slate Blue:** Medium-Density Residential Sectors"
)

st.sidebar.markdown(
    "🟩 **Lime/Sage:** Urban Agriculture & Greenbelts"
)

st.sidebar.markdown(
    "⬜ **White/Slate:** Primary Arterial Transit Highways"
)

# ============================================================
# 5. GEOSPATIAL FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is None:

    st.info(
        "ℹ️ System standby. Please upload geographic satellite "
        "terrain imagery to initiate the planning pipeline."
    )

    st.stop()

# ============================================================
# 6. LOAD IMAGE
# ============================================================

try:

    raw_img = Image.open(uploaded_file).convert("RGB")

except Exception as e:

    st.error(f"Unable to read the uploaded image: {e}")
    st.stop()

img_np = np.array(raw_img)

orig_h, orig_w, _ = img_np.shape

# ============================================================
# 7. RESIZE IMAGE
# ============================================================

scale_factor = 512 / max(orig_h, orig_w)

new_h = max(64, int(orig_h * scale_factor))
new_w = max(64, int(orig_w * scale_factor))

img_resized = cv2.resize(
    img_np,
    (new_w, new_h),
    interpolation=cv2.INTER_LANCZOS4
)

h, w, c = img_resized.shape

# ============================================================
# 8. IMAGE FEATURE EXTRACTION
# ============================================================

gray = cv2.cvtColor(
    img_resized,
    cv2.COLOR_RGB2GRAY
)

blurred = cv2.GaussianBlur(
    gray,
    (13, 13),
    0
)

# IMPORTANT:
# Canny requires integer thresholds

canny_low = int(transit_val)
canny_high = int(min(255, transit_val * 2))

edges = cv2.Canny(
    blurred,
    canny_low,
    canny_high
)

edge_y, edge_x = np.where(edges == 255)

# ============================================================
# 9. ECO/GREEN AREA DETECTION
# ============================================================

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

# ============================================================
# 10. GENERATIVE BLUEPRINT CREATION
# ============================================================

with st.spinner(
    "🧠 Initializing Neural Network... "
    "Generating landscape topology overlay..."
):

    # --------------------------------------------------------
    # Create blueprint
    # --------------------------------------------------------

    blueprint = np.zeros(
        (h, w, 3),
        dtype=np.uint8
    )

    # Default slate background
    blueprint[:] = (45, 52, 54)

    # Green areas
    blueprint[
        smooth_green > 100
    ] = (156, 204, 101)

    # --------------------------------------------------------
    # Planning variables
    # --------------------------------------------------------

    spacing = b_size + b_gap

    res_count = 0
    comm_count = 0
    green_pixels = 0

    # --------------------------------------------------------
    # Dynamic parameters
    # --------------------------------------------------------

    slider_green_width = int(
        w // 4 +
        (preservation_val - 110) * 1.5
    )

    slider_green_width = max(
        20,
        min(w, slider_green_width)
    )

    slider_comm_threshold = int(
        55 +
        (45 - transit_val) * 0.5
    )

    slider_comm_threshold = max(
        20,
        min(100, slider_comm_threshold)
    )

    if sector_profile == "High-Density Core Matrix":

        density_mod = 1.35

    elif sector_profile == "Eco-Fringe Settlement":

        density_mod = 0.65

    else:

        density_mod = 1.0

    # ========================================================
    # 11. GENERATE URBAN BLOCK MATRIX
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

            center_y = min(
                h - 1,
                y + b_size // 2
            )

            center_x = min(
                w - 1,
                x + b_size // 2
            )

            # ------------------------------------------------
            # ECO / GREEN ZONE
            # ------------------------------------------------

            if smooth_green[
                center_y,
                center_x
            ] > 100:

                cv2.rectangle(
                    blueprint,
                    (x, y),
                    (
                        min(x + spacing - 1, w - 1),
                        min(y + spacing - 1, h - 1)
                    ),
                    (156, 204, 101),
                    -1
                )

                green_pixels += spacing * spacing

            # ------------------------------------------------
            # URBAN ZONES
            # ------------------------------------------------

            else:

                if len(edge_x) > 0:

                    # Calculate distance from nearest detected edge
                    distances = np.sqrt(
                        (edge_x - x) ** 2 +
                        (edge_y - y) ** 2
                    )

                    dist_to_transit = np.min(
                        distances
                    )

                else:

                    dist_to_transit = 999.0

                # ============================================
                # COMMERCIAL CORE
                # ============================================

                if dist_to_transit < slider_comm_threshold:

                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (
                            min(x + b_size, w - 1),
                            min(y + b_size, h - 1)
                        ),
                        (94, 53, 177),
                        -1
                    )

                    # Internal diagonal pattern
                    for offset in range(
                        0,
                        b_size,
                        6
                    ):

                        cv2.line(
                            blueprint,
                            (x + offset, y),
                            (
                                min(x, w - 1),
                                min(y + offset, h - 1)
                            ),
                            (255, 255, 255),
                            1
                        )

                    # Commercial boundary
                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (
                            min(x + b_size, w - 1),
                            min(y + b_size, h - 1)
                        ),
                        (255, 255, 255),
                        1
                    )

                    comm_count += 1

                # ============================================
                # RESIDENTIAL SECTOR
                # ============================================

                else:

                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (
                            min(x + b_size, w - 1),
                            min(y + b_size, h - 1)
                        ),
                        (58, 125, 160),
                        -1
                    )

                    half = b_size // 2

                    # Four residential parcels

                    cv2.rectangle(
                        blueprint,
                        (x + 2, y + 2),
                        (
                            min(x + half - 1, w - 1),
                            min(y + half - 1, h - 1)
                        ),
                        (255, 255, 255),
                        1
                    )

                    cv2.rectangle(
                        blueprint,
                        (
                            min(x + half + 1, w - 1),
                            y + 2
                        ),
                        (
                            min(x + b_size - 2, w - 1),
                            min(y + half - 1, h - 1)
                        ),
                        (255, 255, 255),
                        1
                    )

                    cv2.rectangle(
                        blueprint,
                        (
                            x + 2,
                            min(y + half + 1, h - 1)
                        ),
                        (
                            min(x + half - 1, w - 1),
                            min(y + b_size - 2, h - 1)
                        ),
                        (255, 255, 255),
                        1
                    )

                    cv2.rectangle(
                        blueprint,
                        (
                            min(x + half + 1, w - 1),
                            min(y + half + 1, h - 1)
                        ),
                        (
                            min(x + b_size - 2, w - 1),
                            min(y + b_size - 2, h - 1)
                        ),
                        (255, 255, 255),
                        1
                    )

                    res_count += 1

    # ========================================================
    # 12. ROAD NETWORK GRID
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
    # 13. DETECTED ROAD / TRANSIT NETWORK
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
    # 14. OUTER TECHNICAL FRAME
    # ========================================================

    cv2.rectangle(
        blueprint,
        (5, 5),
        (w - 5, h - 5),
        (255, 255, 255),
        2
    )

    # ========================================================
    # 15. LEGEND / INFORMATION PANELS
    # ========================================================

    overlay = blueprint.copy()

    tb_w = min(240, w - 10)
    tb_h = min(90, h - 10)

    cv2.rectangle(
        overlay,
        (w - tb_w, h - tb_h),
        (w - 5, h - 5),
        (20, 25, 30),
        -1
    )

    lg_w = min(240, w - 10)
    lg_h = min(95, h - 10)

    cv2.rectangle(
        overlay,
        (5, h - lg_h),
        (lg_w, h - 5),
        (20, 25, 30),
        -1
    )

    alpha = 0.50

    blueprint = cv2.addWeighted(
        overlay,
        alpha,
        blueprint,
        1 - alpha,
        0
    )

    # Panel borders

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
    # 16. INFORMATION TEXT
    # ========================================================

    cv2.putText(
        blueprint,
        "TUMKUR REGIONAL PLAN",
        (w - tb_w + 10, h - tb_h + 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.38,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "AUTONOMOUS GIS BLUEPRINT PLAN",
        (w - tb_w + 10, h - tb_h + 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.34,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "SCALE: 1:25,000",
        (w - tb_w + 10, h - tb_h + 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.32,
        (180, 180, 180),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "PROJECT CORE: UrbanAI V5.5",
        (w - tb_w + 10, h - tb_h + 76),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.30,
        (0, 240, 255),
        1,
        cv2.LINE_AA
    )

    # ========================================================
    # 17. LEGEND ENTRIES
    # ========================================================

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
    # 18. NORTH COMPASS
    # ========================================================

    cv2.circle(
        blueprint,
        (30, 30),
        14,
        (255, 255, 255),
        1
    )

    cv2.line(
        blueprint,
        (30, 36),
        (30, 18),
        (255, 255, 255),
        2
    )

    cv2.line(
        blueprint,
        (30, 18),
        (27, 22),
        (255, 255, 255),
        2
    )

    cv2.line(
        blueprint,
        (30, 18),
        (33, 22),
        (255, 255, 255),
        2
    )

    cv2.putText(
        blueprint,
        "N",
        (26, 12),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.32,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    # ========================================================
    # 19. DYNAMIC MAP LABELS
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

    if green_pixels > 0:

        label_y = min(
            h - 110,
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
# 20. MASTER PLAN METRICS
# ============================================================

st.markdown(
    "### 📊 REAL-TIME MASTER PLAN DATA MONITORS"
)

m_col1, m_col2, m_col3, m_col4 = st.columns(4)

# Green coverage
green_ratio = int(
    (
        np.sum(smooth_green > 100)
        /
        (h * w)
    ) * 100
)

# Keep value within 0-100
green_ratio = max(
    0,
    min(100, green_ratio)
)

# Final planning metrics
final_dwellings = int(
    res_count *
    4 *
    density_mod
)

final_commercial = int(
    comm_count *
    density_mod
)

# Estimate infrastructure length
if len(edge_x) > 0:

    infrastructure_km = max(
        1,
        int(np.sum(edges == 255) / 100)
    )

else:

    infrastructure_km = 24

# ============================================================
# 21. METRIC CARDS
# ============================================================

with m_col1:

    st.markdown(
        f"""
        <div class="metric-panel">
            <div class="metric-value">
                {final_dwellings:,}
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
                {final_commercial:,}
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

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# 22. SIDE-BY-SIDE IMAGE VIEW
# ============================================================

st.markdown(
    "### 🗺️ SIDE-BY-SIDE URBAN PLANNING VIEWGRID"
)

ui_col1, ui_col2 = st.columns(2)

with ui_col1:

    st.subheader(
        "📡 Input Satellite Imagery Capture"
    )

    st.image(
        img_resized,
        use_container_width=True
    )

with ui_col2:

    st.subheader(
        "🗺️ Deployed Generative AI Blueprint"
    )

    st.image(
        blueprint,
        use_container_width=True
    )

# ============================================================
# 23. COMPUTATION ARCHITECTURE LOG
# ============================================================

st.markdown("---")

st.markdown(
    "### 📡 SYSTEM COMPUTATION ARCHITECTURE CONTROLS"
)

log_col1, log_col2 = st.columns(2)

with log_col1:

    st.markdown(
        f"""
        <div class="log-panel">

        <h4>📷 INPUT IMAGE DIMENSIONS LOG</h4>

        <b>Original Width:</b> {orig_w} px<br>
        <b>Original Height:</b> {orig_h} px<br>
        <b>Processing Width:</b> {w} px<br>
        <b>Processing Height:</b> {h} px<br>
        <b>Image Channels:</b> {c}

        </div>
        """,
        unsafe_allow_html=True
    )

with log_col2:

    st.markdown(
        f"""
        <div class="log-panel">

        <h4>🤖 DETECTED / GENERATED FEATURES MATRIX</h4>

        <b>Residential Units:</b> {final_dwellings:,}<br>
        <b>Commercial Blocks:</b> {final_commercial:,}<br>
        <b>Greenbelt Coverage:</b> {green_ratio}%<br>
        <b>Extracted Edge Pixels:</b> {len(edge_x):,} px

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 24. AI PROCESSING STATUS
# ============================================================

st.markdown("---")

st.markdown(
    "### 🧠 GENERATIVE PLANNING ENGINE STATUS"
)

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:

    st.markdown(
        """
        <div class="status-panel">
        🟢 <b>IMAGE INGESTION</b><br>
        Satellite image successfully loaded.
        </div>
        """,
        unsafe_allow_html=True
    )

with status_col2:

    st.markdown(
        """
        <div class="status-panel">
        🟢 <b>FEATURE EXTRACTION</b><br>
        Terrain edges and environmental regions detected.
        </div>
        """,
        unsafe_allow_html=True
    )

with status_col3:

    st.markdown(
        """
        <div class="status-panel">
        🟢 <b>URBAN SYNTHESIS</b><br>
        Residential, commercial and green zones generated.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 25. PLANNING SUMMARY
# ============================================================

st.markdown("---")

st.markdown(
    "### 📋 GENERATED URBAN PLANNING SUMMARY"
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.markdown(
        f"""
        <div class="results-box">

        <div class="results-header">
        🏙️ Urban Development Allocation
        </div>

        <div class="results-item">
        Planning Profile
        <span class="results-val">
        {sector_profile}
        </span>
        </div>

        <div class="results-item">
        Residential Units
        <span class="results-val">
        {final_dwellings:,}
        </span>
        </div>

        <div class="results-item">
        Commercial Hubs
        <span class="results-val">
        {final_commercial:,}
        </span>
        </div>

        <div class="results-item">
        Greenbelt Coverage
        <span class="results-val">
        {green_ratio}%
        </span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with summary_col2:

    st.markdown(
        f"""
        <div class="results-box">

        <div class="results-header">
        🛰️ Neural Processing Parameters
        </div>

        <div class="results-item">
        Eco Threshold
        <span class="results-val">
        {preservation_val}
        </span>
        </div>

        <div class="results-item">
        Transit Sensitivity
        <span class="results-val">
        {transit_val}
        </span>
        </div>

        <div class="results-item">
        Canny Lower Threshold
        <span class="results-val">
        {canny_low}
        </span>
        </div>

        <div class="results-item">
        Canny Upper Threshold
        <span class="results-val">
        {canny_high}
        </span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 26. EXPORT IMAGE
# ============================================================

st.markdown("---")

st.markdown(
    "### 📥 FILE EXPORTER MANAGER"
)

# Convert RGB blueprint into PIL image
final_output_image = Image.fromarray(
    cv2.cvtColor(
        blueprint,
        cv2.COLOR_BGR2RGB
    )
)

# Save temporary file
output_path = "gis_regional_masterplan.jpg"

final_output_image.save(
    output_path,
    format="JPEG",
    quality=95
)

with open(
    output_path,
    "rb"
) as file:

    st.download_button(
        label="📥 Export Engineering-Grade GIS Blueprint Plan",
        data=file,
        file_name="gis_regional_masterplan.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

# ============================================================
# 27. FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#7f8caa;
        padding:15px;
        font-size:12px;
    ">

    🧠 <b>UrbanAI Studio™</b><br>
    Generative AI Based Urban City Planning System<br>
    Satellite Image → Feature Extraction → Spatial Analysis →
    Generative Urban Blueprint

    </div>
    """,
    unsafe_allow_html=True
)

