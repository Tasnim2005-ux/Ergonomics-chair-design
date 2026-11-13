import streamlit as st
import pandas as pd
import numpy as np
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ergonomic Chair Design",
    page_icon="🪑",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data"
)


# ============================================================
# ANTHROPOMETRIC MEASUREMENTS
# ============================================================

MEASUREMENTS = [

    "POPLITEAL_HEIGHTCM",

    "BUTTOCK_POPLITEAL_HIGHTCM",

    "HIP_BREADTHCM",

    "SITTING_SHOULDER_HEIGHTCM",

    "SITTING_KNEE_HEIGHTCM",

    "TIGH_CLEARENCECM",

    "BUTTOCK_KNEE_LENGTHCM",

    "FOOT_LENGTHCM",

    "SITTING_ELBOW_HEIGHTCM"
]


DISPLAY_NAMES = {

    "POPLITEAL_HEIGHTCM":
        "Popliteal Height",

    "BUTTOCK_POPLITEAL_HIGHTCM":
        "Buttock-Popliteal Length",

    "HIP_BREADTHCM":
        "Hip Breadth",

    "SITTING_SHOULDER_HEIGHTCM":
        "Sitting Shoulder Height",

    "SITTING_KNEE_HEIGHTCM":
        "Sitting Knee Height",

    "TIGH_CLEARENCECM":
        "Thigh Clearance",

    "BUTTOCK_KNEE_LENGTHCM":
        "Buttock-Knee Length",

    "FOOT_LENGTHCM":
        "Foot Length",

    "SITTING_ELBOW_HEIGHTCM":
        "Sitting Elbow Height"
}


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    male_path = os.path.join(
        DATA_PATH,
        "male.xlsx"
    )

    female_path = os.path.join(
        DATA_PATH,
        "female.xlsx"
    )

    # --------------------------------------------------------
    # FILE EXISTENCE CHECK
    # --------------------------------------------------------

    if not os.path.exists(male_path):

        raise FileNotFoundError(
            f"Male dataset not found:\n{male_path}"
        )

    if not os.path.exists(female_path):

        raise FileNotFoundError(
            f"Female dataset not found:\n{female_path}"
        )

    # --------------------------------------------------------
    # READ EXCEL FILES
    # --------------------------------------------------------

    male = pd.read_excel(
        male_path
    )

    female = pd.read_excel(
        female_path
    )

    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    def clean_columns(df):

        df.columns = (

            df.columns
            .astype(str)
            .str.strip()
            .str.upper()

            .str.replace(
                "(CM)",
                "CM",
                regex=False
            )

            .str.replace(
                "(",
                "",
                regex=False
            )

            .str.replace(
                ")",
                "",
                regex=False
            )

            .str.replace(
                " ",
                "_",
                regex=False
            )

            .str.replace(
                "-",
                "_",
                regex=False
            )
        )

        return df

    male = clean_columns(male)
    female = clean_columns(female)

    # --------------------------------------------------------
    # CONVERT MEASUREMENTS TO NUMERIC
    # --------------------------------------------------------

    for col in MEASUREMENTS:

        if col in male.columns:

            male[col] = pd.to_numeric(
                male[col],
                errors="coerce"
            )

        if col in female.columns:

            female[col] = pd.to_numeric(
                female[col],
                errors="coerce"
            )

    # --------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------------------------

    male_missing = [
        col
        for col in MEASUREMENTS
        if col not in male.columns
    ]

    female_missing = [
        col
        for col in MEASUREMENTS
        if col not in female.columns
    ]

    if male_missing:

        raise ValueError(

            "Male dataset is missing these required columns:\n"
            + "\n".join(male_missing)

            + "\n\nActual Male columns:\n"
            + "\n".join(male.columns)
        )

    if female_missing:

        raise ValueError(

            "Female dataset is missing these required columns:\n"
            + "\n".join(female_missing)

            + "\n\nActual Female columns:\n"
            + "\n".join(female.columns)
        )

    # --------------------------------------------------------
    # REMOVE INCOMPLETE ROWS
    # --------------------------------------------------------

    male = male.dropna(
        subset=MEASUREMENTS
    ).copy()

    female = female.dropna(
        subset=MEASUREMENTS
    ).copy()

    return male, female


# ============================================================
# LOAD DATASETS
# ============================================================

male_df, female_df = load_data()


# ============================================================
# STATISTICS FUNCTION
# ============================================================

def calculate_statistics(df):

    results = []

    for col in MEASUREMENTS:

        data = df[col].dropna()

        if data.empty:
            continue

        results.append({

            "Measurement":
                DISPLAY_NAMES[col],

            "Min":
                data.min(),

            "Max":
                data.max(),

            "Mean":
                data.mean(),

            "Median":
                data.median(),

            "Std. Deviation":
                data.std(),

            "Variance":
                data.var(),

            "P5":
                np.percentile(
                    data,
                    5
                ),

            "P25":
                np.percentile(
                    data,
                    25
                ),

            "P50":
                np.percentile(
                    data,
                    50
                ),

            "P75":
                np.percentile(
                    data,
                    75
                ),

            "P95":
                np.percentile(
                    data,
                    95
                )
        })

    return pd.DataFrame(
        results
    )


# ============================================================
# CALCULATE STATISTICS
# ============================================================

male_stats = calculate_statistics(
    male_df
)

female_stats = calculate_statistics(
    female_df
)


# ============================================================
# CHAIR + WRITING TABLET DESIGN CALCULATION
# ============================================================

