# 🌽 Corn Yield Forecasting App

A Streamlit-based forecasting tool that predicts annual corn yield (in tons/acre) for Texas using an ARIMAX model. The model incorporates three key exogenous variables:

- 🧪 **Seasonal Fertilizer Use (kg/ha)**
- 🌧️ **Rainfall (March–July) in mm**
- 🌡️ **Average Growing Season Temperature (°C)**

---

## 🚀 Features

- Input custom values for fertilizer, rainfall, and temperature
- View forecasted yield with 95% confidence intervals
- Compare actual vs fitted historical yields with a clear chart
- Clean, responsive, and professional interface

---

## ✅ Assumptions

To ensure the model is realistic and meaningful, the following assumptions were made:

- Soil quality did not significantly degrade over time.
- Fertilizer type has minimal effect on yield — only total seasonal quantity matters.
- The average of daily temperatures from March–July has the greatest impact on yield (not full-year average).
- Annual average rainfall is representative of the March–July corn growing season.
- Farms under study are not irrigated.
- Impact of pests is negligible — farms are assumed to use adequate pest control.
- No extreme weather phenomena (e.g., floods, droughts, heatwaves) are assumed to occur.

---

## 🧩 Simplifications

To keep the model tractable and practical, the following simplifications were applied:

- Seasonal (March–July) averages were used instead of monthly data for:
- Fertilizer use
- Temperature

This reduces noise and aligns data resolution with available annual yield records.

---

## 🛠️ Requirements

Install Python packages using:

```bash
pip install -r requirements.txt
```

### Contents of `requirements.txt`:

```
streamlit
pandas
matplotlib
statsmodels
```

---

## 📂 File Structure

```
.
├── streamlit run yield_prediction_model_GUI.py                         # Main Streamlit app
├── corn_yield_model_data.csv     # Cleaned training data
├── README.md                     # Project documentation
└── requirements.txt              # Python dependencies
```

---

## ▶️ How to Run the App

Make sure you're in the project directory, then run:

```bash
streamlit run yield_prediction_model_GUI.py
```

This will open the app in your default web browser.

---

## 🧠 How the Model Works

The app uses the **SARIMAX** model from `statsmodels` to fit a time series prediction based on:

- Past corn yield values (auto-regression)
- Differencing to remove trend
- External climate and input factors (exogenous variables)

### Variables used:

- `Yield_tons_per_acre` – Target (endogenous)
- `Seasonal_Fertilizer_Use_kg_per_ha`
- `Rainfall_Mar_Jul_mm`
- `Season_Avg_Temp_C`

### ARIMAX Order:

- `order=(1, 1, 1)` – one lag, first difference, one moving average

### Forecasting Method:

The app allows you to input your own values for the three exogenous variables. The model will then output:

- 📊 Forecasted corn yield in tons/acre
- 📉 95% confidence interval

---

## 📊 Sample Use in Code

```python
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
```

---

## 📬 Contact

For questions or contributions, contact **[Takunda - takundamugug@gmail.com]**.

---

## 📄 License

This project is open-source and licensed under the MIT License.
