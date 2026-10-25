import streamlit as st
import pandas as pd
import joblib


def efficiency_to_rating(score):
    if score >= 92:
        return "A"
    elif score >= 81:
        return "B"
    elif score >= 69:
        return "C"
    elif score >= 55:
        return "D"
    elif score >= 39:
        return "E"
    elif score >= 21:
        return "F"
    else:
        return "G"


def map_wall_score(text):
    if not isinstance(text, str):
        return 1
    text = text.lower()
    if "cavity" in text:
        return 3
    if "timber" in text:
        return 2
    if any(word in text for word in ["sandstone", "stone", "solid", "granite", "rubble"]):
        return 1
    return 1  # default to solid wall if unknown


def roof_ins_score(text):
    if not isinstance(text, str):
        return 0
    t = text.lower()
    if "flat" in t:
        return 1
    if "pitched" in t:
        return 3
    if "roof room" in t:
        return 3
    if "thatched" in t:
        return 3
    return 0


def window_score(text):
    # Handle missing or non-string values
    if not isinstance(text, str):
        return 0

    t = text.lower()

    # --- SINGLE GLAZING (score = 3) ---
    if "single" in t:
        return 3

    # --- DOUBLE GLAZING (score = 2) ---
    if "double" in t:
        return 2

    # --- TRIPLE GLAZING (score = 0) ---
    if "triple" in t:
        return 0

    # --- UNKNOWN / OTHER (fallback) ---
    return 1


def calculate_ruc_cost(walls_description, roof_description, windows_description, potential_gain):
    wall = map_wall_score(walls_description)
    roof = roof_ins_score(roof_description)
    window = window_score(windows_description)

    total_score = wall + roof + window

    # stronger penalty for expensive upgrades
    modifier = 4 / (1 + total_score)

    # realistic UK cost per SAP point
    base_cost_per_point = 150

    ruc = potential_gain * base_cost_per_point * modifier
    return ruc


