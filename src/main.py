from stable_baselines3 import DQN

from src.modules.battery import Battery
from src.modules.wind import WindTurbine
from src.modules.solar import SolarPV
from src.modules.generator import Generator
from src.environment import MicrogridEnv
from microgrid import Microgrid
import agents.sb3_agent as sb3

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

# TODO: specify solar, or wind and solar


def random_actor(env):
    observation, info = env.reset()
    score = 0
    i = 0
    terminated = False
    while not terminated:
        action = env.action_space.sample()
        print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        print(observation)
        print(reward)
        score += reward
        i += 1
    print("random actor:")
    print(score/i)

    env.close()


def baseline_agent_ppo(env, timesteps, name):
    print("trained actor")
    sb3.train_ppo(env, timesteps, name)


def baseline_agent_dqn(env, timesteps, name):
    print("trained actor")
    sb3.train_dqn(env, timesteps, name)


if __name__ == "__main__":
    microgrid = Microgrid(
        Battery(**battery_config),
        WindTurbine(**wind_config),
        SolarPV(**solar_config),
        Generator(**generator_config)
    )

    env = MicrogridEnv(microgrid, 100)
    env_dqn = MicrogridEnv(microgrid, 100, True)



    random_actor(env)
    #baseline_agent_ppo(env, 30000)
    #deep_actor(env)
    #baseline_agent_dqn(env_dqn, 100000, "Dqn-100h")