def calculate_chair_design(stats):

    def get_value(
        measurement,
        percentile
    ):

        rows = stats[
            stats["Measurement"]
            == measurement
        ]

        if rows.empty:
            return np.nan

        return rows.iloc[0][percentile]

    # ========================================================
    # 1. SEAT HEIGHT
    # ========================================================

    popliteal_p5 = get_value(
        "Popliteal Height",
        "P5"
    )

    seat_height = (
        popliteal_p5
        - 2.0
    )

    # ========================================================
    # 2. SEAT DEPTH
    # ========================================================

    bpl_p5 = get_value(
        "Buttock-Popliteal Length",
        "P5"
    )

    seat_depth = (
        bpl_p5
        - 3.0
    )

    # ========================================================
    # 3. SEAT WIDTH
    # ========================================================

    hip_p95 = get_value(
        "Hip Breadth",
        "P95"
    )

    seat_width_min = (
        hip_p95
        + 2.0
    )

    seat_width_max = (
        hip_p95
        + 3.0
    )

    # ========================================================
    # 4. BACKREST HEIGHT
    # ========================================================

    shoulder_p50 = get_value(
        "Sitting Shoulder Height",
        "P50"
    )

    backrest_height = (
        shoulder_p50
    )

    # ========================================================
    # 5. WRITING TABLET HEIGHT
    # ========================================================
    #
    # Hinged writing tablet is part of the chair design.
    # Sitting Elbow Height is therefore a PRIMARY
    # anthropometric design parameter.
    #
    # Preliminary design rule:
    #
    # Writing Tablet Height = P50 Sitting Elbow Height
    #
    # ========================================================

    elbow_p50 = get_value(
        "Sitting Elbow Height",
        "P50"
    )

    writing_tablet_height = (
        elbow_p50
    )

    # ========================================================
    # RETURN DESIGN VALUES
    # ========================================================

    return {

        "Popliteal P5":
            popliteal_p5,

        "Seat Height":
            seat_height,

        "BPL P5":
            bpl_p5,

        "Seat Depth":
            seat_depth,

        "Hip Breadth P95":
            hip_p95,

        "Seat Width Min":
            seat_width_min,

        "Seat Width Max":
            seat_width_max,

        "Shoulder Height P50":
            shoulder_p50,

        "Backrest Height":
            backrest_height,

        "Elbow Height P50":
            elbow_p50,

        "Writing Tablet Height":
            writing_tablet_height
    }


# ============================================================
# CHAIR DESIGN DISPLAY FUNCTION
# ============================================================

