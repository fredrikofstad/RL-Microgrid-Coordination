from src.modules.module import Module

class SolarPV(Module):

    def __init__(self, unit_operational_cost_solar, area_solarPV, efficiency_solarPV, delta_t=1):
        super().__init__()
        self.unit_operational_cost_solar = unit_operational_cost_solar
        self.area_solarPV = area_solarPV
        self.efficiency_solarPV = efficiency_solarPV
        self.delta_t = delta_t

    def energy_generated(self, solar_irradiance):
        # calculate the energy generated by the solar PV , e_t^s#
        if self.working_status:
            return solar_irradiance * self.area_solarPV * self.efficiency_solarPV / 1000 * self.delta_t
        return 0

    def operational_cost(self, solar_irradiance):
        return self.energy_generated(solar_irradiance) * self.unit_operational_cost_solar

