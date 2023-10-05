
class Microgrid(object):
    def __init__(self, battery, wind, solar, generator):
        self.battery = battery
        self.wind = wind
        self.solar = solar
        self.generator = generator

    def actions(self, actions, solar_actions, wind_actions, generator_actions, grid_actions, battery_actions,
                wind_speed):
        # do solar
        self.solar.set(actions[0])
        # do wind
        self.wind.set_cond(actions[1], wind_speed)
        # do generator
        self.generator.set(actions[2])
        # do battery
        self.battery.charge(solar_actions[1]
                            + wind_actions[1]
                            + generator_actions[1]
                            + grid_actions[1]
                            , battery_actions)

    def status(self):
        return (self.solar.working_status(),
                self.wind.working_status(),
                self.generator.working_status(),
                self.battery.soc_status())

    def energy_consumption(self, solar_actions, wind_actions, generator_actions, battery_actions):
        # returns the energy consumption from the grid #
        return -(solar_actions[0] + wind_actions[0] + generator_actions[0] + battery_actions)

    def operational_cost(self, solar_irradiance, wind_speed):
        # returns the operational cost for the onsite generation system
        return (self.solar.operational_cost(solar_irradiance)
                + self.wind.operational_cost(wind_speed)
                + self.generator.operational_cost()
                + self.battery.operational_cost())

    def SoldBackReward(self, solar_actions, wind_actions, generator_actions, energy_price):
        # calculate the sold back reward ( benefit )#
        return (solar_actions[2] + wind_actions[2] + generator_actions[2]) * energy_price
