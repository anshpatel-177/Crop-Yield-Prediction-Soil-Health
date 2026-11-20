import streamlit as st
import pandas as pd
import joblib
import requests


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Agriculture System",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Crop Yield Prediction & Soil Health Analysis")

st.write(
    "A machine learning based system for crop yield prediction "
    "and soil health analysis."
)


# --------------------------------------------------
# LOAD MODEL AND PREPROCESSOR
# --------------------------------------------------

@st.cache_resource
def load_models():
    preprocessor = joblib.load("models/preprocessor.pkl")
    model = joblib.load("models/best_crop_yield_model.pkl")

    return preprocessor, model


preprocessor, model = load_models()
def fetch_current_weather(district):

    api_key = st.secrets["OPENWEATHER_API_KEY"]

    # Find district coordinates
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"

    geo_params = {
        "q": f"{district},Uttar Pradesh,IN",
        "limit": 1,
        "appid": api_key
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params,
        timeout=15
    )

    geo_response.raise_for_status()
    locations = geo_response.json()

    if not locations:
        raise ValueError("District location not found.")

    lat = locations[0]["lat"]
    lon = locations[0]["lon"]

    # Fetch current weather
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=15
    )

    weather_response.raise_for_status()
    weather_data = weather_response.json()

    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    condition = weather_data["weather"][0]["description"]

    return temperature, humidity, condition

# --------------------------------------------------
# SOIL HEALTH FUNCTION
# --------------------------------------------------

def calculate_soil_health(
    ph,
    nitrogen,
    phosphorus,
    potassium,
    organic_matter
):

    score = 0

    # pH
    if 6.0 <= ph <= 7.5:
        score += 20
    elif 5.5 <= ph <= 8.0:
        score += 15
    else:
        score += 10

    # Nitrogen
    if nitrogen >= 80:
        score += 20
    elif nitrogen >= 50:
        score += 15
    else:
        score += 10

    # Phosphorus
    if phosphorus >= 40:
        score += 20
    elif phosphorus >= 20:
        score += 15
    else:
        score += 10

    # Potassium
    if potassium >= 150:
        score += 20
    elif potassium >= 100:
        score += 15
    else:
        score += 10

    # Organic Matter
    if organic_matter >= 2.5:
        score += 20
    elif organic_matter >= 1.5:
        score += 15
    else:
        score += 10

    # Final category
    if score >= 80:
        health = "Good"
    elif score >= 60:
        health = "Moderate"
    else:
        health = "Poor"

    return score, health

def generate_soil_recommendations(
    ph,
    nitrogen,
    phosphorus,
    potassium,
    organic_matter
):

    recommendations = []

    if ph < 5.5:
        recommendations.append(
            "Soil is highly acidic. Consider a soil test and suitable pH correction."
        )
    elif ph > 7.5:
        recommendations.append(
            "Soil is alkaline. Check nutrient availability through soil testing."
        )

    if nitrogen < 50:
        recommendations.append(
            "Nitrogen level is low. Consider an appropriate nitrogen source."
        )

    if phosphorus < 20:
        recommendations.append(
            "Phosphorus level is low. Consider suitable phosphorus management."
        )

    if potassium < 100:
        recommendations.append(
            "Potassium level is low. Consider suitable potassium management."
        )

    if organic_matter < 1.5:
        recommendations.append(
            "Organic matter is low. Consider compost or well-decomposed organic manure."
        )

    if not recommendations:
        recommendations.append(
            "The entered soil parameters are within this project's target ranges. "
            "Continue regular soil testing and balanced nutrient management."
        )

    return recommendations
# --------------------------------------------------
# CREATE TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "🌾 Crop Yield Prediction",
        "🌱 Soil Health Analysis",
        "📊 Model Performance"
    ]
)


# ==================================================
# TAB 1 - CROP YIELD PREDICTION
# ==================================================

