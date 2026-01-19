"""
Streamlit application for DORA (Data-Oriented Report Automator).
"""

import logging
import os
import shutil
import uuid
from pathlib import Path

import streamlit as st

from src.dora.data_loader import read_data
from src.dora.kaggle import KaggleHandler
from src.dora.profiling import generate_profile
from src.dora.plots import univariate, bivariate, multivariate
from src.dora.reporting.generator import create_report

logging.basicConfig(level=logging.INFO)


def init_session_state():
    """Initialize session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "df" not in st.session_state:
        st.session_state.df = None
    if "output_dir" not in st.session_state:
        # Create a unique output directory for this session
        base_output = Path("output") / st.session_state.session_id
        base_output.mkdir(parents=True, exist_ok=True)
        st.session_state.output_dir = base_output
    if "input_source" not in st.session_state:
        st.session_state.input_source = None


def setup_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="DORA | Data-Oriented Report Automator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("📊 DORA: Data-Oriented Report Automator")
    st.markdown(
        """
        Welcome to DORA! This tool automates the Exploratory Data Analysis (EDA) process.
        Upload a dataset or connect to Kaggle to get started.
        """
    )


def load_local_data(uploaded_file):
    """Handle loading of local file uploads."""
    # We need to save the uploaded file to a temporary path so read_data can read it
    temp_path = st.session_state.output_dir / uploaded_file.name
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Loading data..."):
            df = read_data(temp_path)
            st.session_state.df = df
            st.session_state.input_source = uploaded_file.name
            st.success(f"Successfully loaded '{uploaded_file.name}'")
    except Exception as e:
        st.error(f"Error loading file: {e}")


def load_kaggle_data(kaggle_input):
    """Handle loading of Kaggle datasets."""
    try:
        with st.spinner("Connecting to Kaggle..."):
            # Extract ID if it's a URL
            if KaggleHandler.is_kaggle_url(kaggle_input):
                dataset_id = KaggleHandler.extract_dataset_id(kaggle_input)
            else:
                dataset_id = kaggle_input

            st.text(f"Dataset ID: {dataset_id}")

            # Download using existing handler
            file_path = KaggleHandler.download_dataset(dataset_id)
            st.write(f"Downloaded to: {file_path}")

            # Load data
            df = read_data(file_path)
            st.session_state.df = df
            st.session_state.input_source = dataset_id
            st.success(f"Successfully loaded data from '{dataset_id}'")

    except Exception as e:
        st.error(f"Error processing Kaggle dataset: {e}")


def render_ingestion():
    """Render the data ingestion section (Local File & Kaggle Tabs)."""
    st.header("1. Data Ingestion")
    tab_local, tab_kaggle = st.tabs(["Local File", "Kaggle Dataset"])

    with tab_local:
        st.info("Upload a CSV, Excel, JSON, or Parquet file.")
        uploaded_file = st.file_uploader(
            "Choose a file", type=["csv", "xlsx", "xls", "json", "parquet"]
        )

        if uploaded_file is not None:
            # Button to trigger load
            if st.button("Load Local Data", key="btn_local"):
                load_local_data(uploaded_file)

    with tab_kaggle:
        st.info("Enter a Kaggle Dataset ID (e.g., `owner/dataset`) or full URL.")
        kaggle_input = st.text_input("Kaggle Dataset ID or URL")

        if st.button("Download & Load from Kaggle", key="btn_kaggle"):
            if kaggle_input:
                load_kaggle_data(kaggle_input)
            else:
                st.warning("Please enter a valid Dataset ID or URL.")


def render_preview():
    """Render the dataframe preview."""
    if st.session_state.df is not None:
        st.divider()
        st.subheader(f"Dataset Preview: {st.session_state.input_source}")
        st.write(
            f"**Shape:** {st.session_state.df.shape[0]} rows x {st.session_state.df.shape[1]} columns"
        )
        st.dataframe(st.session_state.df.head())


def render_sidebar():
    """Render the configuration sidebar."""
    if st.session_state.df is None:
        return None

    st.sidebar.header("2. Configuration")

    # Target Variable
    target_variable = st.sidebar.selectbox(
        "Target Variable (for Bivariate Analysis)",
        options=["None"] + list(st.session_state.df.columns),
        index=0,
    )
    if target_variable == "None":
        target_variable = None

    st.sidebar.subheader("Analysis Steps")
    config = {
        "target_variable": target_variable,
        "run_profile": st.sidebar.checkbox("Data Profile", value=True),
        "run_univariate": st.sidebar.checkbox("Univariate Analysis", value=True),
        "run_bivariate": st.sidebar.checkbox("Bivariate Analysis", value=True),
        "run_multivariate": st.sidebar.checkbox("Multivariate Analysis", value=True),
    }
    return config


def run_profile_step(df, current_report_data):
    """Run data profiling step."""
    try:
        profile_data = generate_profile(df)
        current_report_data["profile"] = profile_data
    except Exception as e:
        st.error(f"Error in Profiling: {e}")


def run_univariate_step(df, charts_dir, current_report_data):
    """Run univariate analysis step."""
    try:
        params = {
            "plot_types": {
                "numerical": ["histogram", "boxplot"],
                "categorical": ["barplot"],
            },
            "max_categories": 20,
        }
        plot_paths = univariate.generate_plots(df, charts_dir, params)
        current_report_data["univariate_plots"] = plot_paths
    except Exception as e:
        st.error(f"Error in Univariate Analysis: {e}")


def run_bivariate_step(df, config, charts_dir, current_report_data):
    """Run bivariate analysis step."""
    if not config["target_variable"]:
        st.warning("Skipping Bivariate Analysis: No Target Variable selected.")
        return

    try:
        params = {"target_centric": True, "max_categories": 20}
        plot_paths = bivariate.generate_plots(
            df,
            config["target_variable"],
            charts_dir,
            params,
        )
        current_report_data["bivariate_plots"] = plot_paths
    except Exception as e:
        st.error(f"Error in Bivariate Analysis: {e}")


def run_multivariate_step(df, charts_dir, current_report_data):
    """Run multivariate analysis step."""
    try:
        params = {"correlation_cols": []}
        plot_paths = multivariate.generate_plots(df, charts_dir, params)
        current_report_data["multivariate_plots"] = plot_paths
    except Exception as e:
        st.error(f"Error in Multivariate Analysis: {e}")


def generate_final_report(current_report_data):
    """Generate the HTML report and ZIP archive."""
    try:
        create_report(current_report_data, st.session_state.output_dir)

        # Create ZIP
        zip_base_name = (
            st.session_state.output_dir.parent
            / f"{st.session_state.session_id}_report"
        )
        shutil.make_archive(zip_base_name, "zip", st.session_state.output_dir)
        st.success(
            f"Analysis Complete! Report generated in {st.session_state.output_dir}"
        )
    except Exception as e:
        st.error(f"Error generating final report: {e}")


def execute_analysis(config):
    """Execute the analysis steps based on configuration."""
    with st.spinner("Running Analysis..."):
        # Reset output dir components
        charts_dir = st.session_state.output_dir / "charts"
        if charts_dir.exists():
            shutil.rmtree(charts_dir, ignore_errors=True)

        report_path = st.session_state.output_dir / "eda_report.html"
        if report_path.exists():
            try:
                os.remove(report_path)
            except OSError:
                pass

        st.session_state.output_dir.mkdir(parents=True, exist_ok=True)
        charts_dir.mkdir(exist_ok=True)

        current_report_data = {
            "title": f"EDA Report for {st.session_state.input_source}",
        }

        # Run configured steps
        if config["run_profile"]:
            run_profile_step(st.session_state.df, current_report_data)

        if config["run_univariate"]:
            run_univariate_step(st.session_state.df, charts_dir, current_report_data)

        if config["run_bivariate"]:
            run_bivariate_step(st.session_state.df, config, charts_dir, current_report_data)

        if config["run_multivariate"]:
            run_multivariate_step(st.session_state.df, charts_dir, current_report_data)

        # Update Session State
        st.session_state.report_data = current_report_data
        st.session_state.analysis_complete = True

        # Generate Physical Report Immediately
        generate_final_report(current_report_data)


def render_profile_tab(report_data):
    """Render the data profile content."""
    st.header("Data Profile")
    try:
        profile_data = report_data["profile"]
        col1, col2 = st.columns(2)
        col1.metric("Rows", profile_data["dataset_shape"][0])
        col2.metric("Columns", profile_data["dataset_shape"][1])

        st.subheader("Column Profiles")
        for col_prof in profile_data["column_profiles"]:
            with st.expander(f"{col_prof['name']} ({col_prof['type']})"):
                st.json(col_prof["stats"])
                if col_prof.get("sparkline_base64"):
                    st.markdown(
                        f'<img src="data:image/png;base64,{col_prof["sparkline_base64"]}" />',
                        unsafe_allow_html=True,
                    )

        if profile_data.get("missing_values_html"):
            st.subheader("Missing Values")
            st.markdown(
                profile_data["missing_values_html"], unsafe_allow_html=True
            )
    except Exception as e:  # pylint: disable=broad-exception-caught
        st.error(f"Error displaying profile: {e}")


def render_univariate_tab(report_data, charts_dir):
    """Render the univariate analysis content."""
    st.header("Univariate Analysis")
    plot_paths = report_data["univariate_plots"]
    if not plot_paths:
        st.info("No plots generated.")
    else:
        cols = st.columns(2)
        for i, path_str in enumerate(plot_paths):
            full_path = charts_dir / Path(path_str).name
            if full_path.exists():
                cols[i % 2].image(str(full_path), width="stretch")


def render_bivariate_tab(report_data, charts_dir):
    """Render the bivariate analysis content."""
    st.header("Bivariate Analysis")
    plot_paths = report_data["bivariate_plots"]
    if not plot_paths:
        st.info("No plots generated.")
    else:
        cols = st.columns(2)
        for i, path_str in enumerate(plot_paths):
            full_path = charts_dir / Path(path_str).name
            if full_path.exists():
                cols[i % 2].image(str(full_path), width="stretch")


def render_multivariate_tab(report_data, charts_dir):
    """Render the multivariate analysis content."""
    st.header("Multivariate Analysis")
    plot_paths = report_data["multivariate_plots"]
    for path_str in plot_paths:
        full_path = charts_dir / Path(path_str).name
        if full_path.exists():
            st.image(str(full_path), width="stretch")


def render_report_tabs():
    """Render the analysis results in tabs."""
    if not (st.session_state.analysis_complete and st.session_state.report_data):
        return

    charts_dir = st.session_state.output_dir / "charts"
    report_data = st.session_state.report_data

    tabs_list = []
    if "profile" in report_data:
        tabs_list.append("Profile")
    if "univariate_plots" in report_data:
        tabs_list.append("Univariate")
    if "bivariate_plots" in report_data:
        tabs_list.append("Bivariate")
    if "multivariate_plots" in report_data:
        tabs_list.append("Multivariate")

    if tabs_list:
        tabs = st.tabs(tabs_list)
        tab_idx = 0

        # Profile Render
        if "profile" in report_data:
            with tabs[tab_idx]:
                render_profile_tab(report_data)
            tab_idx += 1

        # Univariate Render
        if "univariate_plots" in report_data:
            with tabs[tab_idx]:
                render_univariate_tab(report_data, charts_dir)
            tab_idx += 1

        # Bivariate Render
        if "bivariate_plots" in report_data:
            with tabs[tab_idx]:
                render_bivariate_tab(report_data, charts_dir)
            tab_idx += 1

        # Multivariate Render
        if "multivariate_plots" in report_data:
            with tabs[tab_idx]:
                render_multivariate_tab(report_data, charts_dir)
            tab_idx += 1


def render_download_section():
    """Render the download button for the full report."""
    if not (st.session_state.analysis_complete and st.session_state.report_data):
        return

    st.divider()
    st.subheader("Download Report Data")
    zip_base_name = (
        st.session_state.output_dir.parent / f"{st.session_state.session_id}_report"
    )
    zip_path = zip_base_name.with_suffix(".zip")

    if zip_path.exists():
        with open(zip_path, "rb") as f:
            st.download_button(
                label="Download Full Report (ZIP)",
                data=f,
                file_name="dora_analysis.zip",
                mime="application/zip",
            )


def main():
    """Main function to run the Streamlit application."""
    setup_page()
    init_session_state()

    # Data Ingestion
    render_ingestion()

    # Data Preview
    render_preview()

    # Configuration & Analysis
    config = render_sidebar()

    # Visualization Layer (Main Area)
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "report_data" not in st.session_state:
        st.session_state.report_data = None

    if config:
        if st.button("Run Analysis", type="primary"):
            execute_analysis(config)

    # Render Results and Download
    render_report_tabs()
    render_download_section()

    # Placeholder for next steps
    if st.session_state.df is not None and not st.session_state.analysis_complete:
        st.info("Data loaded! Analysis configuration needed next.")


if __name__ == "__main__":
    main()
