from Application.Map import Map
from Entities import Hero
from Items import Weapon
from Items import Armor
from Utility import Vector2d
from Utility import Directions

if __name__=="__main__":
    map=Map()
    map.generate_demo()

    weapon = Weapon("Sword", "A sharp blade", 10, 5,[Vector2d(0,1),Vector2d(1,1),Vector2d(-1,1),Vector2d(0,2)])
    armor = Armor("Shield", "A sturdy shield", 15, 3)
    position = Vector2d(5, 0)
    list_of_moves = [Directions.NORTH]
    max_health = 100

    hero=Hero(1,weapon,armor,position,list_of_moves,max_health,"Jajowiec",Directions.NORTH)

    map[position].entities.append(hero)
    print()
    print(map[Vector2d(5,4)].wall.type,map[Vector2d(5,4)].wall.facing)
    print()
    for i in range(27):
        print(hero.position)
        print(hero.current_direction)
        hero.move(map)