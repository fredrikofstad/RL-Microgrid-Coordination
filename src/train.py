""" training from stable ?? """

import numpy as np
import gym
from gym import spaces

seed = 5460
class MicrogridEnv(gym.Env):
    def __init__(self):
        super(MicrogridEnv, self).__init__()

        # action space (change status 3, solar 2, wind 2, generator 2, grid 2 battery 1
        self.action_space = spaces.MultiDiscrete([3, 2, 2, 2, 2, 1])

        # Define observation space
        # observations:
        # data: [solar, wind, price, load, status of modules, charge]
        low =  [0,  0,  0,  0,   0, 0, 0, 0]  # Lower bounds
        high = [10, 10, 10, 100, 1, 1, 1, 1]  # Upper bounds
        self.observation_space = spaces.Box(low=np.array(low), high=np.array(high), dtype=np.float32)

    def step(self, action):
        # Handle the action and return the new observation, reward, done, and info
        pass

    def reset(self, seed=seed):
        # Reset the environment to its initial state and return the initial observation
        pass

    def render(self, mode='human'):
        # Implement the render method
        pass
