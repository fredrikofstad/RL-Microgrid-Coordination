class Module:

    def __init__(self):
        self.working_status = False

    def set(self, value):
        if value == 1:
            self.turn_on()
        else:
            self.turn_off()

    def turn_on(self):
        self.working_status = True

    def turn_off(self):
        self.working_status = False

    def get_working_status(self):
        return 1 if self.working_status else 0
