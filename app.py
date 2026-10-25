from pathlib import Path

import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import streamlit as st

from app_pages.multi_page import MultiPage
from app_pages.epc_midland_dashboard import dashboard_body_visuals
from app_pages.epc_prediction import dashboard_body


@st.cache_data
def load_unimproved_data():
    file_path = "unimproved_subset.csv"

    # KaggleHub returns a DataFrame when using the PANDAS adapter
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "johntandy/epc-midlands-july-2023",
        file_path,
    )

    # Select only the columns you need
    use_columns = [
        "POSTTOWN",
        "POTENTIAL_GAIN",
        "CONSTRUCTION_AGE_GROUP",
        "column00",
        "easy_win_index",
        "retrofit_cost_score",
    ]

    df = df[use_columns]

    return df


df_unimproved = load_unimproved_data()

app = MultiPage(app_name="EPC-Analysis-Across-the-Midlands")
app.add_page("EPC-Prediction", dashboard_body)
app.add_page(
    "EPC-Map-Of-Midlands dashboard",
    lambda: dashboard_body_visuals(df_unimproved),
)
# Start the Streamlit application.
app.run()
