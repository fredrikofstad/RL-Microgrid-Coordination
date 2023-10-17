import time

from src.modules.battery import Battery
from src.modules.wind import WindTurbine
from src.modules.solar import SolarPV
from src.modules.generator import Generator
from src.environment import MicrogridEnv
from src.plotting import *
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
    "area_solarPV": 1400/ (1000*1000),  # (km ^2=1000*1000 m^2) , a#
    "efficiency_solarPV": 0.2,  # delta
}

generator_config = {
    "amount": 1,  # amount of generators
    "unit_operational_cost_generator": 0.55/10,  # (10^4 $/ MegaWattHour =10 $/ kWHour ), r_omc ^g#
    "rated_output_power_generator": 60/1000,  # ( MegaWatt =1000 kW), G_p#
}


def random_actor(env):
    observation, info = env.reset()
    score = 0
    i = 0
    info_matrix = np.zeros((9, env.data_len()))
    terminated = False
    while not terminated:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)
        score += reward
        info_list = list(info.values())
        for j, value in enumerate(info_list):
            info_matrix[j, i] = value
        i += 1
    print("random actor:")
    print(f"Average per hour:{score/i} Total: {score}")
    env.close()
    return info_matrix


def baseline_agent_ppo(env, timesteps, name):
    #start_time = time.time()
    #train_ppo(env, timesteps, name)
    #end_time = time.time()
    #print(f"Time taken: {end_time-start_time}")
    info_matrix = test_model(env, name, PPO)
    return info_matrix


def baseline_agent_dqn(env, timesteps, name):
    train_dqn(env, timesteps, name)
    test_model(env, name, DQN)


if __name__ == "__main__":
    microgrid_new = Microgrid(
        Battery(**battery_config),
        SolarPV(**solar_config),
        WindTurbine(**wind_config),
        Generator(**generator_config),
        True
    )

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

    microgrid_solar_wind = Microgrid(
        Battery(**battery_config),
        SolarPV(**solar_config),
        WindTurbine(**wind_config),
    )

    env_solar = MicrogridEnv(microgrid_solar, 256)
    env_solar_wind = MicrogridEnv(microgrid_solar_wind, 100)
    env_full = MicrogridEnv(microgrid_full, 100)
    env_full_new_formula = MicrogridEnv(microgrid_full, 100)

    #env_dqn = MicrogridEnv(microgrid_solar, 200, True)
    #plot_solar_both(env, random_actor(env), baseline_agent_ppo(env, 1000, "PPO-solar-wind-h100-1000"))

    #ppo_solar = baseline_agent_ppo(env_solar, 1000, "PPO-solar")
    rand_solar = random_actor(env_solar)
    #ppo_solar_wind = baseline_agent_ppo(env_solar_wind, 1000, "PPO-solar-wind")
    #rand_solar_wind = random_actor(env_solar_wind)
    #ppo_full = baseline_agent_ppo(env_full, 1000, "PPO-full")
    #rand_full = random_actor(env_full)
    #ppo_new = baseline_agent_ppo(env_full_new_formula, 1000, "PPO-full-new")
    #rand_new = random_actor(env_full_new_formula)

    #plot_q2(env_solar_wind, rand_solar_wind, ppo_solar_wind)
    #plot_q2_2(env_solar_wind, ppo_solar, ppo_solar_wind)
    #plot_q3(env_full, rand_new, ppo_new)
    #plot_q3_2(env_full, ppo_solar, ppo_new)

    plot_reward(env_solar, rand_solar)

    #plot_q4()