with tab1:

    st.header("🌾 Crop Yield Prediction")

    st.write(
        "Enter crop, soil and weather information."
    )

    col1, col2, col3 = st.columns(3)

    # -------------------------------
    # COLUMN 1 - FARM DETAILS
    # -------------------------------

    with col1:

        year = st.number_input(
            "Year",
            min_value=2018,
            max_value=2035,
            value=2026
        )

        district = st.selectbox(
            "District",
            [
                "Lucknow",
                "Barabanki",
                "Kanpur Nagar",
                "Prayagraj",
                "Varanasi",
                "Agra",
                "Gorakhpur",
                "Ayodhya",
                "Meerut",
                "Bareilly",
                "Moradabad",
                "Aligarh",
                "Mathura",
                "Unnao",
                "Sitapur",
                "Lakhimpur Kheri",
                "Azamgarh",
                "Jaunpur",
                "Ghaziabad",
                "Sultanpur"
            ]
        )
        if st.button("🌤️ Get Current Weather"):

            try:
                temperature, humidity, condition = (
                    fetch_current_weather(district)
                )

                st.session_state["temperature_input"] = float(temperature)
                st.session_state["humidity_input"] = float(humidity)

                st.success(
                    f"Weather fetched for {district}: {condition}"
                )

            except Exception as error:
                st.error(f"Weather API Error: {error}")

        crop = st.selectbox(
            "Crop",
            [
                "Wheat",
                "Rice",
                "Maize",
                "Sugarcane",
                "Potato",
                "Mustard",
                "Pigeon Pea",
                "Barley"
            ]
        )

        season = st.selectbox(
            "Season",
            [
                "Rabi",
                "Kharif",
                "Zaid"
            ]
        )

        farm_area = st.number_input(
            "Farm Area (acres)",
            min_value=0.1,
            value=5.0
        )

    # -------------------------------
    # COLUMN 2 - SOIL DETAILS
    # -------------------------------

    with col2:

        soil_ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.8
        )

        nitrogen = st.number_input(
            "Nitrogen (kg/ha)",
            min_value=0.0,
            value=90.0
        )

        phosphorus = st.number_input(
            "Phosphorus (kg/ha)",
            min_value=0.0,
            value=45.0
        )

        potassium = st.number_input(
            "Potassium (kg/ha)",
            min_value=0.0,
            value=170.0
        )

        organic_matter = st.number_input(
            "Organic Matter (%)",
            min_value=0.0,
            value=3.0
        )

        soil_moisture = st.number_input(
            "Soil Moisture (%)",
            min_value=0.0,
            max_value=100.0,
            value=45.0
        )

    # -------------------------------
    # COLUMN 3 - WEATHER DETAILS
    # -------------------------------

    with col3:

        if "temperature_input" not in st.session_state:
            st.session_state["temperature_input"] = 22.0

        temperature = st.number_input(
            "Temperature (°C)",
            key="temperature_input"
        )

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=550.0
        )

        if "humidity_input" not in st.session_state:
            st.session_state["humidity_input"] = 65.0

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            key="humidity_input"
        )

        irrigation_type = st.selectbox(
            "Irrigation Type",
            [
                "Canal",
                "Tube Well",
                "Rainfed",
                "Drip",
                "Sprinkler"
            ]
        )

        fertilizer_use = st.number_input(
            "Fertilizer Use (kg/ha)",
            min_value=0.0,
            value=120.0
        )

        pesticide_use = st.number_input(
            "Pesticide Use (L/ha)",
            min_value=0.0,
            value=2.0
        )

    # -------------------------------
    # PREDICTION BUTTON
    # -------------------------------

    st.divider()

    if st.button(
        "🌾 Predict Crop Yield",
        type="primary"
    ):

        input_data = pd.DataFrame({
            "Year": [year],
            "District": [district],
            "Crop": [crop],
            "Season": [season],
            "Farm_Area_acres": [farm_area],
            "Soil_pH": [soil_ph],
            "Nitrogen_kg_ha": [nitrogen],
            "Phosphorus_kg_ha": [phosphorus],
            "Potassium_kg_ha": [potassium],
            "Organic_Matter_pct": [organic_matter],
            "Temperature_C": [temperature],
            "Rainfall_mm": [rainfall],
            "Humidity_pct": [humidity],
            "Soil_Moisture_pct": [soil_moisture],
            "Irrigation_Type": [irrigation_type],
            "Fertilizer_Use_kg_ha": [fertilizer_use],
            "Pesticide_Use_L_ha": [pesticide_use]
        })

        try:

            processed_data = preprocessor.transform(
                input_data
            )

            prediction = model.predict(
                processed_data
            )

            st.success(
                f"🌾 Predicted Crop Yield: "
                f"{prediction[0]:.2f} tonnes/hectare"
            )

            # Create downloadable prediction report

            report_data = input_data.copy()

            report_data["Predicted_Yield_tonnes_ha"] = round(
                float(prediction[0]), 2
            )

            csv_report = report_data.to_csv(index=False)

            st.download_button(
                label="📥 Download Prediction Report",
                data=csv_report,
                file_name="crop_yield_prediction_report.csv",
                mime="text/csv"
            )


        except Exception as error:

            st.error(
                f"Prediction Error: {error}"
            )


