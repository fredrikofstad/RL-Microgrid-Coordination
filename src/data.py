import pandas as pd
from itertools import islice
import os
import csv

data_path = "../data/"
residential_path = data_path + "residential/"

solar_df = pd.read_csv(data_path + "SolarIrradiance.csv", header=None)
wind_df = pd.read_csv(data_path + "WindSpeed.csv", header=None)
consumption_df = pd.read_csv(data_path + "rate_consumption_charge.csv", header=None)


def make_solar_ts():
    return solar_df.iloc[:, 3]


def make_wind_ts():
    return wind_df.iloc[:, 3]


def make_consumption_ts():
    return consumption_df.iloc[:, 4]


def make_total_load(household_number):
    csv_files = [file for file in os.listdir(residential_path) if file.endswith('.csv')][:household_number]
    total_load = []
    for file in csv_files:
        with open(os.path.join(residential_path, file), 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(islice(reader, 1, len(wind_df)+1)):
                value = float(row[1])
                if i == len(total_load):
                    total_load.append(value)
                else:
                    total_load[i] += float(value)
    return total_load


if __name__ == "__main__":
    print("---Test---")
    print(make_solar_ts()[111])        # 275
    print(make_wind_ts()[111])         # 3.5
    print(make_consumption_ts()[111])  # 0.06
    print(make_total_load(1)[111])      # 1.25 // +1 for header skipped
