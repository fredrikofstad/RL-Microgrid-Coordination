import pandas as pd
import numpy as np

data_path = "../data/"

# reading data
solar_df = pd.read_csv(data_path + "SolarIrradiance.csv")
wind_df = pd.read_csv(data_path + "WindSpeed.csv")
consumption_df = pd.read_csv(data_path + "rate_consumption_charge.csv")

# MegaWatt/km^2
solar_irradiance = np.array(solar_df.iloc[:, 2])

# km/h = 1/3.6 m/s
wind_speed = 3.6 * np.array(wind_df.iloc[:, 3])

# rate of consumption charge
consumption_charge = np.array(consumption_df.iloc[:, 4])/10

print(solar_irradiance)
print(wind_speed)
print(consumption_charge)
