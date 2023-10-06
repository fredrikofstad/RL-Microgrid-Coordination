from stable_baselines3 import PPO, DQN


def train_ppo(env, timesteps, output_name="ppo_microgrid"):
    model = PPO("MlpPolicy", env, verbose=1)
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
    while not terminated:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, terminated, trans, info = env.step(action)
        score += rewards
        i += 1
    print(f"Testing {method.__name__} model: {model_name}")
    print(f"Average per hour:{score/i} Total: {score}")
