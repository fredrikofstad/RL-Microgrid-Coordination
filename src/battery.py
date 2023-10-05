
class Battery:
    def __init__(self, operational_cost, capacity, soc_max, soc_min):
        self.operational_cost = operational_cost
        self.soc_max = soc_max * capacity
        self.soc_min = soc_min * capacity
        self.soc = 0

    def charge(self):
        return self.soc