def show_chair_design(
    stats,
    gender
):

    design = calculate_chair_design(
        stats
    )

    st.title(
        f"🪑 {gender} Classroom Chair Design"
    )

    st.markdown(
        f"""
        The following preliminary dimensions are calculated from
        the **{gender.lower()} anthropometric dataset** using
        percentile-based ergonomic design rules.

        The proposed classroom chair includes an **integrated
        hinged writing tablet**, therefore Sitting Elbow Height
        is treated as a primary design parameter.
        """
    )

    st.divider()

    # ========================================================
    # 1. SEAT HEIGHT
    # ========================================================

    st.subheader(
        "1️⃣ Seat Height"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "P5 Popliteal Height",
            f"{design['Popliteal P5']:.2f} cm"
        )

    with col2:

        st.metric(
            "Adjustment",
            "- 2.00 cm"
        )

    with col3:

        st.metric(
            "Design Seat Height",
            f"{design['Seat Height']:.2f} cm"
        )

    st.code(
        "Seat Height = P5 Popliteal Height − 2 cm"
    )

    st.caption(
        f"Preliminary dimension: "
        f"{design['Seat Height']:.2f} cm "
        f"({design['Seat Height'] * 10:.0f} mm)"
    )

    st.divider()

    # ========================================================
    # 2. SEAT DEPTH
    # ========================================================

    st.subheader(
        "2️⃣ Seat Depth"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "P5 Buttock-Popliteal Length",
            f"{design['BPL P5']:.2f} cm"
        )

    with col2:

        st.metric(
            "Clearance",
            "- 3.00 cm"
        )

    with col3:

        st.metric(
            "Design Seat Depth",
            f"{design['Seat Depth']:.2f} cm"
        )

    st.code(
        "Seat Depth = P5 Buttock-Popliteal Length − 3 cm"
    )

    st.caption(
        f"Preliminary dimension: "
        f"{design['Seat Depth']:.2f} cm "
        f"({design['Seat Depth'] * 10:.0f} mm)"
    )

    st.divider()

    # ========================================================
    # 3. SEAT WIDTH
    # ========================================================

    st.subheader(
        "3️⃣ Seat Width"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "P95 Hip Breadth",
            f"{design['Hip Breadth P95']:.2f} cm"
        )

    with col2:

        st.metric(
            "Clearance",
            "+ 2–3 cm"
        )

    with col3:

        st.metric(
            "Design Seat Width",
            f"{design['Seat Width Min']:.2f}–"
            f"{design['Seat Width Max']:.2f} cm"
        )

    st.code(
        "Seat Width = P95 Hip Breadth + 2–3 cm"
    )

    st.caption(
        f"Recommended preliminary range: "
        f"{design['Seat Width Min']:.2f}–"
        f"{design['Seat Width Max']:.2f} cm "
        f"({design['Seat Width Min'] * 10:.0f}–"
        f"{design['Seat Width Max'] * 10:.0f} mm)"
    )

    st.divider()

    # ========================================================
    # 4. BACKREST HEIGHT
    # ========================================================

    st.subheader(
        "4️⃣ Backrest Height"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "P50 Sitting Shoulder Height",
            f"{design['Shoulder Height P50']:.2f} cm"
        )

    with col2:

        st.metric(
            "Design Backrest Height",
            f"{design['Backrest Height']:.2f} cm"
        )

    st.code(
        "Backrest Height = P50 Sitting Shoulder Height"
    )

    st.caption(
        f"Preliminary dimension: "
        f"{design['Backrest Height']:.2f} cm "
        f"({design['Backrest Height'] * 10:.0f} mm)"
    )

    st.divider()

    # ========================================================
    # 5. HINGED WRITING TABLET HEIGHT
    # ========================================================

    st.subheader(
        "5️⃣ Hinged Writing Tablet Height"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "P50 Sitting Elbow Height",
            f"{design['Elbow Height P50']:.2f} cm"
        )

    with col2:

        st.metric(
            "Design Basis",
            "P50"
        )

    with col3:

        st.metric(
            "Writing Tablet Height",
            f"{design['Writing Tablet Height']:.2f} cm"
        )

    st.code(
        "Writing Tablet Height = P50 Sitting Elbow Height"
    )

    st.caption(
        f"Preliminary tablet height: "
        f"{design['Writing Tablet Height']:.2f} cm "
        f"({design['Writing Tablet Height'] * 10:.0f} mm)"
    )

    st.info(
        """
        **Hinged Writing Tablet Design**

        The writing tablet is considered an integrated component
        of the classroom chair. Sitting Elbow Height is therefore
        included as a primary anthropometric input rather than
        an additional consideration.

        The tablet is intended to provide a suitable writing
        surface for seated users while maintaining the hinged
        functionality required for classroom use.

        The tablet position, thickness, width, depth, hinge
        mechanism and structural support should be validated
        during CAD modelling and prototype testing.
        """
    )

    st.divider()

    # ========================================================
    # DESIGN SUMMARY
    # ========================================================

    st.subheader(
        "📋 Preliminary Chair + Writing Tablet Design Summary"
    )

    summary = pd.DataFrame({

        "Design Parameter": [

            "Seat Height",

            "Seat Depth",

            "Seat Width",

            "Backrest Height",

            "Writing Tablet Height"
        ],

        "Dimension (cm)": [

            f"{design['Seat Height']:.2f}",

            f"{design['Seat Depth']:.2f}",

            f"{design['Seat Width Min']:.2f}–"
            f"{design['Seat Width Max']:.2f}",

            f"{design['Backrest Height']:.2f}",

            f"{design['Writing Tablet Height']:.2f}"
        ],

        "Dimension (mm)": [

            f"{design['Seat Height'] * 10:.0f}",

            f"{design['Seat Depth'] * 10:.0f}",

            f"{design['Seat Width Min'] * 10:.0f}–"
            f"{design['Seat Width Max'] * 10:.0f}",

            f"{design['Backrest Height'] * 10:.0f}",

            f"{design['Writing Tablet Height'] * 10:.0f}"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "All dimensions are preliminary anthropometric design "
        "values and require CAD-based and practical ergonomic validation."
    )

    st.divider()

    # ========================================================
    # ADDITIONAL ANTHROPOMETRIC CONSIDERATIONS
    # ========================================================

    st.subheader(
        "📐 Additional Anthropometric Considerations"
    )

    additional = pd.DataFrame({

        "Measurement": [

            "Sitting Knee Height",

            "Thigh Clearance",

            "Buttock-Knee Length",

            "Foot Length"
        ],

        "Purpose": [

            "Knee and lower-leg clearance",

            "Clearance between thigh and underside of seat structure",

            "Leg-space and forward clearance validation",

            "Foot placement and floor contact"
        ]
    })

    st.dataframe(
        additional,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        """
        **Design Note**

        The current chair concept includes an integrated hinged
        writing tablet. Therefore, Sitting Elbow Height is treated
        as a primary design measurement and is used to determine
        the preliminary writing tablet height.

        The remaining anthropometric variables are used for
        dimensional validation and ergonomic assessment rather
        than as the primary dimensions in the current design.
        """
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title(
    "🪑 Ergonomic Chair Design"
)

st.sidebar.markdown(
    """
    **Anthropometric Data Analysis**

    Gender-Specific Classroom Chair
    with Integrated Hinged Writing Tablet
    """
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Descriptive Statistics",
        "Percentile Analysis",
        "Male vs Female",
        "Male Chair Design",
        "Female Chair Design",
        "Final Design Summary"
    ]
)


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "Overview":

    st.title(
        "🪑 Anthropometric-Based Ergonomic Classroom Chair Design"
    )

    st.markdown(
        """
        ### Project Overview

        This project analyzes anthropometric measurements of male
        and female participants to develop **gender-specific
        ergonomic classroom chair dimensions**.

        The proposed chair incorporates an **integrated hinged
        writing tablet**, allowing the user to use the chair as
        a classroom workstation.

        Python is used as the analytical engine, while Streamlit
        provides an interactive data-analysis and engineering
        decision-support interface.
        """
    )

    st.divider()

    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Male Participants",
            len(male_df)
        )

    with col2:

        st.metric(
            "Female Participants",
            len(female_df)
        )

    with col3:

        st.metric(
            "Total Participants",
            len(male_df) + len(female_df)
        )

    with col4:

        st.metric(
            "Anthropometric Variables",
            len(MEASUREMENTS)
        )

    st.divider()

    # ========================================================
    # PRIMARY DESIGN PARAMETERS
    # ========================================================

    st.subheader(
        "🪑 Primary Design Parameters"
    )

    primary_design_table = pd.DataFrame({

        "Design Parameter": [

            "Seat Height",

            "Seat Depth",

            "Seat Width",

            "Backrest Height",

            "Writing Tablet Height"
        ],

        "Anthropometric Input": [

            "Popliteal Height",

            "Buttock-Popliteal Length",

            "Hip Breadth",

            "Sitting Shoulder Height",

            "Sitting Elbow Height"
        ],

        "Percentile": [

            "P5",

            "P5",

            "P95",

            "P50",

            "P50"
        ],

        "Design Rule": [

            "P5 − 2 cm",

            "P5 − 3 cm",

            "P95 + 2–3 cm",

            "P50",

            "P50"
        ]
    })

    st.dataframe(
        primary_design_table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # ANTHROPOMETRIC MEASUREMENTS
    # ========================================================

    st.subheader(
        "Anthropometric Measurements"
    )

    measurement_table = pd.DataFrame({

        "Variable": [

            DISPLAY_NAMES[col]
            for col in MEASUREMENTS
        ],

        "Unit":
            ["cm"] * len(MEASUREMENTS),

        "Application": [

            "Primary — Seat Height",

            "Primary — Seat Depth",

            "Primary — Seat Width",

            "Primary — Backrest Height",

            "Knee and lower-leg clearance",

            "Under-seat / thigh clearance",

            "Leg-space validation",

            "Foot placement",

            "Primary — Writing Tablet Height"
        ]
    })

    st.dataframe(
        measurement_table,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# PAGE 2 — DESCRIPTIVE STATISTICS
# ============================================================

elif page == "Descriptive Statistics":

    st.title(
        "📊 Descriptive Statistics"
    )

    st.write(
        "Statistical summary of the collected anthropometric "
        "measurements for the selected gender group."
    )

    # --------------------------------------------------------
    # GROUP SELECTION
    # --------------------------------------------------------

    gender = st.selectbox(
        "Select Group",
        ["Male", "Female"],
        key="descriptive_gender"
    )

    if gender == "Male":

        stats = male_stats
        selected_df = male_df

    else:

        stats = female_stats
        selected_df = female_df

    # --------------------------------------------------------
    # STATISTICAL SUMMARY
    # --------------------------------------------------------

    st.subheader(
        f"{gender} Anthropometric Statistics"
    )

    st.dataframe(
        stats.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "All anthropometric dimensions are reported in centimeters (cm)."
    )

    # --------------------------------------------------------
    # DESIGN-CRITICAL PARAMETERS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🪑 Design-Critical Anthropometric Parameters"
    )

    critical_measurements = [

        "POPLITEAL_HEIGHTCM",

        "BUTTOCK_POPLITEAL_HIGHTCM",

        "HIP_BREADTHCM",

        "SITTING_SHOULDER_HEIGHTCM",

        "SITTING_ELBOW_HEIGHTCM"
    ]

    critical_rows = []

    for measurement in critical_measurements:

        # Find corresponding row in statistics table
        matching_rows = stats[
            stats["Measurement"]
            == DISPLAY_NAMES[measurement]
        ]

        if not matching_rows.empty:

            row = matching_rows.iloc[0]

            critical_rows.append({

                "Measurement":
                    DISPLAY_NAMES[measurement],

                "P5 (cm)":
                    row["P5"],

                "P50 (cm)":
                    row["P50"],

                "P95 (cm)":
                    row["P95"]
            })

    if critical_rows:

        critical_stats = pd.DataFrame(
            critical_rows
        )

        st.dataframe(
            critical_stats.round(2),
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # DESIGN APPLICATION
    # --------------------------------------------------------

    st.info(
        """
        **Primary Preliminary Design Application**

        • **Popliteal Height** → Seat Height  
        • **Buttock-Popliteal Length** → Seat Depth  
        • **Hip Breadth** → Seat Width  
        • **Sitting Shoulder Height** → Backrest Height  
        • **Sitting Elbow Height** → Hinged Writing Tablet Height
        """
    )

    # --------------------------------------------------------
    # DISTRIBUTION ANALYSIS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📦 Distribution Analysis"
    )

    selected_measurement = st.selectbox(

        "Select Measurement",

        MEASUREMENTS,

        format_func=lambda x:
            DISPLAY_NAMES[x],

        key="descriptive_measurement"
    )

    # --------------------------------------------------------
    # PREPARE DATA
    # --------------------------------------------------------

    # Make sure selected column exists
    if selected_measurement not in selected_df.columns:

        st.error(
            f"Measurement column "
            f"'{selected_measurement}' "
            f"was not found in the selected dataset."
        )

    else:

        plot_data = selected_df[
            [selected_measurement]
        ].copy()

        plot_data = plot_data.rename(
            columns={
                selected_measurement:
                    DISPLAY_NAMES[selected_measurement]
            }
        )

        # Remove missing/non-numeric values
        plot_data[
            DISPLAY_NAMES[selected_measurement]
        ] = pd.to_numeric(
            plot_data[
                DISPLAY_NAMES[selected_measurement]
            ],
            errors="coerce"
        )

        plot_data = plot_data.dropna()

        # ----------------------------------------------------
        # BOX PLOT
        # ----------------------------------------------------

        if not plot_data.empty:

            # Import Plotly locally so the rest of the app
            # remains unaffected if this page is not selected.
            try:

                import plotly.express as px

                measurement_name = DISPLAY_NAMES[
                    selected_measurement
                ]

                fig = px.box(
                    plot_data,
                    y=measurement_name,
                    points="outliers",
                    title=(
                        f"{measurement_name} Distribution — "
                        f"{gender}"
                    )
                )

                fig.update_layout(
                    yaxis_title="Measurement (cm)",
                    xaxis_title="",
                    height=450
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            except ImportError:

                st.warning(
                    "Plotly is not installed. "
                    "Please install it using: "
                    "`py -m pip install plotly`"
                )

            # ------------------------------------------------
            # DISTRIBUTION INTERPRETATION
            # ------------------------------------------------

            st.caption(
                f"Box plot showing the distribution, median, "
                f"quartiles, and potential outliers of "
                f"{DISPLAY_NAMES[selected_measurement]} "
                f"for {gender} participants."
            )

        else:

            st.warning(
                "No valid numerical observations are available "
                "for the selected measurement."
            )

    # --------------------------------------------------------
    # SELECTED MEASUREMENT QUICK STATISTICS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📌 Selected Measurement Summary"
    )

    selected_stat_rows = stats[
        stats["Measurement"]
        == DISPLAY_NAMES[selected_measurement]
    ]

    if not selected_stat_rows.empty:

        selected_row = selected_stat_rows.iloc[0]

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            st.metric(
                "Minimum",
                f"{selected_row['Min']:.2f} cm"
            )

        with col2:

            st.metric(
                "P5",
                f"{selected_row['P5']:.2f} cm"
            )

        with col3:

            st.metric(
                "Median",
                f"{selected_row['P50']:.2f} cm"
            )

        with col4:

            st.metric(
                "P95",
                f"{selected_row['P95']:.2f} cm"
            )

        with col5:

            st.metric(
                "Maximum",
                f"{selected_row['Max']:.2f} cm"
            )

    # --------------------------------------------------------
    # ENGINEERING INTERPRETATION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔧 Engineering Interpretation"
    )

    measurement_application = {

        "POPLITEAL_HEIGHTCM":
            "Used primarily for determining seat height. "
            "A lower percentile is considered to accommodate "
            "shorter users.",

        "BUTTOCK_POPLITEAL_HIGHTCM":
            "Used for determining seat depth. "
            "A lower percentile helps reduce excessive "
            "seat-depth interference for shorter users.",

        "HIP_BREADTHCM":
            "Used for determining seat width. "
            "A high percentile is considered to provide "
            "adequate lateral accommodation.",

        "SITTING_SHOULDER_HEIGHTCM":
            "Used as a reference for backrest height "
            "and upper-body support.",

        "SITTING_ELBOW_HEIGHTCM":
            "Used as the primary anthropometric reference "
            "for the height of the hinged writing tablet.",

        "SITTING_KNEE_HEIGHTCM":
            "Provides a reference for knee clearance "
            "and under-desk/under-table spatial requirements.",

        "TIGH_CLEARENCECM":
            "Provides a reference for vertical thigh clearance "
            "between the seat and writing-table structure.",

        "BUTTOCK_KNEE_LENGTHCM":
            "Provides additional information for lower-limb "
            "clearance and overall chair geometry.",

        "FOOT_LENGTHCM":
            "Provides a reference for foot placement "
            "and lower-limb support."
    }

    if selected_measurement in measurement_application:

        st.write(
            measurement_application[
                selected_measurement
            ]
        )

    # --------------------------------------------------------
    # PRELIMINARY DESIGN EMPHASIS
    # --------------------------------------------------------

    if selected_measurement == "SITTING_ELBOW_HEIGHTCM":

        st.success(
            """
            **Writing Tablet Design Focus**

            Sitting Elbow Height is a primary design parameter
            in this chair because the chair incorporates a
            hinged writing tablet.

            The preliminary writing-tablet height is based on
            the **P50 (median) Sitting Elbow Height** of the
            selected gender group.

            Final CAD validation should additionally consider
            tablet thickness, hinge position, writing angle,
            elbow/forearm clearance, and the relationship
            between the tablet and the seat surface.
            """
        )

    elif selected_measurement == "POPLITEAL_HEIGHTCM":

        st.success(
            """
            **Seat Height Design Focus**

            Popliteal Height is the primary anthropometric
            reference for preliminary seat-height design.
            The current design methodology uses the P5 value
            with an allowance for footwear/postural clearance.
            """
        )

    elif selected_measurement == "BUTTOCK_POPLITEAL_HIGHTCM":

        st.success(
            """
            **Seat Depth Design Focus**

            Buttock-Popliteal Length is used as the primary
            anthropometric reference for preliminary seat-depth
            design.
            """
        )

    elif selected_measurement == "HIP_BREADTHCM":

        st.success(
            """
            **Seat Width Design Focus**

            Hip Breadth is used as the primary anthropometric
            reference for preliminary seat-width design.
            The high percentile is considered to accommodate
            a wider range of users.
            """
        )

    elif selected_measurement == "SITTING_SHOULDER_HEIGHTCM":

        st.success(
            """
            **Backrest Design Focus**

            Sitting Shoulder Height provides the primary
            anthropometric reference for preliminary backrest
            height.
            """
        )    

# ============================================================
# PAGE 3 — PERCENTILE ANALYSIS
# ============================================================

elif page == "Percentile Analysis":

    st.title(
        "📐 Percentile Analysis"
    )

    st.write(
        "Percentile analysis shows the distribution of "
        "anthropometric measurements and identifies the body "
        "dimensions used for ergonomic chair and writing-tablet design."
    )

    # --------------------------------------------------------
    # GROUP SELECTION
    # --------------------------------------------------------

    gender = st.selectbox(
        "Select Group",
        ["Male", "Female"],
        key="percentile_gender"
    )

    if gender == "Male":

        stats = male_stats

    else:

        stats = female_stats

    # --------------------------------------------------------
    # MEASUREMENT SELECTION
    # --------------------------------------------------------

    selected_measurement = st.selectbox(

        "Select Anthropometric Measurement",

        MEASUREMENTS,

        format_func=lambda x:
            DISPLAY_NAMES.get(x, x),

        key="percentile_measurement"
    )

    # --------------------------------------------------------
    # FIND SELECTED MEASUREMENT
    # --------------------------------------------------------

    selected_rows = stats[
        stats["Measurement"]
        == DISPLAY_NAMES[
            selected_measurement
        ]
    ]

    if not selected_rows.empty:

        row = selected_rows.iloc[0]

        measurement_name = (
            DISPLAY_NAMES[
                selected_measurement
            ]
        )

        # ----------------------------------------------------
        # SELECTED MEASUREMENT
        # ----------------------------------------------------

        st.subheader(
            f"📊 {measurement_name}"
        )

        # ----------------------------------------------------
        # PERCENTILE VALUES
        # ----------------------------------------------------

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            st.metric(
                "P5",
                f"{row['P5']:.2f} cm"
            )

        with col2:

            st.metric(
                "P25",
                f"{row['P25']:.2f} cm"
            )

        with col3:

            st.metric(
                "P50",
                f"{row['P50']:.2f} cm"
            )

        with col4:

            st.metric(
                "P75",
                f"{row['P75']:.2f} cm"
            )

        with col5:

            st.metric(
                "P95",
                f"{row['P95']:.2f} cm"
            )

        # ----------------------------------------------------
        # PERCENTILE TABLE
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📋 Percentile Summary"
        )

        percentile_table = pd.DataFrame({

            "Percentile": [

                "P5",
                "P25",
                "P50",
                "P75",
                "P95"
            ],

            "Value (cm)": [

                row["P5"],
                row["P25"],
                row["P50"],
                row["P75"],
                row["P95"]
            ]
        })

        st.dataframe(
            percentile_table.round(2),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # PERCENTILE PROFILE
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📈 Percentile Profile"
        )

        chart_data = pd.DataFrame({

            "Percentile": [

                "P5",
                "P25",
                "P50",
                "P75",
                "P95"
            ],

            "Value (cm)": [

                row["P5"],
                row["P25"],
                row["P50"],
                row["P75"],
                row["P95"]
            ]
        })

        st.line_chart(
            chart_data.set_index(
                "Percentile"
            )
        )

        st.caption(
            f"Percentile distribution of "
            f"{measurement_name} for "
            f"{gender} participants."
        )

        # ----------------------------------------------------
        # ENGINEERING APPLICATION
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "🪑 Engineering Application"
        )

        design_application = {

            "POPLITEAL_HEIGHTCM":
                (
                    "Seat Height",
                    "P5"
                ),

            "BUTTOCK_POPLITEAL_HIGHTCM":
                (
                    "Seat Depth",
                    "P5"
                ),

            "HIP_BREADTHCM":
                (
                    "Seat Width",
                    "P95"
                ),

            "SITTING_SHOULDER_HEIGHTCM":
                (
                    "Backrest Height",
                    "P50"
                ),

            "SITTING_ELBOW_HEIGHTCM":
                (
                    "Hinged Writing Tablet Height",
                    "P50"
                )
        }

        if selected_measurement in design_application:

            design_parameter, percentile_used = (
                design_application[
                    selected_measurement
                ]
            )

            st.success(
                f"""
                **Design Parameter:** {design_parameter}

                **Design Percentile:** {percentile_used}

                **Selected Group:** {gender}

                The selected anthropometric measurement is used
                as a primary input for the preliminary ergonomic
                chair and writing-tablet design.
                """
            )

        else:

            st.info(
                """
                This measurement is included for anthropometric
                analysis and dimensional validation but is not
                directly used as a primary chair-dimension parameter.
                """
            )

    else:

        st.warning(
            "Selected measurement was not found in the statistics table."
        )


