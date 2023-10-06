
class Microgrid(object):
    def __init__(self, battery, wind, solar, generator):
        self.battery = battery
        self.wind = wind
        self.solar = solar
        self.generator = generator

    def actions(self, actions, wind_speed):
        # do solar
        self.solar.set(actions[0])
        # do wind
        self.wind.set_cond(actions[1], wind_speed)
        # do generator
        self.generator.set(actions[2])

    def reset(self):
        self.battery.reset()

    def status(self):
        return (self.solar.get_working_status(),
                self.wind.get_working_status(),
                self.generator.get_working_status(),
                self.battery.soc_status())

    def operational_cost(self, solar_irradiance, wind_speed):
        # returns the operational cost for the onsite generation system
        return (self.solar.operational_cost(solar_irradiance)
                + self.wind.operational_cost(wind_speed)
                + self.generator.operational_cost()
                + self.battery.operational_cost())

    def reward(self, solar_actions, wind_actions, generator_actions, grid_actions,
               battery_actions, solar_irradiance, wind_speed, energy_price, total_load):

        energy_purchased = 0
        sell_back_reward = 0
        charge = 0
        module_actions = [solar_actions, wind_actions, generator_actions]
        modules = [self.solar, self.wind, self.generator]
        data = [solar_irradiance, wind_speed, None]
        for i, action in enumerate(module_actions):
            if action == 0:
                total_load - modules[i].energy_generated(data[i])
            if action == 1:
                # TODO:P u g (t) is the sell-back price to the utility grid, which is fixed as 0.2 × 104$/MW h. ???
                # ask about the units: 0.2 vs 0.06
                sell_back_reward + modules[i].energy_generated(data[i]) * energy_price
            if action == 2:
                charge = modules[i].energy_generated(data[i])
        self.battery.charge(charge, battery_actions)
        total_load - self.battery.support_load(battery_actions)

        if grid_actions == 1:
            energy_purchased += total_load * energy_price
            total_load = 0
        elif grid_actions == 2:
            energy_purchased += self.battery.charge_full() * energy_price

        # TODO: what happens if the grid doesn't get enough power to power houses?
        # Current assumption: grid needs to buy the remaining power for total load
        energy_purchased += total_load
        operational_cost = self.operational_cost(solar_irradiance, wind_speed)

        return -(energy_purchased + operational_cost - sell_back_reward)

