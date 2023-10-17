
## Coordinating energy management for microgrid using reinforcement learning

This repository is an attempt to develop a reinforcement learning mechanism that can control the
demand supply of a microgrid in order to reduce the overall energy cost.
The microgrid has renewable and conventional generation and energy storage, and can buy energy from the
utility grid when necessary. The profile of the energy load varies over the time.

The environment itself is a modified gym environment.
The action space is a tuple representing the actions the microgrid can take: \
Turning on or off solar power, wind power and the gas generator, \
For each of the aforementioned modules: use power generated to support the load, sell to the utility grid,
or charge the battery. \
The microgrid can also buy energy from the utility grid to either support the load or charge the battery. \
Finally the microgrid can use the power stored in the battery to support the load. \
\
This is represented in the multidicrete tuple: (2, 2, 2, 3, 3, 3, 3, 2) \
\
The observation space is as follows: Three timeseries of hourly data on solar irradiance, wind speed and the price of 
energy from the utility grid; The total load of all households connected with the microgrid <a id="1">[1]</a>; The status of the energy 
modules connected to the microgrid; and the current charge of the battery.

For each step in the environment, the microgrid python class interprets the action space and calculates 
the rewards and costs returning this value to the environment for the RL agent to learn from.
When the microgrid class is first initialized the user can choose what modules to include in the microgrid, as well as the 
parameters associated with these modules. Agents compatible with gymnasium environments can be trained on this microgrid
environment. In this repository we have trained PPO and DQN models using Stablebaseline 3 running pytorch (the dqn model 
can only use discreet values, so we pass discreet=true to the microgrid environment which will convert the action space accordingly).
The amount of households included in the total load can also be specified when initializing the microgrid class, to which
up to 256 households can be chosen. All data is configured and handled in the data.py module.




## References
<a id="1">[1]</a> National Renewable Energy Laboratory. (2014). Commercial and Residential Hourly Load Profiles for all TMY3 Locations in the United States [data set]. Retrieved from https://dx.doi.org/10.25984/1788456.

<a id="1">[2]</a> Gonzague Henri, Tanguy Levent, Avishai Halev, Reda Alami, & Philippe Cordier. (2020). pymgrid: An Open-Source Python Microgrid Simulator for Applied Artificial Intelligence Research.