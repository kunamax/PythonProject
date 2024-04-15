class Tile:
    def __init__(self,cells_dict,lower_left_vector2d,map):
        # assert len(cell_matrix)==len(wall_matrix)-1,Exception TODO: jakis error wpisywania danych
        self.cells_dict=cells_dict #should have 100 vectors
        self.lower_left_vector2d=lower_left_vector2d
        self.map=map