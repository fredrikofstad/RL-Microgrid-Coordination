import numpy as np
import gymnasium as gym
from gymnasium import spaces

from src.data import Data


class MicrogridEnv(gym.Env):
    def __init__(self, microgrid, household_num, discreet=False):
        super(MicrogridEnv, self).__init__()

        # setup
        self.microgrid = microgrid
        self.data = Data(household_num)
        self.discreet = discreet

        # action space (change status 3, solar 3, wind 3, generator 3, grid 3 battery 1
        self.n_actions = (2, 2, 2, 3, 3, 3, 3, 2)

        if discreet:
            self.action_space = spaces.Discrete(np.prod(self.n_actions))
        else:
            self.action_space = spaces.MultiDiscrete(list(self.n_actions))
        self.observation = []
        self.reward = 0
        self.households = household_num

        # Define observation space
        # observations:

        # [solar,  wind, price, load, status of modules, charge]

        low = [0, 0, 0, 0, 0, 0, 0, 0]  # Lower bounds
        high = [1100, 20, 0.5, 250, 1, 1, 1, 1]  # Upper bounds
        self.observation_space = spaces.Box(np.array(low), np.array(high), dtype=np.float32)

    def step(self, action):
        # Handle the action
        if self.discreet:  # needs to be discreet for dqn
            mapping = tuple(np.ndindex(self.n_actions))
            action = mapping[action]

        module_actions = action[0:3]
        solar_actions = action[3]
        wind_actions = action[4]
        generator_actions = action[5]
        grid_actions = action[6]
        battery_actions = action[7]

        # data: [solar, wind, price, load, status of modules, charge]
        solar_irradiance = self.observation[0]
        wind_speed = self.observation[1]
        price = self.observation[2]
        load = self.observation[3]

        self.microgrid.actions(module_actions, wind_speed)
        # return the new observation, reward, if terminated, and info
        self.reward = self.microgrid.reward(solar_actions, wind_actions, generator_actions, grid_actions,
                                            battery_actions, solar_irradiance, wind_speed, price, load)

        terminated = self.data.is_complete()
        info = self.get_info()
        self.observation = [*self.data.get_observation(), *self.microgrid.status()]
        return self.observation, self.reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Reset the environment to its initial state and return the initial observation
        self.data.reset()  # resets ts to index 0
        self.microgrid.reset()  # resets microgrid to default

        # data: [solar, wind, price, load, status of modules, charge]
        self.observation = [*self.data.get_observation(), *self.microgrid.status()]
        info = self.get_info()
        return self.observation, info

    def get_info(self):
        solar, wind, generator, sell_back, operational_cost = self.microgrid.get_info(self.observation[0],
                                                                                      self.observation[1])
        purchase = self.microgrid.purchase
        return {
            "iteration": self.data.index,
            "reward": self.reward,
            "solar_energy": solar,
            "wind_energy": wind,
            "generator_energy": generator,
            "sell_back": sell_back,
            "purchase": purchase,
            "operational_cost": operational_cost
        }

    def data_len(self):
        return self.data.length()