def dashboard_body():
    st.header("EPC Estimation & Recommendations")

    st.write("Provides an estimation of EPC score and suggested improvements.")

    # --- Dropdowns with text ---
    # CURRENT_ENERGY_RATING
    current_energy_rating = st.selectbox(
        "Current Energy Rating",
        ["E", "F", "G"]
    )

    # BUILT_FORM
    build_form = st.selectbox(
        "Build Form",
        ["Detached", "Enclosed End-Terrace", "Enclosed Mid-Terrace",
            "End-Terrace", "Mid-Terrace", "Semi-Detached"]
    )

    # GLAZE TYPE
    glaze_type = st.selectbox(
        "Window Glaze type",
        ["double glazing installed before 2002", "double glazing, unknown install date", "double, known data", "NO DATA!", "not defined",
            "secondary glazing", "single glazing"]
    )

    # WINDOWS_DESCRIPTION
    windows_description = st.selectbox(
        "Window Description",
        ["double glazing", "Full secondary glazing", "Fully double glazed", "Fully double glazing", "Fully secondary glazed", "Fully secondary glazing", "Gwydrau dwbl llawn", "Gwydrau sengl", "High performance glazing", "Mostly  double glazing", "Mostly  multiple glazing", "Mostly double glazing", "Mostly multiple glazing", "Mostly secondary glazing", "Multiple glazing throughout", "Partial double glazing",
            "Partial multiple glazing", "Partial multiple glazingdouble glazing", "Partial secondary glazing", "Secondary glazing", "Single and multiple glazing", "Single glazed", "Single glazeddouble glazing", "Single glazedsecondary glazing", "Single glazedSingle glazing", "Some  double glazing", "Some  secondary glazing", "Some double glazing", "Some multiple glazing", "Some secondary glazing"]
    )

    # WALLS_DESCRIPTION
    walls_description = st.selectbox(
        "Walls Description",
        ["Average thermal transmittance 0.37 W/m-Â¦K", "Average thermal transmittance 0.39 W/m-Â¦K", "Average thermal transmittance 0.41 W/m-Â¦K", "Average thermal transmittance 0.42 W/m-Â¦K", "Average thermal transmittance 0.43 W/m-Â¦K", "Average thermal transmittance 0.46 W/m+Ã©-Â¦K", "Average thermal transmittance 0.46 W/m-Â¦K", "Average thermal transmittance 0.48 W/m-Â¦K", "Average thermal transmittance 0.50 W/m+Ã©-Â¦K", "Average thermal transmittance 0.51 W/m?K", "Average thermal transmittance 0.55 W/m-Â¦K", "Average thermal transmittance 0.60 W/m-Â¦K", "Average thermal transmittance 0.65 W/m-Â¦K", "Average thermal transmittance 0.75 W/m-Â¦K", "Average thermal transmittance 0.93 W/m-Â¦K", "Average thermal transmittance 1.06 W/m-Â¦K", "Average thermal transmittance 1.11 W/m-Â¦K", "Average thermal transmittance 1.15 W/m-Â¦K", "Average thermal transmittance 1.18 W/m-Â¦K", "Average thermal transmittance 1.26 W/m-Â¦K", "Average thermal transmittance 1.39 W/m?K", "Average thermal transmittance 1.68 W/m-Â¦K", "Average thermal transmittance 1.73 W/m-Â¦K", "Average thermal transmittance 1.74 W/m-Â¦K", "Average thermal transmittance 1.77 W/m-Â¦K", "Average thermal transmittance 2.02 W/m-Â¦K", "Average thermal transmittance 2.10 W/m?K", "Average thermal transmittance 2.10 W/m-Â¦K",
            "Average thermal transmittance 2.19 W/m?K", "Average thermal transmittance 2.20 W/m?K", "Average thermal transmittance 2.21 W/m?K", "Average thermal transmittance 3.40 W/m-Â¦K", "Briciau solet", " fel yGÃ‡Ã–u hadeiladwyd", " dim inswleiddio (rhagdybiaeth)", "Cavity wall", "", "Cavity wall", " as built", " no insulation (assumed)", "Cavity wall", " as built", " partial insulation (assumed)", "Cavity wall", " no insulation (assumed)", "Cob", " as built", "Granite or whin", " as built", " no insulation (assumed)", "Granite or whinstone", " as built", " no insulation (assumed)", "Sandstone or limestone", " as built", " no insulation (assumed)", "Sandstone or limestone", " as built", " partial insulation (assumed)", "Sandstone", " as built", " no insulation (assumed)", "Sandstone", " as built", " partial insulation (assumed)", "Solid brick", " as built", " no insulation (assumed)", "Solid brick", " as built", " partial insulation (assumed)", "System built", " as built", " no insulation (assumed)", "System built", " as built", " partial insulation (assumed)", "Timber frame", " as built", " no insulation (assumed)", "Timber frame", " as built", " partial insulation (assumed)", "Waliau ceudod", " fel yGÃ‡Ã–u hadeiladwyd", " dim inswleiddio (rhagdybiaeth)"]
    )

    # WALLS_ENERGY_EFF
    walls_energy_eff = st.selectbox(
        "Walls energy efficency",
        ["Average", "Good", "Poor", "Very Poor"]
    )

    # ROOF_DESCRIPTION
    roof_description = st.selectbox(
        "Roof description",
        ["(another dwelling above)", "Ar oleddf", " 12 mm o inswleiddio yn y llofft", "Ar oleddf", " 50 mm o inswleiddio yn y llofft", "Ar oleddf", " dim inswleiddio (rhagdybiaeth)", "Average thermal transmittance 0.11 W/m-Â¦K", "Average thermal transmittance 0.13 W/m+Ã©-Â¦K", "Average thermal transmittance 0.15 W/m-Â¦K", "Average thermal transmittance 0.16 W/m-Â¦K", "Average thermal transmittance 0.17 W/m-Â¦K", "Average thermal transmittance 0.18 W/m?K", "Average thermal transmittance 0.18 W/m-Â¦K", "Average thermal transmittance 0.19 W/m?K", "Average thermal transmittance 0.2 W/m-Â¦K", "Average thermal transmittance 0.21 W/m-Â¦K", "Average thermal transmittance 0.22 W/m-Â¦K", "Average thermal transmittance 0.25 W/m?K", "Average thermal transmittance 0.27 W/m+Ã©-Â¦K", "Average thermal transmittance 0.29 W/m?K", "Average thermal transmittance 0.32 W/m-Â¦K", "Average thermal transmittance 0.37 W/m-Â¦K", "Average thermal transmittance 0.44 W/m-Â¦K", "Average thermal transmittance 0.45 W/m-Â¦K", "Average thermal transmittance 0.70 W/m-Â¦K", "Average thermal transmittance 0.93 W/m?K", "Average thermal transmittance 1.34 W/m-Â¦K", "Average thermal transmittance 1.35 W/m-Â¦K", "Average thermal transmittance 1.36 W/m-Â¦K", "Average thermal transmittance 1.47 W/m-Â¦K", "Flat", "", "Flat", " insulated", "Flat", " insulated (assumed)", "Flat", " limited insulation", "Flat", " limited insulation (assumed)", "Flat", " no insulation", "Flat", " no insulation (assumed)", "Pitched", "", "Pitched", "  loft insulation",
         "Pitched", " *** INVALID INPUT Code : 57 *** loft insulation", "Pitched", " 0 mm loft insulation", "Pitched", " 0mm loft insulation", "Pitched", " 100 mm loft insulation", "Pitched", " 100mm loft insulation", "Pitched", " 12 mm loft insulation", "Pitched", " 12mm loft insulation", "Pitched", " 150 mm loft insulation", "Pitched", " 150mm loft insulation", "Pitched", " 200 mm loft insulation", "Pitched", " 200mm loft insulation", "Pitched", " 25 mm loft insulation", "Pitched", " 25mm loft insulation", "Pitched", " 270 mm loft insulation", "Pitched", " 50 mm loft insulation", "Pitched", " 50mm loft insulation", "Pitched", " 75 mm loft insulation", "Pitched", " 75mm loft insulation", "Pitched", " insulated", "Pitched", " insulated (assumed)", "Pitched", " insulated at rafters", "Pitched", " limited insulation", "Pitched", " limited insulation (assumed)", "Pitched", " loft insulation", "Pitched", " mm loft insulation", "Pitched", " no insulation", "Pitched", " no insulation (assumed)", "Pitched", " no insulation(assumed)", "Pitched", " Unknown loft insulation", "Roof room(s)", " ceiling insulated", "Roof room(s)", " insulated", "Roof room(s)", " insulated (assumed)", "Roof room(s)", " limited insulation", "Roof room(s)", " limited insulation (assumed)", "Roof room(s)", " no insulation", "Roof room(s)", " no insulation (assumed)", "Roof room(s)", " no insulation(assumed)", "Roof room(s)", " thatched", "Roof room(s)", " thatched with additional insulation", "Thatched", "Thatched", " with additional insulation"]
    )

    # ROOF_ENERGY_EFF
    roof_energy_eff = st.selectbox(
        "Roof energy efficency",
        ["Average", "Good", "Poor", "Very Good", "Very Poor"]
    )

    # MAINHEAT_DESCRIPTION
    mainheat_description = st.selectbox(
        "Main heat description",
        ["Air source heat pump, radiators, electric", "Air source heat pump, Underfloor heating and radiators, pipes in screed above insulation, electric, Boiler And radiators, LPG", "Air source heat pump, underfloor, electric", "Air source heat pump, underfloor, electric, Air source heat pump, radiators, electric", "Air source heat pump, warm air, electric", "Air source heat pump, warm air, mains gas", "Boiler & underfloor, mains gas", "Boiler & underfloor, wood pellets", "Boiler and radiators,", "Boiler and radiators, anthracite", "Boiler and radiators, B30K", "Boiler and radiators, bottled gas", "Boiler and radiators, bottled LPG", "Boiler and radiators, coal", "Boiler and radiators, dual fuel (mineral and wood)", "Boiler and radiators, dual fuel (mineral and wood), Electric storage heaters", "Boiler and radiators, dual fuel (mineral and wood), Room heaters, electric", "Boiler and radiators, electric", "Boiler and radiators, LPG", "Boiler and radiators, LPG, Air source heat pump, underfloor, electric", "Boiler and radiators, LPG, Electric storage heaters", "Boiler and radiators, mains gas", "Boiler and radiators, mains gas, Boiler and radiators, mains gas", "Boiler and radiators, mains gas, Boiler and underfloor heating, mains gas", "Boiler and radiators, mains gas, Electric ceiling heating, electric", "Boiler and radiators, mains gas, Electric storage heaters", "Boiler and radiators, mains gas, Electric underfloor heating", "Boiler and radiators, mains gas, Room heaters, electric", "Boiler and radiators, mains gas, Room heaters, mains gas", "Boiler and radiators, mains gas, Warm air, mains gas", "Boiler and radiators, oil", "Boiler and radiators, oil, Air source heat pump, underfloor, electric", "Boiler and radiators, oil, Air source heat pump, warm air, electric", "Boiler and radiators, oil, Boiler and radiators, LPG", "Boiler and radiators, oil, Boiler and radiators, oil", "Boiler and radiators, oil, Boiler and radiators, wood chips", "Boiler and radiators, oil, Boiler and underfloor heating, oil", "Boiler and radiators, oil, Electric storage heaters", "Boiler and radiators, oil, Electric underfloor heating", "Boiler and radiators, oil, Room heaters, electric", "Boiler and radiators, smokeless fuel", "Boiler and radiators, wood chips",
         "Boiler and radiators, wood logs", "Boiler and radiators, wood pellets", "Boiler and underfloor heating, electric", "Boiler and underfloor heating, LPG", "Boiler and underfloor heating, mains gas", "Boiler and underfloor heating, oil", "Boiler and underfloor heating, oil, Boiler and radiators, oil", "Boiler, mains gas", "Boiler, smokeless fuel", "Bwyler a rheiddiaduron, nwy prif gyflenwad", "Community scheme", "Electric ceiling heating", "Electric ceiling heating, electric", "Electric storage heaters", "Electric storage heaters, Boiler and radiators, coal", "Electric storage heaters, Boiler and radiators, dual fuel (mineral and wood)", "Electric storage heaters, Boiler and radiators, electric", "Electric storage heaters, Boiler and radiators, mains gas", "Electric storage heaters, Electric storage heaters", "Electric storage heaters, Room heaters, electric", "Electric underfloor heating", "Ground source heat pump, radiators, electric", "Ground source heat pump, radiators, mains gas", "Ground source heat pump, underfloor, electric", "No system present: electric heaters assumed", "No system present: electric heaters assumed, gas", "No system present: electric heaters assumed, mains gas", "Portable electric heaters assumed for most rooms", "Portable electric heating assumed for most rooms", "Room heaters", "Room heaters, anthracite", "Room heaters, bottled LPG", "Room heaters, coal", "Room heaters, coal, Room heaters, mains gas", "Room heaters, dual fuel (mineral and wood)", "Room heaters, dual fuel (mineral and wood), Room heaters, electric", "Room heaters, dual fuel appliance", "Room heaters, electric", "Room heaters, electric, Room heaters, electric", "Room heaters, electricity", "Room heaters, LPG", "Room heaters, mains gas", "Room heaters, mains gas, Electric storage heaters", "Room heaters, mains gas, Room heaters, dual fuel (mineral and wood)", "Room heaters, mains gas, Room heaters, electric", "Room heaters, mains gas, Room heaters, mains gas", "Room heaters, oil", "Room heaters, smokeless fuel", "Room heaters, smokeless fuel, Room heaters, smokeless fuel", "Room heaters, wood logs", "Warm air, electric", "Warm air, Electricaire", "Warm air, LPG", "Warm air, mains gas", "Warm air, oil", "Water source heat pump, radiators, electric"]
    )

    # MAINHEAT_ENERGY_EFF
    mainheat_energy_eff = st.selectbox(
        "Main heat energy efficency",
        ["Average", "Good", "Poor", "Very Good", "Very Poor"]
    )

    # CONSTRUCTION_AGE_GROUP
    construction_age_group = st.selectbox(
        "Contraction Age Group",
        ["<1900", "1900-1929", "1930-1949", "1950-1966", "1967-1975", "1976-1982",
            "1983-1990", "1991-1995", "1996-2002", "2003-2006", "2012-2023", "ignore", ""]
    )

    # --- Dropdowns with numbers ---
    # CURRENT_ENERGY_EFFICIENCY
    current_energy_efficiency = st.slider(
        "Currency energy efficiency",
        min_value=1,
        max_value=54,
        value=50
    )

    # ENERGY_CONSUMPTION_CURRENT
    energy_consumption_current = st.slider(
        "Currency energy consumption",
        min_value=1,
        max_value=4000,
        value=750
    )

    # CO2_EMISSIONS_CURRENT
    co2_emissions_current = st.slider(
        "Current C02 Emissions",
        min_value=1,
        max_value=300,
        value=100
    )

    # HEATING_COST_CURRENT
    heating_cost_current = st.slider(
        "Current heating cost",
        min_value=0,
        max_value=50000,
        value=750
    )

    # HOT_WATER_COST_CURRENT
    hot_water_cost_current = st.slider(
        "Current hot water cost",
        min_value=0,
        max_value=2000,
        value=450
    )

    # TOTAL_FLOOR_AREA
    total_floor_area = st.slider(
        "Total floor area",
        min_value=0,
        max_value=2500,
        value=850
    )

    # 1. Load the trained model
    model = joblib.load("epc_boost_model.pkl")

    # Force single-thread mode for Heroku
    if hasattr(model, "n_jobs"):
        model.n_jobs = 1

    # 2. Create an example input row (must match your feature names)
    # --- Prediction Button ---
    if st.button("Predict EPC potential and show improvement cost"):
        # Build model input row
        row = pd.DataFrame([{
            'CURRENT_ENERGY_RATING': current_energy_rating,
            'BUILT_FORM': build_form,
            'GLAZED_TYPE': glaze_type,
            'WINDOWS_DESCRIPTION': windows_description,
            'WALLS_DESCRIPTION': walls_description,
            'WALLS_ENERGY_EFF': walls_energy_eff,
            'ROOF_DESCRIPTION': roof_description,
            'ROOF_ENERGY_EFF': roof_energy_eff,
            'MAINHEAT_DESCRIPTION': mainheat_description,
            'MAINHEAT_ENERGY_EFF': mainheat_energy_eff,
            'CONSTRUCTION_AGE_GROUP': construction_age_group,
            'CURRENT_ENERGY_EFFICIENCY': current_energy_efficiency,
            'ENERGY_CONSUMPTION_CURRENT': energy_consumption_current,
            'CO2_EMISSIONS_CURRENT': co2_emissions_current,
            'HEATING_COST_CURRENT': heating_cost_current,
            'HOT_WATER_COST_CURRENT': hot_water_cost_current,
            'TOTAL_FLOOR_AREA': total_floor_area
        }])

        # 3. Predict potential EPC efficiency score
        prediction = model.predict(row)[0]
        # 4. Extract result
        potential_efficiency = float(prediction)
        rating = efficiency_to_rating(potential_efficiency)
        potential_gain = potential_efficiency - current_energy_efficiency

        ruc = calculate_ruc_cost(
            walls_description, roof_description, windows_description, potential_gain)
        # --- Output---
        st.success(
            f"**Predicted potential EPC score will be:** {potential_efficiency:.2f}%\n\n"
            f"**Potential Rating:** {rating}\n\n"
            f"**Estimated retrofit cost for maximum impact:**£ {ruc:.2f}"
        )
