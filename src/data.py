import pandas as pd

data_path = "../data/"


solar_df = pd.read_csv(data_path + "SolarIrradiance.csv")
wind_df = pd.read_csv(data_path + "WindSpeed.csv")
consumption_df = pd.read_csv(data_path + "rate_consumption_charge.csv")


solar_ts = solar_df.iloc[:, 3]
wind_ts = wind_df.iloc[:, 3]
consumption_ts = consumption_df.iloc[:, 4]   # ?

if __name__ == "__main__":
    print(solar_ts)
    print(wind_ts)
    print(consumption_ts)
