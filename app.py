import streamlit as st
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("mock_texas_corn_yield_data.csv")
df["Year"] = pd.to_datetime(df["Year"], format="%Y")

# Set index for time series modeling
df.set_index("Year", inplace=True)

st.title("🌽 Texas Corn Yield Forecast")
st.write("This app uses an ARIMAX model to predict corn yield based on rainfall, temperature, and fertilizer use.")

# Show data
if st.checkbox("Show raw data"):
    st.dataframe(df)

# Select forecast period
n_years = st.slider("Years to forecast", min_value=1, max_value=10, value=5)

# Prepare model inputs
endog = df["Yield_BU_per_ACRE"]
exog = df[["Rainfall_Mar_Jul_mm", "Temperature_GrowSeason_C", "Fertilizer_Use_kg_per_ha"]]

# Fit ARIMAX model
model = SARIMAX(endog, exog=exog, order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
results = model.fit(disp=False)

# Forecast future exog values (mock: repeat last year)
last_exog = exog.iloc[-1]
future_exog = pd.DataFrame([last_exog.values] * n_years, columns=exog.columns)

# Forecast
forecast = results.get_forecast(steps=n_years, exog=future_exog)
pred_mean = forecast.predicted_mean
pred_ci = forecast.conf_int()

# Display forecast
future_years = pd.date_range(start=df.index[-1] + pd.DateOffset(years=1), periods=n_years, freq="Y")
pred_mean.index = future_years
pred_ci.index = future_years

st.subheader("📈 Forecasted Yield")
fig, ax = plt.subplots()
df["Yield_BU_per_ACRE"].plot(ax=ax, label="Observed", color="blue")
pred_mean.plot(ax=ax, label="Forecast", color="orange")
ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color="orange", alpha=0.3)
ax.set_ylabel("Yield (bu/acre)")
ax.set_xlabel("Year")
ax.legend()
st.pyplot(fig)
