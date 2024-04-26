class Map:
    def __init__(self,tiles_dictionary,lower_left_vector2d):
        self.tiles_dictionary=tiles_dictionary
        #key: lower left vector that is dividible by 10
        #val: tile that lower left vector is key
        self.lower_left_vector2d=lower_left_vector2d

    def add_tile(self, vector, tile):
        self.tiles_dictionary[vector] = tile

    def remove_tile(self, vector):
        if vector in self.tiles_dictionary:
            del self.tiles_dictionary[vector]

    def get_tile(self, vector):
        return self.tiles_dictionary.get(vector)

    def has_tile(self, vector):
        return vector in self.tiles_dictionary