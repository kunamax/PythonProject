class HeroOnMap:
    def __init__(self, initial_position):
        self.position = initial_position

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position