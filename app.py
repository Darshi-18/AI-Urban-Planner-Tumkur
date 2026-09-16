import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os


# ============================================================
# 1. INITIALIZE STREAMLIT APPLICATION
# ============================================================

st.set_page_config(
    page_title="UrbanAI Studio | GIS Suite",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. MODERN DARK ARCHITECTURAL UI
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #0b132b;
        color: #edf2f4;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #101936;
    }

    [data-testid="stSidebar"] * {
        color: #edf2f4;
    }

    /* Buttons */
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
        background-color: #2563eb;
        color: white;
    }

    /* Metric panels */
    .metric-panel {
        background-color: #1c2541;
        padding: 20px;
        border-radius: 8px;
        border-top: 4px solid #3a86ff;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.20);
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #4cc9f0;
    }

    .metric-label {
        font-size: 12px;
        color: #b0c4de;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* Status panels */
    .status-panel {
        background-color: #1c2541;
        padding: 18px;
        border-radius: 8px;
        border-left: 4px solid #4cc9f0;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
    }

    /* Info box */
    .info-panel {
        background-color: #151f3d;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #26345c;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. APPLICATION HEADER
# ============================================================

st.title("🏙️ UrbanAI Studio™ — Engineering Layout Suite")

st.markdown(
    "`[SYSTEM PROTOCOL: DYNAMIC TECHNICAL RECONSTRUCTION CORE]`"
)

st.markdown("---")


# ============================================================
# 4. SIDEBAR CONFIGURATION
# ============================================================

st.sidebar.header("📡 LAYOUT FREQUENCY CONFIGURATION")

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

# Block parameters
b_size = 28
b_gap = 10

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **🎨 GEOSPATIAL MAP LEGEND**

    🟥🟪 **Angled Hatch Lines**  
    High-Density Commercial Core

    🟦⬜ **Horizontal Subdivisions**  
    Medium-Density Residential

    🟩🟢 **Dotted Pasture**  
    Urban Agriculture & Greenbelts

    ⬜🛣️ **Double Slate Lines**  
    Primary Arterial Transit Highways
    """
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Upload a satellite or aerial image to start the "
    "urban planning reconstruction pipeline."
)


# ============================================================
# 5. GEOSPATIAL FILE UPLOAD
# ============================================================

st.subheader("🛰️ Geographic Aerial Footprint Input")

uploaded_file = st.file_uploader(
    "UPLOAD GEOGRAPHIC AERIAL FOOTPRINT GRAPHIC",
    type=["png", "jpg", "jpeg"]
)


# ============================================================
# 6. WAIT FOR IMAGE
# ============================================================

if uploaded_file is None:

    st.info(
        "ℹ️ System standby. Please upload geographic satellite "
        "terrain imagery to initiate the planning pipeline."
    )

    st.markdown(
        """
        <div class="info-panel">

        ### Recommended Satellite Image

        For better results, upload an image containing:

        - Roads
        - Buildings
        - Vegetation
        - Open land
        - Urban areas
        - Agricultural areas
        - Water bodies if available

        <br>

        <b>Supported formats:</b> PNG, JPG, JPEG

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# 7. READ IMAGE
# ============================================================

try:

    raw_img = Image.open(uploaded_file).convert("RGB")

except Exception as e:

    st.error(f"❌ Unable to read the uploaded image: {e}")
    st.stop()


img_np = np.array(raw_img)


# ============================================================
# 8. IMAGE DIMENSIONS
# ============================================================

orig_h, orig_w, _ = img_np.shape


# ============================================================
# 9. RESIZE IMAGE
# ============================================================

max_dimension = 512

scale_factor = max_dimension / max(
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
# 10. IMAGE PROCESSING
# ============================================================

gray = cv2.cvtColor(
    img_resized,
    cv2.COLOR_RGB2GRAY
)


blurred = cv2.GaussianBlur(
    gray,
    (11, 11),
    0
)


# ============================================================
# 11. ROAD / TRANSIT EXTRACTION
# ============================================================

edges = cv2.Canny(
    blurred,
    transit_val,
    int(transit_val * 2.5)
)

edge_y, edge_x = np.where(
    edges == 255
)


# ============================================================
# 12. VEGETATION / GREENBELT EXTRACTION
# ============================================================

_, green_mask = cv2.threshold(
    blurred,
    preservation_val,
    255,
    cv2.THRESH_BINARY_INV
)


green_kernel = np.ones(
    (9, 9),
    np.uint8
)


green_mask = cv2.dilate(
    green_mask,
    green_kernel,
    iterations=1
)


smooth_green = cv2.GaussianBlur(
    green_mask,
    (25, 25),
    0
)


# ============================================================
# 13. BLUEPRINT GENERATION
# ============================================================

with st.spinner(
    "⚡ Simulating engineering blueprint drawing..."
):

    # --------------------------------------------------------
    # BASE BLUEPRINT
    # --------------------------------------------------------

    blueprint = np.zeros(
        (h, w, 3),
        dtype=np.uint8
    )

    # Slate grey
    blueprint[:] = (
        53,
        59,
        72
    )


    # --------------------------------------------------------
    # GREENBELT AREAS
    # --------------------------------------------------------

    green_indices = (
        smooth_green > 100
    )

    blueprint[
        green_indices
    ] = (
        76,
        154,
        42
    )


    # --------------------------------------------------------
    # FAST STIPPLE DOT PATTERN
    # --------------------------------------------------------

    stipple_mask = np.zeros(
        (h, w),
        dtype=np.uint8
    )

    stipple_mask[
        ::8,
        ::8
    ] = 255


    dot_indices = (
        green_indices &
        (stipple_mask == 255)
    )


    blueprint[
        dot_indices
    ] = (
        139,
        195,
        74
    )


    # --------------------------------------------------------
    # BLOCK PARAMETERS
    # --------------------------------------------------------

    spacing = b_size + b_gap

    res_count = 0
    comm_count = 0


    # --------------------------------------------------------
    # COMMERCIAL BUFFER
    # --------------------------------------------------------

    commercial_cushion = int(
        55 +
        (45 - transit_val) * 0.5
    )


    # --------------------------------------------------------
    # DENSITY MODIFIER
    # --------------------------------------------------------

    if sector_profile == "High-Density Core Matrix":

        density_mod = 1.35

    elif sector_profile == "Eco-Fringe Settlement":

        density_mod = 0.65

    else:

        density_mod = 1.0


    # --------------------------------------------------------
    # URBAN BLOCK GENERATION
    # --------------------------------------------------------

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

            # -----------------------------------------------
            # DISTANCE FROM ROAD
            # -----------------------------------------------

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


            # -----------------------------------------------
            # CENTER PIXEL
            # -----------------------------------------------

            center_y = min(
                y + b_size // 2,
                h - 1
            )

            center_x = min(
                x + b_size // 2,
                w - 1
            )


            # -----------------------------------------------
            # DO NOT DEVELOP GREENBELTS
            # -----------------------------------------------

            if smooth_green[
                center_y,
                center_x
            ] <= 100:


                # ===========================================
                # ZONE A — COMMERCIAL
                # ===========================================

                if (
                    dist_to_transit
                    <
                    commercial_cushion
                ):

                    x2 = min(
                        x + b_size,
                        w - 1
                    )

                    y2 = min(
                        y + b_size,
                        h - 1
                    )


                    # Commercial block
                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x2, y2),
                        (41, 128, 185),
                        -1
                    )


                    # Diagonal hatch
                    for offset in range(
                        0,
                        b_size,
                        5
                    ):

                        x1 = min(
                            x + offset,
                            w - 1
                        )

                        y1 = y

                        x_end = x

                        y_end = min(
                            y + offset,
                            h - 1
                        )

                        cv2.line(
                            blueprint,
                            (x1, y1),
                            (x_end, y_end),
                            (231, 76, 60),
                            1
                        )


                    # Block border
                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x2, y2),
                        (255, 255, 255),
                        1
                    )


                    comm_count += 1


                # ===========================================
                # ZONE B — RESIDENTIAL
                # ===========================================

                else:

                    x2 = min(
                        x + b_size,
                        w - 1
                    )

                    y2 = min(
                        y + b_size,
                        h - 1
                    )


                    # Residential block
                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x2, y2),
                        (47, 54, 114),
                        -1
                    )


                    # Horizontal subdivision lines
                    for y_offset in range(
                        4,
                        b_size,
                        6
                    ):

                        yy = min(
                            y + y_offset,
                            h - 1
                        )

                        cv2.line(
                            blueprint,
                            (x + 2, yy),
                            (
                                min(
                                    x + b_size - 2,
                                    w - 1
                                ),
                                yy
                            ),
                            (255, 255, 255),
                            1
                        )


                    # Residential border
                    cv2.rectangle(
                        blueprint,
                        (x, y),
                        (x2, y2),
                        (120, 120, 120),
                        1
                    )


                    res_count += 1


    # ========================================================
    # 14. LOCAL STREET GRID
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
            (87, 101, 116),
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
            (87, 101, 116),
            1
        )


    # ========================================================
    # 15. PRIMARY HIGHWAY NETWORK
    # ========================================================

    if len(edge_x) > 0:

        # Road casing
        road_casing = cv2.dilate(
            edges,
            np.ones((9, 9), np.uint8),
            iterations=1
        )


        blueprint[
            road_casing == 255
        ] = (
            44,
            62,
            80
        )


        # Road core
        road_core = cv2.dilate(
            edges,
            np.ones((3, 3), np.uint8),
            iterations=1
        )


        blueprint[
            road_core == 255
        ] = (
            255,
            255,
            255
        )


        # Center / median
        blueprint[
            edges == 255
        ] = (
            44,
            62,
            80
        )


    # ========================================================
    # 16. ENGINEERING FRAME
    # ========================================================

    cv2.rectangle(
        blueprint,
        (5, 5),
        (w - 5, h - 5),
        (255, 255, 255),
        2
    )


    # ========================================================
    # 17. TITLE BLOCK
    # ========================================================

    tb_w = min(
        250,
        max(100, w - 10)
    )

    tb_h = min(
        95,
        max(50, h - 10)
    )


    tb_x = w - tb_w
    tb_y = h - tb_h


    cv2.rectangle(
        blueprint,
        (tb_x, tb_y),
        (w - 5, h - 5),
        (30, 39, 46),
        -1
    )


    cv2.rectangle(
        blueprint,
        (tb_x, tb_y),
        (w - 5, h - 5),
        (255, 255, 255),
        2
    )


    cv2.putText(
        blueprint,
        "URBANAI MASTER REGION",
        (tb_x + 12, tb_y + 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.40,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        blueprint,
        "REGIONAL DEVELOPMENT PLAN",
        (tb_x + 12, tb_y + 44),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        blueprint,
        "SCALE: 1:25,000",
        (tb_x + 12, tb_y + 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.34,
        (180, 180, 180),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        blueprint,
        "PROJECT CORE: UrbanAI v5.5",
        (tb_x + 12, tb_y + 82),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.32,
        (0, 240, 255),
        1,
        cv2.LINE_AA
    )


    # ========================================================
    # 18. LEGEND
    # ========================================================

    lg_w = min(
        240,
        max(100, w - 10)
    )

    lg_h = min(
        95,
        max(50, h - 10)
    )


    lg_x = 5
    lg_y = h - lg_h


    cv2.rectangle(
        blueprint,
        (lg_x, lg_y),
        (lg_w, h - 5),
        (30, 39, 46),
        -1
    )


    cv2.rectangle(
        blueprint,
        (lg_x, lg_y),
        (lg_w, h - 5),
        (255, 255, 255),
        2
    )


    # --------------------------------------------------------
    # Commercial legend
    # --------------------------------------------------------

    cv2.rectangle(
        blueprint,
        (15, lg_y + 12),
        (35, lg_y + 27),
        (41, 128, 185),
        -1
    )


    cv2.line(
        blueprint,
        (15, lg_y + 12),
        (35, lg_y + 27),
        (231, 76, 60),
        1
    )


    cv2.putText(
        blueprint,
        "Commercial Core Hubs",
        (45, lg_y + 24),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # --------------------------------------------------------
    # Residential legend
    # --------------------------------------------------------

    cv2.rectangle(
        blueprint,
        (15, lg_y + 37),
        (35, lg_y + 52),
        (47, 54, 114),
        -1
    )


    cv2.line(
        blueprint,
        (15, lg_y + 44),
        (35, lg_y + 44),
        (255, 255, 255),
        1
    )


    cv2.putText(
        blueprint,
        "Residential Sectors",
        (45, lg_y + 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # --------------------------------------------------------
    # Greenbelt legend
    # --------------------------------------------------------

    cv2.rectangle(
        blueprint,
        (15, lg_y + 62),
        (35, lg_y + 77),
        (76, 154, 42),
        -1
    )


    cv2.circle(
        blueprint,
        (25, lg_y + 70),
        1,
        (255, 255, 255),
        -1
    )


    cv2.putText(
        blueprint,
        "Eco Preservation Belts",
        (45, lg_y + 73),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )


    # ========================================================
    # 19. NORTH COMPASS
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
    # 20. MAP LABELS
    # ========================================================

    if comm_count > 0:

        cv2.putText(
            blueprint,
            "COMMERCIAL INFRASTRUCTURE CORE",
            (100, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.38,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )


    if res_count > 0:

        label_y = max(
            30,
            h - 120
        )

        cv2.putText(
            blueprint,
            "PROPOSED HOUSING SUBDIVISIONS",
            (40, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.38,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )


    if np.sum(
        smooth_green > 100
    ) > 0:

        cv2.putText(
            blueprint,
            "NATURAL GREENBELT",
            (40, max(30, h // 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.38,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )


# ============================================================
# 21. CALCULATE SYSTEM METRICS
# ============================================================

green_ratio = int(
    (
        np.sum(
            smooth_green > 100
        )
        /
        (h * w)
    )
    * 100
)


if len(edge_x) > 0:

    infrastructure_km = int(
        np.sum(edges == 255) / 100
    )

else:

    infrastructure_km = 0


planned_dwellings = int(
    res_count *
    4 *
    density_mod
)


commercial_hubs = int(
    comm_count *
    density_mod
)


# ============================================================
# 22. COMMAND CENTER
# ============================================================

st.markdown("---")

st.subheader(
    "📊 REAL-TIME LIVE DATA ANALYSIS COMMAND CENTER"
)


m_col1, m_col2, m_col3, m_col4 = st.columns(4)


# ------------------------------------------------------------
# Metric 1
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Metric 2
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Metric 3
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# Metric 4
# ------------------------------------------------------------

with m_col4:

    st.markdown(
        f"""
        <div class="metric-panel">

            <div class="metric-value">
                {infrastructure_km}
            </div>

            <div class="metric-label">
                🛣️ Highway Route Index
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 23. PLANNING PROFILE
# ============================================================

st.markdown("---")

st.subheader(
    "⚙️ ACTIVE PLANNING CONFIGURATION"
)


config_col1, config_col2, config_col3 = st.columns(3)


with config_col1:

    st.markdown(
        f"""
        <div class="status-panel">

        <b>Planning Preset</b>

        <br><br>

        {sector_profile}

        </div>
        """,
        unsafe_allow_html=True
    )


with config_col2:

    st.markdown(
        f"""
        <div class="status-panel">

        <b>Eco Preservation Threshold</b>

        <br><br>

        {preservation_val}

        </div>
        """,
        unsafe_allow_html=True
    )


with config_col3:

    st.markdown(
        f"""
        <div class="status-panel">

        <b>Transit Sensitivity</b>

        <br><br>

        {transit_val}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 24. SIDE-BY-SIDE PRESENTATION
# ============================================================

st.markdown("---")

st.subheader(
    "🗺️ SIDE-BY-SIDE URBAN PLANNING VIEWGRID"
)


ui_col1, ui_col2 = st.columns(2)


# ------------------------------------------------------------
# Original image
# ------------------------------------------------------------

with ui_col1:

    st.markdown(
        "### 🛰️ Input Satellite Imagery Capture"
    )

    st.image(
        img_resized,
        use_container_width=True
    )


# ------------------------------------------------------------
# Blueprint
# ------------------------------------------------------------

with ui_col2:

    st.markdown(
        "### 🗺️ Synthesized Engineering Blueprint"
    )

    st.image(
        blueprint,
        use_container_width=True
    )


# ============================================================
# 25. PROCESSING INFORMATION
# ============================================================

st.markdown("---")

st.subheader(
    "🔬 IMAGE PROCESSING RESULTS"
)


result_col1, result_col2 = st.columns(2)


with result_col1:

    st.markdown(
        f"""
        <div class="status-panel">

        <b>INPUT IMAGE</b>

        <br><br>

        Original Width: {orig_w} px

        <br>

        Original Height: {orig_h} px

        <br>

        Processing Width: {w} px

        <br>

        Processing Height: {h} px

        </div>
        """,
        unsafe_allow_html=True
    )


with result_col2:

    st.markdown(
        f"""
        <div class="status-panel">

        <b>DETECTED / GENERATED FEATURES</b>

        <br><br>

        Residential Blocks:
        {res_count}

        <br>

        Commercial Blocks:
        {comm_count}

        <br>

        Greenbelt Coverage:
        {green_ratio}%

        <br>

        Extracted Edge Pixels:
        {len(edge_x):,}

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 26. EXPORT BLUEPRINT
# ============================================================

st.markdown("---")

st.subheader(
    "📁 FILE EXPORTER MANAGER"
)


final_output_image = Image.fromarray(
    blueprint
)


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
# 27. PROJECT INFORMATION
# ============================================================

st.markdown("---")

st.subheader(
    "🏙️ URBANAI PIPELINE"
)


st.markdown(
    """
    <div class="info-panel">

    <b>Satellite Image</b>
    &nbsp;→&nbsp;

    <b>Image Preprocessing</b>
    &nbsp;→&nbsp;

    <b>Road Extraction</b>
    &nbsp;→&nbsp;

    <b>Greenbelt Detection</b>
    &nbsp;→&nbsp;

    <b>Land-Use Zoning</b>
    &nbsp;→&nbsp;

    <b>Residential Planning</b>
    &nbsp;→&nbsp;

    <b>Commercial Planning</b>
    &nbsp;→&nbsp;

    <b>Engineering Blueprint</b>

    <br><br>

    <b>Current architecture:</b>
    Computer Vision + Rule-Based Generative Layout

    <br>

    <b>Future architecture:</b>
    Satellite Data + GIS + Generative AI + Urban Planning Constraints

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 28. FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#718096;">

    <b>UrbanAI Studio™</b>

    <br>

    Generative AI Based Urban City Planning

    <br><br>

    Satellite Image → Computer Vision → Land Use →
    Transportation → Greenbelts → Urban Master Plan

    </div>
    """,
    unsafe_allow_html=True
)
