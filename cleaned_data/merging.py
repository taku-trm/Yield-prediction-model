import pandas as pd

yield_df = pd.read_csv("yield_tons_per_acre_cleaned.csv")
fert_df = pd.read_csv("fertilizer_use_kg_per_ha.csv")
rain_df = pd.read_csv("seasonal_rainfall_in_mm.csv")
temp_df = pd.read_csv("temperature_farenheit_revised.csv")

#Temperature converion to celcius... we don't understand farenheight ;)
temp_df["Season_Avg_Temp_C"] = ((temp_df["Season_Average_Temp"] - 32) * 5/9).round(2)

temp_df.drop(columns=["Season_Average_Temp"], inplace=True)

rain_df.rename(columns={"Total_Rainfall_Mar_Jul_mm": "Rainfall_Mar_Jul_mm"}, inplace=True)

# Merge step-by-step
merged_df = (
    yield_df
    .merge(fert_df, on="Year", how="inner")
    .merge(rain_df, on="Year", how="inner")
    .merge(temp_df, on="Year", how="inner")
)

merged_df.to_csv("corn_yield_model_data.csv", index=False)
