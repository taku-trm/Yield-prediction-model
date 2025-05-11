import pandas as pd

# temperature_farenheit = pd.read_csv('texas_temperature_data_2003_2022.csv')

# temperature_farenheit_revised = temperature_farenheit[['Year', 'Month', 'Average_Temp']]

# temperature_farenheit_revised = temperature_farenheit_revised[temperature_farenheit_revised['Month'].isin(['March', 'April', 'May', 'June', 'July'])]

# temperature_farenheit_revised['Season_Average_Temp'] = temperature_farenheit_revised.groupby('Year')['Average_Temp'].transform('mean')
# temperature_farenheit_revised = temperature_farenheit_revised[['Year', 'Season_Average_Temp']]

# temperature_farenheit_revised = temperature_farenheit_revised.drop_duplicates()

# temperature_farenheit_revised["Season_Average_Temp"] = temperature_farenheit_revised["Season_Average_Temp"].round(2)
# temperature_farenheit_revised = temperature_farenheit_revised.set_index('Year')
# print(temperature_farenheit_revised.head())

# temperature_farenheit_revised.to_csv('temperature_farenheit_revised.csv')

# fertilizer

# fertilizer_use = pd.read_csv('texas_fertilizer_usage_corn_2007_2023.csv')

# fertilizer_use_kg_per_ha = fertilizer_use[fertilizer_use['Season'].isin(['Spring', 'Summer'])]

# fertilizer_use_kg_per_ha = fertilizer_use_kg_per_ha.groupby("Year")["Amount Used (kg/ha)"].mean().reset_index()

# fertilizer_use_kg_per_ha.rename(columns={"Amount Used (kg/ha)": "Seasonal_Fertilizer_Use_kg_per_ha"}, inplace=True)

# fertilizer_use_kg_per_ha = fertilizer_use_kg_per_ha.set_index('Year')

# print(fertilizer_use_kg_per_ha.head())

# fertilizer_use_kg_per_ha.to_csv('fertilizer_use_kg_per_ha.csv')


#rainfall


df = pd.read_csv("DFW - Monthly and Annual Precipitation.csv")


df.replace("T", 0.01, inplace=True)

for month in ['Mar', 'Apr', 'May', 'Jun', 'Jul']:
    df[month] = pd.to_numeric(df[month], errors='coerce')

df["Total_Rainfall_Mar_Jul_in"] = df[['Mar', 'Apr', 'May', 'Jun', 'Jul']].sum(axis=1)

df["Total_Rainfall_Mar_Jul_mm"] = (df["Total_Rainfall_Mar_Jul_in"] * 25.4).round(2)

#df = df.set_index("Year")
df = df[["Year", "Total_Rainfall_Mar_Jul_mm"]]
df = df.set_index("Year")
print(df.head())
df.to_csv("seasonal_rainfall_in_mm.csv")
