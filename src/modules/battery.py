import numpy as np


class Battery:
    def __init__(self, operational_cost, capacity, soc_max, soc_min, efficiency):
        self.operational_cost = operational_cost
        self.capacity = capacity
        self.soc_max = soc_max * capacity
        self.soc_min = soc_min * capacity
        self.efficiency = efficiency
        self.soc = 0
        self.charged = 0

    def soc_status(self):
        return self.soc

    def charge(self, charged, use):
        self.charged = charged
        self.soc += charged * self.efficiency
        self.soc -= use / self.efficiency
        self.soc = np.clip(self.soc, self.soc_min, self.soc_max)

    def operational_cost(self):
        return self.charged * self.operational_cost / (2 * self.capacity * (self.soc_max - self.soc_min))


if __name__ == "__main__":
    battery_config = {
        "operational_cost": 0.95/10,
        "capacity": 300/1000,
        "soc_max": 0.95,
        "soc_min": 0.05,
        "efficiency": 0.95,
    }

    test_battery = Battery(**battery_config)
    test_battery.charge(0.5, 0.5)
    print(test_battery.soc_status())