# ============================================================
# PAGE 4 — MALE VS FEMALE
# ============================================================

elif page == "Male vs Female":

    st.title(
        "⚖️ Male vs Female Comparison"
    )

    st.write(
        "Comparison of anthropometric measurements between "
        "male and female participants."
    )

    # --------------------------------------------------------
    # COMPARISON TABLE
    # --------------------------------------------------------

    comparison = pd.DataFrame({

        "Measurement":
            male_stats["Measurement"],

        "Male Mean":
            male_stats["Mean"],

        "Female Mean":
            female_stats["Mean"],

        "Male P5":
            male_stats["P5"],

        "Female P5":
            female_stats["P5"],

        "Male P50":
            male_stats["P50"],

        "Female P50":
            female_stats["P50"],

        "Male P95":
            male_stats["P95"],

        "Female P95":
            female_stats["P95"]
    })

    st.subheader(
        "📋 Anthropometric Comparison"
    )

    st.dataframe(
        comparison.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "All dimensions are reported in centimeters (cm)."
    )

    # --------------------------------------------------------
    # MEASUREMENT SELECTION
    # --------------------------------------------------------

    st.divider()

    measurement = st.selectbox(

        "Select Measurement",

        comparison[
            "Measurement"
        ].tolist(),

        key="comparison_measurement"
    )

    selected = comparison[
        comparison["Measurement"]
        == measurement
    ].iloc[0]

    # --------------------------------------------------------
    # MEAN COMPARISON
    # --------------------------------------------------------

    st.subheader(
        f"📊 Mean Comparison — {measurement}"
    )

    mean_chart = pd.DataFrame({

        "Group": [

            "Male",
            "Female"
        ],

        "Mean": [

            selected["Male Mean"],
            selected["Female Mean"]
        ]
    })

    st.bar_chart(
        mean_chart.set_index(
            "Group"
        )
    )

    # --------------------------------------------------------
    # PERCENTILE COMPARISON
    # --------------------------------------------------------

    st.subheader(
        f"📈 Percentile Comparison — {measurement}"
    )

    percentile_chart = pd.DataFrame({

        "Percentile": [

            "P5",
            "P50",
            "P95"
        ],

        "Male": [

            selected["Male P5"],
            selected["Male P50"],
            selected["Male P95"]
        ],

        "Female": [

            selected["Female P5"],
            selected["Female P50"],
            selected["Female P95"]
        ]
    })

    st.line_chart(
        percentile_chart.set_index(
            "Percentile"
        )
    )

    # --------------------------------------------------------
    # DESIGN APPLICATION
    # --------------------------------------------------------

    st.divider()

    design_application = {

        "Popliteal Height":
            (
                "Seat Height",
                "P5"
            ),

        "Buttock-Popliteal Length":
            (
                "Seat Depth",
                "P5"
            ),

        "Hip Breadth":
            (
                "Seat Width",
                "P95"
            ),

        "Sitting Shoulder Height":
            (
                "Backrest Height",
                "P50"
            ),

        "Sitting Elbow Height":
            (
                "Hinged Writing Tablet Height",
                "P50"
            )
    }

    if measurement in design_application:

        design_parameter, percentile_used = (
            design_application[
                measurement
            ]
        )

        st.info(
            f"""
            **Design Application**

            Anthropometric Measurement: **{measurement}**

            Design Parameter: **{design_parameter}**

            Design Percentile: **{percentile_used}**

            This measurement is directly used in the
            preliminary ergonomic design.
            """
        )

    else:

        st.info(
            """
            This measurement is included in the anthropometric
            comparison but is not directly used as a primary
            design dimension.
            """
        )


