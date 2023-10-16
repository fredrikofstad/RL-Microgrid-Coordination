
class Microgrid(object):
    def __init__(self, battery, solar=None, wind=None, generator=None, new_cost_equation=False):
        self.battery = battery
        self.solar = solar
        self.wind = wind
        self.generator = generator
        self.modules = [self.solar, self.wind, self.generator]
        self.new_cost_equation = new_cost_equation

    def actions(self, actions, wind_speed):
        # do solar
        if self.solar:
            self.solar.set(actions[0])
        # do wind
        if self.wind:
            self.wind.set_cond(actions[1], wind_speed)
        # do generator
        if self.generator:
            self.generator.set(actions[2])

    def reset(self):
        self.battery.reset()

    def status(self):
        solar = self.solar.get_working_status() if self.solar is not None else 0
        wind = self.wind.get_working_status() if self.wind is not None else 0
        generator = self.generator.get_working_status() if self.generator is not None else 0
        # TODO: Do we really need the status??

        return solar, wind, generator, self.battery.soc_status()

    def operational_cost(self, solar_irradiance, wind_speed):
        # returns the operational cost for the onsite generation system
        operational_cost = self.battery.operational_cost()
        data = [solar_irradiance, wind_speed, None]
        for i, module in enumerate(self.modules):
            if module is None:
                continue
            operational_cost += module.operational_cost(data[i])

        return operational_cost

    def cost_of_energy_purchase(self, total_load, energy_price):
        if self.new_cost_equation:
            0.25 * total_load**2 * energy_price + 0.5 * total_load * energy_price
        return total_load * energy_price


    def reward(self, solar_actions, wind_actions, generator_actions, grid_actions,
               battery_actions, solar_irradiance, wind_speed, energy_price, total_load):

        energy_purchased = 0
        sell_back_reward = 0
        charge = 0
        module_actions = [solar_actions, wind_actions, generator_actions]
        data = [solar_irradiance, wind_speed, None]
        for i, action in enumerate(module_actions):
            if self.modules[i] is None:
                continue
            if action == 0:
                total_load - self.modules[i].energy_generated(data[i])
            if action == 1:
                # TODO:P u g (t) is the sell-back price to the utility grid, which is fixed as 0.2 × 104$/MW h. ???
                # ask about the units: 0.2 vs 0.06
                sell_back_reward + self.modules[i].energy_generated(data[i]) * energy_price
            if action == 2:
                charge = self.modules[i].energy_generated(data[i])
        self.battery.charge(charge, battery_actions)
        total_load - self.battery.support_load(battery_actions)

        if grid_actions == 1:
            energy_purchased += self.cost_of_energy_purchase(total_load, energy_price)
            total_load = 0
        elif grid_actions == 2:
            energy_purchased += self.battery.charge_full() * energy_price

        # Current assumption: grid needs to buy the remaining power for total load
        self.cost_of_energy_purchase(total_load, energy_price)
        energy_purchased += total_load  # TODO: change equation
        operational_cost = self.operational_cost(solar_irradiance, wind_speed)

        return -(energy_purchased + operational_cost - sell_back_reward)

