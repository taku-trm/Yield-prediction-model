import streamlit as st
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Loading and Preparing Data
yield_model_data = pd.read_csv("corn_yield_model_data.csv")
yield_model_data.set_index("Year", inplace=True)

# Variables
endog = yield_model_data["Yield_tons_per_acre"]
exog = yield_model_data[["Seasonal_Fertilizer_Use_kg_per_ha", "Rainfall_Mar_Jul_mm", "Season_Avg_Temp_C"]]

# Building the ARIMAX Model 
yield_model = SARIMAX(endog, exog=exog, order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
results = yield_model.fit(disp=False)

# Add fitted values for plotting
yield_model_data["Fitted"] = results.fittedvalues

# UI
st.set_page_config(page_title="🌽 Corn Yield Forecaster", layout="centered")
st.title("🌽 Corn Yield Forecasting App")
st.markdown("Enter the values below to forecast expected **corn yield (tons/acre)** based on fertilizer, rainfall, and temperature.")

# User input fields
user_fertilizer = st.number_input("🧪 Fertilizer Use (kg/ha)", value=150.0, step=1.0)
user_rainfall = st.number_input("🌧️ Rainfall Total (Mar–Jul) in mm", value=400.0, step=10.0)
user_temp = st.number_input("🌡️ Avg Temp (Mar–Jul) in °C", value=24.0, step=0.1)

# Function for prediction
def predict_yield(fertilizer, rainfall, temp):
    input_df = pd.DataFrame({
        "Seasonal_Fertilizer_Use_kg_per_ha": [fertilizer],
        "Rainfall_Mar_Jul_mm": [rainfall],
        "Season_Avg_Temp_C": [temp]
    })
    forecast = results.get_forecast(steps=1, exog=input_df)
    pred = forecast.predicted_mean.iloc[0]
    conf = forecast.conf_int().iloc[0]
    return round(pred, 2), (round(conf[0], 2), round(conf[1], 2))

# Start the prediction
if st.button("📈 Forecast Yield"):
    pred_yield, (ci_lower, ci_upper) = predict_yield(user_fertilizer, user_rainfall, user_temp)

    st.success(f"🌾 **Predicted Yield**: {pred_yield} tons/acre")
    st.info(f"🔍 95% Confidence Interval: ({ci_lower}, {ci_upper}) tons/acre")

    st.markdown("---")
    st.subheader("📊 Historical Actual vs Fitted Yields")

    fig, ax = plt.subplots(figsize=(10, 5))
    yield_model_data["Yield_tons_per_acre"].plot(ax=ax, label="Actual Yield", color="green", marker='o')
    yield_model_data["Fitted"].plot(ax=ax, label="Fitted (Model)", color="orange", linestyle="--")
    ax.set_ylabel("Yield (tons/acre)")
    ax.set_xlabel("Year")
    ax.set_title("Actual vs Model Fitted Corn Yields")
    ax.legend()
    st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Group 1")
