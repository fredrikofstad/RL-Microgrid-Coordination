"""
Configuration file for the microgrid
function create_microgrid() returns the microgrid with the specified configuration

The microgrid system model consists of battery, wind turbine, solar PV, and gas turbine
generator. The microgrid is connected with the utility grid, and provides energy supply for
the energy load

"""

import numpy as np
from data import *

from pymgrid import Microgrid
from pymgrid.modules import (
    BatteryModule,
    LoadModule,
    RenewableModule,
    GridModule)

np.random.seed(5460)


def create_microgrid(load_ts, renewable_ts, grid_ts):
    # fill in with correct values
    battery = BatteryModule(min_capacity=10,
                            max_capacity=100,
                            max_charge=50,
                            max_discharge=50,
                            efficiency=0.9,
                            init_soc=0.2)

    load = LoadModule(time_series=load_ts)

    pv = RenewableModule(time_series=renewable_ts)

    grid_ts = grid_ts

    grid = GridModule(max_import=100,
                      max_export=100,
                      time_series=grid_ts)

    modules = [
        battery,
        ('pv', pv),
        load,
        grid]

    return Microgrid(modules)


# Testing microgrid creation
if __name__ == "__main__":
    load_ts = 100+100*np.random.rand(24*182)  # how to get 25/100 households ?
    microgrid = create_microgrid(load_ts,
                                 wind_ts,
                                 consumption_ts)

    print(microgrid.controllable)

# All none have to be replaced to control the microgrid
    print(microgrid.get_empty_action())

    print(microgrid.state_series().to_frame())
