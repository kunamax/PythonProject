class Map:
    def __init__(self,tiles_dictionary,lower_left_vector2d):
        self.tiles_dictionary=tiles_dictionary
        #key: lower left vector that is dividible by 10
        #val: tile that lower left vector is key