# ==================================================
# TAB 2 - SOIL HEALTH ANALYSIS
# ==================================================

with tab2:

    st.header("🌱 Soil Health Analysis")

    st.write(
        "Enter soil parameters to analyze soil health."
    )

    soil_col1, soil_col2 = st.columns(2)

    # -------------------------------
    # SOIL COLUMN 1
    # -------------------------------

    with soil_col1:

        sh_ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.8,
            key="soil_health_ph"
        )

        sh_nitrogen = st.number_input(
            "Nitrogen (kg/ha)",
            min_value=0.0,
            value=90.0,
            key="soil_health_n"
        )

        sh_phosphorus = st.number_input(
            "Phosphorus (kg/ha)",
            min_value=0.0,
            value=45.0,
            key="soil_health_p"
        )

    # -------------------------------
    # SOIL COLUMN 2
    # -------------------------------

    with soil_col2:

        sh_potassium = st.number_input(
            "Potassium (kg/ha)",
            min_value=0.0,
            value=170.0,
            key="soil_health_k"
        )

        sh_organic = st.number_input(
            "Organic Matter (%)",
            min_value=0.0,
            value=3.0,
            key="soil_health_organic"
        )

    st.divider()

    # -------------------------------
    # ANALYZE BUTTON
    # -------------------------------

    if st.button(
       "🌱 Analyze Soil Health", type="primary", key="soil_health_analysis_button"
       
    ):

        score, health = calculate_soil_health(
            sh_ph,
            sh_nitrogen,
            sh_phosphorus,
            sh_potassium,
            sh_organic
        )

        st.metric(
            "Soil Health Score",
            f"{score}/100"
        )

        if health == "Good":
            st.success(
                f"🌱 Soil Health: {health}"
            )

        elif health == "Moderate":
            st.warning(
                f"🌱 Soil Health: {health}"
            )

        else:
            st.error(
                f"🌱 Soil Health: {health}"
            )
        if st.button("🌱 Analyze Soil Health", type="primary", key="analyzes_soils_health_btn"):
                    st.subheader("🌿 Soil Improvement Suggestions")

        recommendations = generate_soil_recommendations(
            sh_ph,
            sh_nitrogen,
            sh_phosphorus,
            sh_potassium,
            sh_organic
        )

        for recommendation in recommendations:
            st.info("💡 " + recommendation)

    
# ==================================================
# TAB 3 - MODEL PERFORMANCE DASHBOARD
# ==================================================

with tab3:

    st.header("📊 Model Performance Dashboard")

    st.write(
        "Comparison of machine learning models "
        "used for crop yield prediction."
    )

    try:

        # Load saved performance data
        results_df = pd.read_csv(
            "models/model_performance.csv"
        )

        prediction_results = pd.read_csv(
            "data/prediction_results.csv"
        )

        # Find best model
        best_row = results_df.sort_values(
            by="R2 Score",
            ascending=False
        ).iloc[0]

        st.subheader("🏆 Best Performing Model")

        st.success(
            f"Best Model: {best_row['Model']}"
        )

        # Display metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "MAE",
            f"{best_row['MAE']:.3f}"
        )

        col2.metric(
            "RMSE",
            f"{best_row['RMSE']:.3f}"
        )

        col3.metric(
            "R² Score",
            f"{best_row['R2 Score']:.3f}"
        )

        st.divider()

        # Model comparison table
        st.subheader("Model Comparison")

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

        # R2 comparison chart
        st.subheader("R² Score Comparison")

        chart_data = results_df.set_index("Model")[["R2 Score"]]

        st.bar_chart(chart_data)

        # MAE comparison
        st.subheader("MAE Comparison")

        mae_data = results_df.set_index("Model")[["MAE"]]

        st.bar_chart(mae_data)

        # Actual vs Predicted
        st.subheader("Actual vs Predicted Crop Yield")

        st.scatter_chart(
            prediction_results,
            x="Actual_Yield",
            y="Predicted_Yield"
        )

        st.caption(
            "Each point represents a test-set prediction. "
            "Values are based on the saved model evaluation."
        )

    except FileNotFoundError:

        st.error(
            "Performance files not found. "
            "Please run the model evaluation notebook first."
        )

    except Exception as error:

        st.error(f"Dashboard Error: {error}")
        