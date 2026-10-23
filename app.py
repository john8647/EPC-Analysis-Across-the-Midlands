
# from app_pages.batteryPerformanceDashboard import dashboard_body_visuals
# from app_pages.batteryFailurePrediction import dashboard_body
# import streamlit as st
# from app_pages.multi_page import MultiPage
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

file_path = "unimproved_subset.csv"

# Load the latest version
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "johntandy/epc-midlands-july-2023",
    file_path,
    # Provide any additional arguments like
    # sql_query or pandas_kwargs. See the
    # documenation for more information:
    # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)


# Create the multi-page Streamlit application
# app = MultiPage(app_name="EV Battery Health & Degradation Prediction App")
# Register the Dashboard page and its body function.
# app.add_page("Main Prediction App", dashboard_body)
# app.add_page("EV Battery dashboard", dashboard_body_visuals)
# Start the Streamlit application.
# app.run()

# Display the first few rows to verify
df_unimproved.head()
