from Application.Map import Map
from Application.Map.Entities import Hero
from Application.Map.Entities.Items import Weapon, Armor
from Application.Map.Entities.Items.Utility import Vector2d, Directions
from Application.Map import MapMaker
from Application.Map import Wall, WallType

if __name__ == "__main__":
    # map=Map()
    # map.generate_demo_shop()
    #
    # weapon = Weapon("Sword", "A sharp blade", 10, 5,[Vector2d(0,1),Vector2d(1,1),Vector2d(-1,1),Vector2d(0,2)])
    # armor = Armor("Shield", "A sturdy shield", 15, 3)
    # position = Vector2d(5, 0)
    # list_of_moves = [Directions.NORTH]
    # max_health = 100
    #
    # hero=Hero(1,weapon,armor,position,list_of_moves,max_health,"Jajowiec",Directions.NORTH)
    #
    # map[position].entities.append(hero)
    # print()
    # print(map[Vector2d(5,4)].wall.type,map[Vector2d(5,4)].wall.facing)
    # print()

    # print(map.tiles_dictionary[Vector2d(-10,-10)][Vector2d(1,1)].wall.type)
    # v=Vector2d(-9,-8)
    # print(v.x//10*10,v.y//10*10)
    # print(v.x%10,v.y%10)

    # for x in range(-10,0):
    #     s=""
    #     for y in range(10,20):
    #         s+=str(map[Vector2d(x,y)].wall.facing.to_int())
    #         # print(x,y,map[Vector2d(x,y)].wall.facing)
    #     print(s)

    mm = MapMaker()
    # tile=mm.create_tile("1211",Vector2d(0,0))
    # for x in range(10):
    #     s=""
    #     for y in range(10):
    #         s += str(tile.cells_dict[Vector2d(x,y)].wall.type.__int__())
    #     print(s)
    # print("====================")
    # for x in range(10):
    #     s=""
    #     for y in range(10):
    #         s += str(tile.cells_dict[Vector2d(x,y)].wall.facing.to_int())
    #     print(s)
    # siema="siema"
    # siema[2]='s'
    # print(siema)
    tmp = {
        # EMPTY = 0
        (0, 0): "_",
        (1, 0): "X",
        (2, 1): "1",
        (2, 3): "3",
        (2, 5): "5",
        (2, 7): "7",
        (3, 0): "0",
        (3, 2): "2",
        (3, 4): "4",
        (3, 6): "6"
    }
    size=4
    siema = mm.create_map(size)
    for x in range(size*10):
        s = ""
        for y in range(size*10):
            # print(type(siema[Vector2d(x,y)].wall))
            s += tmp[(siema[Vector2d(x, y)].wall.type.__int__(),siema[Vector2d(x,y)].wall.facing.to_int())]
        print(s)
