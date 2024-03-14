class Tile:
    def __init__(self,north_face_id,east_face_id,south_face_id,west_face_id,cell_matrix,wall_matrix):
        # assert len(cell_matrix)==len(wall_matrix)-1,Exception TODO: jakis error wpisywania danych
        self.north_face_id = north_face_id
        self.east_face_id = east_face_id
        self.south_face_id = south_face_id
        self.west_face_id = west_face_id
        self.cell_matrix=cell_matrix
        self.wall_matrix = wall_matrix

