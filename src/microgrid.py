"""
Configuration file for the microgrid
function create_microgrid() returns the microgrid with the specified configuration
"""

import numpy as np

from pymgrid import Microgrid
from pymgrid.modules import (
    BatteryModule,
    LoadModule,
    RenewableModule,
    GridModule)

np.random.seed(5460)


def create_microgrid():

    small_battery = BatteryModule(min_capacity=10,
                                  max_capacity=100,
                                  max_charge=50,
                                  max_discharge=50,
                                  efficiency=0.9,
                                  init_soc=0.2)

    large_battery = BatteryModule(min_capacity=10,
                                  max_capacity=1000,
                                  max_charge=10,
                                  max_discharge=10,
                                  efficiency=0.7,
                                  init_soc=0.2)

    load_ts = 100+100*np.random.rand(24*90)  # random load data in the range [100, 200].
    pv_ts = 200*np.random.rand(24*90)  # random pv data in the range [0, 200].

    load = LoadModule(time_series=load_ts)

    pv = RenewableModule(time_series=pv_ts)

    grid_ts = [0.2, 0.1, 0.5] * np.ones((24*90, 3))

    grid = GridModule(max_import=100,
                      max_export=100,
                      time_series=grid_ts)

    modules = [
        small_battery,
        large_battery,
        ('pv', pv),
        load,
        grid]

    return Microgrid(modules)


# Testing microgrid creation
if __name__ == "__main__":
    microgrid = create_microgrid()
    print(microgrid)
    print(microgrid.modules.pv)
    print(microgrid.modules.grid is microgrid.modules['grid'])

    print(microgrid.controllable)

# All none have to be replaced to control the microgrid
    print(microgrid.get_empty_action())

    print(microgrid.state_series().to_frame())
