from src.modules.module import Module

class Generator(Module):
    def __init__(self, amount, unit_operational_cost_generator, rated_output_power_generator, delta_t=1):
        super().__init__()
        self.amount = amount
        self.unit_operational_cost_generator = unit_operational_cost_generator
        self.rated_output_power_generator = rated_output_power_generator
        self.delta_t = delta_t

    def energy_generated(self, none):
        # calculate the energy generated bv the generator , e_t^g#
        if self.working_status:
            return self.amount * self.rated_output_power_generator * self.delta_t
        return 0

    def operational_cost(self, _):
        return self.energy_generated(None) * self.unit_operational_cost_generator