# ============================================================
# PAGE 5 — MALE CHAIR DESIGN
# ============================================================

elif page == "Male Chair Design":

    show_chair_design(
        male_stats,
        "Male"
    )


# ============================================================
# PAGE 6 — FEMALE CHAIR DESIGN
# ============================================================

elif page == "Female Chair Design":

    show_chair_design(
        female_stats,
        "Female"
    )


# ============================================================
# PAGE 7 — FINAL DESIGN SUMMARY
# ============================================================

elif page == "Final Design Summary":

    st.title(
        "📋 Final Chair + Hinged Writing Tablet Design Summary"
    )

    st.markdown(
        """
        This page presents the **final preliminary dimensions**
        of the male and female classroom chair designs derived
        from the collected anthropometric data.

        The proposed design includes an **integrated hinged
        writing tablet**, for which Sitting Elbow Height is
        treated as a primary anthropometric design parameter.
        """
    )

    # ========================================================
    # CALCULATE DESIGN
    # ========================================================

    male_design = calculate_chair_design(
        male_stats
    )

    female_design = calculate_chair_design(
        female_stats
    )

    # ========================================================
    # KEY DESIGN DIMENSIONS
    # ========================================================

    st.subheader(
        "🪑 Final Preliminary Chair Dimensions"
    )

    summary = pd.DataFrame({

        "Design Parameter": [

            "Seat Height",

            "Seat Depth",

            "Seat Width",

            "Backrest Height",

            "Writing Tablet Height"
        ],

        "Male Chair (cm)": [

            f"{male_design['Seat Height']:.2f}",

            f"{male_design['Seat Depth']:.2f}",

            f"{male_design['Seat Width Min']:.2f}–"
            f"{male_design['Seat Width Max']:.2f}",

            f"{male_design['Backrest Height']:.2f}",

            f"{male_design['Writing Tablet Height']:.2f}"
        ],

        "Male Chair (mm)": [

            f"{male_design['Seat Height'] * 10:.0f}",

            f"{male_design['Seat Depth'] * 10:.0f}",

            f"{male_design['Seat Width Min'] * 10:.0f}–"
            f"{male_design['Seat Width Max'] * 10:.0f}",

            f"{male_design['Backrest Height'] * 10:.0f}",

            f"{male_design['Writing Tablet Height'] * 10:.0f}"
        ],

        "Female Chair (cm)": [

            f"{female_design['Seat Height']:.2f}",

            f"{female_design['Seat Depth']:.2f}",

            f"{female_design['Seat Width Min']:.2f}–"
            f"{female_design['Seat Width Max']:.2f}",

            f"{female_design['Backrest Height']:.2f}",

            f"{female_design['Writing Tablet Height']:.2f}"
        ],

        "Female Chair (mm)": [

            f"{female_design['Seat Height'] * 10:.0f}",

            f"{female_design['Seat Depth'] * 10:.0f}",

            f"{female_design['Seat Width Min'] * 10:.0f}–"
            f"{female_design['Seat Width Max'] * 10:.0f}",

            f"{female_design['Backrest Height'] * 10:.0f}",

            f"{female_design['Writing Tablet Height'] * 10:.0f}"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # DESIGN BASIS
    # ========================================================

    st.subheader(
        "📐 Anthropometric Design Basis"
    )

    design_basis = pd.DataFrame({

        "Chair / Tablet Dimension": [

            "Seat Height",

            "Seat Depth",

            "Seat Width",

            "Backrest Height",

            "Writing Tablet Height"
        ],

        "Anthropometric Parameter": [

            "Popliteal Height",

            "Buttock-Popliteal Length",

            "Hip Breadth",

            "Sitting Shoulder Height",

            "Sitting Elbow Height"
        ],

        "Percentile Used": [

            "P5",

            "P5",

            "P95",

            "P50",

            "P50"
        ],

        "Design Rule": [

            "P5 − 2 cm",

            "P5 − 3 cm",

            "P95 + 2–3 cm",

            "P50",

            "P50"
        ]
    })

    st.dataframe(
        design_basis,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # MALE vs FEMALE DESIGN COMPARISON
    # ========================================================

    st.subheader(
        "⚖️ Male vs Female Design Comparison"
    )

    comparison = pd.DataFrame({

        "Dimension": [

            "Seat Height",

            "Seat Depth",

            "Seat Width",

            "Backrest Height",

            "Writing Tablet Height"
        ],

        "Male (cm)": [

            male_design["Seat Height"],

            male_design["Seat Depth"],

            male_design["Seat Width Min"],

            male_design["Backrest Height"],

            male_design["Writing Tablet Height"]
        ],

        "Female (cm)": [

            female_design["Seat Height"],

            female_design["Seat Depth"],

            female_design["Seat Width Min"],

            female_design["Backrest Height"],

            female_design["Writing Tablet Height"]
        ]
    })

    st.bar_chart(
        comparison.set_index(
            "Dimension"
        )
    )

    st.caption(
        "For Seat Width, the lower value of the recommended "
        "2–3 cm clearance range is shown in the comparison chart."
    )

    st.divider()

    # ========================================================
    # DESIGN INTERPRETATION
    # ========================================================

    st.subheader(
        "🔍 Design Interpretation"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            ### 👨 Male Chair

            **Seat Height:**  
            {male_design['Seat Height']:.2f} cm

            **Seat Depth:**  
            {male_design['Seat Depth']:.2f} cm

            **Seat Width:**  
            {male_design['Seat Width Min']:.2f}–{male_design['Seat Width Max']:.2f} cm

            **Backrest Height:**  
            {male_design['Backrest Height']:.2f} cm

            **Writing Tablet Height:**  
            {male_design['Writing Tablet Height']:.2f} cm
            """
        )

    with col2:

        st.markdown(
            f"""
            ### 👩 Female Chair

            **Seat Height:**  
            {female_design['Seat Height']:.2f} cm

            **Seat Depth:**  
            {female_design['Seat Depth']:.2f} cm

            **Seat Width:**  
            {female_design['Seat Width Min']:.2f}–{female_design['Seat Width Max']:.2f} cm

            **Backrest Height:**  
            {female_design['Backrest Height']:.2f} cm

            **Writing Tablet Height:**  
            {female_design['Writing Tablet Height']:.2f} cm
            """
        )

    st.divider()

    # ========================================================
    # ADDITIONAL DESIGN CONSIDERATIONS
    # ========================================================

    st.subheader(
        "📌 Additional Anthropometric Considerations"
    )

    considerations = pd.DataFrame({

        "Anthropometric Parameter": [

            "Sitting Knee Height",

            "Thigh Clearance",

            "Buttock-Knee Length",

            "Foot Length"
        ],

        "Design Consideration": [

            "Knee and lower-leg clearance",

            "Clearance between thigh and underside of seat structure",

            "Leg-space and forward clearance",

            "Foot placement and floor contact"
        ]
    })

    st.dataframe(
        considerations,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # WRITING TABLET DESIGN CONSIDERATIONS
    # ========================================================

    st.subheader(
        "📝 Hinged Writing Tablet — Design Considerations"
    )

    tablet_considerations = pd.DataFrame({

        "Parameter": [

            "Primary Anthropometric Input",

            "Height Reference",

            "Tablet Function",

            "Hinge Mechanism",

            "Structural Support",

            "CAD Validation"
        ],

        "Design Basis": [

            "Sitting Elbow Height",

            "P50 Sitting Elbow Height",

            "Seated writing / classroom work",

            "Hinged / foldable mechanism",

            "Load-bearing support under writing surface",

            "Required before final fabrication"
        ]
    })

    st.dataframe(
        tablet_considerations,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # FINAL DESIGN NOTE
    # ========================================================

    st.info(
        """
        ### 📝 Final Design Note

        The dimensions presented on this page are **preliminary
        anthropometric design dimensions** calculated from the
        collected male and female datasets using percentile-based
        design rules.

        The proposed classroom chair includes an **integrated
        hinged writing tablet**. Therefore, Sitting Elbow Height
        is treated as a primary design measurement and is used
        to determine the preliminary writing tablet height.

        Before final manufacturing, the proposed dimensions should
        be evaluated through **technical drawing, CAD modelling,
        prototype development and ergonomic validation**.

        Additional engineering factors such as writing-tablet
        thickness, tablet width and depth, hinge location,
        opening angle, structural strength, stability, seat-pan
        angle,
        backrest angle, material selection and classroom space
        should also be considered during final design.
        """
    )

