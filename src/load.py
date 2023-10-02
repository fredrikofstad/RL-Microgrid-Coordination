import pandas as pd

data_path = "../data/"


class Data:

    def __init__(self):
        self.solar_df = pd.read_csv(data_path + "SolarIrradiance.csv")
        self.wind_df = pd.read_csv(data_path + "WindSpeed.csv")
        self.consumption_df = pd.read_csv(data_path + "rate_consumption_charge.csv")
        self.residential_df = pd.read_csv(data_path + "residential/residential.csv")

    def get_solar(self):
        return self.solar_df

    def get_wind(self):
        return self.wind_df

    def get_consumption(self):
        return self.consumption_df

    def get_residential(self):
        return self.residential_df