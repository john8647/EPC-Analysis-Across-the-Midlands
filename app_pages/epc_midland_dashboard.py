import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def dashboard_body_visuals(df_unimproved: pd.DataFrame):
    st.header("Midlands EPC Improvements Dashboard")
    age_band = st.selectbox(
        "Select Construction Age Band",
        [
            "All",
            "<1900",
            "1900-1929",
            "1930-1949",
            "1950-1966",
            "1967-1975",
            "1976-1982",
            "1983-1990",
            "1991-1995",
            "1996-2002",
            "2003-2006",
            "2012-2023",
        ],
        key="age_band",
    )

    if age_band == "All":
        unimproved_filtered = df_unimproved.copy()
    else:
        unimproved_filtered = df_unimproved[
            df_unimproved["CONSTRUCTION_AGE_GROUP"] == age_band
        ].copy()

    st.write(
        f"Properties in age band '{age_band}': {len(unimproved_filtered):,}"
    )

    town_summary = (
        unimproved_filtered.groupby("POSTTOWN")
        .agg(
            Average_Gain=("POTENTIAL_GAIN", "mean"),
            Average_Easy_Win=("easy_win_index", "mean"),
            House_Count=("column00", "count"),
            Cost_Easy_Win=("retrofit_cost_score", "mean"),
        )
        .reset_index()
    )
    town_summary_filtered = town_summary[
        town_summary["House_Count"] >= 50
    ].sort_values(by="Average_Gain", ascending=False)

    if town_summary_filtered.empty:
        st.info("No post towns have at least 50 properties in this age band.")
        return

    sns.set_theme(style="whitegrid")
    fig, ax1 = plt.subplots(figsize=(16, 8))
    barplot = sns.barplot(
        data=town_summary_filtered,
        x="POSTTOWN",
        y="Average_Gain",
        palette="viridis",
        hue="Cost_Easy_Win",
        ax=ax1,
    )

    for patch in barplot.patches:
        height = patch.get_height()
        if height > 0:
            barplot.annotate(
                f"{height:.1f}",
                (patch.get_x() + patch.get_width() / 2, height),
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                xytext=(0, 4),
                textcoords="offset points",
            )

    ax2 = ax1.twinx()
    x_coords = range(len(town_summary_filtered))
    sns.lineplot(
        x=x_coords,
        y=town_summary_filtered["Average_Easy_Win"],
        color="crimson",
        marker="o",
        linewidth=2.5,
        ax=ax2,
        label="Average Easy Win Index",
    )
    ax2.set_ylabel(
        "Average Easy Win Index",
        color="crimson",
        fontsize=12,
        fontweight="bold",
        labelpad=10,
    )
    ax2.tick_params(axis="y", labelcolor="crimson")
    ax2.grid(False)

    ax1.set_title(
        "Average Potential Gain vs. Easy Win Index by Post Town (N >= 50)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    ax1.set_xlabel("Post Town (POSTTOWN)", fontsize=12, fontweight="bold", labelpad=10)
    ax1.set_ylabel("Average Potential Gain (SAP Points)", fontsize=12, fontweight="bold")
    ax1.set_xticks(list(x_coords))
    ax1.set_xticklabels(town_summary_filtered["POSTTOWN"], rotation=45, ha="right")
    ax1.legend(
        title="Avg Retrofit Cost Score",
        bbox_to_anchor=(1.12, 1.0),
        loc="upper left",
        borderaxespad=0,
    )
    ax2.legend(
        bbox_to_anchor=(1.12, 0.5),
        loc="upper left",
        borderaxespad=0,
    )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
