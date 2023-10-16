from stable_baselines3 import DQN

from src.modules.battery import Battery
from src.modules.wind import WindTurbine
from src.modules.solar import SolarPV
from src.modules.generator import Generator
from src.environment import MicrogridEnv
from microgrid import Microgrid
from agents.sb3_agent import *

battery_config = {
    "cost": 0.95/10,
    "capacity": 300/1000,
    "soc_max": 0.95,
    "soc_min": 0.05,
    "efficiency": 0.95,
}

wind_config = {
    "amount": 1,  # amount of turbines
    "cutin_windspeed": 3*3.6,    # (km/h =1/3.6 m/s)
    "cutoff_windspeed": 11*3.6,  # (km/h =1/3.6 m/s), v^co#
    "rated_windspeed": 7*3.6,    # (km/h =1/3.6 m/s), v^r#
    "unit_operational_cost_wind": 0.085/10,
    "density_of_air": 1.225,  # density of air (10^6 kg/km ^3=1 kg/m^3) , rho#
    "radius_wind_turbine_blade": 25/1000,  # radius of the wind turbine blade (km =1000 m), r#
    "average_wind_speed": 3.952*3.6,  # average wind speed (km/h =1/3.6 m/s), v_avg ( from the wind speed table )#
    "power_coefficient": 0.593,  # power coefficient , theta #
    "gearbox_transmission_efficiency": 0.95,  # gearbox transmission efficiency , eta_t #
    "electrical_generator_efficiency": 0.95,  # electrical generator efficiency , eta_g #
}

solar_config = {
    "unit_operational_cost_solar": 0.15/10,  # from solar PV (10^4 $/ MegaWattHour =10 $/ kWHour ), r_omc ^s#
    "area_solarPV": 1400/(1000*1000),  # (km ^2=1000*1000 m^2) , a#
    "efficiency_solarPV": 0.2,  # delta
}

generator_config = {
    "amount": 1, # amount of generators
    "unit_operational_cost_generator": 0.55/10,  # (10^4 $/ MegaWattHour =10 $/ kWHour ), r_omc ^g#
    "rated_output_power_generator": 60/1000,  # ( MegaWatt =1000 kW), G_p#
}


def random_actor(env):
    observation, info = env.reset()
    score = 0
    i = 0
    terminated = False
    while not terminated:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        score += reward
        i += 1
    print("random actor:")
    print(f"Average per hour:{score/i} Total: {score}")

    env.close()


def baseline_agent_ppo(env, timesteps, name):
    name = train_ppo(env, timesteps, name)
    test_model(env, name, PPO)


def baseline_agent_dqn(env, timesteps, name):
    name = train_dqn(env, timesteps, name)
    test_model(env, name, DQN)


if __name__ == "__main__":
    microgrid_full = Microgrid(
        Battery(**battery_config),
        SolarPV(**solar_config),
        WindTurbine(**wind_config),
        Generator(**generator_config),
        False
    )

    microgrid_solar = Microgrid(
        Battery(**battery_config),
        SolarPV(**solar_config),
    )

    env = MicrogridEnv(microgrid_full, 200)
    env_dqn = MicrogridEnv(microgrid_full, 200, True)

    random_actor(env)
    #deep_actor(env)
    baseline_agent_ppo(env, 1000, "PPO-full_10000")
    #baseline_agent_dqn(env_dqn, 1000, "DQN-full_10000")












