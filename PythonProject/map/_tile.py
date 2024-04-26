class Tile:
    def __init__(self,cells_dict,lower_left_vector2d,map):
        # assert len(cell_matrix)==len(wall_matrix)-1,Exception TODO: jakis error wpisywania danych
        self.cells_dict=cells_dict #should have 100 vectors
        self.lower_left_vector2d=lower_left_vector2d
        self.map=map

    def add_cell(self, vector, cell):
        self.cells_dict[vector] = cell

    def remove_cell(self, vector):
        if vector in self.cells_dict:
            del self.cells_dict[vector]

    def get_cell(self, vector):
        return self.cells_dict.get(vector)

    def has_cell(self, vector):
        return vector in self.cells_dict