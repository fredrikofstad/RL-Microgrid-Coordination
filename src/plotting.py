import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_results(env, info_matrix):
    time_index = pd.date_range(start='2023-01-01', periods=env.data_len(), freq='H')

    data = {
        "Time": time_index,
        "Solar_power": info_matrix[2],
        "Wind_power": info_matrix[3],
        "generator_power": info_matrix[4],
        "Reward": info_matrix[1],
        "operational_cost": info_matrix[6],
        "Sell_back_to_grid": info_matrix[5],
    }

    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Time"], value_vars=["Solar_power", "Wind_power", "generator_power", "Reward", "operational_cost", "Sell_back_to_grid"])

    # Create a facet grid
    g = sns.FacetGrid(df_melted, col="variable", col_wrap=4, height=3, aspect=1.5)
    g.map(sns.lineplot, "Time", "value")
    g.set_axis_labels("Time", "Value")
    g.set_titles(col_template="{col_name}")
    plt.show()
