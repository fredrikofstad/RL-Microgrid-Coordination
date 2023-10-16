from stable_baselines3 import PPO, DQN
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def train_ppo(env, timesteps, output_name="ppo_microgrid"):
    model = PPO("MlpPolicy", env, verbose=1,  tensorboard_log=f"./tensorboard/")
    model.learn(total_timesteps=timesteps)

    model_name = f"models/{output_name}"
    model.save(model_name)
    return model_name


def train_dqn(env, timesteps, output_name="dqn_microgrid"):
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps, log_interval=4)
    model_name = f"models/{output_name}"
    model.save(model_name)
    return model_name


def test_model(env, model_name, method):
    model = method.load(model_name)
    obs, info = env.reset()
    terminated = False
    score = 0
    i = 0

    reward_list = []
    info_matrix = np.zeros((9, env.data_len()))

    while not terminated:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, terminated, trans, info = env.step(action)
        score += rewards
        reward_list.append(rewards)
        info_list = list(info.values())
        for j, value in enumerate(info_list):
            info_matrix[j, i] = value
        i += 1

    print(f"Testing {method.__name__} model: {model_name}")
    print(f"Average per hour:{score/i} Total: {score}")

    time_index = pd.date_range(start='2023-01-01', periods=env.data_len(), freq='H')

    data = {
        "Time": time_index,
        "Solar_power": info_matrix[2],
        "Wind_power": info_matrix[3],
        "generator_power": info_matrix[4],
        "Reward": info_matrix[1],
        "operational_cost": info_matrix[6],
        "Sell_back_to_grid":info_matrix[5],
    }

    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Time"], value_vars=["Solar_power", "Wind_power", "generator_power", "Reward", "operational_cost", "Sell_back_to_grid"])

    # Create a facet grid
    g = sns.FacetGrid(df_melted, col="variable", col_wrap=4, height=3, aspect=1.5)
    g.map(sns.lineplot, "Time", "value")
    g.set_axis_labels("Time", "Value")
    g.set_titles(col_template="{col_name}")
    plt.show()


