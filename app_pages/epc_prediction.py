import streamlit as st
import pandas as pd


def dashboard_body():
    st.header("🔋 EV Battery Health Estimation")

    st.write("Provide battery details below to estimate State of Health (SoH), "
             "remaining cycles (RUL), and degradation risk.")
