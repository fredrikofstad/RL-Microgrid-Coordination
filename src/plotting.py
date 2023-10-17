import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker


def plot_solar_both(env, info1, info2):

    time_index = pd.date_range(start='2016-01-01', periods=env.data_len(), freq='H')
    reward_sum1 = [sum(info1[1, :i+1]) for i in range(len(info1[1]))]
    reward_sum2 = [sum(info2[1, :i+1]) for i in range(len(info2[1]))]
    solar_sum1 = [sum(info1[2, :i+1]) for i in range(len(info1[2]))]
    solar_sum2 = [sum(info2[2, :i+1]) for i in range(len(info2[2]))]
    wind_sum1 = [sum(info1[3, :i+1]) for i in range(len(info1[3]))]
    wind_sum2 = [sum(info2[3, :i+1]) for i in range(len(info2[3]))]
    gas_sum1 = [sum(info1[4, :i+1]) for i in range(len(info1[4]))]
    gas_sum2 = [sum(info2[4, :i+1]) for i in range(len(info2[4]))]

    energy_sum1 = [x + y + z for x, y, z in zip(solar_sum1, wind_sum1, gas_sum1)]
    energy_sum2 = [x + y + z for x, y, z in zip(solar_sum2, wind_sum2, gas_sum2)]


    data = {
        "Time": time_index,
        "Reward": reward_sum1,
        "energy_generated": energy_sum1,
    }
    data2 = {
        "Time": time_index,
        "Reward": reward_sum2,
        "energy_generated": energy_sum2,
    }

    df = pd.DataFrame(data)
    df2 = pd.DataFrame(data2)
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(df["Time"], df["energy_generated"], color="red", label='Random Energy generated')
    ax.plot(df2["Time"], df2["energy_generated"], color='blue', label='PPO Energy generated')

    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Energy (Log scale)")
    plt.title("Energy generated from Solar, Wind and Gas power (100 households)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

"""
    #reward plot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(df["Time"], df["Reward"], color="maroon", label='Random Reward')
    ax.plot(df2["Time"], df2["Reward"], color='royalblue', label='PPO Reward')

    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Reward")
    plt.title("Total reward (energy purchased + operational cost - energy sold)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

    

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(df2["Time"], df2["Reward"], color='royalblue', label='PPO Reward')

    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Reward")
    plt.title("Total reward (energy purchased + operational cost - energy sold)")
    plt.xticks(rotation=45)
    ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter(useMathText=False))
    plt.legend()
    plt.show() """




def plot_solar(env, info_matrix, color='royalblue'):
    time_index = pd.date_range(start='2016-01-01', periods=env.data_len(), freq='H')
    solar_sum = [sum(info_matrix[2, :i+1]) for i in range(len(info_matrix[2]))]
    data = {
        "Time": time_index,
        "Solar_power": solar_sum,
    }

    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(30, 15))

    ax.plot(df["Time"], df["Solar_power"], color=color)

    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Energy")
    plt.title("Energy generated from Solar power")
    plt.xticks(rotation=45)
    plt.show()

def plot_results(env, info_matrix):
    time_index = pd.date_range(start='2016-01-01', periods=env.data_len()/2, freq='H')

    data = {
        "Time": time_index,
        "Solar_power": info_matrix[2],
        "Wind_power": info_matrix[3],
        "generator_power": info_matrix[4],
    }

    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Time"], value_vars=["Solar_power", "Wind_power", "generator_power"])

    # Create a facet grid
    g = sns.FacetGrid(df_melted, col="variable", col_wrap=4, height=3, aspect=1.5)
    g.map(sns.lineplot, "Time", "value")
    g.set_axis_labels("Time", "Value")
    g.set_titles(col_template="{col_name}")
    plt.show()
