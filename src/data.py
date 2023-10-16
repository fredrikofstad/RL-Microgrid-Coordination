import pandas as pd
from itertools import islice
import os
import csv

data_path = "../data/"
residential_path = data_path + "residential/"

solar_df = pd.read_csv(data_path + "SolarIrradiance.csv")
wind_df = pd.read_csv(data_path + "WindSpeed.csv")
energy_price_df = pd.read_csv(data_path + "rate_consumption_charge.csv")


class Data:

    def __init__(self, household_num):
        self.solar_ts = solar_df.iloc[:, 3]
        self.wind_ts = wind_df.iloc[:, 3]
        self.energy_price_ts = energy_price_df.iloc[:, 4]
        self.total_load_ts = self.make_total_load(household_num)
        self.index = 0

    def is_complete(self):
        return self.index == len(self.solar_ts) - 2

    def get_observation(self):
        index = self.index
        self.index += 1
        return self.solar_ts[index], self.wind_ts[index], self.energy_price_ts[index], self.total_load_ts[index]

    def reset(self):
        self.index = 0

    def make_total_load(self, household_number):
        csv_files = [file for file in os.listdir(residential_path) if file.endswith('.csv')][:household_number]
        total_load = []
        for file in csv_files:
            with open(os.path.join(residential_path, file), 'r') as f:
                reader = csv.reader(f)

                for i, row in enumerate(islice(reader, 1, len(wind_df)+1)):
                    value = float(row[1] + row[2] + row[3] + row[4] +row[5])
                    if i == len(total_load):
                        total_load.append(value)
                    else:
                        total_load[i] += float(value)
        return total_load


if __name__ == "__main__":
    print("---Test---")
    data = Data(1)
    print(data.solar_ts[0])    # 25
    print(len(data.solar_ts))   #8640
    print(data.solar_ts[111])        # 275
    print(data.wind_ts[111])         # 3.5
    print(data.energy_price_ts[111])  # 0.06
    print(data.total_load_ts[111])      # 1.25 // +1 for header skipped
    print(max(data.total_load_ts))
