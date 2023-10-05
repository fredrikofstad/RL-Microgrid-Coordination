import numpy as np
from module import Module

class WindTurbine(Module):
    def __init__(self, amount, cutin_windspeed, cutoff_windspeed, rated_windspeed, unit_operational_cost_wind,
                 density_of_air, radius_wind_turbine_blade, average_wind_speed, power_coefficient,
                 gearbox_transmission_efficiency, electrical_generator_efficiency):
        super().__init__()
        self.amount = amount
        self.cutin_windspeed = cutin_windspeed   # (km/h =1/3.6 m/s)
        self.cutoff_windspeed = cutoff_windspeed  # (km/h =1/3.6 m/s), v^co#
        self.rated_windspeed = rated_windspeed   # (km/h =1/3.6 m/s), v^r#
        self.unit_operational_cost_wind = unit_operational_cost_wind

        self.rated_power_wind_turbine = (0.5 * density_of_air * np.pi
                                         * radius_wind_turbine_blade ** 2
                                         * average_wind_speed ** 3
                                         * power_coefficient
                                         * gearbox_transmission_efficiency
                                         * electrical_generator_efficiency) / (3.6**3)

    def turbine_safety(self, wind_speed):
        if wind_speed > self.cutoff_windspeed or wind_speed < self.cutin_windspeed:
            return False
        return True

    def energy_generated_wind(self, wind_speed):
        # calculate the energy generated by the wind turbine , e_t^w#
        if not self.working_status:
            return 0
        elif self.rated_windspeed > wind_speed >= self.cutin_windspeed:
            return (self.amount * self.rated_power_wind_turbine *
                    (wind_speed - self.cutin_windspeed) / (self.rated_windspeed - self.cutin_windspeed))

        elif self.cutoff_windspeed > wind_speed >= self.rated_windspeed:
            return self.amount * self.rated_power_wind_turbine
        else:
            return 0
