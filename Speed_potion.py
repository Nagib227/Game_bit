class Speed_potion:
    def __init__(self, speed, time, x, y):
        self.x = x
        self.y = y

        self.speed = speed
        self.time = time

    def get_speed(self):
        return self.speed

    def get_time(self):
        return self.time

    def sub_time(self, sub=1):
        self.time -= sub
