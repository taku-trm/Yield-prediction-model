import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

#loading our cleaned data
yield_model_data = pd.read_csv('corn_yield_model_data.csv')

#setting year as index 
yield_model_data.set_index('Year', inplace=True)

#definition of key variables
endog = yield_model_data['Yield_tons_per_acre']  #this is our target variable that we want to forecast - the endogeneous variable
exog = yield_model_data[['Seasonal_Fertilizer_Use_kg_per_ha', 'Rainfall_Mar_Jul_mm', 'Season_Avg_Temp_C']] # the x factors, the outside factors(variables) that influence the value of our endog/yield 

#building the ARIMAX model
yield_model = SARIMAX(endog, exog=exog, order=(1, 1, 1), enforce_stationarity=False, enforce_invertibility=False)
results = yield_model.fit() 

#summary to assess our model 
#print(results.summary())

#comparison for validation
#yield_model_data["Fitted"] = results.fittedvalues
#yield_model_data[["Yield_tons_per_acre", "Fitted"]].plot(title="Actual vs Fitted Yield", figsize=(10,5))
#plt.ylabel("Yield (tons/acre)")
#plt.show()

#prediction trial: 
def predict_yield(fertilizer, rainfall, temp):
    input_df = pd.DataFrame({
        "Seasonal_Fertilizer_Use_kg_per_ha": [fertilizer],
        "Rainfall_Mar_Jul_mm": [rainfall],
        "Season_Avg_Temp_C": [temp]
    })
    forecast = results.get_forecast(steps=1, exog=input_df)
    pred = forecast.predicted_mean.iloc[0]
    conf = forecast.conf_int().iloc[0]
    return {
        "Predicted_Yield": round(pred, 2),
        "95%_CI": (round(conf[0], 2), round(conf[1], 2))
    }

# Example use
print(predict_yield(fertilizer=152, rainfall=262, temp=24))
