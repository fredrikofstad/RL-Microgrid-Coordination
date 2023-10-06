from stable_baselines3 import PPO, DQN


def train_ppo(env, timesteps, output_name="ppo_microgrid"):
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps)
    model.save(f"models/{output_name}")

    del model  # delete and load to test our model

    model = PPO.load(f"models/{output_name}")

    obs, info = env.reset()
    terminated = False
    score = 0
    i = 0
    while not terminated:
        action, _states = model.predict(obs)
        obs, rewards, terminated, trans, info = env.step(action)
        score += rewards
        i += 1
    print(score/i)


def train_dqn(env, timesteps, output_name="dqn_microgrid"):
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps, log_interval=4)
    model.save(f"models/{output_name}")

    del model

    model = DQN.load(f"models/{output_name}")

    obs, info = env.reset()
    terminated = False
    score = 0
    i = 0
    while not terminated:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, terminated, trans, info = env.step(action)
        score += rewards
        i += 1
    print(score/i)
