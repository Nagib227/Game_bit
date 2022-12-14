class Speed_potion:
    def __init__(self, speed, time):
        self.speed = speed
        self.time = time

    def get_speed(self):
        return self.speed

    def get_time(self):
        return self.time

    def sub_time(self, sub=1):
        self.time -= sub
