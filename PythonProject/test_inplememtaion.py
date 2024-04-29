from Map.Map import Map
from Entities.Hero import Hero
from Items.Weapon import Weapon
from Items.Armor import Armor
from Utility.Vector2d import Vector2d
from Utility.Directions import Directions

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
    for i in range(28):
        print(hero.position)
        print(hero.current_direction)
        hero.move(map)