from stable_baselines3 import PPO


def train(env):
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=200000)
    model.save("models/ppo_microgrid")

    del model  # delete and load to test our model

    model = PPO.load("models/ppo_microgrid")

    obs, info = env.reset()
    terminated = False
    score = 0
    i = 0
    while not terminated:
        action, _states = model.predict(obs)
        print(action)
        obs, rewards, terminated, trans, info = env.step(action)
        score += rewards
        i += 1
    print(score/i)
