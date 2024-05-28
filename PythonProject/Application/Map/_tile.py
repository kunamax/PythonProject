from Application.Map.Entities.Items.Utility import Vector2d, Directions
from ._cell import Cell
from ._wall import Wall,WallType
class Tile:
    def __init__(self,lower_left_vector2d:Vector2d,cells_dict:dict[Vector2d,Cell]={}):
        # assert TODO: jakis error wpisywania danych
        self.cells_dict=cells_dict #should have 100 vectors
        self.lower_left_vector2d=lower_left_vector2d
    def __getitem__(self, item:Vector2d)->Cell:
        return self.cells_dict[item]
    def generate_demo_blank(self):
        size=10
        for x in range(size):
            for y in range(size):
                self.cells_dict[Vector2d(x,y)]=Cell(Wall(WallType(0),Directions(0)),[])
    def generate_demo_cross(self):
        self.generate_demo_blank()
        wall_coordinates=[0,1,2,7,8,9]
        for x in wall_coordinates:
            for y in wall_coordinates:
                self.cells_dict[Vector2d(x, y)] = Cell(Wall(WallType(1), Directions(0)), [])
        self.cells_dict[Vector2d(4, 4)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(5, 4)] = Cell(Wall(WallType(2), Directions(3)), [])
        self.cells_dict[Vector2d(4, 5)] = Cell(Wall(WallType(2), Directions(7)), [])
        self.cells_dict[Vector2d(5, 5)] = Cell(Wall(WallType(2), Directions(1)), [])
    def generate_demo_turn(self):
        size = 10
        self.generate_demo_blank()
        for x in range(size):
            for y in [7,8,9]:
                self.cells_dict[Vector2d(x,y)]=Cell(Wall(WallType(1),Directions(0)),[])

        for x in [7,8,9]:
            for y in range(size):
                self.cells_dict[Vector2d(x,y)]=Cell(Wall(WallType(1),Directions(0)),[])

        for vec in [Vector2d(0,0),Vector2d(1,0),Vector2d(0,1),Vector2d(1,1),Vector2d(2,0),Vector2d(0,2),
                    Vector2d(6,6),Vector2d(6,5),Vector2d(5,6),Vector2d(5,5),Vector2d(6,4),Vector2d(4,6)]:
            self.cells_dict[vec]=Cell(Wall(WallType(1),Directions(0)),[])

        self.cells_dict[Vector2d(1,2)] = Cell(Wall(WallType(2), Directions(1)), [])
        self.cells_dict[Vector2d(2,1)] = Cell(Wall(WallType(2), Directions(1)), [])

        self.cells_dict[Vector2d(3,6)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(4,5)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(5,4)] = Cell(Wall(WallType(2), Directions(5)), [])
        self.cells_dict[Vector2d(6,3)] = Cell(Wall(WallType(2), Directions(5)), [])
    def __hash__(self):
        return hash(self.lower_left_vector2d)

if __name__=="__main__":
    tile=Tile()
    tile.generate_demo_cross()
    print(tile[Vector2d(2,4)].wall.type)