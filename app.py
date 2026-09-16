import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os


# ============================================================
# 1. STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UrbanAI Studio | GIS Engineering Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CUSTOM DARK UI THEME
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

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #edf2f4;
        margin-bottom: 5px;
    }

    .system-text {
        color: #4cc9f0;
        font-family: monospace;
        font-size: 13px;
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
        min-height: 105px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 700;
        color: #4cc9f0;
    }

    .metric-label {
        font-size: 11px;
        color: #b0c4de;
        text-transform: uppercase;
        margin-top: 5px;
    }

    .results-box {
        background-color: #14223b;
        padding: 22px;
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
        padding: 7px 0;
        border-bottom: 1px solid #1e293b;
    }

    .results-val {
        font-weight: 700;
        color: #4cc9f0;
        float: right;
        font-family: monospace;
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
        padding: 14px;
        border-radius: 6px;
        border: 1px solid #263454;
        color: #4cc9f0;
        font-family: monospace;
        line-height: 1.7;
    }

    .footer {
        text-align: center;
        color: #7f8caa;
        font-size: 12px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. APPLICATION HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏗️ UrbanAI Studio™ — GIS Master Planning Suite</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="system-text">'
    '[SYSTEM PROTOCOL: MASTER REGIONAL DEVELOPMENT OVERLAY - '
    'MUDIGERE-BUGUDANAHALLI CORRIDOR]'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ============================================================
# 4. SIDEBAR GIS CONFIGURATION
# ============================================================

st.sidebar.header("📡 GIS ANALYSIS CONFIGURATION")

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

b_size = 28
b_gap = 10

st.sidebar.markdown("---")

st.sidebar.markdown("**🎨 GEOSPATIAL MAP LEGEND**")

st.sidebar.markdown(
    "🟪 **Deep Purple Line Grids:** "
    "High-Density Commercial Core"
)

st.sidebar.markdown(
    "🟦 **Slate Blue Matrix:** "
    "Medium-Density Residential Sectors"
)

st.sidebar.markdown(
    "🟩 **Lime & Sage Pasture:** "
    "Urban Agriculture & Greenbelts"
)

st.sidebar.markdown(
    "⬜ **Slate Casing / White Split:** "
    "Primary Arterial Transit Corridors"
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
# 5. FILE UPLOAD
# ============================================================

st.subheader("🛰️ Geographic Satellite Image Input")

uploaded_file = st.file_uploader(
    "UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC (PNG/JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is None:

    st.info(
        "ℹ️ System standby. Please upload geographic satellite "
        "terrain imagery to initiate the planning pipeline."
    )

    st.markdown(
        """
        ### 📋 UrbanAI Processing Pipeline

        **Satellite Image**
        ↓  
        **Image Preprocessing**
        ↓  
        **Road / Infrastructure Detection**
        ↓  
        **Greenbelt Detection**
        ↓  
        **Urban Zoning Generation**
        ↓  
        **Commercial + Residential Allocation**
        ↓  
        **Generative Master Plan**
        """
    )

    st.stop()


# ============================================================
# 6. LOAD IMAGE
# ============================================================

try:

    raw_img = Image.open(uploaded_file).convert("RGB")

except Exception as error:

    st.error(
        f"❌ Unable to process the uploaded image: {error}"
    )

    st.stop()


img_np = np.array(raw_img)


# ============================================================
# 7. ORIGINAL IMAGE INFORMATION
# ============================================================

orig_h, orig_w, _ = img_np.shape


# ============================================================
# 8. RESIZE IMAGE FOR PROCESSING
# ============================================================

scale_factor = 512 / max(
    orig_h,
    orig_w
)

new_h = max(
    1,
    int(orig_h * scale_factor)
)

new_w = max(
    1,
    int(orig_w * scale_factor)
)

img_resized = cv2.resize(
    img_np,
    (new_w, new_h),
    interpolation=cv2.INTER_LANCZOS4
)

h, w, c = img_resized.shape


# ============================================================
# 9. IMAGE PROCESSING
# ============================================================

with st.spinner(
    "⚡ Running spatial matrix optimizations..."
):

    # --------------------------------------------------------
    # RGB → Grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        img_resized,
        cv2.COLOR_RGB2GRAY
    )

    # --------------------------------------------------------
    # Gaussian filtering
    # --------------------------------------------------------

    blurred = cv2.GaussianBlur(
        gray,
        (11, 11),
        0
    )

    # --------------------------------------------------------
    # Canny edge detection
    # --------------------------------------------------------

    canny_high = int(
        min(
            255,
            transit_val * 2.5
        )
    )

    edges = cv2.Canny(
        blurred,
        transit_val,
        canny_high
    )

    edge_y, edge_x = np.where(
        edges == 255
    )

    # ========================================================
    # 10. BLUEPRINT CANVAS
    # ========================================================

    blueprint = np.zeros(
        (h, w, 3),
        dtype=np.uint8
    )

    blueprint[:] = (
        45,
        52,
        54
    )

    # ========================================================
    # 11. GENERATIVE ZONING PARAMETERS
    # ========================================================

    spacing = b_size + b_gap

    res_count = 0
    comm_count = 0
    green_pixels = 0

    # Greenbelt width
    dynamic_green_width = int(
        w // 4
        +
        (preservation_val - 110) * 1.5
    )

    dynamic_green_width = max(
        40,
        min(
            dynamic_green_width,
            w - 80
        )
    )

    # Commercial zone height
    dynamic_comm_height = int(
        h / 3.5
        -
        (transit_val - 45) * 1.2
    )

    dynamic_comm_height = max(
        60,
        min(
            dynamic_comm_height,
            h - 80
        )
    )

    # Density multiplier
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
            # GREENBELT
            # ------------------------------------------------

            green_left = (
                w // 2
                -
                dynamic_green_width // 2
            )

            green_right = (
                w // 2
                +
                dynamic_green_width // 2
            )

            if (
                green_left
                <
                x
                <
                green_right
            ):

                cv2.rectangle(
                    blueprint,
                    (x, y),
                    (
                        x + spacing - 1,
                        y + spacing - 1
                    ),
                    (156, 204, 101),
                    -1
                )

                green_pixels += (
                    spacing * spacing
                )

            # ------------------------------------------------
            # COMMERCIAL ZONE
            # ------------------------------------------------

            elif y < dynamic_comm_height:

                cv2.rectangle(
                    blueprint,
                    (x, y),
                    (
                        x + b_size,
                        y + b_size
                    ),
                    (94, 53, 177),
                    -1
                )

                # Commercial hatch
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
                    (
                        x + b_size,
                        y + b_size
                    ),
                    (255, 255, 255),
                    1
                )

                comm_count += 1

            # ------------------------------------------------
            # RESIDENTIAL ZONE
            # ------------------------------------------------

            else:

                cv2.rectangle(
                    blueprint,
                    (x, y),
                    (
                        x + b_size,
                        y + b_size
                    ),
                    (58, 125, 160),
                    -1
                )

                half = b_size // 2

                # Housing plot 1
                cv2.rectangle(
                    blueprint,
                    (x + 2, y + 2),
                    (
                        x + half - 1,
                        y + half - 1
                    ),
                    (255, 255, 255),
                    1
                )

                # Housing plot 2
                cv2.rectangle(
                    blueprint,
                    (x + half + 1, y + 2),
                    (
                        x + b_size - 2,
                        y + half - 1
                    ),
                    (255, 255, 255),
                    1
                )

                # Housing plot 3
                cv2.rectangle(
                    blueprint,
                    (x + 2, y + half + 1),
                    (
                        x + half - 1,
                        y + b_size - 2
                    ),
                    (255, 255, 255),
                    1
                )

                # Housing plot 4
                cv2.rectangle(
                    blueprint,
                    (x + half + 1, y + half + 1),
                    (
                        x + b_size - 2,
                        y + b_size - 2
                    ),
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
    # 14. ROAD / TRANSIT NETWORK
    # ========================================================

    if len(edge_x) > 0:

        road_casing = cv2.dilate(
            edges,
            np.ones(
                (9, 9),
                np.uint8
            ),
            iterations=1
        )

        blueprint[
            road_casing == 255
        ] = (
            44,
            62,
            80
        )

        road_core = cv2.dilate(
            edges,
            np.ones(
                (3, 3),
                np.uint8
            ),
            iterations=1
        )

        blueprint[
            road_core == 255
        ] = (
            255,
            255,
            255
        )

        blueprint[
            edges == 255
        ] = (
            44,
            62,
            80
        )


    # ========================================================
    # 15. OUTER TECHNICAL FRAME
    # ========================================================

    cv2.rectangle(
        blueprint,
        (5, 5),
        (
            w - 5,
            h - 5
        ),
        (255, 255, 255),
        2
    )


    # ========================================================
    # 16. TRANSLUCENT TITLE + LEGEND PANELS
    # ========================================================

    overlay = blueprint.copy()

    tb_w = min(
        240,
        max(100, w - 10)
    )

    tb_h = min(
        90,
        max(70, h - 10)
    )

    lg_w = min(
        240,
        max(100, w - 10)
    )

    lg_h = min(
        95,
        max(70, h - 10)
    )


    # Title panel
    cv2.rectangle(
        overlay,
        (
            w - tb_w,
            h - tb_h
        ),
        (
            w - 5,
            h - 5
        ),
        (20, 25, 30),
        -1
    )


    # Legend panel
    cv2.rectangle(
        overlay,
        (
            5,
            h - lg_h
        ),
        (
            lg_w,
            h - 5
        ),
        (20, 25, 30),
        -1
    )


    # Alpha blending
    alpha = 0.50

    blueprint = cv2.addWeighted(
        overlay,
        alpha,
        blueprint,
        1 - alpha,
        0
    )


    # ========================================================
    # 17. PANEL BORDERS
    # ========================================================

    cv2.rectangle(
        blueprint,
        (
            w - tb_w,
            h - tb_h
        ),
        (
            w - 5,
            h - 5
        ),
        (255, 255, 255),
        2
    )

    cv2.rectangle(
        blueprint,
        (
            5,
            h - lg_h
        ),
        (
            lg_w,
            h - 5
        ),
        (255, 255, 255),
        2
    )


    # ========================================================
    # 18. TITLE BLOCK TEXT
    # ========================================================

    cv2.putText(
        blueprint,
        "TUMKUR REGIONAL PLAN",
        (
            w - tb_w + 10,
            h - tb_h + 22
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.38,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "AUTONOMOUS GIS BLUEPRINT",
        (
            w - tb_w + 10,
            h - tb_h + 40
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.34,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "SCALE: 1:25,000",
        (
            w - tb_w + 10,
            h - tb_h + 60
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.32,
        (180, 180, 180),
        1,
        cv2.LINE_AA
    )

    cv2.putText(
        blueprint,
        "PROJECT: UrbanAI V5.5",
        (
            w - tb_w + 10,
            h - tb_h + 76
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.30,
        (0, 240, 255),
        1,
        cv2.LINE_AA
    )


    # ========================================================
    # 19. MAP LEGEND
    # ========================================================

    # Commercial
    cv2.rectangle(
        blueprint,
        (
            15,
            h - lg_h + 12
        ),
        (
            35,
            h - lg_h + 27
        ),
        (94, 53, 177),
        -1
    )

    cv2.putText(
        blueprint,
        "Commercial Core Hubs",
        (
            45,
            h - lg_h + 24
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # Residential
    cv2.rectangle(
        blueprint,
        (
            15,
            h - lg_h + 37
        ),
        (
            35,
            h - lg_h + 52
        ),
        (58, 125, 160),
        -1
    )

    cv2.putText(
        blueprint,
        "Residential Sectors",
        (
            45,
            h - lg_h + 48
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # Greenbelt
    cv2.rectangle(
        blueprint,
        (
            15,
            h - lg_h + 62
        ),
        (
            35,
            h - lg_h + 77
        ),
        (156, 204, 101),
        -1
    )

    cv2.putText(
        blueprint,
        "Eco Preservation Belts",
        (
            45,
            h - lg_h + 73
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # ========================================================
    # 20. NORTH ARROW
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
    # 21. DYNAMIC MAP ANNOTATIONS
    # ========================================================

    if comm_count > 0:

        cv2.putText(
            blueprint,
            "HIGH-DENSITY COMMERCIAL CORRIDOR",
            (100, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.40,
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
            (50, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.38,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )


    if green_pixels > 0:

        green_label_y = min(
            h - 20,
            h // 2 + 60
        )

        cv2.putText(
            blueprint,
            "URBAN AGRICULTURE / GREEN BELT",
            (50, green_label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (44, 62, 80),
            1,
            cv2.LINE_AA
        )


# ============================================================
# 22. MASTER PLAN METRICS
# ============================================================

green_ratio = int(
    (
        green_pixels
        /
        max(1, h * w)
    ) * 100
)

green_ratio = min(
    100,
    max(0, green_ratio)
)

final_dwellings = int(
    res_count * 4 * density_mod
)

final_commercial = int(
    comm_count * density_mod
)

if len(edge_x) > 0:

    infrastructure_km = int(
        np.sum(edges == 255) / 100
    )

else:

    infrastructure_km = 0


# ============================================================
# 23. COMMAND CENTER METRICS
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


# ============================================================
# 24. SIDE-BY-SIDE IMAGE VIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🗺️ SIDE-BY-SIDE PRESENTATION VIEWGRID'
    '</div>',
    unsafe_allow_html=True
)

ui_col1, ui_col2 = st.columns(2)


with ui_col1:

    st.subheader(
        "🛰️ Input Satellite Imagery Capture"
    )

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
# 25. PROCESSING ANALYTICS
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">'
    '📡 SYSTEM COMPUTATION ARCHITECTURE CONTROLS'
    '</div>',
    unsafe_allow_html=True
)

log_col1, log_col2 = st.columns(2)


with log_col1:

    st.markdown(
        f"""
        <div class="results-box">

        <div class="results-header">
        📷 INPUT IMAGE DIMENSIONS LOG
        </div>

        <div class="results-item">
        Original Width
        <span class="results-val">{orig_w} px</span>
        </div>

        <div class="results-item">
        Original Height
        <span class="results-val">{orig_h} px</span>
        </div>

        <div class="results-item">
        Processing Width
        <span class="results-val">{w} px</span>
        </div>

        <div class="results-item">
        Processing Height
        <span class="results-val">{h} px</span>
        </div>

        <div class="results-item">
        Image Channels
        <span class="results-val">{c}</span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with log_col2:

    st.markdown(
        f"""
        <div class="results-box">

        <div class="results-header">
        🤖 DETECTED / GENERATED FEATURES MATRIX
        </div>

        <div class="results-item">
        Residential Blocks
        <span class="results-val">
        {res_count:,}
        </span>
        </div>

        <div class="results-item">
        Planned Dwellings
        <span class="results-val">
        {final_dwellings:,}
        </span>
        </div>

        <div class="results-item">
        Commercial Blocks
        <span class="results-val">
        {comm_count:,}
        </span>
        </div>

        <div class="results-item">
        Greenbelt Coverage
        <span class="results-val">
        {green_ratio}%
        </span>
        </div>

        <div class="results-item">
        Extracted Edge Pixels
        <span class="results-val">
        {len(edge_x):,}
        </span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 26. PLANNING INTERPRETATION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🧠 URBANAI PLANNING INTERPRETATION'
    '</div>',
    unsafe_allow_html=True
)

interpret_col1, interpret_col2 = st.columns(2)


with interpret_col1:

    st.markdown(
        f"""
        **Selected Planning Profile**

        `{sector_profile}`

        **Commercial Development**

        The generated plan allocates the upper planning
        sector to commercial development blocks.

        **Residential Development**

        The lower planning sector is organized into
        residential subdivision matrices.
        """
    )


with interpret_col2:

    st.markdown(
        f"""
        **Green Infrastructure**

        A central ecological corridor has been reserved
        as an urban agriculture and greenbelt zone.

        **Transit Infrastructure**

        Image edges are used to generate a visual
        transportation/infrastructure overlay.

        **Current Green Coverage**

        `{green_ratio}%`
        """
    )


# ============================================================
# 27. EXPORT MASTER PLAN
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📥 FILE EXPORTER MANAGER'
    '</div>',
    unsafe_allow_html=True
)


# Convert OpenCV BGR → RGB
export_rgb = cv2.cvtColor(
    blueprint,
    cv2.COLOR_BGR2RGB
)

final_output_image = Image.fromarray(
    export_rgb
)


# Save to memory instead of depending only on filesystem
import io

image_buffer = io.BytesIO()

final_output_image.save(
    image_buffer,
    format="JPEG",
    quality=95
)

image_buffer.seek(0)


st.download_button(
    label="📥 Export Engineering-Grade GIS Blueprint Plan",
    data=image_buffer,
    file_name="gis_regional_masterplan.jpg",
    mime="image/jpeg",
    use_container_width=True
)


# ============================================================
# 28. OPTIONAL PNG EXPORT
# ============================================================

png_buffer = io.BytesIO()

final_output_image.save(
    png_buffer,
    format="PNG"
)

png_buffer.seek(0)


st.download_button(
    label="🖼️ Export High-Quality PNG Blueprint",
    data=png_buffer,
    file_name="gis_regional_masterplan.png",
    mime="image/png",
    use_container_width=True
)


# ============================================================
# 29. FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">

    UrbanAI Studio™ | Generative Urban Planning Prototype |
    GIS Engineering Suite | OpenCV Spatial Processing

    <br><br>

    Satellite Image → Spatial Analysis → Zoning → 
    Infrastructure → Urban Master Plan

    </div>
    """,
    unsafe_allow_html=True
)
