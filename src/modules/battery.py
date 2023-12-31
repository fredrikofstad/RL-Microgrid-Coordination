import numpy as np


class Battery:
    def __init__(self, cost, capacity, soc_max, soc_min, efficiency):
        self.cost = cost
        self.capacity = capacity
        self.soc_max = soc_max * capacity
        self.soc_min = soc_min * capacity
        self.efficiency = efficiency
        self.soc = 0
        self.charged = 0

    def soc_status(self):
        return self.soc

    def reset(self):
        self.soc = 0

    def charge(self, charged):
        self.charged = charged
        self.soc += charged * self.efficiency
        self.soc = np.clip(self.soc, self.soc_min, self.soc_max)

    def charge_full(self):
        # but from grid to fully charge battery
        charge = self.soc_max - self.soc
        self.soc = self.soc_max
        return charge

    def support_load(self, battery_actions):
        # support the load with available charge
        if battery_actions == 1:
            support = self.soc * self.efficiency
            self.soc = self.soc_min
            return support
        return 0

    def operational_cost(self):
        return self.charged * self.cost / (2 * self.capacity * (self.soc_max - self.soc_min))


if __name__ == "__main__":
    battery_config = {
        "cost": 0.95,
        "capacity": 300,
        "soc_max": 0.95,
        "soc_min": 0.05,
        "efficiency": 0.95,
    }
    test_battery = Battery(**battery_config)
    print(test_battery.soc_max)
    print(test_battery.soc_min)
    test_battery.charge(300, 10)
    print(test_battery.soc_status())
