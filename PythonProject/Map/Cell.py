from PythonProject.Entities import Entity
from Wall import Wall,WallType
class Cell:
    def __init__(self,wall:Wall,entities:list[Entity]):
        self.wall=wall
        self.entities=entities