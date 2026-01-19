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


def reset_analysis():
    """Reset the analysis state when new data is loaded."""
    st.session_state.df = None
    st.session_state.input_source = None
    # Clear previous outputs
    if st.session_state.output_dir.exists():
        shutil.rmtree(st.session_state.output_dir)
    st.session_state.output_dir.mkdir(parents=True, exist_ok=True)


def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="DORA | Data-Oriented Report Automator",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    st.title("📊 DORA: Data-Oriented Report Automator")
    st.markdown(
        """
        Welcome to DORA! This tool automates the Exploratory Data Analysis (EDA) process.
        Upload a dataset or connect to Kaggle to get started.
        """
    )

    # Data Ingestion Layer
    st.header("1. Data Ingestion")

    tab_local, tab_kaggle = st.tabs(["📁 Local File", "🌐 Kaggle Dataset"])

    with tab_local:
        st.info("Upload a CSV, Excel, JSON, or Parquet file.")
        uploaded_file = st.file_uploader(
            "Choose a file", type=["csv", "xlsx", "xls", "json", "parquet"]
        )

        if uploaded_file is not None:
            # We need to save the uploaded file to a temporary path so read_data can read it
            # or modify read_data to accept file-like objects (but read_data takes a Path).
            # For reuse, we'll save it to the session output dir.
            temp_path = st.session_state.output_dir / uploaded_file.name

            # Button to trigger load
            if st.button("Load Local Data", key="btn_local"):
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

    with tab_kaggle:
        st.info("Enter a Kaggle Dataset ID (e.g., `owner/dataset`) or full URL.")
        kaggle_input = st.text_input("Kaggle Dataset ID or URL")

        if st.button("Download & Load from Kaggle", key="btn_kaggle"):
            if kaggle_input:
                try:
                    with st.spinner("Connecting to Kaggle..."):
                        # Extract ID if it's a URL
                        if KaggleHandler.is_kaggle_url(kaggle_input):
                            dataset_id = KaggleHandler.extract_dataset_id(kaggle_input)
                        else:
                            dataset_id = kaggle_input

                        st.text(f"Dataset ID: {dataset_id}")

                        # Download using existing handler
                        # Note: KaggleHandler.download_dataset handles the download path internally via kagglehub logic,
                        # which caches it in ~/.cache/kagglehub. It returns the Path to the specific file.
                        file_path = KaggleHandler.download_dataset(dataset_id)

                        st.write(f"Downloaded to: {file_path}")

                        # Load data
                        df = read_data(file_path)
                        st.session_state.df = df
                        st.session_state.input_source = dataset_id
                        st.success(f"Successfully loaded data from '{dataset_id}'")

                except Exception as e:
                    st.error(f"Error processing Kaggle dataset: {e}")
            else:
                st.warning("Please enter a valid Dataset ID or URL.")

    # Data Preview
    if st.session_state.df is not None:
        st.divider()
        st.subheader(f"Dataset Preview: {st.session_state.input_source}")
        st.write(
            f"**Shape:** {st.session_state.df.shape[0]} rows × {st.session_state.df.shape[1]} columns"
        )
        st.dataframe(st.session_state.df.head())

        # Configuration Layer (Sidebar)
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
        run_profile = st.sidebar.checkbox("Data Profile", value=True)
        run_univariate = st.sidebar.checkbox("Univariate Analysis", value=True)
        run_bivariate = st.sidebar.checkbox("Bivariate Analysis", value=True)
        run_multivariate = st.sidebar.checkbox("Multivariate Analysis", value=True)

        # Visualization Layer (Main Area)
        if "analysis_complete" not in st.session_state:
            st.session_state.analysis_complete = False
        if "report_data" not in st.session_state:
            st.session_state.report_data = None

        # Visualization Layer (Main Area)
        if st.button("Run Analysis", type="primary"):
            with st.spinner("Running Analysis..."):
                # Reset output dir components for fresh run (granular cleanup to avoid Windows permissions issues)
                charts_dir = st.session_state.output_dir / "charts"
                if charts_dir.exists():
                    shutil.rmtree(charts_dir, ignore_errors=True)

                report_path = st.session_state.output_dir / "eda_report.html"
                if report_path.exists():
                    try:
                        os.remove(report_path)
                    except OSError:
                        pass  # Best effort

                st.session_state.output_dir.mkdir(parents=True, exist_ok=True)
                charts_dir.mkdir(exist_ok=True)

                # Dictionary to collect data for HTML report generation
                # We store this in a local var first, then move to session state
                current_report_data = {
                    "title": f"EDA Report for {st.session_state.input_source}",
                }

                # 1. Profile Step
                if run_profile:
                    try:
                        from src.dora.profiling import generate_profile

                        profile_data = generate_profile(st.session_state.df)
                        current_report_data["profile"] = profile_data
                    except Exception as e:
                        st.error(f"Error in Profiling: {e}")

                # 2. Univariate Step
                if run_univariate:
                    try:
                        from src.dora.plots import univariate

                        # Default params matching existing config defaults
                        params = {
                            "plot_types": {
                                "numerical": ["histogram", "boxplot"],
                                "categorical": ["barplot"],
                            },
                            "max_categories": 20,
                        }
                        plot_paths = univariate.generate_plots(
                            st.session_state.df, charts_dir, params
                        )
                        current_report_data["univariate_plots"] = plot_paths
                    except Exception as e:
                        st.error(f"Error in Univariate Analysis: {e}")

                # 3. Bivariate Step
                if run_bivariate:
                    if not target_variable:
                        st.warning(
                            "Skipping Bivariate Analysis: No Target Variable selected."
                        )
                    else:
                        try:
                            from src.dora.plots import bivariate

                            params = {"target_centric": True, "max_categories": 20}
                            plot_paths = bivariate.generate_plots(
                                st.session_state.df, target_variable, charts_dir, params
                            )
                            current_report_data["bivariate_plots"] = plot_paths
                        except Exception as e:
                            st.error(f"Error in Bivariate Analysis: {e}")

                # 4. Multivariate Step
                if run_multivariate:
                    try:
                        from src.dora.plots import multivariate

                        params = {
                            "correlation_cols": []
                        }  # Empty list means all numerical
                        plot_paths = multivariate.generate_plots(
                            st.session_state.df, charts_dir, params
                        )
                        current_report_data["multivariate_plots"] = plot_paths
                    except Exception as e:
                        st.error(f"Error in Multivariate Analysis: {e}")

                # Update Session State
                st.session_state.report_data = current_report_data
                st.session_state.analysis_complete = True

                # Generate Physical Report Immediately
                try:
                    from src.dora.reporting.generator import create_report

                    create_report(current_report_data, st.session_state.output_dir)

                    # Create ZIP (save outside to avoid recursion)
                    zip_base_name = (
                        st.session_state.output_dir.parent
                        / f"{st.session_state.session_id}_report"
                    )
                    shutil.make_archive(
                        zip_base_name, "zip", st.session_state.output_dir
                    )
                    st.success(
                        f"Analysis Complete! Report generated in {st.session_state.output_dir}"
                    )

                except Exception as e:
                    st.error(f"Error generating final report: {e}")

        # Render Results (Persistent)
        if st.session_state.analysis_complete and st.session_state.report_data:
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

                # 1. Profile Render
                if "profile" in report_data:
                    with tabs[tab_idx]:
                        st.header("Data Profile")
                        try:
                            profile_data = report_data["profile"]
                            col1, col2 = st.columns(2)
                            col1.metric("Rows", profile_data["dataset_shape"][0])
                            col2.metric("Columns", profile_data["dataset_shape"][1])

                            st.subheader("Column Profiles")
                            for col_prof in profile_data["column_profiles"]:
                                with st.expander(
                                    f"{col_prof['name']} ({col_prof['type']})"
                                ):
                                    st.json(col_prof["stats"])
                                    if col_prof.get("sparkline_base64"):
                                        st.markdown(
                                            f'<img src="data:image/png;base64,{col_prof["sparkline_base64"]}" />',
                                            unsafe_allow_html=True,
                                        )

                            if profile_data.get("missing_values_html"):
                                st.subheader("Missing Values")
                                st.markdown(
                                    profile_data["missing_values_html"],
                                    unsafe_allow_html=True,
                                )
                        except Exception as e:
                            st.error(f"Error displaying profile: {e}")
                    tab_idx += 1

                # 2. Univariate Render
                if "univariate_plots" in report_data:
                    with tabs[tab_idx]:
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
                    tab_idx += 1

                # 3. Bivariate Render
                if "bivariate_plots" in report_data:
                    with tabs[tab_idx]:
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
                    tab_idx += 1

                # 4. Multivariate Render
                if "multivariate_plots" in report_data:
                    with tabs[tab_idx]:
                        st.header("Multivariate Analysis")
                        plot_paths = report_data["multivariate_plots"]
                        for path_str in plot_paths:
                            full_path = charts_dir / Path(path_str).name
                            if full_path.exists():
                                st.image(str(full_path), width="stretch")
                    tab_idx += 1

            # Download Button (Persistent)
            st.divider()
            st.subheader("Download Report Data")
            zip_base_name = (
                st.session_state.output_dir.parent
                / f"{st.session_state.session_id}_report"
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

    # Placeholder for next steps
    if st.session_state.df is not None:
        st.info("Data loaded! Analysis configuration needed next.")


if __name__ == "__main__":
    main()
