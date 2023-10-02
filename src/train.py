from garage.experiment.deterministic import set_seed
from garage.np.exploration_policies import EpsilonGreedyPolicy
from garage.replay_buffer import PathBuffer
from garage.sampler import LocalSampler, RaySampler
from garage.tf.policies import CategoricalMLPPolicy
from garage.torch.algos.dqn import DQN
from garage.torch.policies import DiscreteQFArgmaxPolicy
from garage.torch.q_functions import DiscreteMLPQFunction

from garage.trainer import Trainer

import pandas as pd

from pymgrid_config import *

from pymgrid.envs import DiscreteMicrogridEnv

env = DiscreteMicrogridEnv.from_microgrid(create_microgrid())


def step():
    pass
    # turn off or on energy generation from solar, PV, wind turbine, gas generator
    # we can use this energy to 1) support energy load 2) sell back to utility grid 3) store in battery
    # purchase energy from utility grid for energy load or to charge battery
    # battery can also support energy load

"""The microgrid system model consists of battery, wind turbine, solar PV, and gas turbine
generator. The microgrid is connected with the utility grid, and provides energy supply for
the energy load"""

