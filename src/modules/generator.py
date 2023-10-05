from module import Module


class Generator(Module):
    def __init__(self, amount, unit_operational_cost_generator, rated_output_power_generator):
        super().__init__()
        self.amount = amount
        self.unit_operational_cost_generator = unit_operational_cost_generator
        self.rated_output_power_generator = rated_output_power_generator

    def energy_generated(self):
        # calculate the energy generated bv the generator , e_t^g#
        if self.working_status:
            return self.amount * self.rated_output_power_generator
        return 0

    def operational_cost(self):
        return self.energy_generated() + self.unit_operational_cost_generator
